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
from gui.dashboard_tab import DashboardTab
from gui.clientes_tab import ClientesTab
from gui.equipamentos_tab import EquipamentosTab
from gui.movimentacoes_tab import MovimentacoesTab
from gui.consultas_tab import ConsultasTab
from gui.configuracoes_tab import ConfiguracoesTab

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
        # Estado
        self.equipamento_selecionado = None
        
        # Campos do formulário
        self.numero_serie_field = ft.TextField(
            label="Número de Série *",
            hint_text="Ex: NB-2024-001",
            width=400,
        )
        
        self.tipo_dropdown = ft.Dropdown(
            label="Tipo de Equipamento *",
            hint_text="Selecione o tipo",
            width=400,
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
        
        self.marca_field = ft.TextField(
            label="Marca",
            hint_text="Ex: Dell, HP, Samsung",
            width=190,
        )
        
        self.modelo_field = ft.TextField(
            label="Modelo",
            hint_text="Ex: Latitude 5420",
            width=190,
        )
        
        self.status_dropdown = ft.Dropdown(
            label="Status",
            width=400,
            value="Em Estoque",
            options=[
                ft.dropdown.Option("Em Estoque"),
                ft.dropdown.Option("Com o Cliente"),
                ft.dropdown.Option("Em Manutenção"),
                ft.dropdown.Option("Descartado"),
            ],
        )
        
        self.valor_field = ft.TextField(
            label="Valor Estimado (R$)",
            hint_text="0.00",
            width=190,
        )
        
        self.garantia_field = ft.TextField(
            label="Data Garantia",
            hint_text="AAAA-MM-DD",
            width=190,
        )
        
        self.obs_field = ft.TextField(
            label="Observações",
            hint_text="Informações adicionais",
            width=400,
            multiline=True,
            min_lines=3,
            max_lines=5,
        )
        
        # Status message
        self.equipamento_status = ft.Text("", size=14)
        
        # Tabela de equipamentos
        self.equipamentos_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Série", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Marca", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )
        
        # Busca e filtro
        self.equipamento_search = ft.TextField(
            label="Buscar equipamento",
            hint_text="Número de série, tipo ou marca...",
            width=300,
            on_submit=lambda e: self.buscar_equipamentos(),
        )
        
        self.status_filter = ft.Dropdown(
            label="Filtrar por status",
            width=200,
            value="Todos",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Em Estoque"),
                ft.dropdown.Option("Com o Cliente"),
                ft.dropdown.Option("Em Manutenção"),
                ft.dropdown.Option("Descartado"),
            ],
        )
        self.status_filter.on_change = lambda e: self.carregar_equipamentos()
        
        # Botões
        def salvar_equipamento(e):
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
                    
                    # Registrar no histórico
                    self.db.inserir_historico(
                        equip_id,
                        "Cadastro",
                        "Sistema",
                        None,
                        observacoes="Cadastro inicial"
                    )
                    
                    self.equipamento_status.value = f"✅ Equipamento '{numero_serie}' cadastrado!"
                
                self.equipamento_status.color = ft.Colors.GREEN
                self.limpar_form_equipamento()
                self.carregar_equipamentos()
                self.page.update()
            except Exception as ex:
                self.equipamento_status.value = f"❌ Erro: {str(ex)}"
                self.equipamento_status.color = ft.Colors.RED
                self.page.update()
        
        def limpar_form(e):
            self.limpar_form_equipamento()
            self.page.update()
        
        # Layout
        formulario = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Cadastro de Equipamento", size=18, weight=ft.FontWeight.BOLD),
                    self.numero_serie_field,
                    self.tipo_dropdown,
                    ft.Row([self.marca_field, self.modelo_field], spacing=20),
                    self.status_dropdown,
                    ft.Row([self.valor_field, self.garantia_field], spacing=20),
                    self.obs_field,
                    self.equipamento_status,
                    ft.Row(
                        [
                            ft.FilledButton("💾 Salvar", on_click=salvar_equipamento),
                            ft.FilledButton("🔄 Limpar", on_click=limpar_form),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=450,
            padding=20,
            bgcolor=self.get_bg_color(),
            border_radius=10,
        )
        
        lista = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Equipamentos Cadastrados", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.equipamento_search,
                            self.status_filter,
                            ft.FilledButton("🔍 Buscar", on_click=lambda e: self.buscar_equipamentos()),
                            ft.FilledButton("🔄 Todos", on_click=lambda e: self.carregar_equipamentos()),
                        ],
                        spacing=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [self.equipamentos_table],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        height=500,
                    ),
                ],
                spacing=10,
            ),
            expand=True,
            padding=20,
            bgcolor=self.get_bg_color(),
            border_radius=10,
        )
        
        # Carregar equipamentos inicialmente
        self.carregar_equipamentos()
        
        return ft.Container(
            content=ft.Row(
                [
                    formulario,
                    ft.Container(width=20),
                    lista,
                ],
            ),
            padding=20,
            expand=True,
        )
    
    def limpar_form_equipamento(self):
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
    
    def carregar_equipamentos(self):
        """Carrega todos os equipamentos na tabela"""
        status_filtro = self.status_filter.value
        status = None if status_filtro == "Todos" else status_filtro
        
        equipamentos = self.db.buscar_equipamentos(status=status)
        self.equipamentos_table.rows.clear()
        
        for e in equipamentos:
            def editar_equipamento(ev, equip=e):
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
            
            def ver_historico(ev, equip=e):
                self.mostrar_historico_equipamento(equip)
            
            self.equipamentos_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(e['id']))),
                        ft.DataCell(ft.Text(e['numero_serie'])),
                        ft.DataCell(ft.Text(e['tipo'])),
                        ft.DataCell(ft.Text(e['marca'] or '-')),
                        ft.DataCell(ft.Text(e['status_atual'])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton("✏️", on_click=editar_equipamento, tooltip="Editar"),
                                    ft.TextButton("👁️", on_click=ver_historico, tooltip="Ver Histórico"),
                                ],
                                spacing=5,
                            )
                        ),
                    ],
                )
            )
        
        if hasattr(self, 'page'):
            self.page.update()
    
    def buscar_equipamentos(self):
        """Busca equipamentos pelo termo"""
        termo = self.equipamento_search.value or ""
        status_filtro = self.status_filter.value
        status = None if status_filtro == "Todos" else status_filtro
        
        equipamentos = self.db.buscar_equipamentos(termo, status)
        self.equipamentos_table.rows.clear()
        
        for e in equipamentos:
            def editar_equipamento(ev, equip=e):
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
            
            def ver_historico(ev, equip=e):
                self.mostrar_historico_equipamento(equip)
            
            self.equipamentos_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(e['id']))),
                        ft.DataCell(ft.Text(e['numero_serie'])),
                        ft.DataCell(ft.Text(e['tipo'])),
                        ft.DataCell(ft.Text(e['marca'] or '-')),
                        ft.DataCell(ft.Text(e['status_atual'])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton("✏️", on_click=editar_equipamento, tooltip="Editar"),
                                    ft.TextButton("👁️", on_click=ver_historico, tooltip="Ver Histórico"),
                                ],
                                spacing=5,
                            )
                        ),
                    ],
                )
            )
        
        self.page.update()
    
    def mostrar_historico_equipamento(self, equip):
        """Mostra o histórico do equipamento em um diálogo"""
        historico = self.db.buscar_historico_equipamento(equip['id'])
        
        # Criar tabela de histórico
        hist_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ação", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cliente", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Usuário", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )
        
        for h in historico:
            status_icon = "🟢" if h['data_fim'] is None else "⚪"
            hist_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{status_icon} {h['data_inicio']}")),
                        ft.DataCell(ft.Text(h['acao'])),
                        ft.DataCell(ft.Text(h['cliente_nome'] or '-')),
                        ft.DataCell(ft.Text(h['usuario_responsavel'])),
                    ],
                )
            )
        
        def fechar_dialogo(e):
            dialogo.open = False
            self.page.update()
        
        dialogo = ft.AlertDialog(
            title=ft.Text(f"📜 Histórico - {equip['numero_serie']}"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"{equip['tipo']} {equip['marca']} {equip['modelo']}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Status: {equip['status_atual']}", size=14),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column([hist_table], scroll=ft.ScrollMode.AUTO),
                            height=300,
                        ),
                    ],
                ),
                width=700,
            ),
            actions=[
                ft.TextButton("Fechar", on_click=fechar_dialogo),
            ],
        )
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def criar_movimentacoes(self):
        """Cria a aba de movimentações"""
        # Estado
        self.equipamento_mov_selecionado = None
        
        # Campos do formulário
        self.acao_dropdown = ft.Dropdown(
            label="Tipo de Movimentação *",
            hint_text="Selecione o tipo",
            width=400,
            options=[
                ft.dropdown.Option("Cadastro"),
                ft.dropdown.Option("Entrega"),
                ft.dropdown.Option("Devolução"),
                ft.dropdown.Option("Manutenção"),
                ft.dropdown.Option("Reparo"),
                ft.dropdown.Option("Transferência"),
                ft.dropdown.Option("Baixa"),
            ],
        )
        self.acao_dropdown.on_change = lambda e: self.on_acao_change()
        
        self.equipamento_mov_dropdown = ft.Dropdown(
            label="Equipamento *",
            hint_text="Selecione o equipamento",
            width=400,
            options=[],
        )
        self.equipamento_mov_dropdown.on_change = lambda e: self.on_equipamento_mov_change()
        
        self.info_equipamento_mov = ft.Text("", size=12, color=ft.Colors.GREY_400)
        
        self.cliente_mov_dropdown = ft.Dropdown(
            label="Cliente *",
            hint_text="Selecione o cliente",
            width=400,
            options=[],
            visible=False,
        )
        
        self.usuario_field = ft.TextField(
            label="Seu Nome (Responsável) *",
            value="Técnico",
            width=400,
        )
        
        self.obs_mov_field = ft.TextField(
            label="Observações",
            hint_text="Informações adicionais",
            width=400,
            multiline=True,
            min_lines=3,
            max_lines=5,
        )
        
        # Status message
        self.movimentacao_status = ft.Text("", size=14)
        
        # Tabela de movimentações
        self.movimentacoes_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ação", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Equipamento", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cliente", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Usuário", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )
        
        # Filtros
        self.acao_filter_mov = ft.Dropdown(
            label="Filtrar por ação",
            width=150,
            value="Todas",
            options=[
                ft.dropdown.Option("Todas"),
                ft.dropdown.Option("Cadastro"),
                ft.dropdown.Option("Entrega"),
                ft.dropdown.Option("Devolução"),
                ft.dropdown.Option("Manutenção"),
                ft.dropdown.Option("Reparo"),
                ft.dropdown.Option("Transferência"),
                ft.dropdown.Option("Baixa"),
            ],
        )
        self.acao_filter_mov.on_change = lambda e: self.carregar_movimentacoes()
        
        self.limite_dropdown = ft.Dropdown(
            label="Mostrar",
            width=100,
            value="25",
            options=[
                ft.dropdown.Option("10"),
                ft.dropdown.Option("25"),
                ft.dropdown.Option("50"),
                ft.dropdown.Option("100"),
            ],
        )
        self.limite_dropdown.on_change = lambda e: self.carregar_movimentacoes()
        
        # Botões
        def registrar_movimentacao(e):
            acao = self.acao_dropdown.value
            equip_key = self.equipamento_mov_dropdown.value
            usuario = self.usuario_field.value
            
            if not acao or not equip_key or not usuario:
                self.movimentacao_status.value = "❌ Preencha todos os campos obrigatórios"
                self.movimentacao_status.color = ft.Colors.RED
                self.page.update()
                return
            
            # Verifica se precisa de cliente
            if acao in ["Entrega", "Transferência"]:
                cliente_key = self.cliente_mov_dropdown.value
                if not cliente_key:
                    self.movimentacao_status.value = "❌ Selecione o cliente de destino"
                    self.movimentacao_status.color = ft.Colors.RED
                    self.page.update()
                    return
            
            try:
                equip = self.equipamento_mov_selecionado
                
                # Finaliza histórico anterior
                hist_ativo = self.db.buscar_historico_ativo_equipamento(equip['id'])
                if hist_ativo:
                    self.db.finalizar_historico(hist_ativo['id'])
                
                # Cliente ID
                cliente_id = None
                if self.cliente_mov_dropdown.visible and self.cliente_mov_dropdown.value:
                    cliente_id = int(self.cliente_mov_dropdown.value.split(" - ")[0])
                
                # Determina novo status
                novo_status = self.determinar_status(acao, cliente_id)
                
                # Registra movimentação
                self.db.inserir_historico(
                    equip['id'],
                    acao,
                    usuario,
                    cliente_id,
                    observacoes=self.obs_mov_field.value or None
                )
                
                # Atualiza status
                self.db.atualizar_status_equipamento(equip['id'], novo_status)
                
                self.movimentacao_status.value = f"✅ Movimentação registrada! {equip['numero_serie']} → {novo_status}"
                self.movimentacao_status.color = ft.Colors.GREEN
                self.limpar_form_movimentacao()
                self.carregar_movimentacoes()
                self.carregar_equipamentos_mov()
                self.page.update()
            except Exception as ex:
                self.movimentacao_status.value = f"❌ Erro: {str(ex)}"
                self.movimentacao_status.color = ft.Colors.RED
                self.page.update()
        
        def limpar_form(e):
            self.limpar_form_movimentacao()
            self.page.update()
        
        # Layout
        formulario = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Nova Movimentação", size=18, weight=ft.FontWeight.BOLD),
                    self.acao_dropdown,
                    self.equipamento_mov_dropdown,
                    self.info_equipamento_mov,
                    self.cliente_mov_dropdown,
                    self.usuario_field,
                    self.obs_mov_field,
                    self.movimentacao_status,
                    ft.Row(
                        [
                            ft.FilledButton("✅ Registrar", on_click=registrar_movimentacao),
                            ft.FilledButton("🔄 Limpar", on_click=limpar_form),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=450,
            padding=20,
            bgcolor=self.get_bg_color(),
            border_radius=10,
        )
        
        lista = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Movimentações Recentes", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.acao_filter_mov,
                            self.limite_dropdown,
                            ft.FilledButton("🔄 Atualizar", on_click=lambda e: self.carregar_movimentacoes()),
                        ],
                        spacing=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [self.movimentacoes_table],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        height=500,
                    ),
                ],
                spacing=10,
            ),
            expand=True,
            padding=20,
            bgcolor=self.get_bg_color(),
            border_radius=10,
        )
        
        # Carregar dados inicialmente
        self.carregar_equipamentos_mov()
        self.carregar_clientes_mov()
        self.carregar_movimentacoes()
        
        return ft.Container(
            content=ft.Row(
                [
                    formulario,
                    ft.Container(width=20),
                    lista,
                ],
            ),
            padding=20,
            expand=True,
        )
    
    def carregar_equipamentos_mov(self):
        """Carrega equipamentos no dropdown"""
        equipamentos = self.db.buscar_equipamentos()
        self.equipamentos_mov_dict = {}
        options = []
        
        for e in equipamentos:
            key = f"{e['numero_serie']} - {e['tipo']} - {e['status_atual']}"
            self.equipamentos_mov_dict[key] = e
            options.append(ft.dropdown.Option(key))
        
        self.equipamento_mov_dropdown.options = options
        if options:
            self.equipamento_mov_dropdown.value = options[0].key
            self.on_equipamento_mov_change()
    
    def carregar_clientes_mov(self):
        """Carrega clientes no dropdown"""
        clientes = self.db.buscar_clientes()
        options = []
        
        for c in clientes:
            key = f"{c['id']} - {c['nome']} - {c['telefone']}"
            options.append(ft.dropdown.Option(key))
        
        self.cliente_mov_dropdown.options = options
    
    def on_acao_change(self):
        """Chamado quando a ação muda"""
        acao = self.acao_dropdown.value
        
        if acao in ["Entrega", "Transferência"]:
            self.cliente_mov_dropdown.visible = True
            self.cliente_mov_dropdown.label = "Cliente (Destino) *"
        elif acao == "Devolução":
            self.cliente_mov_dropdown.visible = True
            self.cliente_mov_dropdown.label = "Cliente (Origem)"
        else:
            self.cliente_mov_dropdown.visible = False
        
        if hasattr(self, 'page'):
            self.page.update()
    
    def on_equipamento_mov_change(self):
        """Chamado quando o equipamento muda"""
        equip_key = self.equipamento_mov_dropdown.value
        
        if equip_key and equip_key in self.equipamentos_mov_dict:
            equip = self.equipamentos_mov_dict[equip_key]
            self.equipamento_mov_selecionado = equip
            
            info_text = f"📦 {equip['tipo']} {equip['marca'] or ''} {equip['modelo'] or ''} | Status: {equip['status_atual']}"
            
            hist_ativo = self.db.buscar_historico_ativo_equipamento(equip['id'])
            if hist_ativo and hist_ativo.get('cliente_nome'):
                info_text += f" | Com: {hist_ativo['cliente_nome']}"
            
            self.info_equipamento_mov.value = info_text
        
        if hasattr(self, 'page'):
            self.page.update()
    
    def determinar_status(self, acao, cliente_id=None):
        """Determina o novo status baseado na ação"""
        if acao == "Entrega":
            return "Com o Cliente"
        elif acao == "Devolução":
            return "Em Estoque"
        elif acao in ["Manutenção", "Reparo"]:
            return "Em Manutenção"
        elif acao == "Transferência":
            return "Com o Cliente"
        elif acao == "Baixa":
            return "Descartado"
        else:
            return "Em Estoque"
    
    def limpar_form_movimentacao(self):
        """Limpa o formulário de movimentação"""
        self.acao_dropdown.value = None
        self.usuario_field.value = "Técnico"
        self.obs_mov_field.value = ""
        self.cliente_mov_dropdown.visible = False
        self.info_equipamento_mov.value = ""
        self.movimentacao_status.value = ""
        self.carregar_equipamentos_mov()
    
    def carregar_movimentacoes(self):
        """Carrega movimentações recentes"""
        self.db.cursor.execute("""
            SELECT h.*, 
                   e.numero_serie, e.tipo,
                   c.nome as cliente_nome
            FROM historico_posse h
            JOIN equipamentos e ON h.equipamento_id = e.id
            LEFT JOIN clientes c ON h.cliente_id = c.id
            ORDER BY h.data_inicio DESC
        """)
        
        historicos = [dict(row) for row in self.db.cursor.fetchall()]
        
        # Filtro de ação
        acao_filtro = self.acao_filter_mov.value
        if acao_filtro != "Todas":
            historicos = [h for h in historicos if h['acao'] == acao_filtro]
        
        # Limite
        limite = int(self.limite_dropdown.value)
        historicos = historicos[:limite]
        
        self.movimentacoes_table.rows.clear()
        
        for h in historicos:
            status_icon = "🟢" if h['data_fim'] is None else "⚪"
            self.movimentacoes_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{status_icon} {h['data_inicio'][:16]}")),
                        ft.DataCell(ft.Text(h['acao'])),
                        ft.DataCell(ft.Text(f"{h['numero_serie']} ({h['tipo']})")),
                        ft.DataCell(ft.Text(h['cliente_nome'] or '-')),
                        ft.DataCell(ft.Text(h['usuario_responsavel'])),
                    ],
                )
            )
        
        if hasattr(self, 'page'):
            self.page.update()
    
    def criar_consultas(self):
        """Cria a aba de consultas"""
        # Criar sub-navegação
        self.consulta_view = "equipamento"  # equipamento, cliente, relatorios
        
        # Container para conteúdo dinâmico
        self.consulta_content_container = ft.Container(expand=True)
        
        def ir_para_equipamento(e):
            self.consulta_view = "equipamento"
            self.consulta_content_container.content = self.criar_consulta_equipamento()
            self.page.update()
        
        def ir_para_cliente(e):
            self.consulta_view = "cliente"
            self.consulta_content_container.content = self.criar_consulta_cliente()
            self.page.update()
        
        def ir_para_relatorios(e):
            self.consulta_view = "relatorios"
            self.consulta_content_container.content = self.criar_consulta_relatorios()
            self.page.update()
        
        # Sub-navegação
        subnav = ft.Container(
            content=ft.Row(
                [
                    ft.FilledButton("📦 Por Equipamento", on_click=ir_para_equipamento),
                    ft.FilledButton("👤 Por Cliente", on_click=ir_para_cliente),
                    ft.FilledButton("📊 Relatórios", on_click=ir_para_relatorios),
                ],
                spacing=10,
            ),
            padding=15,
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
        )
        
        # Inicializar com primeira view
        self.consulta_content_container.content = self.criar_consulta_equipamento()
        
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
    
    def criar_consulta_equipamento(self):
        """Cria a view de busca por equipamento"""
        # Campo de busca
        self.equip_search_field = ft.TextField(
            label="Número de Série",
            hint_text="Digite o número de série...",
            width=400,
            on_submit=lambda e: self.buscar_equipamento_consulta(),
        )
        
        # Resultado
        self.equip_result_container = ft.Container(
            content=ft.Text(
                "Digite um número de série e clique em Buscar",
                size=14,
                color=ft.Colors.GREY_400,
            ),
            expand=True,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Buscar Equipamento por Número de Série", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.equip_search_field,
                            ft.FilledButton("🔍 Buscar", on_click=lambda e: self.buscar_equipamento_consulta()),
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
        
        # Busca equipamento
        equip = self.db.buscar_equipamento_por_serie(termo)
        
        if not equip:
            self.equip_result_container.content = ft.Text(
                f"❌ Equipamento '{termo}' não encontrado",
                size=14,
                color=ft.Colors.RED,
            )
            self.page.update()
            return
        
        # Informações do equipamento
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
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )
        
        # Cliente atual
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
        
        # Histórico completo
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
        
        # Montar resultado
        result_content = [
            info_card,
        ]
        
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
    
    def criar_consulta_cliente(self):
        """Cria a view de busca por cliente"""
        # Campo de busca - responsivo
        self.cliente_search_field = ft.TextField(
            label="Buscar Cliente",
            hint_text="Digite nome, telefone ou documento...",
            expand=True,
            on_submit=lambda e: self.buscar_cliente_consulta(),
        )
        
        # Resultado
        self.cliente_result_container = ft.Container(
            content=ft.Text(
                "Digite nome, telefone ou documento e clique em Buscar",
                size=14,
                color=ft.Colors.GREY_400,
            ),
            expand=True,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Buscar Cliente e seus Equipamentos", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.cliente_search_field,
                            ft.FilledButton("🔍 Buscar", on_click=lambda e: self.buscar_cliente_consulta()),
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
        
        # Busca clientes
        clientes = self.db.buscar_clientes(termo)
        
        if not clientes:
            self.cliente_result_container.content = ft.Text(
                f"❌ Nenhum cliente encontrado com '{termo}'",
                size=14,
                color=ft.Colors.RED,
            )
            self.page.update()
            return
        
        # Se encontrou múltiplos, mostra lista
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
        # Informações do cliente
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
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )
        
        result_content = [info_card]
        
        # Equipamentos ativos
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
        
        # Histórico completo
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
    
    def criar_consulta_relatorios(self):
        """Cria a view de relatórios"""
        # Estatísticas
        self.stats_text = ft.Text("Carregando estatísticas...", size=14)
        
        stats_card = ft.Container(
            content=self.stats_text,
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )
        
        # Status message
        self.relatorio_status = ft.Text("", size=14)
        
        # Atualizar estatísticas
        self.atualizar_estatisticas_consulta()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Relatórios e Estatísticas", size=18, weight=ft.FontWeight.BOLD),
                    stats_card,
                    ft.Text("Exportar Dados", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.FilledButton("📄 Exportar Clientes (CSV)", on_click=lambda e: self.exportar_clientes_csv()),
                            ft.FilledButton("📄 Exportar Equipamentos (CSV)", on_click=lambda e: self.exportar_equipamentos_csv()),
                            ft.FilledButton("📄 Exportar Histórico (CSV)", on_click=lambda e: self.exportar_historico_csv()),
                        ],
                        spacing=10,
                    ),
                    self.relatorio_status,
                    ft.FilledButton("🔄 Atualizar Estatísticas", on_click=lambda e: self.atualizar_estatisticas_consulta()),
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
        )
    
    def atualizar_estatisticas_consulta(self):
        """Atualiza estatísticas gerais"""
        stats = self.db.get_estatisticas()
        
        texto = f"""📊 ESTATÍSTICAS GERAIS

Total de Clientes: {stats['total_clientes']}
Total de Equipamentos: {stats['total_equipamentos']}

Equipamentos por Status:
"""
        
        for status, total in stats['por_status'].items():
            texto += f"  • {status}: {total}\n"
        
        texto += "\nEquipamentos por Tipo:\n"
        
        for tipo, total in stats['por_tipo'].items():
            texto += f"  • {tipo}: {total}\n"
        
        # Estatísticas adicionais
        self.db.cursor.execute("SELECT COUNT(*) FROM historico_posse")
        total_movimentacoes = self.db.cursor.fetchone()[0]
        
        self.db.cursor.execute("SELECT COUNT(*) FROM historico_posse WHERE data_fim IS NULL")
        movimentacoes_ativas = self.db.cursor.fetchone()[0]
        
        texto += f"\nTotal de Movimentações: {total_movimentacoes}\n"
        texto += f"Movimentações Ativas: {movimentacoes_ativas}\n"
        
        self.stats_text.value = texto.strip()
        
        if hasattr(self, 'page'):
            self.page.update()
    
    def exportar_clientes_csv(self):
        """Exporta clientes para CSV"""
        import csv
        
        try:
            clientes = self.db.buscar_clientes()
            
            filename = f"clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Nome', 'Telefone', 'Email', 'Documento', 'Setor', 'Endereço', 'Data Cadastro'])
                
                for c in clientes:
                    writer.writerow([
                        c['id'],
                        c['nome'],
                        c['telefone'],
                        c['email'] or '',
                        c['documento'] or '',
                        c['setor'] or '',
                        c['endereco'] or '',
                        c['data_cadastro']
                    ])
            
            self.relatorio_status.value = f"✅ {len(clientes)} clientes exportados para {filename}"
            self.relatorio_status.color = ft.Colors.GREEN
        
        except Exception as e:
            self.relatorio_status.value = f"❌ Erro ao exportar: {str(e)}"
            self.relatorio_status.color = ft.Colors.RED
        
        self.page.update()
    
    def exportar_equipamentos_csv(self):
        """Exporta equipamentos para CSV"""
        import csv
        
        try:
            equipamentos = self.db.buscar_equipamentos()
            
            filename = f"equipamentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Número Série', 'Tipo', 'Marca', 'Modelo', 'Status', 'Data Registro', 'Valor', 'Garantia'])
                
                for e in equipamentos:
                    writer.writerow([
                        e['id'],
                        e['numero_serie'],
                        e['tipo'],
                        e['marca'] or '',
                        e['modelo'] or '',
                        e['status_atual'],
                        e['data_registro'],
                        e['valor_estimado'] or '',
                        e['data_garantia'] or ''
                    ])
            
            self.relatorio_status.value = f"✅ {len(equipamentos)} equipamentos exportados para {filename}"
            self.relatorio_status.color = ft.Colors.GREEN
        
        except Exception as e:
            self.relatorio_status.value = f"❌ Erro ao exportar: {str(e)}"
            self.relatorio_status.color = ft.Colors.RED
        
        self.page.update()
    
    def exportar_historico_csv(self):
        """Exporta histórico completo para CSV"""
        import csv
        
        try:
            self.db.cursor.execute("""
                SELECT h.*, 
                       e.numero_serie, e.tipo, e.marca, e.modelo,
                       c.nome as cliente_nome, c.telefone as cliente_telefone
                FROM historico_posse h
                JOIN equipamentos e ON h.equipamento_id = e.id
                LEFT JOIN clientes c ON h.cliente_id = c.id
                ORDER BY h.data_inicio DESC
            """)
            
            historico = [dict(row) for row in self.db.cursor.fetchall()]
            
            filename = f"historico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'ID', 'Equipamento', 'Tipo', 'Marca', 'Modelo', 
                    'Cliente', 'Telefone', 'Ação', 'Data Início', 'Data Fim', 
                    'Usuário', 'Observações'
                ])
                
                for h in historico:
                    writer.writerow([
                        h['id'],
                        h['numero_serie'],
                        h['tipo'],
                        h['marca'] or '',
                        h['modelo'] or '',
                        h['cliente_nome'] or '',
                        h['cliente_telefone'] or '',
                        h['acao'],
                        h['data_inicio'],
                        h['data_fim'] or '',
                        h['usuario_responsavel'],
                        h['observacoes'] or ''
                    ])
            
            self.relatorio_status.value = f"✅ {len(historico)} registros exportados para {filename}"
            self.relatorio_status.color = ft.Colors.GREEN
        
        except Exception as e:
            self.relatorio_status.value = f"❌ Erro ao exportar: {str(e)}"
            self.relatorio_status.color = ft.Colors.RED
        
        self.page.update()
    
    def criar_configuracoes(self):
        """Cria a aba de configurações"""
        # Carregar configurações
        self.carregar_config()
        
        # Sub-navegação
        self.config_view = "backup"
        self.config_content_container = ft.Container(expand=True)
        
        def ir_para_backup(e):
            self.config_view = "backup"
            self.config_content_container.content = self.criar_config_backup()
            self.page.update()
        
        def ir_para_geral(e):
            self.config_view = "geral"
            self.config_content_container.content = self.criar_config_geral()
            self.page.update()
        
        def ir_para_sobre(e):
            self.config_view = "sobre"
            self.config_content_container.content = self.criar_config_sobre()
            self.page.update()
        
        subnav = ft.Container(
            content=ft.Row(
                [
                    ft.FilledButton("💾 Backup", on_click=ir_para_backup),
                    ft.FilledButton("⚙️ Geral", on_click=ir_para_geral),
                    ft.FilledButton("ℹ️ Sobre", on_click=ir_para_sobre),
                ],
                spacing=10,
            ),
            padding=15,
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
        )
        
        # Inicializar com primeira view
        self.config_content_container.content = self.criar_config_backup()
        
        return ft.Container(
            content=ft.Column(
                [
                    subnav,
                    self.config_content_container,
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
        )
    
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
    
    def criar_config_backup(self):
        """Cria a view de configurações de backup"""
        # Checkbox backup automático
        self.backup_auto_check = ft.Checkbox(
            label="Criar backup automático ao iniciar o sistema",
            value=self.config['backup_automatico'],
        )
        
        # Dias para manter backups - responsivo
        self.backup_dias_field = ft.TextField(
            label="Manter backups dos últimos (dias)",
            value=str(self.config['backup_dias']),
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        # Pasta de backup - responsiva
        self.backup_pasta_field = ft.TextField(
            label="Pasta de Backup",
            value=self.config['backup_pasta'],
            expand=True,
        )
        
        # Status
        self.backup_status = ft.Text("", size=14)
        
        def criar_backup_agora(e):
            try:
                backup_path = self.db.backup_database()
                self.backup_status.value = f"✅ Backup criado: {backup_path}"
                self.backup_status.color = ft.Colors.GREEN
            except Exception as ex:
                self.backup_status.value = f"❌ Erro: {str(ex)}"
                self.backup_status.color = ft.Colors.RED
            self.page.update()
        
        def salvar_config_backup(e):
            self.config['backup_automatico'] = self.backup_auto_check.value
            try:
                self.config['backup_dias'] = int(self.backup_dias_field.value)
            except:
                self.config['backup_dias'] = 7
            self.config['backup_pasta'] = self.backup_pasta_field.value
            
            if self.salvar_config():
                self.backup_status.value = "✅ Configurações salvas com sucesso!"
                self.backup_status.color = ft.Colors.GREEN
            else:
                self.backup_status.value = "❌ Erro ao salvar configurações"
                self.backup_status.color = ft.Colors.RED
            self.page.update()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Configurações de Backup", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Backup Automático", size=16, weight=ft.FontWeight.BOLD),
                    self.backup_auto_check,
                    ft.Text("Limpeza Automática", size=16, weight=ft.FontWeight.BOLD),
                    self.backup_dias_field,
                    ft.Text("Pasta de Backup", size=16, weight=ft.FontWeight.BOLD),
                    self.backup_pasta_field,
                    ft.Text("Gerenciar Backups", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.FilledButton("💾 Criar Backup Agora", on_click=criar_backup_agora),
                            ft.FilledButton("💾 Salvar Configurações", on_click=salvar_config_backup),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self.backup_status,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
        )
    
    def criar_config_geral(self):
        """Cria a view de configurações gerais"""
        # Tema
        self.tema_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="claro", label="☀️ Claro"),
                ft.Radio(value="escuro", label="🌙 Escuro"),
            ]),
            value=self.config['tema'],
        )
        
        # Usuário padrão - responsivo
        self.usuario_padrao_field = ft.TextField(
            label="Nome do Usuário Padrão",
            value=self.config['usuario_padrao'],
            expand=True,
            hint_text="Ex: João Silva",
        )
        
        # Status
        self.geral_status = ft.Text("", size=14)
        
        # Estatísticas
        stats = self.db.get_estatisticas()
        
        stats_text = f"""📊 ESTATÍSTICAS GERAIS

Total de Clientes: {stats['total_clientes']}
Total de Equipamentos: {stats['total_equipamentos']}

Equipamentos por Status:
"""
        for status, total in stats['por_status'].items():
            stats_text += f"  • {status}: {total}\n"
        
        stats_card = ft.Container(
            content=ft.Text(stats_text.strip(), size=14),
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )
        
        def salvar_config_geral(e):
            self.config['tema'] = self.tema_radio.value
            self.config['usuario_padrao'] = self.usuario_padrao_field.value
            
            if self.salvar_config():
                # Aplicar tema imediatamente
                if self.config['tema'] == 'claro':
                    self.page.theme_mode = ft.ThemeMode.LIGHT
                else:
                    self.page.theme_mode = ft.ThemeMode.DARK
                self.page.update()
                
                self.geral_status.value = "✅ Configurações salvas e tema aplicado!"
                self.geral_status.color = ft.Colors.GREEN
            else:
                self.geral_status.value = "❌ Erro ao salvar configurações"
                self.geral_status.color = ft.Colors.RED
            self.page.update()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Configurações Gerais", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Aparência", size=16, weight=ft.FontWeight.BOLD),
                    self.tema_radio,
                    ft.Text("(O tema será aplicado imediatamente ao salvar)", size=12, color=ft.Colors.GREY_400),
                    ft.Text("Usuário Padrão", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Nome usado por padrão ao registrar movimentações:", size=12, color=ft.Colors.GREY_400),
                    self.usuario_padrao_field,
                    ft.Text("Estatísticas do Sistema", size=16, weight=ft.FontWeight.BOLD),
                    stats_card,
                    ft.Text("Banco de Dados", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Arquivo: fastech.db\nTamanho: {self.get_db_size()}", size=14),
                    ft.FilledButton("💾 Salvar Configurações", on_click=salvar_config_geral),
                    self.geral_status,
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
        )
    
    def criar_config_sobre(self):
        """Cria a view sobre o sistema"""
        info_text = """Versão: 1.0.0
Data: 02/12/2024

Desenvolvido para gestão interna de equipamentos
e rastreamento de responsáveis.

Funcionalidades:
• Gestão de Clientes
• Gestão de Equipamentos
• Controle de Movimentações
• Consultas e Relatórios
• Backup Automático
• Exportação de Dados

Tecnologias:
• Python 3.8+
• SQLite
• Flet"""
        
        info_card = ft.Container(
            content=ft.Text(info_text, size=14, text_align=ft.TextAlign.CENTER),
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )
        
        def verificar_sistema(e):
            try:
                stats = self.db.get_estatisticas()
                
                def fechar_dialogo(ev):
                    dialogo.open = False
                    self.page.update()
                
                mensagem = f"""✓ Sistema OK!

Banco de dados: Conectado
Clientes: {stats['total_clientes']}
Equipamentos: {stats['total_equipamentos']}
Tamanho do banco: {self.get_db_size()}"""
                
                dialogo = ft.AlertDialog(
                    title=ft.Text("Verificação do Sistema"),
                    content=ft.Text(mensagem),
                    actions=[
                        ft.TextButton("OK", on_click=fechar_dialogo),
                    ],
                )
                
                self.page.dialog = dialogo
                dialogo.open = True
                self.page.update()
            except Exception as ex:
                pass
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=20),
                    ft.Text("⚙️", size=48),
                    ft.Text("FastTech Control", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Sistema de Gestão de Equipamentos", size=14, color=ft.Colors.GREY_400),
                    ft.Container(height=10),
                    info_card,
                    ft.Container(height=10),
                    ft.FilledButton("🔧 Verificar Sistema", on_click=verificar_sistema),
                    ft.Container(height=20),
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
        )
    
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
