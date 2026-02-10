"""
Janela principal da aplicação
"""

import tkinter as tk
from tkinter import ttk
from gui.styles import COLORS, FONTS, PADDING
from gui.cliente_form import ClienteForm
from database import Database


class MainWindow(tk.Tk):
    """Janela principal do sistema"""
    
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("FastTech Control - Sistema de Gestão de Equipamentos")
        self.geometry("1200x700")
        self.configure(bg=COLORS['white'])
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Inicializa banco de dados
        self.db = Database()
        
        # Carrega configurações
        self._carregar_config()
        
        # Cria a interface
        self._criar_interface()
        
        # Backup automático (se configurado)
        if self.app_config.get('backup_automatico', False):
            self.after(1000, self._backup_automatico_inicial)
    
    def _centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = 1200
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _criar_interface(self):
        """Cria a interface principal"""
        
        # Menu superior
        self._criar_menu()
        
        # Header
        self._criar_header()
        
        # Container principal com abas
        self._criar_notebook()
        
        # Barra de status
        self._criar_status_bar()
        
        # Atalhos de teclado
        self._configurar_atalhos()
    
    def _carregar_config(self):
        """Carrega configurações do arquivo"""
        import json
        import os
        
        self.app_config = {
            'backup_automatico': False,
            'backup_dias': 7,
            'backup_pasta': 'backups',
            'tema': 'claro',
            'usuario_padrao': 'Técnico'
        }
        
        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # Validar e filtrar configurações carregadas para evitar injeção de configurações maliciosas
                    for key in saved_config:
                        if key in self.app_config and isinstance(saved_config[key], type(self.app_config[key])):
                            self.app_config[key] = saved_config[key]
            except (json.JSONDecodeError, TypeError):
                pass
    
    def _backup_automatico_inicial(self):
        """Cria backup automático ao iniciar"""
        try:
            backup_path = self.db.backup_database()
            self.status_label.config(
                text=f"✓ Backup automático criado: {os.path.basename(backup_path)}",
                fg=COLORS['success']
            )
            self.after(5000, lambda: self.status_label.config(text="✓ Sistema pronto", fg=COLORS['text']))
        except Exception as e:
            self.status_label.config(text=f"⚠ Erro no backup automático", fg=COLORS['warning'])
    
    def _criar_menu(self):
        """Cria o menu superior"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Backup do Banco", command=self._criar_backup, accelerator="Ctrl+B")
        menu_arquivo.add_command(label="Atualizar Estatísticas", command=self._atualizar_stats, accelerator="F5")
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Salvar Configurações", command=self._salvar_config_menu, accelerator="Ctrl+S")
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.on_closing, accelerator="Alt+F4")
        
        # Menu Navegação
        menu_nav = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Navegação", menu=menu_nav)
        menu_nav.add_command(label="Dashboard", command=lambda: self.notebook.select(0), accelerator="Ctrl+0")
        menu_nav.add_command(label="Clientes", command=lambda: self.notebook.select(1), accelerator="Ctrl+1")
        menu_nav.add_command(label="Equipamentos", command=lambda: self.notebook.select(2), accelerator="Ctrl+2")
        menu_nav.add_command(label="Movimentações", command=lambda: self.notebook.select(3), accelerator="Ctrl+3")
        menu_nav.add_command(label="Consultas", command=lambda: self.notebook.select(4), accelerator="Ctrl+4")
        
        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Como Usar", command=self._mostrar_ajuda)
        menu_ajuda.add_command(label="Atalhos de Teclado", command=self._mostrar_atalhos, accelerator="F1")
        menu_ajuda.add_separator()
        menu_ajuda.add_command(label="Sobre", command=self._mostrar_sobre)
    
    def _criar_header(self):
        """Cria o cabeçalho da aplicação"""
        header = tk.Frame(self, bg=COLORS['primary'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título
        title = tk.Label(
            header,
            text="⚙️ FastTech Control",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['white']
        )
        title.pack(side='left', padx=PADDING['large'], pady=PADDING['large'])
        
        # Subtítulo
        subtitle = tk.Label(
            header,
            text="Sistema de Gestão de Equipamentos e Clientes",
            font=FONTS['normal'],
            bg=COLORS['primary'],
            fg=COLORS['white']
        )
        subtitle.pack(side='left', padx=(0, PADDING['large']))
        
        # Informações de licença
        licenca_info = tk.Label(
            header,
            text="Licença: Grátis",  # Pode ser alterado para Padrão ou Premium
            font=FONTS['normal'],
            bg=COLORS['primary'],
            fg=COLORS['white']
        )
        licenca_info.pack(side='right', padx=PADDING['large'])
    
    def _criar_notebook(self):
        """Cria o notebook com abas"""
        # Container para o notebook
        notebook_container = tk.Frame(self, bg=COLORS['white'])
        notebook_container.pack(fill='both', expand=True)
        
        # Estilo do notebook
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure(
            'TNotebook',
            background=COLORS['white'],
            borderwidth=0
        )
        
        style.configure(
            'TNotebook.Tab',
            background=COLORS['bg_dark'],
            foreground=COLORS['text'],
            padding=[20, 10],
            font=FONTS['subtitle']
        )
        
        style.map(
            'TNotebook.Tab',
            background=[('selected', COLORS['white'])],
            foreground=[('selected', COLORS['primary'])]
        )
        
        # Notebook
        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Aba Dashboard (Nova!)
        from gui.dashboard import Dashboard
        self.aba_dashboard = Dashboard(self.notebook, self.db)
        self.notebook.add(self.aba_dashboard, text='🏠 Dashboard')
        
        # Aba de Clientes
        self.aba_clientes = ClienteForm(self.notebook, self.db)
        self.notebook.add(self.aba_clientes, text='👥 Clientes')
        
        # Aba de Equipamentos
        from gui.equipamento_form import EquipamentoForm
        self.aba_equipamentos = EquipamentoForm(self.notebook, self.db)
        self.notebook.add(self.aba_equipamentos, text='📦 Equipamentos')
        
        # Aba de Movimentações
        from gui.movimentacao_form import MovimentacaoForm
        self.aba_movimentacoes = MovimentacaoForm(self.notebook, self.db)
        self.notebook.add(self.aba_movimentacoes, text='🔄 Movimentações')
        
        # Aba de Consultas
        from gui.consulta_form import ConsultaForm
        self.aba_consultas = ConsultaForm(self.notebook, self.db)
        self.notebook.add(self.aba_consultas, text='🔍 Consultas')
        
        # Aba de Configurações
        from gui.config_form import ConfigForm
        self.aba_config = ConfigForm(self.notebook, self.db)
        self.notebook.add(self.aba_config, text='⚙️ Configurações')
    
    def _criar_aba_placeholder(self, titulo, mensagem):
        """Cria uma aba placeholder para futuras funcionalidades"""
        frame = tk.Frame(self.notebook, bg=COLORS['white'])
        
        label = tk.Label(
            frame,
            text=mensagem,
            font=FONTS['title'],
            bg=COLORS['white'],
            fg=COLORS['text_light']
        )
        label.pack(expand=True)
        
        self.notebook.add(frame, text=titulo)
    
    def _criar_status_bar(self):
        """Cria a barra de status inferior"""
        self.status_bar = tk.Frame(self, bg=COLORS['bg_dark'], height=30)
        self.status_bar.pack(side='bottom', fill='x')
        self.status_bar.pack_propagate(False)
        
        # Label de status
        self.status_label = tk.Label(
            self.status_bar,
            text="✓ Sistema pronto",
            font=FONTS['small'],
            bg=COLORS['bg_dark'],
            fg=COLORS['text'],
            anchor='w'
        )
        self.status_label.pack(side='left', padx=PADDING['medium'])
        
        # Versão
        version_label = tk.Label(
            self.status_bar,
            text="v0.7.0",
            font=FONTS['small'],
            bg=COLORS['bg_dark'],
            fg=COLORS['text_light']
        )
        version_label.pack(side='right', padx=PADDING['medium'])
    
    def _configurar_atalhos(self):
        """Configura atalhos de teclado"""
        # Navegação entre abas
        self.bind('<Control-Key-0>', lambda e: self.notebook.select(0))  # Dashboard
        self.bind('<Control-Key-1>', lambda e: self.notebook.select(1))  # Clientes
        self.bind('<Control-Key-2>', lambda e: self.notebook.select(2))  # Equipamentos
        self.bind('<Control-Key-3>', lambda e: self.notebook.select(3))  # Movimentações
        self.bind('<Control-Key-4>', lambda e: self.notebook.select(4))  # Consultas
        self.bind('<Control-Key-5>', lambda e: self.notebook.select(5))  # Configurações
        self.bind('<Home>', lambda e: self.notebook.select(0))  # Home = Dashboard
        
        # Funções
        self.bind('<Control-b>', lambda e: self._criar_backup())
        self.bind('<Control-s>', lambda e: self._salvar_config_menu())
        self.bind('<F5>', lambda e: self._atualizar_stats())
        self.bind('<F1>', lambda e: self._mostrar_atalhos())
        
        # Atualizar status ao trocar de aba
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_change)
    
    def _on_tab_change(self, event=None):
        """Chamado ao trocar de aba"""
        tab_index = self.notebook.index(self.notebook.select())
        tab_names = ['Dashboard', 'Clientes', 'Equipamentos', 'Movimentações', 'Consultas', 'Configurações']
        if tab_index < len(tab_names):
            self.status_label.config(text=f"📍 {tab_names[tab_index]}", fg=COLORS['text'])
            
            # Atualizar dashboard quando voltar para ela
            if tab_index == 0 and hasattr(self, 'aba_dashboard'):
                self.aba_dashboard.atualizar()
    
    def _criar_backup(self):
        """Cria backup do banco de dados"""
        try:
            import os
            backup_path = self.db.backup_database()
            # Pega apenas o nome do arquivo
            backup_nome = os.path.basename(backup_path)
            self.status_label.config(text=f"✓ Backup criado: {backup_nome}", fg=COLORS['success'])
            self.after(3000, lambda: self.status_label.config(text="✓ Sistema pronto", fg=COLORS['text']))
            
            # Também mostra messagebox
            from tkinter import messagebox
            messagebox.showinfo("Backup", f"Backup criado com sucesso!\n\n{backup_path}")
        except Exception as e:
            self.status_label.config(text=f"✗ Erro ao criar backup: {str(e)}", fg=COLORS['danger'])
            from tkinter import messagebox
            messagebox.showerror("Erro", f"Erro ao criar backup:\n{str(e)}")
    
    def _atualizar_stats(self):
        """Atualiza estatísticas do header"""
        stats = self.db.get_estatisticas()
        # Atualiza o label de estatísticas no header
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == COLORS['primary']:
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and '📊' in child.cget('text'):
                        child.config(text=f"📊 {stats['total_clientes']} Clientes | {stats['total_equipamentos']} Equipamentos")
        
        self.status_label.config(text="✓ Estatísticas atualizadas", fg=COLORS['success'])
        self.after(2000, lambda: self.status_label.config(text="✓ Sistema pronto", fg=COLORS['text']))
    
    def _mostrar_ajuda(self):
        """Mostra janela de ajuda"""
        from tkinter import messagebox
        messagebox.showinfo(
            "Como Usar",
            "FastTech Control - Sistema de Gestão\n\n"
            "📋 Clientes: Cadastre e gerencie clientes\n"
            "📦 Equipamentos: Cadastre equipamentos e vincule a clientes\n"
            "🔄 Movimentações: Registre entregas, devoluções e manutenções\n"
            "🔍 Consultas: Busque equipamentos e clientes, exporte relatórios\n\n"
            "Pressione F1 para ver todos os atalhos de teclado.\n\n"
            "Documentação completa: COMO_USAR.md"
        )
    
    def _mostrar_atalhos(self):
        """Mostra janela com atalhos de teclado"""
        from tkinter import messagebox
        messagebox.showinfo(
            "Atalhos de Teclado",
            "NAVEGAÇÃO:\n"
            "Ctrl+0 ou Home - Dashboard\n"
            "Ctrl+1 - Aba Clientes\n"
            "Ctrl+2 - Aba Equipamentos\n"
            "Ctrl+3 - Aba Movimentações\n"
            "Ctrl+4 - Aba Consultas\n"
            "Ctrl+5 - Aba Configurações\n\n"
            "FUNÇÕES:\n"
            "Ctrl+B - Criar Backup\n"
            "Ctrl+S - Salvar Configurações\n"
            "F5 - Atualizar Estatísticas\n"
            "F1 - Mostrar Atalhos\n"
            "Alt+F4 - Sair\n\n"
            "BUSCA:\n"
            "Enter - Executar busca (em campos de busca)"
        )
    
    def _mostrar_sobre(self):
        """Mostra janela sobre o sistema"""
        from tkinter import messagebox
        messagebox.showinfo(
            "Sobre",
            "FastTech Control\n"
            "Sistema de Gestão de Equipamentos\n\n"
            "Versão: 0.7.0\n"
            "Data: 02/12/2024\n\n"
            "Desenvolvido para gestão interna de equipamentos\n"
            "e rastreamento de responsáveis.\n\n"
            "Funcionalidades:\n"
            "• Gestão Completa de Clientes e Equipamentos\n"
            "• Controle de Movimentações\n"
            "• Consultas e Relatórios\n"
            "• Backup Automático\n"
            "• Configurações Personalizáveis\n\n"
            "Tecnologias:\n"
            "• Python 3.8+\n"
            "• SQLite\n"
            "• tkinter"
        )
    
    def _salvar_config_menu(self):
        """Salva configurações via menu"""
        try:
            if hasattr(self, 'aba_config'):
                self.aba_config.salvar_configuracoes()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
    
    def on_closing(self):
        """Executado ao fechar a janela"""
        self.db.close()
        self.destroy()


def iniciar_aplicacao():
    """Inicia a aplicação GUI"""
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()
