"""
Formulário de configurações do sistema - Versão Flet
"""

import flet as ft
import json
import os
from gui.styles import get_colors, get_fonts, PADDING
from database import Database
from utils.backup import BackupManager


class ConfigForm(ft.UserControl):
    """Formulário de configurações"""
    
    def __init__(self, page: ft.Page, db: Database):
        super().__init__()
        self.page = page
        self.db = db
        self.backup_manager = BackupManager()
        self.config_file = "config.json"
        
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
            self._show_status(f"Erro ao salvar configurações: {str(e)}", "error")
            return False

    def _criar_interface(self):
        """Cria a interface de configurações"""
        
        # Título
        self.title = ft.Text(
            "⚙️ Configurações do Sistema",
            size=get_fonts()['title']['size'],
            weight=get_fonts()['title']['weight'],
            color=get_colors()['text']
        )

        # Abas de configuração
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="💾 Backup",
                    content=self._criar_aba_backup()
                ),
                ft.Tab(
                    text="⚙️ Geral",
                    content=self._criar_aba_geral()
                ),
                ft.Tab(
                    text="📖 Manual de Uso",
                    content=self._criar_aba_manual()
                ),
                ft.Tab(
                    text="ℹ️ Sobre",
                    content=self._criar_aba_sobre()
                )
            ]
        )

        # Botão de Salvar (fixo no rodapé)
        self.btn_salvar = ft.ElevatedButton(
            "💾 Salvar Configurações",
            icon=ft.icons.SAVE,
            on_click=self.salvar_configuracoes,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.GREEN}
            )
        )
        
        self.btn_recarregar = ft.ElevatedButton(
            "🔄 Recarregar",
            icon=ft.icons.REFRESH,
            on_click=self._recarregar_config,
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK87},
                bgcolor={"": ft.colors.GREY}
            )
        )

        self.controls = [self.title, self.tabs, ft.Row([self.btn_recarregar, self.btn_salvar], alignment=ft.MainAxisAlignment.END)]

    def _criar_aba_backup(self):
        """Cria aba de configurações de backup"""
        
        # Backup Automático
        self.backup_auto_check = ft.Checkbox(
            label="Criar backup automático ao iniciar o sistema",
            value=self.config['backup_automatico']
        )

        # Limpeza de Backups Antigos
        self.dias_spinbox = ft.Slider(
            min=1,
            max=90,
            value=self.config['backup_dias'],
            divisions=89,
            label="{value} dias"
        )
        
        dias_text = ft.Text(f"Manter backups dos últimos {int(self.config['backup_dias'])} dias", size=12)

        def on_dias_change(e):
            dias_text.value = f"Manter backups dos últimos {int(float(e.control.value))} dias"
            self.update()

        self.dias_spinbox.on_change = on_dias_change

        # Pasta de Backup
        self.pasta_field = ft.TextField(
            value=self.config['backup_pasta'],
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.btn_escolher_pasta = ft.ElevatedButton(
            "📁 Escolher",
            icon=ft.icons.FOLDER_OPEN,
            on_click=self._escolher_pasta_backup,
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK87},
                bgcolor={"": ft.colors.GREY}
            )
        )

        # Gerenciar Backups
        self.btn_criar_backup = ft.ElevatedButton(
            "💾 Criar Backup Agora",
            icon=ft.icons.BACKUP,
            on_click=self._criar_backup_manual,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.GREEN}
            )
        )
        
        self.btn_listar_backups = ft.ElevatedButton(
            "📋 Listar Backups",
            icon=ft.icons.LIST_ALT,
            on_click=self._listar_backups,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.BLUE}
            )
        )
        
        self.btn_limpar_backups = ft.ElevatedButton(
            "🗑️ Limpar Antigos",
            icon=ft.icons.DELETE_SWEEP,
            on_click=self._limpar_backups_antigos,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.RED}
            )
        )
        
        self.btn_restaurar_backup = ft.ElevatedButton(
            "♻️ Restaurar Backup",
            icon=ft.icons.SETTINGS_BACKUP_RESTORE,
            on_click=self._restaurar_backup,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.ORANGE}
            )
        )

        # Status
        self.backup_status = ft.Text("", size=12)

        # Layout da aba
        layout = ft.Column([
            ft.Text("Backup Automático", size=16, weight=ft.FontWeight.BOLD),
            self.backup_auto_check,
            ft.Divider(height=20),
            ft.Text("Limpeza Automática", size=16, weight=ft.FontWeight.BOLD),
            dias_text,
            self.dias_spinbox,
            ft.Divider(height=20),
            ft.Text("Pasta de Backup", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([self.pasta_field, self.btn_escolher_pasta]),
            ft.Divider(height=20),
            ft.Text("Gerenciar Backups", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([self.btn_criar_backup, self.btn_listar_backups, self.btn_limpar_backups, self.btn_restaurar_backup]),
            self.backup_status
        ], expand=True)

        return layout

    def _criar_aba_geral(self):
        """Cria aba de configurações gerais"""
        
        # Tema
        self.tema_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="claro", label="☀️ Claro"),
                ft.Radio(value="escuro", label="🌙 Escuro")
            ]),
            value=self.config['tema']
        )
        
        tema_aviso = ft.Text("(Reinicie a aplicação para aplicar o tema)", size=12, color=ft.colors.GREY)

        # Usuário Padrão
        self.usuario_field = ft.TextField(
            label="Nome do Usuário",
            hint_text="Ex: João Silva",
            value=self.config['usuario_padrao'],
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        usuario_desc = ft.Text("Nome usado por padrão ao registrar movimentações:", size=12, color=ft.colors.GREY)

        # Estatísticas
        stats = self.db.get_estatisticas()
        
        stats_text = f"""
📊 ESTATÍSTICAS GERAIS

Total de Clientes: {stats['total_clientes']}
Total de Equipamentos: {stats['total_equipamentos']}

Equipamentos por Status:
"""
        for status, total in stats['por_status'].items():
            stats_text += f"  • {status}: {total}\n"

        stats_card = ft.Container(
            content=ft.Text(stats_text.strip(), selectable=True),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            bgcolor=ft.colors.GREY_100
        )

        # Banco de Dados
        db_info = f"Arquivo: fastech.db\nTamanho: {self._get_db_size()}"

        db_card = ft.Text(db_info)

        # Status
        self.geral_status = ft.Text("", size=12)

        # Layout da aba
        layout = ft.Column([
            ft.Text("Aparência", size=16, weight=ft.FontWeight.BOLD),
            self.tema_radio,
            tema_aviso,
            ft.Divider(height=20),
            ft.Text("Usuário Padrão", size=16, weight=ft.FontWeight.BOLD),
            usuario_desc,
            self.usuario_field,
            ft.Divider(height=20),
            ft.Text("Estatísticas do Sistema", size=16, weight=ft.FontWeight.BOLD),
            stats_card,
            ft.Divider(height=20),
            ft.Text("Banco de Dados", size=16, weight=ft.FontWeight.BOLD),
            db_card,
            self.geral_status
        ], expand=True)

        return layout

    def _criar_aba_manual(self):
        """Cria aba de manual de uso"""
        
        manual_content = """
1. CADASTRO DE CLIENTES
   • Acesse "Clientes" → "Novo Cliente"
   • Preencha os dados obrigatórios: Nome, CPF/CNPJ, Email, Telefone
   • O código é gerado automaticamente
   • Use "Salvar" para confirmar ou "Cancelar" para voltar

2. CADASTRO DE EQUIPAMENTOS
   • Acesse "Equipamentos" → "Novo Equipamento"
   • Preencha os dados: Código, Descrição, Marca, Modelo, Patrimônio
   • Selecione o cliente proprietário
   • Defina o status inicial (Disponível, Em Manutenção, etc.)
   • Use "Salvar" para confirmar

3. MOVIMENTAÇÃO DE EQUIPAMENTOS
   • Acesse "Movimentações" → "Nova Movimentação"
   • Selecione o equipamento e o tipo de movimentação
   • Preencha os detalhes: Data, Responsável, Observações
   • Para devolução, selecione "Devolução" como tipo
   • O status do equipamento é atualizado automaticamente

4. CONSULTAS E RELATÓRIOS
   • Acesse "Consultas" para pesquisar equipamentos
   • Use filtros por cliente, status ou data
   • Exporte resultados em Excel usando o botão "Exportar"

5. CONFIGURAÇÕES DO SISTEMA
   • Acesse "Configurações" para ajustar:
     - Backup automático
     - Tema (Claro/Escuro)
     - Usuário padrão
     - Pasta de backups

6. BACKUP E RESTAURAÇÃO
   • Configure backup automático na aba "Configurações"
   • Use "Criar Backup Agora" para backup manual
   • Acompanhe os backups antigos e limpe conforme necessário
   • Use "Restaurar Backup" apenas em casos especiais

7. DICAS IMPORTANTES
   • Sempre faça backup antes de operações críticas
   • Use códigos descritivos para equipamentos
   • Mantenha os dados dos clientes atualizados
   • Utilize o campo de observações nas movimentações

8. SUPORTE E AJUDA
   • Em caso de dúvidas, consulte a documentação
   • Contate o administrador do sistema para problemas técnicos
   • Use a aba "Sobre" para informações da versão
        """.strip()

        # Criar scrollable content
        scrollable_content = ft.Column([
            ft.Text("📖 MANUAL DE USO DO SISTEMA FASTTECH CONTROL", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
            ft.Divider(height=20),
        ], scroll=ft.ScrollMode.AUTO)

        # Adicionar conteúdo formatado
        lines = manual_content.split('\n')
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
                # Título de seção
                scrollable_content.controls.append(
                    ft.Text(line.strip(), size=14, weight=ft.FontWeight.BOLD)
                )
            elif line.startswith('   •'):
                # Item de lista
                scrollable_content.controls.append(
                    ft.Text(line.strip(), size=12, color=ft.colors.GREY)
                )
            elif line.startswith('     -'):
                # Sub-item de lista
                scrollable_content.controls.append(
                    ft.Text(line.strip(), size=12, color=ft.colors.GREY_700)
                )
            else:
                # Texto normal
                scrollable_content.controls.append(
                    ft.Text(line.strip(), size=12)
                )

        # Scrollable container
        manual_scroll = ft.ListView([scrollable_content], expand=True)

        return manual_scroll

    def _criar_aba_sobre(self):
        """Cria aba de informações sobre o sistema"""
        
        sobre_content = ft.Column([
            ft.Text("ℹ️ SOBRE O SISTEMA", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
            ft.Divider(height=20),
            ft.Text("Sistema de Controle de Equipamentos FastTech", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Versão: 1.0.0", size=14),
            ft.Text("Desenvolvedor: FastTech Solutions", size=14),
            ft.Divider(height=20),
            ft.Text("FUNCIONALIDADES PRINCIPAIS:", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("• Cadastro e gerenciamento de clientes", size=12),
            ft.Text("• Cadastro e controle de equipamentos", size=12),
            ft.Text("• Registro de movimentações (entrega, devolução, manutenção)", size=12),
            ft.Text("• Histórico completo de cada equipamento", size=12),
            ft.Text("• Consultas avançadas e relatórios", size=12),
            ft.Text("• Sistema de backup e restauração", size=12),
            ft.Divider(height=20),
            ft.Text("SUPORTE:", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("Para suporte técnico, entre em contato com:", size=12),
            ft.Text("Email: suporte@fasttech.com.br", size=12),
            ft.Text("Telefone: (11) 99999-9999", size=12),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

        return sobre_content

    def _get_db_size(self):
        """Obtém o tamanho do banco de dados"""
        try:
            size_bytes = os.path.getsize("fastech.db")
            size_mb = size_bytes / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        except:
            return "N/A"

    def _escolher_pasta_backup(self, e):
        """Escolhe pasta para backup"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.pasta_field.value = e.path
                self.update()

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        file_picker.get_directory_path(dialog_title="Selecione a pasta para backups")

    def _criar_backup_manual(self, e):
        """Cria backup manualmente"""
        try:
            sucesso = self.backup_manager.criar_backup_manual()
            if sucesso:
                self._show_status("Backup criado com sucesso!", "success")
            else:
                self._show_status("Falha ao criar backup", "error")
        except Exception as ex:
            self._show_status(f"Erro ao criar backup: {str(ex)}", "error")

    def _listar_backups(self, e):
        """Lista backups existentes"""
        try:
            backups = self.backup_manager.listar_backups()
            if backups:
                backup_list = "\\n".join(backups)
                self._show_status(f"Backups encontrados:\\n{backup_list}", "info")
            else:
                self._show_status("Nenhum backup encontrado", "info")
        except Exception as ex:
            self._show_status(f"Erro ao listar backups: {str(ex)}", "error")

    def _limpar_backups_antigos(self, e):
        """Limpa backups antigos"""
        try:
            dias = int(self.dias_spinbox.value)
            removidos = self.backup_manager.limpar_backups_antigos(dias)
            self._show_status(f"{removidos} backups antigos removidos", "success")
        except Exception as ex:
            self._show_status(f"Erro ao limpar backups: {str(ex)}", "error")

    def _restaurar_backup(self, e):
        """Restaura backup"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.path:
                try:
                    sucesso = self.backup_manager.restaurar_backup(e.path)
                    if sucesso:
                        self._show_status("Backup restaurado com sucesso! Reinicie o sistema.", "success")
                    else:
                        self._show_status("Falha ao restaurar backup", "error")
                except Exception as ex:
                    self._show_status(f"Erro ao restaurar backup: {str(ex)}", "error")

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        file_picker.pick_files(
            dialog_title="Selecione o arquivo de backup para restaurar",
            allowed_extensions=["db"]
        )

    def salvar_configuracoes(self, e):
        """Salva as configurações"""
        # Atualiza configurações com valores atuais
        self.config['backup_automatico'] = self.backup_auto_check.value
        self.config['backup_dias'] = int(self.dias_spinbox.value)
        self.config['backup_pasta'] = self.pasta_field.value
        self.config['tema'] = self.tema_radio.value
        self.config['usuario_padrao'] = self.usuario_field.value

        if self._salvar_config():
            self._show_status("Configurações salvas com sucesso!", "success")
        else:
            self._show_status("Erro ao salvar configurações", "error")

    def _recarregar_config(self, e):
        """Recarrega as configurações"""
        self._carregar_config()
        self._criar_interface()
        self.update()
        self._show_status("Configurações recarregadas", "info")

    def _show_status(self, message, level="info"):
        """Mostra mensagem de status"""
        # Atualiza o status na aba atual
        if self.tabs.selected_index == 0:  # Backup
            self.backup_status.value = message
            self.backup_status.color = {"error": ft.colors.RED, "success": ft.colors.GREEN, "warning": ft.colors.ORANGE}.get(level, ft.colors.GREY)
        elif self.tabs.selected_index == 1:  # Geral
            self.geral_status.value = message
            self.geral_status.color = {"error": ft.colors.RED, "success": ft.colors.GREEN, "warning": ft.colors.ORANGE}.get(level, ft.colors.GREY)
        
        self.update()