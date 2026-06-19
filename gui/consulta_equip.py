"""
Consulta por Equipamento - Busca de equipamentos e histórico
"""
import flet as ft


class EquipamentoConsultaView:
    """View de busca de equipamento por número de série"""

    def __init__(self, orc, page, db, config):
        self.orc = orc
        self.page = page
        self.db = db
        self.config = config
        self._init_campos()

    def _init_campos(self):
        """Inicializa campos de busca de equipamento"""
        self.equip_search_field = ft.TextField(
            label="Número de Série",
            hint_text="Digite o número de série...",
            expand=True,
            on_submit=lambda e: self.buscar_equipamento_consulta(),
        )
        self.equip_result_container = ft.Container(
            content=ft.Text(
                "Digite um número de série e clique em Buscar",
                size=14,
                color=ft.Colors.GREY_400,
            ),
            expand=True,
        )

    def montar_view(self):
        """Monta o layout de busca por equipamento"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Buscar Equipamento por Número de Série", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.equip_search_field,
                            self.orc.botao_primario("🔍 Buscar", on_click=lambda e: self.buscar_equipamento_consulta()),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(),
                    self.equip_result_container,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
        )

    def buscar_equipamento_consulta(self):
        """Busca equipamento por número de série"""
        termo = self.equip_search_field.value.strip()

        if not termo:
            self.equip_result_container.content = ft.Text(
                "❌ Digite um número de série para buscar",
                size=14,
                color=ft.Colors.RED,
            )
            self.page.update()
            return

        equip = self.db.buscar_equipamento_por_serie(termo)

        if not equip:
            self.equip_result_container.content = ft.Text(
                f"❌ Equipamento '{termo}' não encontrado",
                size=14,
                color=ft.Colors.RED,
            )
            self.page.update()
            return

        info_text = f"""📦 EQUIPAMENTO ENCONTRADO

Número de Série: {equip['numero_serie']}
Tipo: {equip['tipo']}
Marca: {equip['marca'] or '-'}
Modelo: {equip['modelo'] or '-'}
Status Atual: {equip['status_atual']}
Data de Registro: {equip['data_registro']}
Valor Estimado: R$ {equip['valor_estimado'] or '0.00'}
Data Garantia: {equip['data_garantia'] or '-'}"""

        info_card = ft.Container(
            content=ft.Text(info_text, size=14),
            bgcolor=self.orc.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )

        hist_ativo = self.db.buscar_historico_ativo_equipamento(equip['id'])
        cliente_card = None
        if hist_ativo and hist_ativo.get('cliente_nome'):
            cliente_card = ft.Container(
                content=ft.Text(
                    f"👤 Cliente Atual: {hist_ativo['cliente_nome']} - {hist_ativo['cliente_telefone']}",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=ft.Colors.BLUE_700,
                padding=15,
                border_radius=10,
            )

        historico = self.db.buscar_historico_equipamento(equip['id'])

        hist_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data Início", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data Fim", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ação", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cliente", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Usuário", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )

        for h in historico:
            status = "🟢" if h['data_fim'] is None else "⚪"
            hist_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(status)),
                        ft.DataCell(ft.Text(h['data_inicio'])),
                        ft.DataCell(ft.Text(h['data_fim'] or '-')),
                        ft.DataCell(ft.Text(h['acao'])),
                        ft.DataCell(ft.Text(h['cliente_nome'] or '-')),
                        ft.DataCell(ft.Text(h['usuario_responsavel'])),
                    ],
                )
            )

        result_content = [info_card]
        if cliente_card:
            result_content.append(cliente_card)
        result_content.extend([
            ft.Text("📜 Histórico Completo", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([hist_table], scroll=ft.ScrollMode.AUTO),
                height=300,
            ),
        ])

        self.equip_result_container.content = ft.Column(
            result_content,
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        )
        self.page.update()
