"""
Formulário de registro de movimentações de equipamentos - Versão Flet
"""

import flet as ft
from datetime import datetime
from gui.styles import get_colors, get_fonts, PADDING
from database import Database
from models import AcaoHistorico, StatusEquipamento


class MovimentacaoForm(ft.UserControl):
    """Formulário de registro de movimentações"""
    
    def __init__(self, page: ft.Page, db: Database):
        super().__init__()
        self.page = page
        self.db = db
        self.equipamento_selecionado = None
        self.cliente_selecionado = None
        
        self._criar_interface()
        self._carregar_movimentacoes_recentes()

    def _criar_interface(self):
        """Cria a interface do formulário"""
        
        # Título
        self.title = ft.Text(
            "🔄 Registro de Movimentações",
            size=get_fonts()['title']['size'],
            weight=get_fonts()['title']['weight'],
            color=get_colors()['text']
        )

        # Coluna esquerda - Formulário
        self._criar_formulario()

        # Coluna direita - Histórico recente
        self._criar_historico()

        # Status label
        self.status_label = ft.Text("", size=12)

        # Layout principal em duas colunas
        self.main_row = ft.Row(
            [
                ft.Column([self.form_section], expand=1),
                ft.VerticalDivider(width=1),
                ft.Column([self.historico_section], expand=1)
            ],
            expand=True
        )

        self.controls = [self.title, self.main_row, self.status_label]

    def _criar_formulario(self):
        """Cria o formulário de movimentação"""
        
        # Tipo de Ação
        self.acao_dropdown = ft.Dropdown(
            label="Tipo de Movimentação",
            options=[ft.dropdown.Option(acao) for acao in AcaoHistorico.todos()],
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_change=self._on_acao_change
        )

        # Seleção de Equipamento
        self.equipamento_dropdown = ft.Dropdown(
            label="Equipamento",
            options=[],
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_change=self._on_equipamento_change
        )
        self._carregar_equipamentos_combo()

        # Info do equipamento selecionado
        self.info_equipamento = ft.Text("", size=12, italic=True)

        # Seleção de Cliente (condicional)
        self.cliente_dropdown = ft.Dropdown(
            label="Cliente",
            options=[],
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        self._carregar_clientes_combo()
        self.cliente_dropdown.visible = False  # Oculto inicialmente

        # Usuário Responsável
        self.usuario_field = ft.TextField(
            label="Seu Nome (Responsável)",
            value="Técnico",  # Valor padrão
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )

        # Observações
        self.obs_field = ft.TextField(
            label="Observações",
            multiline=True,
            min_lines=4,
            max_lines=6,
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )

        # Botões
        self.btn_registrar = ft.ElevatedButton(
            "✅ Registrar Movimentação",
            icon=ft.icons.ADD_CIRCLE,
            on_click=self._registrar_movimentacao,
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

        # Monta o formulário
        self.form_controls = ft.Column([
            self.acao_dropdown,
            self.equipamento_dropdown,
            self.info_equipamento,
            ft.Row([self.cliente_dropdown]),
            self.usuario_field,
            self.obs_field,
            ft.Row([self.btn_registrar, self.btn_limpar])
        ], spacing=10)

        self.form_section = ft.Container(
            content=ft.Column([
                ft.Text("Nova Movimentação", size=16, weight=ft.FontWeight.BOLD),
                self.form_controls
            ]),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            expand=True
        )

    def _criar_historico(self):
        """Cria a lista de movimentações recentes"""
        
        # Filtros
        self.acao_filter = ft.Dropdown(
            label="Filtrar por ação",
            options=[ft.dropdown.Option("Todas")] + [ft.dropdown.Option(acao) for acao in AcaoHistorico.todos()],
            value="Todas",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_change=lambda e: self._carregar_movimentacoes_recentes()
        )
        
        self.limite_filter = ft.Dropdown(
            label="Mostrar",
            options=[
                ft.dropdown.Option("10"),
                ft.dropdown.Option("25"),
                ft.dropdown.Option("50"),
                ft.dropdown.Option("100"),
                ft.dropdown.Option("Todos")
            ],
            value="25",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_change=lambda e: self._carregar_movimentacoes_recentes()
        )

        # Tabela de movimentações
        self.movimentacoes_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Data")),
                ft.DataColumn(ft.Text("Ação")),
                ft.DataColumn(ft.Text("Equipamento")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Usuário"))
            ],
            rows=[],
            sort_column_index=0,
            sort_ascending=True
        )

        # Botões de ação
        self.btn_ver_detalhes = ft.ElevatedButton(
            "👁️ Ver Detalhes",
            icon=ft.icons.VISIBILITY,
            on_click=self._ver_detalhes,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.BLUE}
            )
        )
        
        self.btn_atualizar = ft.ElevatedButton(
            "🔄 Atualizar",
            icon=ft.icons.REFRESH,
            on_click=self._carregar_movimentacoes_recentes,
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK87},
                bgcolor={"": ft.colors.GREY}
            )
        )

        # Monta a seção de histórico
        self.historico_controls = ft.Column([
            ft.Text("Movimentações Recentes", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([self.acao_filter, self.limite_filter]),
            ft.Divider(height=10),
            ft.Column([self.movimentacoes_table], scroll=ft.ScrollMode.AUTO, expand=True),
            ft.Row([self.btn_ver_detalhes, self.btn_atualizar])
        ], expand=True)

        self.historico_section = ft.Container(
            content=self.historico_controls,
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            expand=True
        )

    def _carregar_equipamentos_combo(self):
        """Carrega equipamentos no combobox"""
        equipamentos = self.db.buscar_equipamentos()
        
        options = []
        for e in equipamentos:
            option_text = f"{e['numero_serie']} - {e['tipo']} - {e['status_atual']}"
            options.append(ft.dropdown.Option(option_text))
        
        self.equipamento_dropdown.options = options
        if options:
            self.equipamento_dropdown.value = options[0].key
            self._on_equipamento_change(None)

    def _carregar_clientes_combo(self):
        """Carrega clientes no combobox"""
        clientes = self.db.buscar_clientes()
        
        options = []
        for c in clientes:
            option_text = f"{c['id']} - {c['nome']} - {c['telefone']}"
            options.append(ft.dropdown.Option(option_text))
        
        self.cliente_dropdown.options = options

    def _on_acao_change(self, e):
        """Chamado quando a ação é alterada"""
        acao = self.acao_dropdown.value
        
        # Mostra/oculta campo de cliente baseado na ação
        if acao in [AcaoHistorico.ENTREGA, AcaoHistorico.TRANSFERENCIA]:
            self.cliente_dropdown.visible = True
            self.cliente_dropdown.label = "Cliente (Destino)"
        elif acao == AcaoHistorico.DEVOLUCAO:
            self.cliente_dropdown.visible = True
            self.cliente_dropdown.label = "Cliente (Origem)"
        else:
            self.cliente_dropdown.visible = False

        self.update()

    def _on_equipamento_change(self, e):
        """Chamado quando o equipamento é alterado"""
        equip_key = self.equipamento_dropdown.value
        
        # Encontrar equipamento correspondente
        equipamentos = self.db.buscar_equipamentos()
        equip = None
        for e in equipamentos:
            if f"{e['numero_serie']} - {e['tipo']} - {e['status_atual']}" == equip_key:
                equip = e
                break
        
        if equip:
            self.equipamento_selecionado = equip
            
            # Mostra informações do equipamento
            info_text = f"📦 {equip['tipo']} {equip['marca'] or ''} {equip['modelo'] or ''}\n"
            info_text += f"Status atual: {equip['status_atual']}"
            
            # Busca cliente atual se houver
            hist_ativo = self.db.buscar_historico_ativo_equipamento(equip['id'])
            if hist_ativo and hist_ativo.get('cliente_nome'):
                info_text += f" | Com: {hist_ativo['cliente_nome']}"
            
            self.info_equipamento.value = info_text
            self.info_equipamento.visible = True
        else:
            self.info_equipamento.visible = False
            
        self.update()

    def _validar_campos(self):
        """Valida os campos do formulário"""
        acao = self.acao_dropdown.value
        equip_key = self.equipamento_dropdown.value
        usuario = self.usuario_field.value.strip()

        # Ação obrigatória
        if not acao or acao == "":
            self._show_status("Selecione o tipo de movimentação", "error")
            return False

        # Equipamento obrigatório
        if not equip_key or equip_key == "":
            self._show_status("Selecione um equipamento", "error")
            return False

        # Usuário obrigatório
        if not usuario:
            self._show_status("Informe seu nome", "error")
            return False

        # Cliente obrigatório para algumas ações
        if acao in [AcaoHistorico.ENTREGA, AcaoHistorico.TRANSFERENCIA]:
            cliente_key = self.cliente_dropdown.value
            if not cliente_key or cliente_key == "":
                self._show_status("Selecione o cliente de destino", "error")
                return False

        return True

    def _registrar_movimentacao(self, e):
        """Registra uma nova movimentação"""
        if not self._validar_campos():
            return

        acao = self.acao_dropdown.value
        equip = self.equipamento_selecionado
        usuario = self.usuario_field.value.strip()
        obs = self.obs_field.value.strip() or None

        # Cliente (se aplicável)
        cliente_id = None
        cliente_key = self.cliente_dropdown.value
        if cliente_key and cliente_key != "":
            # Extrai o ID do cliente do texto
            try:
                cliente_id = int(cliente_key.split(' - ')[0])
            except (ValueError, IndexError):
                cliente_id = None

        try:
            # Finaliza histórico anterior se necessário
            hist_ativo = self.db.buscar_historico_ativo_equipamento(equip['id'])
            if hist_ativo:
                self.db.finalizar_historico(hist_ativo['id'])

            # Determina novo status baseado na ação
            novo_status = self._determinar_status(acao, cliente_id)

            # Registra nova movimentação
            hist_id = self.db.inserir_historico(
                equip['id'],
                acao,
                usuario,
                cliente_id,
                observacoes=obs
            )

            # Atualiza status do equipamento
            self.db.atualizar_status_equipamento(equip['id'], novo_status)

            # Mensagem de sucesso
            equip_desc = f"{equip['tipo']} ({equip['numero_serie']})"
            if acao == AcaoHistorico.ENTREGA:
                cliente = self.db.buscar_cliente_por_id(cliente_id)
                self._show_status(f"Equipamento entregue ao cliente: {cliente['nome']}", "success")
            elif acao == AcaoHistorico.DEVOLUCAO:
                self._show_status(f"Equipamento devolvido: {equip_desc}", "success")
            elif acao == AcaoHistorico.TRANSFERENCIA:
                cliente = self.db.buscar_cliente_por_id(cliente_id)
                self._show_status(f"Equipamento transferido para: {cliente['nome']}", "success")
            else:
                self._show_status(f"Movimentação registrada: {acao} - {equip_desc}", "success")

            # Atualiza listas
            self._limpar_formulario()
            self._carregar_movimentacoes_recentes()

        except ValueError as ve:
            self._show_status(str(ve), "error")

    def _determinar_status(self, acao, cliente_id):
        """Determina o novo status baseado na ação"""
        if acao == AcaoHistorico.ENTREGA:
            return StatusEquipamento.COM_CLIENTE
        elif acao == AcaoHistorico.DEVOLUCAO:
            return StatusEquipamento.RECEBIDO
        elif acao == AcaoHistorico.TRANSFERENCIA:
            return StatusEquipamento.COM_CLIENTE
        elif acao == AcaoHistorico.MANUTENCAO:
            return StatusEquipamento.EM_MANUTENCAO
        elif acao == AcaoHistorico.RETIRADA_MANUTENCAO:
            return StatusEquipamento.RETIRADO_MANUTENCAO
        else:
            return StatusEquipamento.EM_ESTOQUE

    def _limpar_formulario(self):
        """Limpa o formulário de movimentação"""
        self.acao_dropdown.value = ""
        self.equipamento_dropdown.value = ""
        self.cliente_dropdown.value = ""
        self.usuario_field.value = "Técnico"
        self.obs_field.value = ""
        self.info_equipamento.value = ""
        self.cliente_dropdown.visible = False
        self.update()

    def _carregar_movimentacoes_recentes(self, e=None):
        """Carrega movimentações recentes na tabela"""
        # Obter filtros
        acao_filtro = self.acao_filter.value
        limite_str = self.limite_filter.value
        
        # Converter limite para inteiro
        if limite_str == "Todos":
            limite = None
        else:
            limite = int(limite_str)

        # Buscar movimentações
        movimentacoes = self.db.buscar_historico_completo(acao=acao_filtro if acao_filtro != "Todas" else None, limite=limite)

        rows = []
        for m in movimentacoes:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(m['data_inicio'])),
                ft.DataCell(ft.Text(m['acao'])),
                ft.DataCell(ft.Text(m['equipamento_tipo'])),
                ft.DataCell(ft.Text(m['cliente_nome'] or '-')),
                ft.DataCell(ft.Text(m['usuario_responsavel']))
            ]))

        self.movimentacoes_table.rows = rows
        self.update()

    def _ver_detalhes(self, e):
        """Exibe detalhes da movimentação selecionada"""
        if not self.movimentacoes_table.selected_index:
            self._show_status("Selecione uma movimentação para ver detalhes", "error")
            return

        selected_index = self.movimentacoes_table.selected_index
        if selected_index < 0 or selected_index >= len(self.movimentacoes_table.rows):
            self._show_status("Movimentação selecionada inválida", "error")
            return

        # Obter dados da movimentação selecionada
        mov_data = self.movimentacoes_table.rows[selected_index]
        # Os dados reais não estão armazenados nos widgets, então buscamos novamente
        todas_movimentacoes = self.db.buscar_historico_completo(
            acao=self.acao_filter.value if self.acao_filter.value != "Todas" else None,
            limite=int(self.limite_filter.value) if self.limite_filter.value != "Todos" else None
        )
        
        if selected_index < len(todas_movimentacoes):
            movimentacao = todas_movimentacoes[selected_index]
            
            # Criar diálogo com detalhes
            detalhes_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Detalhes da Movimentação"),
                content=ft.Column([
                    ft.Text(f"Ação: {movimentacao['acao']}", weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10),
                    ft.Text(f"Data: {movimentacao['data_inicio']}"),
                    ft.Text(f"Equipamento: {movimentacao['equipamento_tipo']} ({movimentacao['equipamento_numero_serie']})"),
                    ft.Text(f"Cliente: {movimentacao['cliente_nome'] or 'N/A'}"),
                    ft.Text(f"Responsável: {movimentacao['usuario_responsavel']}"),
                    ft.Text(f"Status: {'Ativo' if movimentacao['data_fim'] is None else 'Finalizado'}"),
                    ft.Divider(height=10),
                    ft.Text("Observações:", weight=ft.FontWeight.BOLD),
                    ft.Text(movimentacao['observacoes'] or "Nenhuma observação registrada")
                ], tight=True),
                actions=[ft.TextButton("Fechar", on_click=lambda e: self.page.dialog.close())],
                actions_alignment=ft.MainAxisAlignment.END
            )

            self.page.dialog = detalhes_dialog
            detalhes_dialog.open = True
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