"""
Aba Configurações - Configurações do sistema
"""
import flet as ft
from gui.base import BaseTab
from utils.backup import BackupManager


class ConfiguracoesTab(BaseTab):
    """Aba de configurações do sistema"""
    
    def __init__(self, page, db, config, carregar_config_callback, salvar_config_callback, get_db_size_callback):
        super().__init__(page, db, config)
        self.carregar_config = carregar_config_callback
        self.salvar_config = salvar_config_callback
        self.get_db_size = get_db_size_callback
        self.config_view = "backup"
        self.config_content_container = None
        self.backup_manager = BackupManager()
    
    def build(self):
        """Constrói a interface de configurações"""
        # Carregar configurações
        self.carregar_config()
        
        # Container para conteúdo dinâmico
        self.config_content_container = ft.Container(expand=True)
        
        # Sub-navegação
        subnav = ft.Container(
            content=ft.Row(
                [
                    ft.FilledButton("💾 Backup", on_click=self.ir_para_backup, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                    ft.FilledButton("⚙️ Geral", on_click=self.ir_para_geral, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                    ft.FilledButton("ℹ️ Sobre", on_click=self.ir_para_sobre, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                ],
                spacing=10,
            ),
            padding=15,
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
        )
        
        # Inicializar com primeira view
        self.config_content_container.content = self.criar_config_backup()
        
        return ft.Container(
            content=ft.Column(
                [
                    subnav,
                    self.config_content_container,
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
        )
    
    def ir_para_backup(self, e):
        """Navega para view de backup"""
        self.config_view = "backup"
        self.config_content_container.content = self.criar_config_backup()
        self.page.update()
    
    def ir_para_geral(self, e):
        """Navega para view geral"""
        self.config_view = "geral"
        self.config_content_container.content = self.criar_config_geral()
        self.page.update()
    
    def ir_para_sobre(self, e):
        """Navega para view sobre"""
        self.config_view = "sobre"
        self.config_content_container.content = self.criar_config_sobre()
        self.page.update()
    
    def criar_config_backup(self):
        """Cria a view de configurações de backup"""
        # Checkbox backup automático
        self.backup_auto_check = ft.Checkbox(
            label="Criar backup automático ao iniciar o sistema",
            value=self.config['backup_automatico'],
        )
        
        # Dias para manter backups
        self.backup_dias_field = ft.TextField(
            label="Manter backups dos últimos (dias)",
            value=str(self.config['backup_dias']),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        # Pasta de backup
        self.backup_pasta_field = ft.TextField(
            label="Pasta de Backup",
            value=self.config['backup_pasta'],
        )
        
        # Status
        self.backup_status = ft.Text("", size=14)
        
        # Lista de backups
        backups = self.backup_manager.listar_backups()
        
        if backups:
            backup_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Tamanho", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
                ],
                rows=[],
            )
            
            for backup in backups[:10]:  # Mostrar apenas os 10 mais recentes
                def deletar_backup(e, caminho=backup['caminho']):
                    try:
                        self.backup_manager.deletar_backup(caminho)
                        self.backup_status.value = "✅ Backup deletado com sucesso!"
                        self.backup_status.color = ft.Colors.GREEN
                        # Recarregar view
                        self.config_content_container.content = self.criar_config_backup()
                        self.page.update()
                    except Exception as ex:
                        self.backup_status.value = f"❌ Erro ao deletar: {str(ex)}"
                        self.backup_status.color = ft.Colors.RED
                        self.page.update()
                
                backup_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(backup['nome'], size=12)),
                            ft.DataCell(ft.Text(self.backup_manager.formatar_tamanho(backup['tamanho']), size=12)),
                            ft.DataCell(ft.Text(backup['data_criacao'].strftime("%d/%m/%Y %H:%M"), size=12)),
                            ft.DataCell(
                                ft.TextButton("🗑️ Deletar", on_click=deletar_backup, tooltip="Deletar backup")
                            ),
                        ],
                    )
                )
            
            backups_section = [
                ft.Text("Backups Disponíveis (10 mais recentes)", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([backup_table], scroll=ft.ScrollMode.AUTO),
                    height=300,
                ),
            ]
        else:
            backups_section = [
                ft.Text("Backups Disponíveis", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Nenhum backup encontrado", size=14, color=ft.Colors.GREY_400),
            ]
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Configurações de Backup", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Backup Automático", size=16, weight=ft.FontWeight.BOLD),
                    self.backup_auto_check,
                    ft.Text("Limpeza Automática", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Backups mais antigos que este período serão removidos automaticamente", size=12, color=ft.Colors.GREY_400),
                    self.backup_dias_field,
                    ft.Text("Pasta de Backup", size=16, weight=ft.FontWeight.BOLD),
                    self.backup_pasta_field,
                    ft.Text("Gerenciar Backups", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.FilledButton("💾 Criar Backup Agora", on_click=self.criar_backup_agora),
                            ft.FilledButton("💾 Salvar Configurações", on_click=self.salvar_config_backup),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self.backup_status,
                    ft.Divider(),
                ] + backups_section,
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
        )
    
    def criar_backup_agora(self, e):
        """Cria um backup imediatamente"""
        try:
            backup_path = self.backup_manager.criar_backup()
            self.backup_status.value = f"✅ Backup criado: {backup_path}"
            self.backup_status.color = ft.Colors.GREEN
        except Exception as ex:
            self.backup_status.value = f"❌ Erro: {str(ex)}"
            self.backup_status.color = ft.Colors.RED
        self.page.update()
    
    def salvar_config_backup(self, e):
        """Salva configurações de backup"""
        self.config['backup_automatico'] = self.backup_auto_check.value
        try:
            dias = int(self.backup_dias_field.value)
            if dias < 0:
                dias = 0
            self.config['backup_dias'] = dias
        except:
            self.config['backup_dias'] = 7
        self.config['backup_pasta'] = self.backup_pasta_field.value
        
        if self.salvar_config():
            # Executar limpeza de backups antigos se configurado
            if self.config['backup_dias'] > 0:
                try:
                    removidos = self.backup_manager.limpar_backups_antigos(self.config['backup_dias'])
                    if removidos > 0:
                        self.backup_status.value = f"✅ Configurações salvas! {removidos} backup(s) antigo(s) removido(s)"
                    else:
                        self.backup_status.value = "✅ Configurações salvas com sucesso!"
                except Exception as ex:
                    self.backup_status.value = f"✅ Configurações salvas (erro ao limpar backups: {str(ex)})"
            else:
                self.backup_status.value = "✅ Configurações salvas com sucesso!"
            self.backup_status.color = ft.Colors.GREEN
        else:
            self.backup_status.value = "❌ Erro ao salvar configurações"
            self.backup_status.color = ft.Colors.RED
        self.page.update()
    
    def criar_config_geral(self):
        """Cria a view de configurações gerais"""
        # Tema
        self.tema_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="claro", label="☀️ Claro"),
                ft.Radio(value="escuro", label="🌙 Escuro"),
            ]),
            value=self.config['tema'],
        )
        
        # Usuário padrão
        self.usuario_padrao_field = ft.TextField(
            label="Nome do Usuário Padrão",
            value=self.config['usuario_padrao'],
            hint_text="Ex: João Silva",
        )
        
        # Status
        self.geral_status = ft.Text("", size=14)
        
        # Estatísticas
        stats = self.db.get_estatisticas()
        
        stats_text = f"""📊 ESTATÍSTICAS GERAIS

Total de Clientes: {stats['total_clientes']}
Total de Equipamentos: {stats['total_equipamentos']}

Equipamentos por Status:
"""
        for status, total in stats['por_status'].items():
            stats_text += f"  • {status}: {total}\n"
        
        stats_card = ft.Container(
            content=ft.Text(stats_text.strip(), size=14),
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Configurações Gerais", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Aparência", size=16, weight=ft.FontWeight.BOLD),
                    self.tema_radio,
                    ft.Text("(O tema será aplicado imediatamente ao salvar)", size=12, color=ft.Colors.GREY_400),
                    ft.Text("Usuário Padrão", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Nome usado por padrão ao registrar movimentações:", size=12, color=ft.Colors.GREY_400),
                    self.usuario_padrao_field,
                    ft.Text("Estatísticas do Sistema", size=16, weight=ft.FontWeight.BOLD),
                    stats_card,
                    ft.Text("Banco de Dados", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Arquivo: fastech.db\nTamanho: {self.get_db_size()}", size=14),
                    ft.FilledButton("💾 Salvar Configurações", on_click=self.salvar_config_geral),
                    self.geral_status,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
        )
    
    def salvar_config_geral(self, e):
        """Salva configurações gerais"""
        self.config['tema'] = self.tema_radio.value
        self.config['usuario_padrao'] = self.usuario_padrao_field.value
        
        if self.salvar_config():
            # Aplicar tema imediatamente
            if self.config['tema'] == 'claro':
                self.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                self.page.theme_mode = ft.ThemeMode.DARK
            self.page.update()
            
            self.geral_status.value = "✅ Configurações salvas e tema aplicado!"
            self.geral_status.color = ft.Colors.GREEN
        else:
            self.geral_status.value = "❌ Erro ao salvar configurações"
            self.geral_status.color = ft.Colors.RED
        self.page.update()
    
    def criar_config_sobre(self):
        """Cria a view sobre o sistema"""
        info_text = """Versão: 1.0.0
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
• Flet"""
        
        info_card = ft.Container(
            content=ft.Text(info_text, size=14, text_align=ft.TextAlign.CENTER),
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=20),
                    ft.Text("⚙️", size=48),
                    ft.Text("FastTech Control", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Sistema de Gestão de Equipamentos", size=14, color=ft.Colors.GREY_400),
                    ft.Container(height=10),
                    info_card,
                    ft.Container(height=10),
                    ft.FilledButton("🔧 Verificar Sistema", on_click=self.verificar_sistema),
                    ft.Container(height=20),
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
        )
    
    def verificar_sistema(self, e):
        """Verifica o status do sistema"""
        try:
            stats = self.db.get_estatisticas()
            
            def fechar_dialogo(ev):
                dialogo.open = False
                self.page.update()
            
            mensagem = f"""✓ Sistema OK!

Banco de dados: Conectado
Clientes: {stats['total_clientes']}
Equipamentos: {stats['total_equipamentos']}
Tamanho do banco: {self.get_db_size()}"""
            
            dialogo = ft.AlertDialog(
                title=ft.Text("Verificação do Sistema"),
                content=ft.Text(mensagem),
                actions=[
                    ft.TextButton("OK", on_click=fechar_dialogo),
                ],
            )
            
            self.page.dialog = dialogo
            dialogo.open = True
            self.page.update()
        except Exception as ex:
            pass
