"""
Aba Equipamentos - Gestão de equipamentos
"""
import flet as ft
from gui.base import BaseTab


class EquipamentosTab(BaseTab):
    """Aba de gestão de equipamentos"""
    
    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        self.equipamento_selecionado = None
        
        # Campos do formulário
        self.numero_serie_field = None
        self.tipo_dropdown = None
        self.marca_field = None
        self.modelo_field = None
        self.status_dropdown = None
        self.valor_field = None
        self.garantia_field = None
        self.obs_field = None
        self.equipamento_status = None
        self.equipamentos_table = None
        self.equipamento_search = None
        self.status_filter = None
    
    def build(self):
        """Constrói a interface de equipamentos"""
        # Criar campos
        self.criar_campos()
        
        # Criar tabela
        self.criar_tabela()
        
        # Layout
        formulario = self.criar_formulario()
        lista = self.criar_lista()
        
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
    
    def criar_campos(self):
        """Cria os campos do formulário"""
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
        
        self.equipamento_status = ft.Text("", size=14)
        
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
    
    def criar_tabela(self):
        """Cria a tabela de equipamentos"""
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
    
    def criar_formulario(self):
        """Cria o formulário de cadastro"""
        return ft.Container(
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
                            ft.FilledButton("💾 Salvar", on_click=self.salvar_equipamento),
                            ft.FilledButton("🔄 Limpar", on_click=self.limpar_form),
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
    
    def criar_lista(self):
        """Cria a lista de equipamentos"""
        return ft.Container(
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
    
    def limpar_form(self, e):
        """Limpa o formulário"""
        self.limpar_form_equipamento()
        self.page.update()
    
    def limpar_form_equipamento(self):
        """Limpa os campos do formulário"""
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
        # Verificar se status_filter existe
        if not hasattr(self, 'status_filter') or self.status_filter is None:
            status = None
        else:
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
        
        # Verificar se status_filter existe
        if not hasattr(self, 'status_filter') or self.status_filter is None:
            status = None
        else:
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
