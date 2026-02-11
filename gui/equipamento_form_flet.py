"""
Formulário de cadastro e edição de equipamentos - Versão Flet
"""

import flet as ft
from datetime import datetime
from gui.styles import get_colors, get_fonts, PADDING
from database import Database
from models import TipoEquipamento, StatusEquipamento, AcaoHistorico
from utils.validators import validar_numero_serie


class EquipamentoForm(ft.UserControl):
    """Formulário completo de gestão de equipamentos"""
    
    def __init__(self, page: ft.Page, db: Database):
        super().__init__()
        self.page = page
        self.db = db
        self.equipamento_selecionado = None
        
        self._criar_interface()
        self._carregar_equipamentos()

    def _criar_interface(self):
        """Cria a interface do formulário"""
        
        # Título
        self.title = ft.Text(
            "📦 Gestão de Equipamentos",
            size=get_fonts()['title']['size'],
            weight=get_fonts()['title']['weight'],
            color=get_colors()['text']
        )

        # Coluna esquerda - Formulário
        self._criar_formulario()

        # Coluna direita - Lista
        self._criar_lista()

        # Status label
        self.status_label = ft.Text("", size=12)

        # Layout principal em duas colunas
        self.main_row = ft.Row(
            [
                ft.Column([self.form_section], expand=1),
                ft.VerticalDivider(width=1),
                ft.Column([self.list_section], expand=1)
            ],
            expand=True
        )

        self.controls = [self.title, self.main_row, self.status_label]

    def _criar_formulario(self):
        """Cria o formulário de cadastro"""
        
        # Campos do formulário
        self.numero_serie_field = ft.TextField(
            label="Número de Série",
            hint_text="Ex: NB-2024-001",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.tipo_dropdown = ft.Dropdown(
            label="Tipo de Equipamento",
            options=[ft.dropdown.Option(tipo) for tipo in TipoEquipamento.todos()],
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        # Marca e Modelo (mesma linha)
        self.marca_field = ft.TextField(
            label="Marca",
            hint_text="Ex: Dell, HP, Samsung",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.modelo_field = ft.TextField(
            label="Modelo",
            hint_text="Ex: Latitude 5420",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        # Cliente (Dropdown)
        self.cliente_dropdown = ft.Dropdown(
            label="Cliente (opcional - deixe vazio para 'Em Estoque')",
            options=[ft.dropdown.Option("(Sem cliente - Em Estoque)")],
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        self._carregar_clientes_combo()

        # Status (Dropdown)
        self.status_dropdown = ft.Dropdown(
            label="Status Inicial",
            options=[ft.dropdown.Option(status) for status in StatusEquipamento.todos()],
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            value=StatusEquipamento.EM_ESTOQUE
        )
        
        # Valor Estimado e Data Garantia (mesma linha)
        self.valor_field = ft.TextField(
            label="Valor Estimado (R$)",
            hint_text="0.00",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.garantia_field = ft.TextField(
            label="Data Garantia",
            hint_text="AAAA-MM-DD",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        # Observações
        self.obs_field = ft.TextField(
            label="Observações",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )

        # Botões
        self.btn_salvar = ft.ElevatedButton(
            "💾 Salvar Equipamento",
            icon=ft.icons.SAVE,
            on_click=self._salvar_equipamento,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.GREEN}
            )
        )
        
        self.btn_limpar = ft.ElevatedButton(
            "🔄 Limpar",
            icon=ft.icons.REFRESH,
            on_click=self._limpar_formulario,
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK87},
                bgcolor={"": ft.colors.GREY}
            )
        )
        
        self.btn_cancelar = ft.ElevatedButton(
            "✖ Cancelar Edição",
            icon=ft.icons.CANCEL,
            on_click=self._cancelar_edicao,
            visible=False,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.RED}
            )
        )

        # Monta o formulário
        self.form_controls = ft.Column([
            self.numero_serie_field,
            self.tipo_dropdown,
            ft.Row([self.marca_field, self.modelo_field]),
            self.cliente_dropdown,
            self.status_dropdown,
            ft.Row([self.valor_field, self.garantia_field]),
            self.obs_field,
            ft.Row([self.btn_salvar, self.btn_limpar, self.btn_cancelar])
        ], spacing=10)

        self.form_section = ft.Container(
            content=ft.Column([
                ft.Text("Cadastro de Equipamento", size=16, weight=ft.FontWeight.BOLD),
                self.form_controls
            ]),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            expand=True
        )

    def _criar_lista(self):
        """Cria a lista de equipamentos"""
        
        # Barra de busca
        self.search_field = ft.TextField(
            hint_text="Buscar por número de série, tipo ou marca...",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_change=lambda e: self._buscar_equipamentos()
        )

        # Filtro por status
        self.status_filter = ft.Dropdown(
            label="Filtrar por status",
            options=[ft.dropdown.Option("Todos")] + [ft.dropdown.Option(status) for status in StatusEquipamento.todos()],
            value="Todos",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_change=lambda e: self._carregar_equipamentos()
        )

        # Tabela de equipamentos
        self.equipamentos_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Série")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Marca")),
                ft.DataColumn(ft.Text("Status"))
            ],
            rows=[],
            sort_column_index=0,
            sort_ascending=True
        )

        # Botões de ação
        self.btn_editar = ft.ElevatedButton(
            "✏️ Editar",
            icon=ft.icons.EDIT,
            on_click=self._editar_equipamento,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.BLUE}
            )
        )
        
        self.btn_ver_historico = ft.ElevatedButton(
            "👁️ Ver Histórico",
            icon=ft.icons.HISTORY,
            on_click=self._ver_historico,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.ORANGE}
            )
        )
        
        self.btn_atualizar = ft.ElevatedButton(
            "🔄 Atualizar",
            icon=ft.icons.REFRESH,
            on_click=self._carregar_equipamentos,
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK87},
                bgcolor={"": ft.colors.GREY}
            )
        )

        # Monta a lista
        self.list_section = ft.Container(
            content=ft.Column([
                ft.Text("Equipamentos Cadastrados", size=16, weight=ft.FontWeight.BOLD),
                self.search_field,
                ft.Row([self.status_filter]),
                ft.Divider(height=10),
                ft.Column([self.equipamentos_table], scroll=ft.ScrollMode.AUTO, expand=True),
                ft.Row([self.btn_editar, self.btn_ver_historico, self.btn_atualizar])
            ], expand=True),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            expand=True
        )

    def _carregar_clientes_combo(self):
        """Carrega clientes no combobox"""
        clientes = self.db.buscar_clientes()
        
        # Formato: "ID - Nome - Telefone"
        options = [ft.dropdown.Option("(Sem cliente - Em Estoque)")]
        for c in clientes:
            option_text = f"{c['id']} - {c['nome']} - {c['telefone']}"
            options.append(ft.dropdown.Option(option_text))
        
        self.cliente_dropdown.options = options
        self.cliente_dropdown.value = "(Sem cliente - Em Estoque)"

    def _validar_campos(self):
        """Valida os campos do formulário"""
        numero_serie = self.numero_serie_field.value
        tipo = self.tipo_dropdown.value

        # Número de série obrigatório
        if not numero_serie or not numero_serie.strip():
            self._show_status("Número de série é obrigatório", "error")
            return False
            
        valido, msg = validar_numero_serie(numero_serie)
        if not valido:
            self._show_status(msg, "error")
            return False

        # Tipo obrigatório
        if not tipo or tipo == "":
            self._show_status("Tipo de equipamento é obrigatório", "error")
            return False

        return True

    def _salvar_equipamento(self, e):
        """Salva ou atualiza um equipamento"""
        if not self._validar_campos():
            return

        numero_serie = self.numero_serie_field.value.strip()
        tipo = self.tipo_dropdown.value
        marca = self.marca_field.value.strip() or None
        modelo = self.modelo_field.value.strip() or None
        status = self.status_dropdown.value

        # Valor estimado
        valor_str = self.valor_field.value.strip()
        valor = float(valor_str.replace(',', '.')) if valor_str else None

        # Data garantia
        garantia = self.garantia_field.value.strip() or None

        # Observações
        obs = self.obs_field.value.strip() or None

        # Cliente selecionado
        cliente_sel = self.cliente_dropdown.value
        cliente_id = None
        if cliente_sel != "(Sem cliente - Em Estoque)":
            # Extrai o ID do cliente do texto
            try:
                cliente_id = int(cliente_sel.split(' - ')[0])
            except (ValueError, IndexError):
                cliente_id = None

        try:
            if self.equipamento_selecionado:
                # Atualizar equipamento existente
                self.db.atualizar_equipamento(
                    self.equipamento_selecionado['id'],
                    numero_serie=numero_serie,
                    tipo=tipo,
                    marca=marca,
                    modelo=modelo,
                    status_atual=status,
                    data_garantia=garantia,
                    valor_estimado=valor,
                    observacoes=obs
                )
                self._show_status(f"Equipamento '{numero_serie}' atualizado!", "success")
            else:
                # Inserir novo equipamento
                equip_id = self.db.inserir_equipamento(
                    numero_serie, tipo, marca, modelo, status, garantia, valor, obs
                )

                # Registrar no histórico
                acao = AcaoHistorico.CADASTRO
                if cliente_id:
                    acao = AcaoHistorico.ENTREGA
                    status = StatusEquipamento.COM_CLIENTE
                    self.db.atualizar_status_equipamento(equip_id, status)

                self.db.inserir_historico(
                    equip_id,
                    acao,
                    "Sistema",
                    cliente_id,
                    observacoes=f"Cadastro inicial: {obs}" if obs else "Cadastro inicial"
                )

                self._show_status(f"Equipamento '{numero_serie}' cadastrado! (ID: {equip_id})", "success")

            self._limpar_formulario()
            self._carregar_equipamentos()

        except ValueError as ve:
            self._show_status(str(ve), "error")

    def _limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.numero_serie_field.value = ""
        self.tipo_dropdown.value = ""
        self.marca_field.value = ""
        self.modelo_field.value = ""
        self.cliente_dropdown.value = "(Sem cliente - Em Estoque)"
        self.status_dropdown.value = StatusEquipamento.EM_ESTOQUE
        self.valor_field.value = ""
        self.garantia_field.value = ""
        self.obs_field.value = ""
        self.equipamento_selecionado = None
        self.btn_cancelar.visible = False
        self.btn_salvar.text = "💾 Salvar Equipamento"
        self.update()

    def _cancelar_edicao(self, e):
        """Cancela a edição"""
        self._limpar_formulario()
        self._show_status("Edição cancelada", "info")

    def _carregar_equipamentos(self, e=None):
        """Carrega todos os equipamentos na tabela"""
        # Obter filtro de status
        status_filtro = self.status_filter.value
        
        if status_filtro == "Todos":
            equipamentos = self.db.buscar_equipamentos()
        else:
            # Filtrar localmente após obter todos os equipamentos
            todos_equipamentos = self.db.buscar_equipamentos()
            equipamentos = [e for e in todos_equipamentos if e['status_atual'] == status_filtro]
        
        # Aplicar busca se houver termo
        termo_busca = self.search_field.value
        if termo_busca and termo_busca.strip():
            termo = termo_busca.lower().strip()
            equipamentos = [
                e for e in equipamentos
                if (termo in e['numero_serie'].lower() or
                    termo in e['tipo'].lower() or
                    (e['marca'] and termo in e['marca'].lower()))
            ]

        rows = []
        for e in equipamentos:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(e['id']))),
                ft.DataCell(ft.Text(e['numero_serie'])),
                ft.DataCell(ft.Text(e['tipo'])),
                ft.DataCell(ft.Text(e['marca'] or '-')),
                ft.DataCell(ft.Text(e['status_atual']))
            ]))

        self.equipamentos_table.rows = rows
        self.update()

    def _buscar_equipamentos(self, e=None):
        """Busca equipamentos pelo termo"""
        # A busca será feita via evento no campo de texto
        # que já chama _carregar_equipamentos que faz o filtro
        self._carregar_equipamentos()

    def _editar_equipamento(self, e):
        """Carrega dados do equipamento selecionado para edição"""
        if not self.equipamentos_table.selected_index:
            self._show_status("Selecione um equipamento para editar", "error")
            return

        selected_index = self.equipamentos_table.selected_index
        if selected_index < 0 or selected_index >= len(self.equipamentos_table.rows):
            self._show_status("Equipamento selecionado inválido", "error")
            return

        equip_id = int(self.equipamentos_table.rows[selected_index].cells[0].content.value)
        equipamento = self.db.buscar_equipamento_por_id(equip_id)

        if equipamento:
            self.equipamento_selecionado = equipamento

            # Preenche o formulário
            self.numero_serie_field.value = equipamento['numero_serie']
            self.tipo_dropdown.value = equipamento['tipo']
            self.marca_field.value = equipamento['marca'] or ""
            self.modelo_field.value = equipamento['modelo'] or ""
            
            # Cliente
            if equipamento['cliente_atual_id']:
                cliente = self.db.buscar_cliente_por_id(equipamento['cliente_atual_id'])
                if cliente:
                    cliente_text = f"{cliente['id']} - {cliente['nome']} - {cliente['telefone']}"
                    self.cliente_dropdown.value = cliente_text
                else:
                    self.cliente_dropdown.value = "(Sem cliente - Em Estoque)"
            else:
                self.cliente_dropdown.value = "(Sem cliente - Em Estoque)"
                
            self.status_dropdown.value = equipamento['status_atual']
            self.valor_field.value = str(equipamento['valor_estimado']) if equipamento['valor_estimado'] else ""
            self.garantia_field.value = equipamento['data_garantia'] or ""
            self.obs_field.value = equipamento['observacoes'] or ""

            # Mostra botão cancelar e muda texto do salvar
            self.btn_cancelar.visible = True
            self.btn_salvar.text = "💾 Atualizar Equipamento"

            self._show_status(f"Editando: {equipamento['numero_serie']}", "info")
            self.update()

    def _ver_historico(self, e):
        """Exibe o histórico do equipamento selecionado"""
        if not self.equipamentos_table.selected_index:
            self._show_status("Selecione um equipamento para ver o histórico", "error")
            return

        selected_index = self.equipamentos_table.selected_index
        if selected_index < 0 or selected_index >= len(self.equipamentos_table.rows):
            self._show_status("Equipamento selecionado inválido", "error")
            return

        equip_id = int(self.equipamentos_table.rows[selected_index].cells[0].content.value)
        equipamento = self.db.buscar_equipamento_por_id(equip_id)

        if equipamento:
            # Obter histórico
            historico = self.db.buscar_historico_equipamento(equip_id)
            
            # Criar tabela de histórico
            historico_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Status")),
                    ft.DataColumn(ft.Text("Data Início")),
                    ft.DataColumn(ft.Text("Data Fim")),
                    ft.DataColumn(ft.Text("Ação")),
                    ft.DataColumn(ft.Text("Cliente")),
                    ft.DataColumn(ft.Text("Usuário"))
                ],
                rows=[]
            )
            
            for h in historico:
                status = "🟢" if h['data_fim'] is None else "⚪"
                cliente_nome = h['cliente_nome'] or '-'
                historico_table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(status)),
                    ft.DataCell(ft.Text(h['data_inicio'])),
                    ft.DataCell(ft.Text(h['data_fim'] or '-')),
                    ft.DataCell(ft.Text(h['acao'])),
                    ft.DataCell(ft.Text(cliente_nome)),
                    ft.DataCell(ft.Text(h['usuario_responsavel']))
                ]))
            
            # Diálogo com histórico
            historico_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Histórico de {equipamento['numero_serie']}"),
                content=ft.Column([
                    ft.Text(f"Tipo: {equipamento['tipo']}", weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10),
                    ft.Column([historico_table], scroll=ft.ScrollMode.AUTO, height=400)
                ], tight=True),
                actions=[ft.TextButton("Fechar", on_click=lambda e: self.page.dialog.close())],
                actions_alignment=ft.MainAxisAlignment.END
            )

            self.page.dialog = historico_dialog
            historico_dialog.open = True
            self.page.update()

    def _show_status(self, message, level="info"):
        """Mostra mensagem de status"""
        colors = get_colors()
        if level == "error":
            self.status_label.color = colors['danger']
            self.status_label.weight = ft.FontWeight.BOLD
        elif level == "success":
            self.status_label.color = colors['success']
        elif level == "warning":
            self.status_label.color = colors['warning']
        else:
            self.status_label.color = colors['text']
            self.status_label.weight = ft.FontWeight.NORMAL

        self.status_label.value = message
        self.update()