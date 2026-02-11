"""
FastTech Control - Aplicação Principal
Sistema de Gestão de Equipamentos com interface moderna Flet
"""

import flet as ft
from database import Database
from datetime import datetime
import calendar
import warnings

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
        
        # Carregar configurações primeiro
        self.carregar_config()
        
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
        # Atualizar layout responsivo se necessário
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
        
        # Botões de navegação
        def ir_para_dashboard(e):
            self.content_container.content = self.dashboard_content
            self.page.update()
        
        def ir_para_clientes(e):
            self.content_container.content = self.clientes_content
            self.page.update()
        
        def ir_para_equipamentos(e):
            self.content_container.content = self.equipamentos_content
            self.page.update()
        
        def ir_para_movimentacoes(e):
            self.content_container.content = self.movimentacoes_content
            self.page.update()
        
        def ir_para_consultas(e):
            self.content_container.content = self.consultas_content
            self.page.update()
        
        def ir_para_configuracoes(e):
            self.content_container.content = self.configuracoes_content
            self.page.update()
        
        # Barra de navegação responsiva
        nav_bar = ft.Container(
            content=ft.Row(
                [
                    ft.FilledButton(
                        "🏠 Dashboard",
                        on_click=ir_para_dashboard,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                            elevation={"": 3, "hovered": 6},
                        ),
                    ),
                    ft.FilledButton(
                        "👥 Clientes",
                        on_click=ir_para_clientes,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                            elevation={"": 3, "hovered": 6},
                        ),
                    ),
                    ft.FilledButton(
                        "📦 Equipamentos",
                        on_click=ir_para_equipamentos,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                            elevation={"": 3, "hovered": 6},
                        ),
                    ),
                    ft.FilledButton(
                        "🔄 Movimentações",
                        on_click=ir_para_movimentacoes,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                            elevation={"": 3, "hovered": 6},
                        ),
                    ),
                    ft.FilledButton(
                        "🔍 Consultas",
                        on_click=ir_para_consultas,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                            elevation={"": 3, "hovered": 6},
                        ),
                    ),
                    ft.FilledButton(
                        "⚙️ Configurações",
                        on_click=ir_para_configuracoes,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                            elevation={"": 3, "hovered": 6},
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=12,
                wrap=True,  # Permite quebra de linha em telas pequenas
                run_spacing=10,  # Espaçamento vertical quando quebra linha
            ),
            bgcolor=self.get_bg_color(),
            padding=15,
        )
        
        # Layout principal
        self.page.add(
            ft.Column(
                [
                    header,
                    nav_bar,
                    self.content_container,
                ],
                spacing=0,
                expand=True,
            )
        )
    
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


def main(page: ft.Page):
    app = FastTechApp(page)


if __name__ == "__main__":
    ft.app(main)
