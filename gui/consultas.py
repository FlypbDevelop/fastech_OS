"""
Aba Consultas - Orquestrador de consultas, relatórios e exportação
"""
import flet as ft
from gui.base import BaseTab
from gui.consulta_equip import EquipamentoConsultaView
from gui.consulta_cliente import ClienteConsultaView
from gui.consulta_relatorio import RelatorioView


class ConsultasTab(BaseTab):
    """Aba de consultas e relatórios — orquestra busca e exportação"""

    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        self.consulta_view = "equipamento"
        self.consulta_content_container = None

        self.equip_view = EquipamentoConsultaView(self, page, db, config)
        self.cliente_view = ClienteConsultaView(self, page, db, config)
        self.relatorio_view = RelatorioView(self, page, db, config)

    def build(self):
        """Constrói a interface de consultas"""
        self.consulta_content_container = ft.Container(expand=True)

        subnav = ft.Container(
            content=ft.Row(
                [
                    self.botao_primario("📦 Por Equipamento", on_click=self.ir_para_equipamento),
                    self.botao_primario("👤 Por Cliente", on_click=self.ir_para_cliente),
                    self.botao_primario("📊 Relatórios", on_click=self.ir_para_relatorios),
                ],
                spacing=10,
            ),
            padding=15,
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
        )

        self.consulta_content_container.content = self.equip_view.montar_view()

        return ft.Container(
            content=ft.Column(
                [
                    subnav,
                    self.consulta_content_container,
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
        )

    def ir_para_equipamento(self, e):
        """Navega para busca por equipamento"""
        self.consulta_view = "equipamento"
        self.consulta_content_container.content = self.equip_view.montar_view()
        self.page.update()

    def ir_para_cliente(self, e):
        """Navega para busca por cliente"""
        self.consulta_view = "cliente"
        self.consulta_content_container.content = self.cliente_view.montar_view()
        self.page.update()

    def ir_para_relatorios(self, e):
        """Navega para relatórios"""
        self.consulta_view = "relatorios"
        self.consulta_content_container.content = self.relatorio_view.montar_view()
        self.page.update()
