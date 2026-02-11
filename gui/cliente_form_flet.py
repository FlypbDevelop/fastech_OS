"""
Formulário de cadastro e edição de clientes - Versão Flet
"""

import flet as ft
from gui.styles import get_colors, get_fonts, PADDING
from database import Database
from utils.validators import (
    validar_telefone, validar_email, validar_documento,
    formatar_telefone, formatar_cpf, formatar_cnpj
)


class ClienteForm(ft.UserControl):
    """Formulário completo de gestão de clientes"""
    
    def __init__(self, page: ft.Page, db: Database):
        super().__init__()
        self.page = page
        self.db = db
        self.cliente_selecionado = None
        
        self._criar_interface()
        self._carregar_clientes()

    def _criar_interface(self):
        """Cria a interface do formulário"""
        
        # Título
        self.title = ft.Text(
            "📋 Gestão de Clientes",
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
        self.nome_field = ft.TextField(
            label="Nome Completo",
            hint_text="Digite o nome do cliente",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.telefone_field = ft.TextField(
            label="Telefone",
            hint_text="(11) 98765-4321",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.email_field = ft.TextField(
            label="Email",
            hint_text="cliente@email.com",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.documento_field = ft.TextField(
            label="CPF/CNPJ",
            hint_text="000.000.000-00",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.setor_field = ft.TextField(
            label="Setor/Departamento",
            hint_text="Ex: TI, RH, Vendas",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )
        
        self.endereco_field = ft.TextField(
            label="Endereço",
            hint_text="Rua, número, bairro, cidade",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True
        )

        # Botões
        self.btn_salvar = ft.ElevatedButton(
            "💾 Salvar Cliente",
            icon=ft.icons.SAVE,
            on_click=self._salvar_cliente,
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
            self.nome_field,
            self.telefone_field,
            self.email_field,
            self.documento_field,
            self.setor_field,
            self.endereco_field,
            ft.Row([self.btn_salvar, self.btn_limpar, self.btn_cancelar])
        ], spacing=10)

        self.form_section = ft.Container(
            content=ft.Column([
                ft.Text("Cadastro de Cliente", size=16, weight=ft.FontWeight.BOLD),
                self.form_controls
            ]),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            expand=True
        )

    def _criar_lista(self):
        """Cria a lista de clientes"""
        
        # Barra de busca
        self.search_field = ft.TextField(
            hint_text="Buscar por nome, telefone ou documento...",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_change=lambda e: self._buscar_clientes()
        )

        # Tabela de clientes
        self.clientes_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Telefone")),
                ft.DataColumn(ft.Text("Setor"))
            ],
            rows=[],
            sort_column_index=0,
            sort_ascending=True
        )

        # Botões de ação
        self.btn_editar = ft.ElevatedButton(
            "✏️ Editar",
            icon=ft.icons.EDIT,
            on_click=self._editar_cliente,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.BLUE}
            )
        )
        
        self.btn_excluir = ft.ElevatedButton(
            "🗑️ Excluir",
            icon=ft.icons.DELETE,
            on_click=self._excluir_cliente,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.RED}
            )
        )
        
        self.btn_atualizar = ft.ElevatedButton(
            "🔄 Atualizar",
            icon=ft.icons.REFRESH,
            on_click=self._carregar_clientes,
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK87},
                bgcolor={"": ft.colors.GREY}
            )
        )

        # Monta a lista
        self.list_section = ft.Container(
            content=ft.Column([
                ft.Text("Clientes Cadastrados", size=16, weight=ft.FontWeight.BOLD),
                self.search_field,
                ft.Divider(height=10),
                ft.Column([self.clientes_table], scroll=ft.ScrollMode.AUTO, expand=True),
                ft.Row([self.btn_editar, self.btn_excluir, self.btn_atualizar])
            ], expand=True),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            expand=True
        )

    def _validar_campos(self):
        """Valida os campos do formulário"""
        nome = self.nome_field.value
        telefone = self.telefone_field.value
        email = self.email_field.value
        documento = self.documento_field.value

        # Nome obrigatório
        if not nome or not nome.strip():
            self._show_status("Nome é obrigatório", "error")
            return False

        # Telefone obrigatório e válido
        if not telefone or not telefone.strip():
            self._show_status("Telefone é obrigatório", "error")
            return False

        valido, msg = validar_telefone(telefone)
        if not valido:
            self._show_status(msg, "error")
            return False

        # Email opcional mas deve ser válido
        if email and email.strip():
            valido, msg = validar_email(email)
            if not valido:
                self._show_status(msg, "error")
                return False

        # Documento opcional mas deve ser válido
        if documento and documento.strip():
            valido, msg = validar_documento(documento)
            if not valido:
                self._show_status(msg, "error")
                return False

        return True

    def _salvar_cliente(self, e):
        """Salva ou atualiza um cliente"""
        if not self._validar_campos():
            return

        nome = self.nome_field.value.strip()
        telefone = formatar_telefone(self.telefone_field.value.strip())
        email = self.email_field.value.strip() or None
        documento = self.documento_field.value.strip()
        setor = self.setor_field.value.strip() or None
        endereco = self.endereco_field.value.strip() or None

        # Formata documento se preenchido
        if documento:
            doc_clean = documento.replace('.', '').replace('-', '').replace('/', '')
            if len(doc_clean) == 11:
                documento = formatar_cpf(documento)
            else:
                documento = formatar_cnpj(documento)
        else:
            documento = None

        try:
            if self.cliente_selecionado:
                # Atualizar cliente existente
                self.db.atualizar_cliente(
                    self.cliente_selecionado['id'],
                    nome=nome,
                    telefone=telefone,
                    email=email,
                    documento=documento,
                    setor=setor,
                    endereco=endereco
                )
                self._show_status(f"Cliente '{nome}' atualizado com sucesso!", "success")
            else:
                # Inserir novo cliente
                cliente_id = self.db.inserir_cliente(
                    nome, telefone, email, endereco, documento, setor
                )
                self._show_status(f"Cliente '{nome}' cadastrado com sucesso! (ID: {cliente_id})", "success")

            self._limpar_formulario()
            self._carregar_clientes()

        except ValueError as ve:
            self._show_status(str(ve), "error")

    def _limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.nome_field.value = ""
        self.telefone_field.value = ""
        self.email_field.value = ""
        self.documento_field.value = ""
        self.setor_field.value = ""
        self.endereco_field.value = ""
        self.cliente_selecionado = None
        self.btn_cancelar.visible = False
        self.btn_salvar.text = "💾 Salvar Cliente"
        self.update()

    def _cancelar_edicao(self, e):
        """Cancela a edição"""
        self._limpar_formulario()
        self._show_status("Edição cancelada", "info")

    def _carregar_clientes(self, e=None):
        """Carrega todos os clientes na tabela"""
        clientes = self.db.buscar_clientes()
        
        rows = []
        for c in clientes:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(c['id']))),
                ft.DataCell(ft.Text(c['nome'])),
                ft.DataCell(ft.Text(c['telefone'])),
                ft.DataCell(ft.Text(c['setor'] or '-'))
            ]))

        self.clientes_table.rows = rows
        self.update()

    def _buscar_clientes(self, e=None):
        """Busca clientes pelo termo"""
        termo = self.search_field.value
        if not termo or not termo.strip():
            self._carregar_clientes()
            return
            
        clientes = self.db.buscar_clientes(termo)
        
        rows = []
        for c in clientes:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(c['id']))),
                ft.DataCell(ft.Text(c['nome'])),
                ft.DataCell(ft.Text(c['telefone'])),
                ft.DataCell(ft.Text(c['setor'] or '-'))
            ]))

        self.clientes_table.rows = rows
        
        if not rows:
            self._show_status("Nenhum cliente encontrado", "info")
            
        self.update()

    def _editar_cliente(self, e):
        """Carrega dados do cliente selecionado para edição"""
        if not self.clientes_table.selected_index:
            self._show_status("Selecione um cliente para editar", "error")
            return

        selected_index = self.clientes_table.selected_index
        if selected_index < 0 or selected_index >= len(self.clientes_table.rows):
            self._show_status("Cliente selecionado inválido", "error")
            return

        cliente_id = int(self.clientes_table.rows[selected_index].cells[0].content.value)
        cliente = self.db.buscar_cliente_por_id(cliente_id)

        if cliente:
            self.cliente_selecionado = cliente

            # Preenche o formulário
            self.nome_field.value = cliente['nome']
            self.telefone_field.value = cliente['telefone']
            self.email_field.value = cliente['email'] or ""
            self.documento_field.value = cliente['documento'] or ""
            self.setor_field.value = cliente['setor'] or ""
            self.endereco_field.value = cliente['endereco'] or ""

            # Mostra botão cancelar e muda texto do salvar
            self.btn_cancelar.visible = True
            self.btn_salvar.text = "💾 Atualizar Cliente"

            self._show_status(f"Editando: {cliente['nome']}", "info")
            self.update()

    def _excluir_cliente(self, e):
        """Exclui o cliente selecionado"""
        if not self.clientes_table.selected_index:
            self._show_status("Selecione um cliente para excluir", "error")
            return

        selected_index = self.clientes_table.selected_index
        if selected_index < 0 or selected_index >= len(self.clientes_table.rows):
            self._show_status("Cliente selecionado inválido", "error")
            return

        cliente_id = int(self.clientes_table.rows[selected_index].cells[0].content.value)
        cliente_nome = self.clientes_table.rows[selected_index].cells[1].content.value

        # Diálogo de confirmação
        def confirmar_exclusao(e):
            self.page.dialog.open = False
            sucesso = self.db.deletar_cliente(cliente_id)

            if sucesso:
                self._show_status(f"Cliente '{cliente_nome}' excluído com sucesso!", "success")
                self._carregar_clientes()
            else:
                self._show_status(
                    "Não é possível excluir este cliente. "
                    "Ele possui equipamentos vinculados.",
                    "error"
                )
            self.update()

        def cancelar_exclusao(e):
            self.page.dialog.open = False
            self.page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(
                f"Deseja realmente excluir o cliente '{cliente_nome}'?\n\n"
                "ATENÇÃO: Não é possível excluir clientes com equipamentos ativos."
            ),
            actions=[
                ft.TextButton("Sim", on_click=confirmar_exclusao),
                ft.TextButton("Não", on_click=cancelar_exclusao)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
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