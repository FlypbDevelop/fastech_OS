"""
Consulta por Cliente - Busca de clientes e equipamentos vinculados
"""
import flet as ft


class ClienteConsultaView:
    """View de busca de cliente e seus equipamentos"""

    def __init__(self, orc, page, db, config):
        self.orc = orc
        self.page = page
        self.db = db
        self.config = config
        self._init_campos()

    def _init_campos(self):
        """Inicializa campos de busca de cliente"""
        self.cliente_search_field = ft.TextField(
            label="Buscar Cliente",
            hint_text="Digite nome, telefone ou documento...",
            expand=True,
            on_submit=lambda e: self.buscar_cliente_consulta(),
        )
        self.cliente_result_container = ft.Container(
            content=ft.Text(
                "Digite nome, telefone ou documento e clique em Buscar",
                size=14,
                color=ft.Colors.GREY_400,
            ),
            expand=True,
        )

    def montar_view(self):
        """Monta o layout de busca por cliente"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Buscar Cliente e seus Equipamentos", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.cliente_search_field,
                            ft.FilledButton("🔍 Buscar", on_click=lambda e: self.buscar_cliente_consulta(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(),
                    self.cliente_result_container,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
        )

    def buscar_cliente_consulta(self):
        """Busca cliente e seus equipamentos"""
        termo = self.cliente_search_field.value.strip()

        if not termo:
            self.cliente_result_container.content = ft.Text(
                "❌ Digite um termo para buscar",
                size=14,
                color=ft.Colors.RED,
            )
            self.page.update()
            return

        clientes = self.db.buscar_clientes(termo)

        if not clientes:
            self.cliente_result_container.content = ft.Text(
                f"❌ Nenhum cliente encontrado com '{termo}'",
                size=14,
                color=ft.Colors.RED,
            )
            self.page.update()
            return

        if len(clientes) > 1:
            self.mostrar_lista_clientes_consulta(clientes)
        else:
            self.mostrar_detalhes_cliente_consulta(clientes[0])

    def mostrar_lista_clientes_consulta(self, clientes):
        """Mostra lista de clientes encontrados"""
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Telefone", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Setor", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )

        for c in clientes:
            def ver_detalhes(e, cliente=c):
                self.mostrar_detalhes_cliente_consulta(cliente)

            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c['id']))),
                        ft.DataCell(ft.Text(c['nome'])),
                        ft.DataCell(ft.Text(c['telefone'])),
                        ft.DataCell(ft.Text(c['setor'] or '-')),
                        ft.DataCell(
                            ft.TextButton("👁️ Ver Detalhes", on_click=ver_detalhes)
                        ),
                    ],
                )
            )

        self.cliente_result_container.content = ft.Column(
            [
                ft.Text(f"✓ {len(clientes)} clientes encontrados. Selecione um:", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([table], scroll=ft.ScrollMode.AUTO),
                    height=400,
                ),
            ],
            spacing=15,
        )
        self.page.update()

    def mostrar_detalhes_cliente_consulta(self, cliente):
        """Mostra detalhes completos do cliente"""
        info_text = f"""👤 CLIENTE ENCONTRADO

Nome: {cliente['nome']}
Telefone: {cliente['telefone']}
Email: {cliente['email'] or '-'}
Documento: {cliente['documento'] or '-'}
Setor: {cliente['setor'] or '-'}
Endereço: {cliente['endereco'] or '-'}
Data de Cadastro: {cliente['data_cadastro']}"""

        info_card = ft.Container(
            content=ft.Text(info_text, size=14),
            bgcolor=self.orc.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )

        result_content = [info_card]

        equipamentos_ativos = self.db.buscar_equipamentos_cliente_ativo(cliente['id'])

        if equipamentos_ativos:
            ativos_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Série", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Marca", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Modelo", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Desde", weight=ft.FontWeight.BOLD)),
                ],
                rows=[],
            )

            for e in equipamentos_ativos:
                ativos_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(e['numero_serie'])),
                            ft.DataCell(ft.Text(e['tipo'])),
                            ft.DataCell(ft.Text(e['marca'] or '-')),
                            ft.DataCell(ft.Text(e['modelo'] or '-')),
                            ft.DataCell(ft.Text(e['data_inicio'][:16])),
                        ],
                    )
                )

            result_content.extend([
                ft.Text(f"📦 Equipamentos Ativos ({len(equipamentos_ativos)})", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                ft.Container(
                    content=ft.Column([ativos_table], scroll=ft.ScrollMode.AUTO),
                    height=200,
                ),
            ])

        historico = self.db.buscar_historico_cliente(cliente['id'])

        if historico:
            hist_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Equipamento", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Ação", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Data Início", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Data Fim", weight=ft.FontWeight.BOLD)),
                ],
                rows=[],
            )

            for h in historico:
                status = "🟢" if h['data_fim'] is None else "⚪"
                equip_info = f"{h['numero_serie']} ({h['tipo']})"
                hist_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(status)),
                            ft.DataCell(ft.Text(equip_info)),
                            ft.DataCell(ft.Text(h['acao'])),
                            ft.DataCell(ft.Text(h['data_inicio'])),
                            ft.DataCell(ft.Text(h['data_fim'] or '-')),
                        ],
                    )
                )

            result_content.extend([
                ft.Text("📜 Histórico Completo de Equipamentos", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([hist_table], scroll=ft.ScrollMode.AUTO),
                    height=300,
                ),
            ])
        else:
            result_content.append(
                ft.Text("Nenhum histórico de equipamentos", size=14, color=ft.Colors.GREY_400)
            )

        self.cliente_result_container.content = ft.Column(
            result_content,
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        )
        self.page.update()
