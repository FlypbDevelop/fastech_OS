"""
Aba Dashboard - Visão geral do sistema
"""
import flet as ft
from datetime import datetime
from gui.base import BaseTab


class DashboardTab(BaseTab):
    """Aba do Dashboard com estatísticas e informações gerais"""
    
    def __init__(self, page, db, config, abrir_calendario_callback, contar_movimentacoes_callback, get_db_size_callback):
        super().__init__(page, db, config)
        self.abrir_calendario = abrir_calendario_callback
        self.contar_movimentacoes_mes = contar_movimentacoes_callback
        self.get_db_size = get_db_size_callback
    
    def build(self):
        """Constrói a interface do dashboard"""
        # Atualizar dados
        stats = self.db.get_estatisticas()
        
        # Saudação
        now = datetime.now()
        hour = now.hour
        if hour < 12:
            greeting = "Bom dia - Seja Bem vindo(a)"
        elif hour < 18:
            greeting = "Boa tarde - Seja Bem vindo(a)"
        else:
            greeting = "Boa noite - Seja Bem vindo(a)"
        
        # Header do dashboard - responsivo com hierarquia tipográfica
        dashboard_header = ft.Container(
            content=ft.Row(
                [
                    ft.Text(greeting, size=self.H2_SIZE, color=ft.Colors.GREY_600, expand=True),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("📅", size=20),
                                        ft.Text(now.strftime("%d/%m/%Y"), size=self.SMALL_SIZE, weight=ft.FontWeight.BOLD),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=4,
                                ),
                                bgcolor=self.PRIMARY_COLOR,
                                padding=16,
                                border_radius=8,
                                on_click=lambda e: self.abrir_calendario(),
                                tooltip="Clique para abrir calendário",
                            ),
                            ft.Container(width=16),
                            ft.Column(
                                [
                                    ft.Text(now.strftime("%H:%M"), size=self.H1_SIZE, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN),
                                    ft.Text("AM" if now.hour < 12 else "PM", size=self.SMALL_SIZE, color=ft.Colors.CYAN),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=24,
        )
        
        # Cards do dashboard
        em_estoque = stats['por_status'].get('Em Estoque', 0)
        com_cliente = stats['por_status'].get('Com o Cliente', 0)
        em_manutencao = stats['por_status'].get('Em Manutenção', 0)
        
        # Grid responsivo de cards com hierarquia visual
        cards_grid = ft.ResponsiveRow(
            [
                # NÍVEL 1 - Cards Principais (maiores)
                ft.Container(
                    content=self.criar_card(
                        "EQUIPAMENTOS", 
                        "CADASTRADOS", 
                        str(stats['total_equipamentos']), 
                        "📦", 
                        self.PRIMARY_COLOR,
                        nivel=1
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    content=self.criar_card(
                        "CLIENTES", 
                        "CADASTRADOS", 
                        str(stats['total_clientes']), 
                        "👥", 
                        self.PRIMARY_COLOR,
                        nivel=1
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                
                # NÍVEL 2 - Cards Secundários
                ft.Container(
                    content=self.criar_card(
                        "MOVIMENTAÇÕES", 
                        "ESTE MÊS", 
                        str(self.contar_movimentacoes_mes()), 
                        "🔄", 
                        self.SECONDARY_COLOR,
                        nivel=2
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    content=self.criar_card(
                        "EM ESTOQUE", 
                        "DISPONÍVEIS", 
                        str(em_estoque), 
                        "📊", 
                        self.SECONDARY_COLOR,
                        nivel=2
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    content=self.criar_card(
                        "COM CLIENTES", 
                        "EM USO", 
                        str(com_cliente), 
                        "📤", 
                        self.SECONDARY_COLOR,
                        nivel=2
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    content=self.criar_card(
                        "EM MANUTENÇÃO", 
                        "EQUIPAMENTOS", 
                        str(em_manutencao), 
                        "🔧", 
                        self.ACCENT_COLOR if em_manutencao > 0 else self.SECONDARY_COLOR,
                        nivel=2
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                
                # NÍVEL 3 - Cards Informativos (menores)
                ft.Container(
                    content=self.criar_card(
                        "SISTEMA", 
                        "STATUS", 
                        "OK", 
                        "✅", 
                        ft.Colors.GREEN_600,
                        nivel=3
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    content=self.criar_card(
                        "BANCO DE DADOS", 
                        self.get_db_size(), 
                        "💾", 
                        "💾", 
                        self.SECONDARY_COLOR,
                        nivel=3
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
            ],
            spacing=16,
            run_spacing=16,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    dashboard_header,
                    ft.Container(height=24),
                    cards_grid,
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=24,
            expand=True,
        )
    
    def criar_card(self, title_line1, title_line2, value, icon, color, nivel=2):
        """Cria um card do dashboard responsivo com hierarquia visual
        
        Args:
            nivel: 1 (principal), 2 (secundário), 3 (informativo)
        """
        title_color = self.get_adaptive_color(ft.Colors.WHITE, ft.Colors.GREY_900)
        subtitle_color = self.get_adaptive_color(ft.Colors.GREY_300, ft.Colors.GREY_800)
        value_color = self.get_adaptive_color(ft.Colors.WHITE, ft.Colors.GREY_900)
        
        # Definir tamanhos baseados no nível
        if nivel == 1:
            height = 180
            padding = 24
            border_width = 4
            title_size = self.BODY_SIZE
            subtitle_size = self.SMALL_SIZE
            value_size = 48
            icon_size = 48
        elif nivel == 3:
            height = 120
            padding = 16
            border_width = 2
            title_size = self.SMALL_SIZE
            subtitle_size = self.CAPTION_SIZE
            value_size = 24
            icon_size = 32
        else:  # nivel == 2
            height = 150
            padding = 20
            border_width = 3
            title_size = self.BODY_SIZE
            subtitle_size = self.SMALL_SIZE
            value_size = 40
            icon_size = 40
        
        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(title_line1, size=title_size, weight=ft.FontWeight.BOLD, color=title_color),
                    ft.Text(title_line2, size=subtitle_size, color=subtitle_color, weight=ft.FontWeight.W_600),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            ft.Text(icon, size=icon_size),
                            ft.Text(
                                value, 
                                size=value_size, 
                                weight=ft.FontWeight.BOLD, 
                                color=value_color,
                                style=ft.TextStyle(
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=2,
                                        color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                                    )
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=4,
            ),
            padding=padding,
            bgcolor=color + "20",
            border_radius=16,
            border=ft.Border(
                left=ft.BorderSide(border_width, color + "60"),
                right=ft.BorderSide(border_width, color + "60"),
                top=ft.BorderSide(border_width, color + "60"),
                bottom=ft.BorderSide(border_width, color + "60"),
            ),
            height=height,
            animate=200,
            on_hover=self.card_hover,
        )
        
        return card
    
    def card_hover(self, e):
        """Efeito hover nos cards"""
        if e.data == "true":
            # Mouse entrou
            e.control.elevation = 12
            e.control.scale = 1.03
            e.control.shadow = ft.BoxShadow(
                spread_radius=4,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_700),
                offset=ft.Offset(0, 4),
            )
        else:
            # Mouse saiu
            e.control.elevation = 0
            e.control.scale = 1.0
            e.control.shadow = None
        e.control.update()
