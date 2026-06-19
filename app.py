"""
FastTech Control - Aplicação Principal
Sistema de Gestão de Equipamentos com interface moderna Flet
"""

import flet as ft
from database import Database
from datetime import datetime
import calendar
import warnings
from utils.backup import BackupManager

# Importar módulos das abas
from gui.dashboard import DashboardTab
from gui.clientes import ClientesTab
from gui.equipamentos import EquipamentosTab
from gui.movimentacoes import MovimentacoesTab
from gui.consultas import ConsultasTab
from gui.configuracoes import ConfiguracoesTab

# Suprimir todos os avisos de depreciação
warnings.filterwarnings("ignore", category=DeprecationWarning)


class FastTechApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database()
        self.lembretes = {}
        self.backup_manager = BackupManager()
        
        # Carregar configurações primeiro
        self.carregar_config()
        
        # Executar backup automático se configurado
        if self.config.get('backup_automatico', False):
            self.executar_backup_automatico()
        
        # Limpar backups antigos se configurado
        dias_manter = self.config.get('backup_dias', 7)
        if dias_manter > 0:
            self.limpar_backups_antigos(dias_manter)
        
        # Configurações da página
        self.page.title = "FastTech Control - Sistema de Gestão"
        # Aplicar tema salvo
        if self.config['tema'] == 'claro':
            self.page.theme_mode = ft.ThemeMode.LIGHT
        else:
            self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        # Remover tamanhos fixos para permitir responsividade
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        
        # Listener para mudanças de tamanho
        self.page.on_resize = self.on_page_resize
        
        # Criar interface
        self.criar_interface()
    
    def get_adaptive_color(self, dark_color, light_color):
        """Retorna cor adaptativa baseada no tema atual"""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            return light_color
        return dark_color
    
    def get_bg_color(self):
        """Retorna cor de fundo adaptativa"""
        return self.get_adaptive_color(ft.Colors.BLUE_GREY_900, ft.Colors.GREY_100)
    
    def get_text_color(self):
        """Retorna cor de texto adaptativa"""
        return self.get_adaptive_color(ft.Colors.WHITE, ft.Colors.BLACK)
    
    def get_secondary_text_color(self):
        """Retorna cor de texto secundário adaptativa"""
        return self.get_adaptive_color(ft.Colors.GREY_400, ft.Colors.GREY_700)
    
    def on_page_resize(self, e):
        """Callback para quando a página é redimensionada"""
        self.page.update()
    
    def is_mobile_view(self):
        """Verifica se está em visualização mobile (largura < 800px)"""
        return self.page.window_width and self.page.window_width < 800
    
    def is_tablet_view(self):
        """Verifica se está em visualização tablet (largura entre 800 e 1200px)"""
        return self.page.window_width and 800 <= self.page.window_width < 1200
    
    def criar_interface(self):
        """Cria a interface principal"""
        # Header
        header = self.criar_header()
        
        # Criar conteúdos das abas
        self.dashboard_content = self.criar_dashboard()
        self.clientes_content = self.criar_clientes()
        self.equipamentos_content = self.criar_equipamentos()
        self.movimentacoes_content = self.criar_movimentacoes()
        self.consultas_content = self.criar_consultas()
        self.configuracoes_content = self.criar_configuracoes()
        
        # Container para conteúdo dinâmico
        self.content_container = ft.Container(
            content=self.dashboard_content,
            expand=True,
        )
        
        # Lista de conteúdos das abas
        self.conteudos_abas = [
            self.dashboard_content,
            self.clientes_content,
            self.equipamentos_content,
            self.movimentacoes_content,
            self.consultas_content,
            self.configuracoes_content,
        ]
        
        # Estado da sidebar
        self.sidebar_expanded = True
        self.sidebar_width = 220
        self.sidebar_collapsed_width = 72
        self.aba_selecionada = 0
        
        # Itens do menu
        self.menu_items = [
            ("🏠", ft.Icons.HOME_OUTLINED, ft.Icons.HOME, "Dashboard"),
            ("👥", ft.Icons.PEOPLE_OUTLINED, ft.Icons.PEOPLE, "Clientes"),
            ("📦", ft.Icons.DEVICES_OUTLINED, ft.Icons.DEVICES, "Equipamentos"),
            ("🔄", ft.Icons.SWAP_HORIZ_OUTLINED, ft.Icons.SWAP_HORIZ, "Movimentações"),
            ("🔍", ft.Icons.SEARCH_OUTLINED, ft.Icons.SEARCH, "Consultas"),
            ("⚙️", ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS, "Configurações"),
        ]
        
        # Container da sidebar (referência para atualização)
        self.sidebar_container = ft.Container()
        self.criar_sidebar()
        
        # Layout principal: Row (sidebar + conteúdo)
        self.page.add(
            ft.Row(
                [
                    self.sidebar_container,
                    ft.Column(
                        [
                            header,
                            self.content_container,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )
    
    def criar_sidebar(self):
        """Cria ou atualiza a sidebar"""
        menu_buttons = []
        
        for i, (emoji, icon_outlined, icon_filled, label) in enumerate(self.menu_items):
            is_selected = (i == self.aba_selecionada)
            
            if self.sidebar_expanded:
                # Modo expandido: ícone + texto lado a lado
                icon_widget = ft.Icon(
                    icon_filled if is_selected else icon_outlined,
                    color=ft.Colors.WHITE if is_selected else ft.Colors.WHITE70,
                    size=22,
                )
                text_widget = ft.Text(
                    label,
                    color=ft.Colors.WHITE if is_selected else ft.Colors.WHITE70,
                    size=13,
                    weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.NORMAL,
                    expand=True,
                )
                btn_content = ft.Row(
                    [icon_widget, text_widget],
                    spacing=12,
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                )
                btn_width = self.sidebar_width - 32
            else:
                # Modo colapsado: apenas ícone
                btn_content = ft.Icon(
                    icon_filled if is_selected else icon_outlined,
                    color=ft.Colors.WHITE if is_selected else ft.Colors.WHITE70,
                    size=22,
                )
                btn_width = 56
            
            btn = ft.Container(
                content=btn_content,
                width=btn_width,
                height=44,
                padding=ft.padding.only(left=14, right=10, top=10, bottom=10),
                border_radius=8,
                bgcolor=ft.Colors.BLUE_700 if is_selected else ft.Colors.TRANSPARENT,
                on_click=lambda e, idx=i: self.navegar_para(idx),
                ink=True,
            )
            menu_buttons.append(btn)
        
        # Botão de colapsar/expandir
        toggle_icon = ft.Icons.CHEVRON_LEFT if self.sidebar_expanded else ft.Icons.CHEVRON_RIGHT
        toggle_btn = ft.Container(
            content=ft.Icon(toggle_icon, color=ft.Colors.WHITE70, size=20),
            width=56 if not self.sidebar_expanded else self.sidebar_width - 32,
            height=42,
            padding=ft.padding.only(left=14, right=10, top=11, bottom=11),
            border_radius=8,
            on_click=lambda e: self.toggle_sidebar(),
            ink=True,
        )
        
        # Montar sidebar
        sidebar_content = ft.Column(
            [
                # Logo/título no topo
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.WHITE, size=24),
                            ft.Text(
                                "FastTech",
                                color=ft.Colors.WHITE,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                visible=self.sidebar_expanded,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER if not self.sidebar_expanded else ft.MainAxisAlignment.START,
                        expand=self.sidebar_expanded,
                    ),
                    padding=ft.padding.only(left=12, right=8, top=16, bottom=16),
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                # Itens do menu
                ft.Column(menu_buttons, spacing=4, expand=True),
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                # Botão colapsar
                toggle_btn,
            ],
            spacing=0,
            expand=True,
        )
        
        self.sidebar_container.content = sidebar_content
        self.sidebar_container.width = self.sidebar_width if self.sidebar_expanded else self.sidebar_collapsed_width
        self.sidebar_container.bgcolor = ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_900)
        self.sidebar_container.padding = ft.padding.only(left=8, right=6, top=0, bottom=0)
    
    def toggle_sidebar(self):
        """Alterna entre sidebar expandida e colapsada"""
        self.sidebar_expanded = not self.sidebar_expanded
        self.criar_sidebar()
        self.page.update()
    
    def navegar_para(self, index):
        """Navega para a aba selecionada"""
        self.aba_selecionada = index
        self.content_container.content = self.conteudos_abas[index]
        self.criar_sidebar()
        self.page.update()
    
    def criar_header(self):
        """Cria o cabeçalho da aplicação"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("⚙️", size=40),
                    ft.Column(
                        [
                            ft.Text("FastTech Control", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text("Sistema de Gestão de Equipamentos", size=12, color=ft.Colors.WHITE70),
                        ],
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor=ft.Colors.BLUE_700,
            padding=20,
        )
    
    def criar_dashboard(self):
        """Cria a aba do dashboard"""
        tab = DashboardTab(
            self.page, 
            self.db, 
            self.config,
            self.abrir_calendario,
            self.contar_movimentacoes_mes,
            self.get_db_size
        )
        return tab.build()
    
    def criar_clientes(self):
        """Cria a aba de clientes"""
        tab = ClientesTab(self.page, self.db, self.config)
        return tab.build()
    
    def criar_equipamentos(self):
        """Cria a aba de equipamentos"""
        tab = EquipamentosTab(self.page, self.db, self.config)
        return tab.build()
    
    def criar_movimentacoes(self):
        """Cria a aba de movimentações"""
        tab = MovimentacoesTab(self.page, self.db, self.config)
        return tab.build()
    
    def criar_consultas(self):
        """Cria a aba de consultas"""
        tab = ConsultasTab(self.page, self.db, self.config)
        return tab.build()
    
    def criar_configuracoes(self):
        """Cria a aba de configurações"""
        tab = ConfiguracoesTab(
            self.page,
            self.db,
            self.config,
            self.carregar_config,
            self.salvar_config,
            self.get_db_size
        )
        return tab.build()
    
    def carregar_config(self):
        """Carrega configurações do arquivo"""
        import json
        import os
        
        self.config = {
            'backup_automatico': False,
            'backup_dias': 7,
            'backup_pasta': 'backups',
            'tema': 'escuro',
            'usuario_padrao': 'Técnico'
        }
        
        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    for key in saved_config:
                        if key in self.config:
                            self.config[key] = saved_config[key]
            except:
                pass
    
    def salvar_config(self):
        """Salva configurações no arquivo"""
        import json
        
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            return False
    
    def abrir_calendario(self):
        """Abre o diálogo do calendário"""
        def fechar_dialogo(e):
            dialogo.open = False
            self.page.update()
        
        dialogo = ft.AlertDialog(
            title=ft.Text("📅 Calendário e Lembretes"),
            content=ft.Container(
                content=ft.Text("Calendário em desenvolvimento", size=16),
                width=500,
                height=400,
            ),
            actions=[
                ft.TextButton("Fechar", on_click=fechar_dialogo),
            ],
        )
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def contar_movimentacoes_mes(self):
        """Conta movimentações do mês atual"""
        try:
            cursor = self.db.conn.cursor()
            agora = datetime.now()
            inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            cursor.execute("""
                SELECT COUNT(*) FROM historico_posse 
                WHERE data_inicio >= ?
            """, (inicio_mes.isoformat(),))
            
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        except:
            return 0
    
    def get_db_size(self):
        """Retorna o tamanho do banco de dados"""
        try:
            import os
            size = os.path.getsize('fastech.db')
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        except:
            return "-- KB"
    
    def executar_backup_automatico(self):
        """Executa backup automático ao iniciar o sistema"""
        try:
            backup_path = self.backup_manager.criar_backup()
            print(f"✅ Backup automático criado: {backup_path}")
        except Exception as e:
            print(f"❌ Erro ao criar backup automático: {str(e)}")
    
    def limpar_backups_antigos(self, dias: int):
        """Limpa backups mais antigos que X dias"""
        try:
            removidos = self.backup_manager.limpar_backups_antigos(dias)
            if removidos > 0:
                print(f"🗑️ {removidos} backup(s) antigo(s) removido(s)")
        except Exception as e:
            print(f"❌ Erro ao limpar backups antigos: {str(e)}")


def main(page: ft.Page):
    app = FastTechApp(page)


if __name__ == "__main__":
    ft.app(main)
