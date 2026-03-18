"""
Aba Equipamentos - Gestão de equipamentos e serviços
"""
import flet as ft
from gui.base import BaseTab
from datetime import datetime


class EquipamentosTab(BaseTab):
    """Aba de gestão de equipamentos com controle de serviços"""

    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        self.equipamento_selecionado = None
        self.view_atual = "busca"  # busca, cadastro, servicos

        # Campos de busca
        self.serial_busca_field = None
        self.info_equipamento_container = None

        # Container principal
        self.content_container = None

        # Inicializar campos de cadastro e serviço no __init__
        self._init_campos_cadastro()
        self._init_campos_servico()

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
        self.status_dropdown = ft.Dropdown(
            label="Status",
            expand=True,
            value="Em Estoque",
            options=[
                ft.dropdown.Option("Em Estoque"),
                ft.dropdown.Option("Com o Cliente"),
                ft.dropdown.Option("Em Manutenção"),
                ft.dropdown.Option("Descartado"),
            ],
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

    def _init_campos_servico(self):
        """Inicializa todos os campos do formulário de serviço"""
        self.data_servico_field = ft.TextField(
            label="Data do Serviço *",
            hint_text="AAAA-MM-DD ou DD/MM/AAAA",
            value=datetime.now().strftime("%Y-%m-%d"),
            expand=True,
        )
        self.tipo_servico_dropdown = ft.Dropdown(
            label="Tipo de Serviço *",
            expand=True,
            options=[
                ft.dropdown.Option("Manutenção Preventiva"),
                ft.dropdown.Option("Manutenção Corretiva"),
                ft.dropdown.Option("Reparo"),
                ft.dropdown.Option("Instalação"),
                ft.dropdown.Option("Configuração"),
                ft.dropdown.Option("Limpeza"),
                ft.dropdown.Option("Atualização"),
                ft.dropdown.Option("Diagnóstico"),
                ft.dropdown.Option("Outro"),
            ],
        )
        self.cliente_servico_dropdown = ft.Dropdown(
            label="Cliente (opcional)",
            expand=True,
            options=[ft.dropdown.Option("0", "Sem cliente")],
            value="0",
        )
        self.descricao_problema_field = ft.TextField(
            label="Descrição do Problema",
            hint_text="Descreva o problema relatado",
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=3,
        )
        self.servico_realizado_field = ft.TextField(
            label="Serviço Realizado *",
            hint_text="Descreva o que foi feito",
            expand=True,
            multiline=True,
            min_lines=3,
            max_lines=5,
        )
        self.situacao_final_dropdown = ft.Dropdown(
            label="Situação Final *",
            expand=True,
            options=[
                ft.dropdown.Option("Resolvido"),
                ft.dropdown.Option("Parcialmente Resolvido"),
                ft.dropdown.Option("Não Resolvido"),
                ft.dropdown.Option("Aguardando Peças"),
                ft.dropdown.Option("Sem Conserto"),
            ],
        )
        self.tecnico_field = ft.TextField(
            label="Técnico Responsável *",
            value=self.config.get('usuario_padrao', 'Técnico'),
            expand=True,
        )
        self.valor_servico_field = ft.TextField(
            label="Valor do Serviço (R$)",
            hint_text="0.00",
            expand=True,
        )
        self.obs_servico_field = ft.TextField(
            label="Observações",
            hint_text="Informações adicionais",
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=3,
        )
        self.servico_status = ft.Text("", size=14)

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
        """Mostra a view de busca por serial"""
        self.view_atual = "busca"

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
                    self.equipamento_selecionado = eq
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

        self.content_container.content = ft.Container(
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
                self.mostrar_cadastro()
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

        self.equipamento_selecionado = equip
        self.mostrar_detalhes_equipamento(equip)

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
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
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
            self.mostrar_servicos()

        def editar_equipamento(e):
            self.mostrar_cadastro()
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

    def mostrar_cadastro(self):
        """Mostra a view de cadastro de equipamento reutilizando campos existentes"""
        self.view_atual = "cadastro"

        self.content_container.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("📦 Cadastro de Equipamento", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Equipamento pode ser cadastrado sem cliente vinculado", size=12, color=ft.Colors.GREY_400),
                    ft.Divider(),
                    self.numero_serie_field,
                    self.tipo_dropdown,
                    ft.Row([self.marca_field, self.modelo_field], spacing=10),
                    self.status_dropdown,
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
            ),
            padding=20,
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
            if self.equipamento_selecionado:
                self.db.atualizar_equipamento(
                    self.equipamento_selecionado['id'],
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
            self.page.update()
        except Exception as ex:
            self.equipamento_status.value = f"❌ Erro: {str(ex)}"
            self.equipamento_status.color = ft.Colors.RED
            self.page.update()

    def carregar_dados_equipamento(self, equip):
        """Carrega dados do equipamento no formulário"""
        self.equipamento_selecionado = equip
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
        self.equipamento_selecionado = None
        self.equipamento_status.value = ""
        self.page.update()

    def mostrar_servicos(self):
        """Mostra a view de registro de serviços reutilizando campos existentes"""
        self.view_atual = "servicos"

        if not self.equipamento_selecionado:
            self.content_container.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("⚠️ Nenhum equipamento selecionado", size=18, color=ft.Colors.ORANGE),
                        ft.Text("Busque um equipamento primeiro para registrar serviços", size=14),
                        ft.FilledButton(
                            "🔍 Buscar Equipamento",
                            on_click=lambda e: self.mostrar_busca(),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=40,
            )
            self.page.update()
            return

        # Atualizar dropdown de clientes com dados atuais
        clientes = self.db.buscar_clientes()
        self.cliente_servico_dropdown.options = [ft.dropdown.Option("0", "Sem cliente")]
        for c in clientes:
            self.cliente_servico_dropdown.options.append(
                ft.dropdown.Option(str(c['id']), f"{c['nome']} - {c['telefone']}")
            )
        self.cliente_servico_dropdown.value = "0"

        equip = self.equipamento_selecionado
        info_equip = ft.Container(
            content=ft.Text(
                f"📦 {equip['tipo']} - {equip['numero_serie']} ({equip['marca']} {equip['modelo']})",
                size=16,
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=15,
            border_radius=10,
        )

        self.content_container.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("🔧 Registrar Serviço", size=20, weight=ft.FontWeight.BOLD),
                    info_equip,
                    ft.Divider(),
                    self.data_servico_field,
                    self.tipo_servico_dropdown,
                    self.cliente_servico_dropdown,
                    self.descricao_problema_field,
                    self.servico_realizado_field,
                    self.situacao_final_dropdown,
                    ft.Row([self.tecnico_field, self.valor_servico_field], spacing=10),
                    self.obs_servico_field,
                    self.servico_status,
                    ft.Row(
                        [
                            ft.FilledButton(
                                "💾 Salvar Serviço",
                                on_click=self.salvar_servico,
                                expand=True,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                            ft.FilledButton(
                                "🔄 Limpar",
                                on_click=self.limpar_form_servico,
                                expand=True,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
        )
        self.page.update()

    def salvar_servico(self, e):
        """Salva um novo serviço"""
        data_servico = self.data_servico_field.value
        tipo_servico = self.tipo_servico_dropdown.value
        servico_realizado = self.servico_realizado_field.value
        situacao_final = self.situacao_final_dropdown.value
        tecnico = self.tecnico_field.value

        if not all([data_servico, tipo_servico, servico_realizado, situacao_final, tecnico]):
            self.servico_status.value = "❌ Preencha todos os campos obrigatórios"
            self.servico_status.color = ft.Colors.RED
            self.page.update()
            return

        try:
            if '/' in data_servico:
                partes = data_servico.split('/')
                data_servico = f"{partes[2]}-{partes[1]}-{partes[0]}"
            datetime.strptime(data_servico, "%Y-%m-%d")
        except Exception:
            self.servico_status.value = "❌ Data inválida. Use AAAA-MM-DD ou DD/MM/AAAA"
            self.servico_status.color = ft.Colors.RED
            self.page.update()
            return

        cliente_id = None
        if self.cliente_servico_dropdown.value != "0":
            cliente_id = int(self.cliente_servico_dropdown.value)

        valor_servico = None
        if self.valor_servico_field.value:
            try:
                valor_servico = float(self.valor_servico_field.value.replace(',', '.'))
            except Exception:
                pass

        try:
            self.db.inserir_servico(
                self.equipamento_selecionado['id'],
                data_servico,
                tipo_servico,
                servico_realizado,
                situacao_final,
                tecnico,
                cliente_id,
                self.descricao_problema_field.value or None,
                valor_servico,
                self.obs_servico_field.value or None,
            )
            self.servico_status.value = "✅ Serviço registrado com sucesso!"
            self.servico_status.color = ft.Colors.GREEN
            self.limpar_form_servico()
            self.page.update()
        except Exception as ex:
            self.servico_status.value = f"❌ Erro: {str(ex)}"
            self.servico_status.color = ft.Colors.RED
            self.page.update()

    def limpar_form_servico(self, e=None):
        """Limpa o formulário de serviço"""
        self.data_servico_field.value = datetime.now().strftime("%Y-%m-%d")
        self.tipo_servico_dropdown.value = None
        self.cliente_servico_dropdown.value = "0"
        self.descricao_problema_field.value = ""
        self.servico_realizado_field.value = ""
        self.situacao_final_dropdown.value = None
        self.tecnico_field.value = self.config.get('usuario_padrao', 'Técnico')
        self.valor_servico_field.value = ""
        self.obs_servico_field.value = ""
        self.servico_status.value = ""
        self.page.update()
