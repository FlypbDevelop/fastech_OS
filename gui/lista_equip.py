"""
Busca, Cadastro e Listagem de Equipamentos
"""
import flet as ft


class EquipamentoView:
    """View de busca, cadastro e listagem de equipamentos"""

    def __init__(self, orc, page, db, config):
        self.orc = orc
        self.page = page
        self.db = db
        self.config = config
        self._init_campos_cadastro()

    # ── Status customizados ──────────────────────────────────────────

    def _get_status_equipamento(self):
        """Retorna lista de status (padrão + customizados)"""
        status_padrao = ["Em Estoque", "Com o Cliente", "Em Manutenção", "Descartado"]
        status_custom = self.config.get('status_equipamento_custom', [])
        return status_padrao + [s for s in status_custom if s not in status_padrao]

    def _salvar_status_custom(self, novo_status: str) -> bool:
        """Persiste um novo status no config.json"""
        lista = self.config.get('status_equipamento_custom', [])
        if novo_status in lista:
            return False
        lista.append(novo_status)
        self.config['status_equipamento_custom'] = lista
        return self.orc.salvar_config()

    def _rebuild_status_dropdown(self):
        """Reconstrói as opções do dropdown de status"""
        status = self._get_status_equipamento()
        self.status_dropdown.options = (
            [ft.dropdown.Option(s) for s in status]
            + [ft.dropdown.Option("__novo_status__", "➕ Novo status...")]
        )

    def _on_status_change(self, e):
        """Mostra/oculta campo de novo status"""
        if self.status_dropdown.value == "__novo_status__":
            self.novo_status_row.visible = True
            self.status_dropdown.value = None
        else:
            self.novo_status_row.visible = False
        self.page.update()

    def _salvar_novo_status(self, e):
        """Salva o novo status e atualiza o dropdown"""
        novo = self.novo_status_field.value.strip()
        if not novo:
            return
        existentes = self._get_status_equipamento()
        if novo not in existentes:
            self._salvar_status_custom(novo)
        self._rebuild_status_dropdown()
        self.status_dropdown.value = novo
        self.novo_status_row.visible = False
        self.novo_status_field.value = ""
        self.page.update()

    # ── Campos de cadastro ──────────────────────────────────────────

    def _init_campos_cadastro(self):
        """Inicializa todos os campos do formulário de cadastro de equipamento"""
        self.numero_serie_field = ft.TextField(
            label="Número de Série *",
            hint_text="Ex: NB-2024-001",
            expand=True,
        )
        self.tipo_dropdown = ft.Dropdown(
            label="Tipo de Equipamento *",
            hint_text="Selecione o tipo",
            expand=True,
            options=[
                ft.dropdown.Option("Notebook"),
                ft.dropdown.Option("Desktop"),
                ft.dropdown.Option("Monitor"),
                ft.dropdown.Option("Impressora"),
                ft.dropdown.Option("Roteador"),
                ft.dropdown.Option("Switch"),
                ft.dropdown.Option("Servidor"),
                ft.dropdown.Option("Outro"),
            ],
        )
        self.marca_field = ft.TextField(label="Marca", hint_text="Ex: Dell, HP, Epson", expand=True)
        self.modelo_field = ft.TextField(label="Modelo", hint_text="Ex: L355, Latitude 5420", expand=True)
        status_iniciais = self._get_status_equipamento()
        self.status_dropdown = ft.Dropdown(
            label="Status",
            expand=True,
            value="Em Estoque",
            options=(
                [ft.dropdown.Option(s) for s in status_iniciais]
                + [ft.dropdown.Option("__novo_status__", "➕ Novo status...")]
            ),
            on_select=self._on_status_change,
        )
        self.novo_status_field = ft.TextField(
            label="Nome do novo status *",
            hint_text="Ex: Em Garantia",
            expand=True,
        )
        self.novo_status_row = ft.Row(
            [
                self.novo_status_field,
                ft.FilledButton(
                    "💾 Salvar status",
                    on_click=self._salvar_novo_status,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                ),
            ],
            spacing=8,
            visible=False,
        )
        self.valor_field = ft.TextField(label="Valor Estimado (R$)", hint_text="0.00", expand=True)
        self.garantia_field = ft.TextField(label="Data Garantia", hint_text="AAAA-MM-DD", expand=True)
        self.obs_field = ft.TextField(
            label="Observações",
            hint_text="Informações adicionais",
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=4,
        )
        self.equipamento_status = ft.Text("", size=14)

    # ── Busca por serial ────────────────────────────────────────────

    def mostrar_busca(self):
        """Mostra a view de busca por serial"""
        self.serial_busca_field = ft.TextField(
            label="Número de Série",
            hint_text="Digite o número de série do equipamento",
            expand=True,
            on_submit=lambda e: self.buscar_por_serial(),
            autofocus=True,
        )

        self.info_equipamento_container = ft.Container(
            content=ft.Text(
                "Digite um número de série e pressione Enter ou clique em Buscar",
                size=14,
                color=ft.Colors.GREY_400,
            ),
            padding=20,
        )

        equipamentos_recentes = self.db.buscar_equipamentos()[:10]

        if equipamentos_recentes:
            tabela_recentes = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Serial", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Marca", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Modelo", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Serviços", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
                ],
                rows=[],
            )

            for equip in equipamentos_recentes:
                total_servicos = self.db.contar_servicos_equipamento(equip['id'])

                def ver_detalhes(e, eq=equip):
                    self.orc.equipamento_selecionado = eq
                    self.mostrar_detalhes_equipamento(eq)

                tabela_recentes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(equip['numero_serie'], size=12)),
                            ft.DataCell(ft.Text(equip['tipo'], size=12)),
                            ft.DataCell(ft.Text(equip['marca'] or '-', size=12)),
                            ft.DataCell(ft.Text(equip['modelo'] or '-', size=12)),
                            ft.DataCell(ft.Text(str(total_servicos), size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)),
                            ft.DataCell(
                                ft.TextButton(
                                    "👁️ Ver",
                                    on_click=ver_detalhes,
                                    tooltip="Ver detalhes",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                )
                            ),
                        ],
                    )
                )

            lista_recentes = ft.Column(
                [
                    ft.Text("📋 Últimos Equipamentos Cadastrados", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column([tabela_recentes], scroll=ft.ScrollMode.AUTO),
                        height=400,
                    ),
                ],
                spacing=10,
            )
        else:
            lista_recentes = ft.Text("Nenhum equipamento cadastrado ainda", size=14, color=ft.Colors.GREY_400)

        self.orc.content_container.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("🔍 Buscar Equipamento por Serial", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.serial_busca_field,
                            ft.FilledButton(
                                "🔍 Buscar",
                                on_click=lambda e: self.buscar_por_serial(),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(),
                    self.info_equipamento_container,
                    ft.Divider(),
                    lista_recentes,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
        )
        self.page.update()

    def buscar_por_serial(self):
        """Busca equipamento por número de série"""
        serial = self.serial_busca_field.value.strip()

        if not serial:
            self.info_equipamento_container.content = ft.Text(
                "❌ Digite um número de série",
                size=14,
                color=ft.Colors.RED,
            )
            self.page.update()
            return

        equip = self.db.buscar_equipamento_por_serie(serial)

        if not equip:
            def cadastrar_novo(e):
                self.orc.mostrar_cadastro()
                self.numero_serie_field.value = serial
                self.page.update()

            self.info_equipamento_container.content = ft.Column(
                [
                    ft.Text(f"❌ Equipamento '{serial}' não encontrado", size=16, color=ft.Colors.RED),
                    ft.Container(height=10),
                    ft.FilledButton(
                        "➕ Cadastrar este equipamento",
                        on_click=cadastrar_novo,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN,
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            self.page.update()
            return

        self.orc.equipamento_selecionado = equip
        self.mostrar_detalhes_equipamento(equip)

    # ── Detalhes do equipamento ─────────────────────────────────────

    def mostrar_detalhes_equipamento(self, equip):
        """Mostra detalhes completos do equipamento"""
        servicos = self.db.buscar_servicos_equipamento(equip['id'])
        total_servicos = len(servicos)
        ultimo_servico = self.db.buscar_ultimo_servico_equipamento(equip['id'])

        info_card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"📦 {equip['tipo']} - {equip['numero_serie']}", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Marca: {equip['marca'] or '-'} | Modelo: {equip['modelo'] or '-'}", size=14),
                    ft.Text(f"Status: {equip['status_atual']}", size=14),
                    ft.Text(f"Total de Serviços: {total_servicos}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                ],
                spacing=5,
            ),
            bgcolor=self.orc.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )

        ultimo_servico_card = None
        if ultimo_servico:
            ultimo_servico_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("🔧 Último Serviço", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Data: {ultimo_servico['data_servico']}", size=12),
                        ft.Text(f"Tipo: {ultimo_servico['tipo_servico']}", size=12),
                        ft.Text(f"Situação: {ultimo_servico['situacao_final']}", size=12),
                        ft.Text(f"Técnico: {ultimo_servico['tecnico_responsavel']}", size=12),
                    ],
                    spacing=3,
                ),
                bgcolor=ft.Colors.GREEN_900 if ultimo_servico['situacao_final'] == 'Resolvido' else ft.Colors.ORANGE_900,
                padding=15,
                border_radius=10,
            )

        servicos_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Problema", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Situação", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Técnico", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )

        for s in servicos:
            servicos_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(s['data_servico'][:10], size=12)),
                        ft.DataCell(ft.Text(s['tipo_servico'], size=12)),
                        ft.DataCell(ft.Text((s['descricao_problema'] or '-')[:30], size=12)),
                        ft.DataCell(ft.Text(s['situacao_final'], size=12)),
                        ft.DataCell(ft.Text(s['tecnico_responsavel'], size=12)),
                    ],
                )
            )

        def registrar_servico_equipamento(e):
            self.orc.mostrar_servicos()

        def editar_equipamento(e):
            self.orc.mostrar_cadastro()
            self.carregar_dados_equipamento(equip)

        acoes = ft.Row(
            [
                ft.FilledButton(
                    "🔧 Registrar Novo Serviço",
                    on_click=registrar_servico_equipamento,
                    expand=True,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                ),
                ft.FilledButton(
                    "✏️ Editar Equipamento",
                    on_click=editar_equipamento,
                    expand=True,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                ),
            ],
            spacing=10,
        )

        content_items = [info_card]
        if ultimo_servico_card:
            content_items.append(ultimo_servico_card)

        content_items.extend([
            ft.Text(f"📋 Histórico de Serviços ({total_servicos})", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([servicos_table], scroll=ft.ScrollMode.AUTO),
                height=300,
            ) if servicos else ft.Text("Nenhum serviço registrado", size=14, color=ft.Colors.GREY_400),
            acoes,
        ])

        self.info_equipamento_container.content = ft.Column(content_items, spacing=15)
        self.page.update()

    # ── Exclusão ─────────────────────────────────────────────────────

    def _confirmar_exclusao(self, eq):
        """Exibe diálogo de confirmação antes de excluir equipamento"""
        def fechar(e):
            dlg.open = False
            self.page.update()

        def confirmar(e):
            dlg.open = False
            self.page.update()
            ok = self.db.deletar_equipamento(eq['id'])
            if ok:
                if self.orc.equipamento_selecionado and self.orc.equipamento_selecionado.get('id') == eq['id']:
                    self.orc.equipamento_selecionado = None
                    self.limpar_form_equipamento()
                self.lista_panel.content = self._build_lista_equipamentos().content
                self.page.update()
            else:
                self.equipamento_status.value = "❌ Erro ao excluir equipamento"
                self.equipamento_status.color = ft.Colors.RED
                self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Deseja excluir o equipamento '{eq['numero_serie']}'?\nTodos os serviços e histórico serão removidos."),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar),
                ft.FilledButton(
                    "Excluir",
                    on_click=confirmar,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    # ── Lista de equipamentos ───────────────────────────────────────

    def _build_lista_equipamentos(self):
        """Constrói o painel de lista de equipamentos cadastrados (mais recente primeiro)"""
        equipamentos = self.db.buscar_equipamentos()
        equipamentos_ordenados = list(reversed(equipamentos))

        STATUS_CORES = {
            "Em Estoque": ft.Colors.GREEN_400,
            "Com o Cliente": ft.Colors.BLUE_400,
            "Em Manutenção": ft.Colors.ORANGE_400,
            "Descartado": ft.Colors.RED_400,
        }

        if not equipamentos_ordenados:
            itens = [ft.Text("Nenhum equipamento cadastrado.", size=12, color=ft.Colors.GREY_400)]
        else:
            itens = [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("Serial", size=11, weight=ft.FontWeight.BOLD, width=110),
                            ft.Text("Tipo", size=11, weight=ft.FontWeight.BOLD, width=90),
                            ft.Text("Marca / Modelo", size=11, weight=ft.FontWeight.BOLD, expand=True),
                            ft.Text("Status", size=11, weight=ft.FontWeight.BOLD, width=100),
                            ft.Text("Ações", size=11, weight=ft.FontWeight.BOLD, width=70),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(horizontal=10, vertical=6),
                    bgcolor=self.orc.get_adaptive_color(ft.Colors.BLUE_GREY_900, ft.Colors.GREY_300),
                    border_radius=6,
                ),
            ]
            for eq in equipamentos_ordenados:
                cor_status = STATUS_CORES.get(eq['status_atual'], ft.Colors.GREY_400)
                marca_modelo = f"{eq.get('marca') or '—'} {eq.get('modelo') or ''}".strip()

                def on_editar(e, equip=eq):
                    self.carregar_dados_equipamento(equip)

                def on_excluir(e, equip=eq):
                    self._confirmar_exclusao(equip)

                itens.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(eq['numero_serie'], size=12, weight=ft.FontWeight.BOLD, width=110, no_wrap=True),
                                ft.Text(eq['tipo'], size=12, width=90, no_wrap=True, color=ft.Colors.GREY_400),
                                ft.Text(marca_modelo, size=12, expand=True, no_wrap=True, color=ft.Colors.GREY_400),
                                ft.Text(eq['status_atual'], size=11, width=100, color=cor_status, no_wrap=True),
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_size=16,
                                            tooltip="Editar",
                                            on_click=on_editar,
                                            icon_color=ft.Colors.BLUE_400,
                                            padding=ft.padding.all(2),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_size=16,
                                            tooltip="Excluir",
                                            on_click=on_excluir,
                                            icon_color=ft.Colors.RED_400,
                                            padding=ft.padding.all(2),
                                        ),
                                    ],
                                    spacing=0,
                                    width=70,
                                ),
                            ],
                            spacing=8,
                        ),
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_800)),
                    )
                )

        self.lista_equipamentos_column = ft.Column(
            itens,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"📋 Equipamentos Cadastrados ({len(equipamentos_ordenados)})",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(),
                    self.lista_equipamentos_column,
                ],
                spacing=8,
                expand=True,
            ),
            padding=20,
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_800),
            border_radius=10,
        )

    # ── Cadastro ────────────────────────────────────────────────────

    def mostrar_cadastro(self):
        """Mostra a view de cadastro de equipamento"""
        self._rebuild_status_dropdown()
        self.novo_status_row.visible = False

        formulario = ft.Container(
            content=ft.Column(
                [
                    ft.Text("📦 Cadastro de Equipamento", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Equipamento pode ser cadastrado sem cliente vinculado", size=12, color=ft.Colors.GREY_400),
                    ft.Divider(),
                    self.numero_serie_field,
                    self.tipo_dropdown,
                    ft.Row([self.marca_field, self.modelo_field], spacing=10),
                    self.status_dropdown,
                    self.novo_status_row,
                    ft.Row([self.valor_field, self.garantia_field], spacing=10),
                    self.obs_field,
                    self.equipamento_status,
                    ft.Row(
                        [
                            ft.FilledButton(
                                "💾 Salvar",
                                on_click=self.salvar_equipamento,
                                expand=True,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                            ft.FilledButton(
                                "🔄 Limpar",
                                on_click=self.limpar_form_equipamento,
                                expand=True,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
            expand=True,
        )

        self.lista_panel = self._build_lista_equipamentos()

        self.orc.content_container.content = ft.Container(
            content=ft.Row(
                [formulario, self.lista_panel],
                spacing=10,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.only(left=0, top=0, right=15, bottom=15),
            expand=True,
        )
        self.page.update()

    def salvar_equipamento(self, e):
        """Salva ou atualiza um equipamento"""
        numero_serie = self.numero_serie_field.value
        tipo = self.tipo_dropdown.value

        if not numero_serie or not tipo:
            self.equipamento_status.value = "❌ Número de série e tipo são obrigatórios"
            self.equipamento_status.color = ft.Colors.RED
            self.page.update()
            return

        try:
            if self.orc.equipamento_selecionado:
                self.db.atualizar_equipamento(
                    self.orc.equipamento_selecionado['id'],
                    numero_serie=numero_serie,
                    tipo=tipo,
                    marca=self.marca_field.value or None,
                    modelo=self.modelo_field.value or None,
                    status_atual=self.status_dropdown.value,
                    data_garantia=self.garantia_field.value or None,
                    valor_estimado=float(self.valor_field.value) if self.valor_field.value else None,
                    observacoes=self.obs_field.value or None,
                )
                self.equipamento_status.value = f"✅ Equipamento '{numero_serie}' atualizado!"
            else:
                equip_id = self.db.inserir_equipamento(
                    numero_serie,
                    tipo,
                    self.marca_field.value or None,
                    self.modelo_field.value or None,
                    self.status_dropdown.value,
                    self.garantia_field.value or None,
                    float(self.valor_field.value) if self.valor_field.value else None,
                    self.obs_field.value or None,
                )
                self.db.inserir_historico(
                    equip_id,
                    "Cadastro",
                    self.config.get('usuario_padrao', 'Sistema'),
                    None,
                    observacoes="Cadastro inicial"
                )
                self.equipamento_status.value = f"✅ Equipamento '{numero_serie}' cadastrado!"

            self.equipamento_status.color = ft.Colors.GREEN
            if self.orc.view_atual == "cadastro" and hasattr(self, 'lista_panel'):
                self.lista_panel.content = self._build_lista_equipamentos().content
            self.page.update()
        except Exception as ex:
            self.equipamento_status.value = f"❌ Erro: {str(ex)}"
            self.equipamento_status.color = ft.Colors.RED
            self.page.update()

    def carregar_dados_equipamento(self, equip):
        """Carrega dados do equipamento no formulário"""
        self.orc.equipamento_selecionado = equip
        self.numero_serie_field.value = equip['numero_serie']
        self.tipo_dropdown.value = equip['tipo']
        self.marca_field.value = equip['marca'] or ""
        self.modelo_field.value = equip['modelo'] or ""
        self.status_dropdown.value = equip['status_atual']
        self.valor_field.value = str(equip['valor_estimado']) if equip['valor_estimado'] else ""
        self.garantia_field.value = equip['data_garantia'] or ""
        self.obs_field.value = equip['observacoes'] or ""
        self.equipamento_status.value = f"✏️ Editando: {equip['numero_serie']}"
        self.equipamento_status.color = ft.Colors.BLUE
        self.page.update()

    def limpar_form_equipamento(self, e=None):
        """Limpa o formulário de equipamento"""
        self.numero_serie_field.value = ""
        self.tipo_dropdown.value = None
        self.marca_field.value = ""
        self.modelo_field.value = ""
        self.status_dropdown.value = "Em Estoque"
        self.valor_field.value = ""
        self.garantia_field.value = ""
        self.obs_field.value = ""
        self.orc.equipamento_selecionado = None
        self.equipamento_status.value = ""
        self.page.update()
