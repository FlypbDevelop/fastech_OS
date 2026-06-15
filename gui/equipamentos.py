"""
Aba Equipamentos - Orquestrador de busca, cadastro e serviços
"""
import flet as ft
from gui.base import BaseTab
from gui.lista_equip import EquipamentoView
from gui.servicos_equip import ServicoView


class EquipamentosTab(BaseTab):
    """Aba de gestão de equipamentos — orquestra busca, cadastro e serviços"""

    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        self.equipamento_selecionado = None
        self.view_atual = "busca"
        self.content_container = None

        self.equip_view = EquipamentoView(self, page, db, config)
        self.servico_view = ServicoView(self, page, db, config)

    def build(self):
        """Constrói a interface de equipamentos"""
        self.content_container = ft.Container(expand=True)
        nav_bar = self.criar_navegacao()
        self.mostrar_busca()
        return ft.Container(
            content=ft.Column(
                [nav_bar, self.content_container],
                spacing=0,
                expand=True,
            ),
            expand=True,
        )

    def criar_navegacao(self):
        """Cria a barra de navegação"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.FilledButton(
                        "🔍 Buscar por Serial",
                        on_click=lambda e: self.mostrar_busca(),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                        ),
                    ),
                    ft.FilledButton(
                        "📦 Cadastrar Equipamento",
                        on_click=lambda e: self.mostrar_cadastro(),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                        ),
                    ),
                    ft.FilledButton(
                        "🔧 Registrar Serviço",
                        on_click=lambda e: self.mostrar_servicos(),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                        ),
                    ),
                ],
                spacing=10,
                wrap=True,
                run_spacing=10,
            ),
            padding=15,
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
        )

    def mostrar_busca(self):
        """Delega à view de busca"""
        self.view_atual = "busca"
        self.equip_view.mostrar_busca()

    def mostrar_cadastro(self):
        """Delega à view de cadastro"""
        self.view_atual = "cadastro"
        self.equip_view.mostrar_cadastro()

    def mostrar_servicos(self):
        """Delega à view de serviços"""
        self.view_atual = "servicos"
        self.servico_view.mostrar_servicos()

    def mostrar_detalhes_equipamento(self, equip):
        """Delega à view de detalhes"""
        self.equip_view.mostrar_detalhes_equipamento(equip)
