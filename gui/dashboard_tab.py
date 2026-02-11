"""
Aba Dashboard - Visão geral do sistema
"""
import flet as ft
from datetime import datetime
from gui.base_tab import BaseTab


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
        
        # Header do dashboard
        dashboard_header = ft.Container(
            content=ft.Row(
                [
                    ft.Text(greeting, size=18, color=ft.Colors.GREY_500),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("📅", size=20),
                                        ft.Text(now.strftime("%d/%m/%Y"), size=12, weight=ft.FontWeight.BOLD),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5,
                                ),
                                bgcolor=ft.Colors.BLUE_900,
                                padding=15,
                                border_radius=10,
                                on_click=lambda e: self.abrir_calendario(),
                                tooltip="Clique para abrir calendário",
                            ),
                            ft.Container(width=20),
                            ft.Column(
                                [
                                    ft.Text(now.strftime("%H:%M"), size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN),
                                    ft.Text("AM" if now.hour < 12 else "PM", size=14, color=ft.Colors.CYAN),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.Padding(left=40, right=40, top=30, bottom=20),
        )
        
        # Cards do dashboard
        em_estoque = stats['por_status'].get('Em Estoque', 0)
        com_cliente = stats['por_status'].get('Com o Cliente', 0)
        em_manutencao = stats['por_status'].get('Em Manutenção', 0)
        
        cards_row1 = ft.Row(
            [
                self.criar_card("EQUIPAMENTOS", "CADASTRADOS", str(stats['total_equipamentos']), "📦", ft.Colors.BLUE),
                self.criar_card("MOVIMENTAÇÕES", "ESTE MÊS", str(self.contar_movimentacoes_mes()), "🔄", ft.Colors.AMBER),
                self.criar_card("EM MANUTENÇÃO", "EQUIPAMENTOS", str(em_manutencao), "🔧", ft.Colors.ORANGE),
                self.criar_card("SISTEMA", "STATUS", "OK", "✅", ft.Colors.GREEN),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True,
            run_spacing=20,
        )
        
        cards_row2 = ft.Row(
            [
                self.criar_card("CLIENTES", "CADASTRADOS", str(stats['total_clientes']), "👥", ft.Colors.GREEN_700),
                self.criar_card("EM ESTOQUE", "DISPONÍVEIS", str(em_estoque), "📊", ft.Colors.BROWN),
                self.criar_card("COM CLIENTES", "EM USO", str(com_cliente), "📤", ft.Colors.INDIGO),
                self.criar_card("BANCO DE DADOS", self.get_db_size(), "💾", "💾", ft.Colors.AMBER_900),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True,
            run_spacing=20,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    dashboard_header,
                    ft.Container(height=20),
                    cards_row1,
                    ft.Container(height=20),
                    cards_row2,
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding(left=40, right=40, bottom=30),
            expand=True,
        )
    
    def criar_card(self, title_line1, title_line2, value, icon, color):
        """Cria um card do dashboard"""
        title_color = self.get_adaptive_color(ft.Colors.WHITE, ft.Colors.GREY_900)
        subtitle_color = self.get_adaptive_color(ft.Colors.GREY_300, ft.Colors.GREY_800)
        value_color = self.get_adaptive_color(ft.Colors.WHITE, ft.Colors.GREY_900)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title_line1, size=13, weight=ft.FontWeight.BOLD, color=title_color),
                    ft.Text(title_line2, size=11, color=subtitle_color, weight=ft.FontWeight.W_600),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.Text(icon, size=40),
                            ft.Text(
                                value, 
                                size=42, 
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
                spacing=5,
            ),
            width=280,
            height=150,
            padding=20,
            bgcolor=color + "20",
            border_radius=15,
            border=ft.Border(
                left=ft.BorderSide(3, color + "60"),
                right=ft.BorderSide(3, color + "60"),
                top=ft.BorderSide(3, color + "60"),
                bottom=ft.BorderSide(3, color + "60"),
            ),
        )
