"""
Formulário de configurações do sistema
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from gui.styles import COLORS, FONTS, PADDING
from gui.widgets import CustomButton, StatusLabel, LabeledEntry
from database import Database
from utils.backup import BackupManager


class ConfigForm(tk.Frame):
    """Formulário de configurações"""
    
    def __init__(self, parent, db: Database):
        super().__init__(parent, bg=COLORS['white'])
        self.db = db
        self.backup_manager = BackupManager()
        self.config_file = "config.json"
        
        self.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        self._carregar_config()
        self._criar_interface()
    
    def _carregar_config(self):
        """Carrega configurações do arquivo"""
        self.config = {
            'backup_automatico': False,
            'backup_dias': 7,
            'backup_pasta': 'backups',
            'tema': 'claro',
            'usuario_padrao': 'Técnico'
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # Validar e filtrar configurações carregadas para evitar injeção de configurações maliciosas
                    for key in saved_config:
                        if key in self.config and isinstance(saved_config[key], type(self.config[key])):
                            self.config[key] = saved_config[key]
            except (json.JSONDecodeError, TypeError):
                pass
    
    def _salvar_config(self):
        """Salva configurações no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
            return False
    
    def _criar_interface(self):
        """Cria a interface de configurações"""
        
        # Título
        title = tk.Label(
            self,
            text="⚙️ Configurações do Sistema",
            font=FONTS['title'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, PADDING['large']))
        
        # Notebook com categorias
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, pady=(0, PADDING['medium']))
        
        # Aba Backup
        self._criar_aba_backup(notebook)
        
        # Aba Geral
        self._criar_aba_geral(notebook)
        
        # Aba Sobre
        self._criar_aba_sobre(notebook)
        
        # Botão de Salvar (fixo no rodapé)
        btn_frame = tk.Frame(self, bg=COLORS['white'])
        btn_frame.pack(fill='x', pady=PADDING['medium'])
        
        CustomButton(
            btn_frame,
            text="💾 Salvar Configurações",
            command=self.salvar_configuracoes,
            style='success'
        ).pack(side='right', padx=PADDING['small'])
        
        CustomButton(
            btn_frame,
            text="🔄 Recarregar",
            command=self._recarregar_config,
            style='default'
        ).pack(side='right', padx=PADDING['small'])
    
    def _criar_aba_backup(self, notebook):
        """Cria aba de configurações de backup"""
        frame = tk.Frame(notebook, bg=COLORS['white'])
        notebook.add(frame, text='💾 Backup')
        
        content = tk.Frame(frame, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Backup Automático
        tk.Label(
            content,
            text="Backup Automático",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, PADDING['medium']))
        
        auto_frame = tk.Frame(content, bg=COLORS['white'])
        auto_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        self.backup_auto_var = tk.BooleanVar(value=self.config['backup_automatico'])
        tk.Checkbutton(
            auto_frame,
            text="Criar backup automático ao iniciar o sistema",
            variable=self.backup_auto_var,
            font=FONTS['normal'],
            bg=COLORS['white'],
            activebackground=COLORS['white']
        ).pack(anchor='w')
        
        # Limpeza de Backups Antigos
        tk.Label(
            content,
            text="Limpeza Automática",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(PADDING['large'], PADDING['medium']))
        
        dias_frame = tk.Frame(content, bg=COLORS['white'])
        dias_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        tk.Label(
            dias_frame,
            text="Manter backups dos últimos:",
            font=FONTS['normal'],
            bg=COLORS['white']
        ).pack(side='left', padx=(0, PADDING['small']))
        
        self.dias_spinbox = tk.Spinbox(
            dias_frame,
            from_=1,
            to=90,
            width=5,
            font=FONTS['normal']
        )
        self.dias_spinbox.delete(0, tk.END)
        self.dias_spinbox.insert(0, self.config['backup_dias'])
        self.dias_spinbox.pack(side='left', padx=(0, PADDING['small']))
        
        tk.Label(
            dias_frame,
            text="dias",
            font=FONTS['normal'],
            bg=COLORS['white']
        ).pack(side='left')
        
        # Pasta de Backup
        tk.Label(
            content,
            text="Pasta de Backup",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(PADDING['large'], PADDING['medium']))
        
        pasta_frame = tk.Frame(content, bg=COLORS['white'])
        pasta_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        self.pasta_entry = tk.Entry(
            pasta_frame,
            font=FONTS['normal'],
            width=40
        )
        self.pasta_entry.insert(0, self.config['backup_pasta'])
        self.pasta_entry.pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            pasta_frame,
            text="📁 Escolher",
            command=self._escolher_pasta_backup,
            style='default'
        ).pack(side='left')
        
        # Gerenciar Backups
        tk.Label(
            content,
            text="Gerenciar Backups",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(PADDING['large'], PADDING['medium']))
        
        btn_frame = tk.Frame(content, bg=COLORS['white'])
        btn_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        CustomButton(
            btn_frame,
            text="💾 Criar Backup Agora",
            command=self._criar_backup_manual,
            style='success'
        ).pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            btn_frame,
            text="📋 Listar Backups",
            command=self._listar_backups,
            style='primary'
        ).pack(side='left', padx=PADDING['small'])
        
        CustomButton(
            btn_frame,
            text="🗑️ Limpar Antigos",
            command=self._limpar_backups_antigos,
            style='danger'
        ).pack(side='left', padx=PADDING['small'])
        
        CustomButton(
            btn_frame,
            text="♻️ Restaurar Backup",
            command=self._restaurar_backup,
            style='primary'
        ).pack(side='left', padx=PADDING['small'])
        
        # Status
        self.backup_status = StatusLabel(content)
        self.backup_status.pack(pady=PADDING['large'])
    
    def _criar_aba_geral(self, notebook):
        """Cria aba de configurações gerais"""
        frame = tk.Frame(notebook, bg=COLORS['white'])
        notebook.add(frame, text='⚙️ Geral')
        
        content = tk.Frame(frame, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Tema
        tk.Label(
            content,
            text="Aparência",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, PADDING['medium']))
        
        tema_frame = tk.Frame(content, bg=COLORS['white'])
        tema_frame.pack(fill='x', pady=(0, PADDING['large']))
        
        tk.Label(
            tema_frame,
            text="Tema:",
            font=FONTS['normal'],
            bg=COLORS['white']
        ).pack(side='left', padx=(0, PADDING['small']))
        
        self.tema_var = tk.StringVar(value=self.config['tema'])
        
        tk.Radiobutton(
            tema_frame,
            text="☀️ Claro",
            variable=self.tema_var,
            value='claro',
            font=FONTS['normal'],
            bg=COLORS['white'],
            activebackground=COLORS['white']
        ).pack(side='left', padx=PADDING['small'])
        
        tk.Radiobutton(
            tema_frame,
            text="🌙 Escuro",
            variable=self.tema_var,
            value='escuro',
            font=FONTS['normal'],
            bg=COLORS['white'],
            activebackground=COLORS['white']
        ).pack(side='left', padx=PADDING['small'])
        
        tk.Label(
            content,
            text="(Reinicie a aplicação para aplicar o tema)",
            font=FONTS['small'],
            bg=COLORS['white'],
            fg=COLORS['text_light']
        ).pack(anchor='w', pady=(0, PADDING['large']))
        
        # Usuário Padrão
        tk.Label(
            content,
            text="Usuário Padrão",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, PADDING['medium']))
        
        tk.Label(
            content,
            text="Nome usado por padrão ao registrar movimentações:",
            font=FONTS['small'],
            bg=COLORS['white'],
            fg=COLORS['text_light']
        ).pack(anchor='w', pady=(0, PADDING['small']))
        
        self.usuario_entry = LabeledEntry(
            content,
            "Nome do Usuário",
            placeholder="Ex: João Silva",
            width=40
        )
        self.usuario_entry.set(self.config['usuario_padrao'])
        self.usuario_entry.pack(fill='x', pady=(0, PADDING['large']))
        
        # Estatísticas
        tk.Label(
            content,
            text="Estatísticas do Sistema",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(PADDING['large'], PADDING['medium']))
        
        stats = self.db.get_estatisticas()
        
        stats_frame = tk.Frame(content, bg=COLORS['bg'], relief='solid', borderwidth=1)
        stats_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        stats_text = f"""
📊 ESTATÍSTICAS GERAIS

Total de Clientes: {stats['total_clientes']}
Total de Equipamentos: {stats['total_equipamentos']}

Equipamentos por Status:
"""
        for status, total in stats['por_status'].items():
            stats_text += f"  • {status}: {total}\n"
        
        tk.Label(
            stats_frame,
            text=stats_text.strip(),
            font=FONTS['normal'],
            bg=COLORS['bg'],
            fg=COLORS['text'],
            justify='left',
            padx=PADDING['large'],
            pady=PADDING['large']
        ).pack(fill='x')
        
        # Banco de Dados
        tk.Label(
            content,
            text="Banco de Dados",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(PADDING['large'], PADDING['medium']))
        
        db_info = f"Arquivo: fastech.db\nTamanho: {self._get_db_size()}"
        
        tk.Label(
            content,
            text=db_info,
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Status
        self.geral_status = StatusLabel(content)
        self.geral_status.pack(pady=PADDING['large'])
    
    def _criar_aba_sobre(self, notebook):
        """Cria aba sobre o sistema"""
        frame = tk.Frame(notebook, bg=COLORS['white'])
        notebook.add(frame, text='ℹ️ Sobre')
        
        content = tk.Frame(frame, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Logo e Título
        tk.Label(
            content,
            text="⚙️",
            font=('Segoe UI', 48),
            bg=COLORS['white']
        ).pack(pady=(PADDING['large'], PADDING['small']))
        
        tk.Label(
            content,
            text="FastTech Control",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['white'],
            fg=COLORS['primary']
        ).pack()
        
        tk.Label(
            content,
            text="Sistema de Gestão de Equipamentos",
            font=FONTS['subtitle'],
            bg=COLORS['white'],
            fg=COLORS['text_light']
        ).pack(pady=(0, PADDING['large']))
        
        # Informações
        info_frame = tk.Frame(content, bg=COLORS['bg'], relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=PADDING['large'])
        
        info_text = """
Versão: 0.7.0
Data: 02/12/2024

Desenvolvido para gestão interna de equipamentos
e rastreamento de responsáveis.

Funcionalidades:
• Gestão de Clientes
• Gestão de Equipamentos
• Controle de Movimentações
• Consultas e Relatórios
• Backup Automático
• Exportação de Dados

Tecnologias:
• Python 3.8+
• SQLite
• tkinter
        """
        
        tk.Label(
            info_frame,
            text=info_text.strip(),
            font=FONTS['normal'],
            bg=COLORS['bg'],
            fg=COLORS['text'],
            justify='center',
            padx=PADDING['large'],
            pady=PADDING['large']
        ).pack()
        
        # Botões
        btn_frame = tk.Frame(content, bg=COLORS['white'])
        btn_frame.pack(pady=PADDING['large'])
        
        CustomButton(
            btn_frame,
            text="📖 Documentação",
            command=lambda: messagebox.showinfo(
                "Documentação",
                "Documentação completa disponível em:\n\n"
                "• README.md - Visão geral\n"
                "• COMO_USAR.md - Guia de uso\n"
                "• INDEX.md - Índice completo"
            ),
            style='primary'
        ).pack(side='left', padx=PADDING['small'])
        
        CustomButton(
            btn_frame,
            text="🔧 Verificar Sistema",
            command=self._verificar_sistema,
            style='default'
        ).pack(side='left', padx=PADDING['small'])
    
    def _escolher_pasta_backup(self):
        """Abre diálogo para escolher pasta de backup"""
        pasta = filedialog.askdirectory(
            title="Escolher Pasta de Backup",
            initialdir=self.config['backup_pasta']
        )
        if pasta:
            self.pasta_entry.delete(0, tk.END)
            self.pasta_entry.insert(0, pasta)
    
    def _criar_backup_manual(self):
        """Cria backup manual"""
        try:
            backup_path = self.db.backup_database()
            self.backup_status.show_success(f"Backup criado: {backup_path}")
        except Exception as e:
            self.backup_status.show_error(f"Erro: {str(e)}")
    
    def _listar_backups(self):
        """Lista backups disponíveis"""
        backups = self.backup_manager.listar_backups()
        
        if not backups:
            messagebox.showinfo("Backups", "Nenhum backup encontrado.")
            return
        
        # Cria janela com lista
        modal = tk.Toplevel(self)
        modal.title("Backups Disponíveis")
        modal.geometry("600x400")
        modal.configure(bg=COLORS['white'])
        modal.transient(self)
        
        # Lista
        lista_frame = tk.Frame(modal, bg=COLORS['white'])
        lista_frame.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        tk.Label(
            lista_frame,
            text=f"📋 {len(backups)} Backups Encontrados",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(pady=(0, PADDING['medium']))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side='right', fill='y')
        
        text = tk.Text(
            lista_frame,
            font=FONTS['small'],
            yscrollcommand=scrollbar.set,
            wrap='word'
        )
        text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=text.yview)
        
        for b in backups:
            tamanho = self.backup_manager.formatar_tamanho(b['tamanho'])
            data = b['data_criacao'].strftime("%d/%m/%Y %H:%M:%S")
            text.insert('end', f"📁 {b['nome']}\n")
            text.insert('end', f"   Tamanho: {tamanho} | Data: {data}\n\n")
        
        text.config(state='disabled')
        
        CustomButton(
            modal,
            text="Fechar",
            command=modal.destroy,
            style='default'
        ).pack(pady=PADDING['medium'])
    
    def _limpar_backups_antigos(self):
        """Limpa backups antigos"""
        dias = int(self.dias_spinbox.get())
        
        resposta = messagebox.askyesno(
            "Confirmar",
            f"Deseja remover backups com mais de {dias} dias?\n\n"
            "Esta ação não pode ser desfeita."
        )
        
        if resposta:
            try:
                removidos = self.backup_manager.limpar_backups_antigos(dias)
                self.backup_status.show_success(f"{removidos} backup(s) removido(s)")
            except Exception as e:
                self.backup_status.show_error(f"Erro: {str(e)}")
    
    def _restaurar_backup(self):
        """Restaura um backup selecionado"""
        import os
        backups = self.backup_manager.listar_backups()
        
        if not backups:
            messagebox.showinfo("Restaurar Backup", "Nenhum backup disponível para restaurar.")
            return
        
        # Cria janela de seleção
        modal = tk.Toplevel(self)
        modal.title("Restaurar Backup")
        modal.geometry("700x500")
        modal.configure(bg=COLORS['white'])
        modal.transient(self)
        modal.grab_set()
        
        # Conteúdo
        content = tk.Frame(modal, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        tk.Label(
            content,
            text="⚠️ ATENÇÃO: Restaurar Backup",
            font=FONTS['title'],
            bg=COLORS['white'],
            fg=COLORS['danger']
        ).pack(pady=(0, PADDING['small']))
        
        tk.Label(
            content,
            text="Esta ação substituirá o banco de dados atual!\nUm backup do banco atual será criado antes da restauração.",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['text_light'],
            justify='center'
        ).pack(pady=(0, PADDING['large']))
        
        # Lista de backups
        tk.Label(
            content,
            text="Selecione o backup para restaurar:",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, PADDING['small']))
        
        # Frame com lista
        list_frame = tk.Frame(content, bg=COLORS['white'])
        list_frame.pack(fill='both', expand=True, pady=(0, PADDING['medium']))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(
            list_frame,
            font=FONTS['normal'],
            yscrollcommand=scrollbar.set,
            selectmode='single'
        )
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Popula lista
        backup_paths = {}
        for i, b in enumerate(backups):
            tamanho = self.backup_manager.formatar_tamanho(b['tamanho'])
            data = b['data_criacao'].strftime("%d/%m/%Y %H:%M:%S")
            texto = f"{b['nome']} - {tamanho} - {data}"
            listbox.insert(tk.END, texto)
            backup_paths[i] = b['caminho']
        
        # Botões
        btn_frame = tk.Frame(content, bg=COLORS['white'])
        btn_frame.pack(fill='x', pady=PADDING['medium'])
        
        def confirmar_restauracao():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Atenção", "Selecione um backup para restaurar.")
                return
            
            backup_path = backup_paths[selection[0]]
            backup_nome = os.path.basename(backup_path)
            
            resposta = messagebox.askyesno(
                "Confirmar Restauração",
                f"Deseja realmente restaurar o backup:\n\n{backup_nome}\n\n"
                "O banco de dados atual será substituído!\n"
                "(Um backup do banco atual será criado automaticamente)"
            )
            
            if resposta:
                try:
                    # Restaura o backup
                    self.backup_manager.restaurar_backup(backup_path)
                    
                    messagebox.showinfo(
                        "Sucesso",
                        "Backup restaurado com sucesso!\n\n"
                        "IMPORTANTE: Reinicie a aplicação para aplicar as mudanças."
                    )
                    
                    modal.destroy()
                    
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao restaurar backup:\n{str(e)}")
        
        CustomButton(
            btn_frame,
            text="♻️ Restaurar Selecionado",
            command=confirmar_restauracao,
            style='success'
        ).pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            command=modal.destroy,
            style='default'
        ).pack(side='left')
    
    def _get_db_size(self):
        """Retorna tamanho do banco de dados"""
        try:
            size = os.path.getsize('fastech.db')
            if size < 1024:
                return f"{size} bytes"
            elif size < 1024 * 1024:
                return f"{size / 1024:.2f} KB"
            else:
                return f"{size / (1024 * 1024):.2f} MB"
        except:
            return "Desconhecido"
    
    def _verificar_sistema(self):
        """Verifica integridade do sistema"""
        try:
            stats = self.db.get_estatisticas()
            
            mensagem = "✓ Sistema OK!\n\n"
            mensagem += f"Banco de dados: Conectado\n"
            mensagem += f"Clientes: {stats['total_clientes']}\n"
            mensagem += f"Equipamentos: {stats['total_equipamentos']}\n"
            mensagem += f"Tamanho do banco: {self._get_db_size()}\n"
            
            messagebox.showinfo("Verificação do Sistema", mensagem)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar sistema:\n{str(e)}")
    
    def _recarregar_config(self):
        """Recarrega configurações do arquivo"""
        self._carregar_config()
        
        # Atualiza os campos da interface
        self.backup_auto_var.set(self.config['backup_automatico'])
        self.dias_spinbox.delete(0, tk.END)
        self.dias_spinbox.insert(0, self.config['backup_dias'])
        self.pasta_entry.delete(0, tk.END)
        self.pasta_entry.insert(0, self.config['backup_pasta'])
        self.tema_var.set(self.config['tema'])
        self.usuario_entry.set(self.config['usuario_padrao'])
        
        messagebox.showinfo("Recarregado", "Configurações recarregadas do arquivo!")
    
    def salvar_configuracoes(self):
        """Salva todas as configurações"""
        self.config['backup_automatico'] = self.backup_auto_var.get()
        self.config['backup_dias'] = int(self.dias_spinbox.get())
        self.config['backup_pasta'] = self.pasta_entry.get()
        self.config['tema'] = self.tema_var.get()
        self.config['usuario_padrao'] = self.usuario_entry.get()
        
        if self._salvar_config():
            messagebox.showinfo(
                "Sucesso", 
                "Configurações salvas com sucesso!\n\n"
                "Se alterou o tema, reinicie a aplicação para aplicar."
            )
            return True
        return False
