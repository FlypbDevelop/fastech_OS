"""
Aba Movimentações - Controle de movimentações de equipamentos
"""
import flet as ft
from gui.base import BaseTab


class MovimentacoesTab(BaseTab):
    """Aba de controle de movimentações"""
    
    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        self.equipamento_mov_selecionado = None
        self.equipamentos_mov_dict = {}
        
        # Campos do formulário
        self.acao_dropdown = None
        self.equipamento_mov_dropdown = None
        self.info_equipamento_mov = None
        self.cliente_mov_dropdown = None
        self.usuario_field = None
        self.obs_mov_field = None
        self.movimentacao_status = None
        self.movimentacoes_table = None
        self.acao_filter_mov = None
        self.limite_dropdown = None
    
    def build(self):
        """Constrói a interface de movimentações"""
        # Criar campos
        self.criar_campos()
        
        # Criar tabela
        self.criar_tabela()
        
        # Layout
        formulario = self.criar_formulario()
        lista = self.criar_lista()
        
        # Carregar dados inicialmente
        self.carregar_equipamentos_mov()
        self.carregar_clientes_mov()
        self.carregar_movimentacoes()
        
        # Layout responsivo com scroll
        return ft.Container(
            content=ft.Column(
                [
                    ft.ResponsiveRow(
                        [
                            ft.Container(
                                content=formulario,
                                col={"sm": 12, "md": 12, "lg": 5, "xl": 4},
                            ),
                            ft.Container(
                                content=lista,
                                col={"sm": 12, "md": 12, "lg": 7, "xl": 8},
                            ),
                        ],
                        spacing=20,
                        run_spacing=20,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
            expand=True,
        )
    
    def criar_campos(self):
        """Cria os campos do formulário"""
        self.acao_dropdown = ft.Dropdown(
            label="Tipo de Movimentação *",
            hint_text="Selecione o tipo",
            expand=True,
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
            expand=True,
            options=[],
        )
        self.equipamento_mov_dropdown.on_change = lambda e: self.on_equipamento_mov_change()
        
        self.info_equipamento_mov = ft.Text("", size=12, color=ft.Colors.GREY_400)
        
        self.cliente_mov_dropdown = ft.Dropdown(
            label="Cliente *",
            hint_text="Selecione o cliente",
            expand=True,
            options=[],
            visible=False,
        )
        
        self.usuario_field = ft.TextField(
            label="Seu Nome (Responsável) *",
            value="Técnico",
            expand=True,
        )
        
        self.obs_mov_field = ft.TextField(
            label="Observações",
            hint_text="Informações adicionais",
            expand=True,
            multiline=True,
            min_lines=3,
            max_lines=5,
        )
        
        self.movimentacao_status = ft.Text("", size=14)
        
        self.acao_filter_mov = ft.Dropdown(
            label="Filtrar por ação",
            expand=True,
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
            expand=True,
            value="25",
            options=[
                ft.dropdown.Option("10"),
                ft.dropdown.Option("25"),
                ft.dropdown.Option("50"),
                ft.dropdown.Option("100"),
            ],
        )
        self.limite_dropdown.on_change = lambda e: self.carregar_movimentacoes()
    
    def criar_tabela(self):
        """Cria a tabela de movimentações"""
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
    
    def criar_formulario(self):
        """Cria o formulário de movimentação"""
        return ft.Container(
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
                            ft.FilledButton("✅ Registrar", on_click=self.registrar_movimentacao, expand=True),
                            ft.FilledButton("🔄 Limpar", on_click=self.limpar_form, expand=True),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
            bgcolor=self.get_bg_color(),
            border_radius=10,
        )
    
    def criar_lista(self):
        """Cria a lista de movimentações"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Movimentações Recentes", size=18, weight=ft.FontWeight.BOLD),
                    ft.ResponsiveRow(
                        [
                            ft.Container(
                                content=self.acao_filter_mov,
                                col={"sm": 12, "md": 4, "lg": 4},
                            ),
                            ft.Container(
                                content=self.limite_dropdown,
                                col={"sm": 12, "md": 3, "lg": 3},
                            ),
                            ft.Container(
                                content=ft.FilledButton("🔄 Atualizar", on_click=lambda e: self.carregar_movimentacoes(), expand=True),
                                col={"sm": 12, "md": 5, "lg": 5},
                            ),
                        ],
                        spacing=10,
                        run_spacing=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [self.movimentacoes_table],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                    ),
                ],
                spacing=10,
            ),
            padding=20,
            bgcolor=self.get_bg_color(),
            border_radius=10,
        )
    
    def registrar_movimentacao(self, e):
        """Registra uma nova movimentação"""
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
    
    def limpar_form(self, e):
        """Limpa o formulário"""
        self.limpar_form_movimentacao()
        self.page.update()
    
    def limpar_form_movimentacao(self):
        """Limpa os campos do formulário"""
        self.acao_dropdown.value = None
        self.usuario_field.value = "Técnico"
        self.obs_mov_field.value = ""
        self.cliente_mov_dropdown.visible = False
        self.info_equipamento_mov.value = ""
        self.movimentacao_status.value = ""
        self.carregar_equipamentos_mov()
    
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
