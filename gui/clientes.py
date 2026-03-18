"""
Aba Clientes - Gestão de clientes
"""
import flet as ft
from gui.base import BaseTab
from utils.validators import validar_telefone, validar_email, validar_documento


class ClientesTab(BaseTab):
    """Aba de gestão de clientes"""
    
    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        self.cliente_selecionado = None
        self.tipo_cliente_atual = "Cliente Final"
        
        # Campos do formulário
        self.tipo_cliente_radio = None
        self.nome_field = None
        self.telefone_field = None
        self.email_field = None
        self.documento_field = None
        self.setor_field = None
        self.endereco_field = None
        
        # Campos específicos para Terceirizado
        self.empresa_field = None
        self.regiao_field = None
        
        self.cliente_status = None
        self.clientes_table = None
        self.cliente_search = None
    
    def build(self):
        """Constrói a interface de clientes"""
        # Criar campos
        self.criar_campos()
        
        # Criar tabela
        self.criar_tabela()
        
        # Layout responsivo
        formulario = self.criar_formulario()
        lista = self.criar_lista()
        
        # Carregar clientes inicialmente
        self.carregar_clientes()
        
        # Layout responsivo com ResponsiveRow e scroll
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
        # Seletor de tipo de cliente
        self.tipo_cliente_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="Cliente Final", label="👤 Cliente Final"),
                ft.Radio(value="Terceirizado", label="🏢 Terceirizado"),
            ]),
            value="Cliente Final",
            on_change=self.on_tipo_cliente_change,
        )
        
        # Campos comuns
        self.nome_field = ft.TextField(
            label="Nome Completo *",
            hint_text="Digite o nome",
            expand=True,
        )
        
        self.telefone_field = ft.TextField(
            label="Telefone/WhatsApp *",
            hint_text="(11) 98765-4321",
            expand=True,
        )
        
        # Campos Cliente Final
        self.email_field = ft.TextField(
            label="Email",
            hint_text="cliente@email.com",
            expand=True,
            visible=True,
        )
        
        self.documento_field = ft.TextField(
            label="CPF/CNPJ",
            hint_text="000.000.000-00",
            expand=True,
            visible=True,
        )
        
        self.setor_field = ft.TextField(
            label="Setor/Departamento",
            hint_text="Ex: TI, RH, Vendas",
            expand=True,
            visible=True,
        )
        
        self.endereco_field = ft.TextField(
            label="Endereço",
            hint_text="Rua, número, bairro, cidade",
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=3,
            visible=True,
        )
        
        # Campos Terceirizado
        self.empresa_field = ft.TextField(
            label="Empresa",
            hint_text="Nome da empresa",
            expand=True,
            visible=False,
        )
        
        self.regiao_field = ft.TextField(
            label="Região",
            hint_text="Ex: Zona Sul, Centro, etc",
            expand=True,
            visible=False,
        )
        
        self.cliente_status = ft.Text("", size=14)
        
        self.cliente_search = ft.TextField(
            label="Buscar cliente",
            hint_text="Nome, telefone ou documento...",
            expand=True,
            on_submit=lambda e: self.buscar_clientes(),
        )
    
    def criar_tabela(self):
        """Cria a tabela de clientes"""
        self.clientes_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Telefone", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Info", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )
    
    def on_tipo_cliente_change(self, e):
        """Chamado quando o tipo de cliente muda"""
        tipo = self.tipo_cliente_radio.value
        self.tipo_cliente_atual = tipo
        
        if tipo == "Terceirizado":
            # Mostrar campos de Terceirizado
            self.empresa_field.visible = True
            self.regiao_field.visible = True
            self.telefone_field.label = "WhatsApp *"
            
            # Ocultar campos de Cliente Final
            self.email_field.visible = False
            self.documento_field.visible = False
            self.setor_field.visible = False
            self.endereco_field.visible = False
        else:
            # Mostrar campos de Cliente Final
            self.email_field.visible = True
            self.documento_field.visible = True
            self.setor_field.visible = True
            self.endereco_field.visible = True
            self.telefone_field.label = "Telefone *"
            
            # Ocultar campos de Terceirizado
            self.empresa_field.visible = False
            self.regiao_field.visible = False
        
        self.page.update()
    
    def criar_formulario(self):
        """Cria o formulário de cadastro"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Cadastro de Cliente", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Tipo de Cliente", size=14, weight=ft.FontWeight.BOLD),
                    self.tipo_cliente_radio,
                    ft.Divider(),
                    self.nome_field,
                    self.telefone_field,
                    # Campos Cliente Final
                    self.email_field,
                    self.documento_field,
                    self.setor_field,
                    self.endereco_field,
                    # Campos Terceirizado
                    self.empresa_field,
                    self.regiao_field,
                    self.cliente_status,
                    ft.Row(
                        [
                            ft.FilledButton("💾 Salvar", on_click=self.confirmar_salvar_cliente, expand=True),
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
        """Cria a lista de clientes"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Clientes Cadastrados", size=18, weight=ft.FontWeight.BOLD),
                    ft.ResponsiveRow(
                        [
                            ft.Container(
                                content=self.cliente_search,
                                col={"sm": 12, "md": 6, "lg": 6},
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.FilledButton("🔍 Buscar", on_click=lambda e: self.buscar_clientes(), expand=True),
                                        ft.FilledButton("🔄 Todos", on_click=lambda e: self.carregar_clientes(), expand=True),
                                    ],
                                    spacing=10,
                                ),
                                col={"sm": 12, "md": 6, "lg": 6},
                            ),
                        ],
                        spacing=10,
                        run_spacing=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [self.clientes_table],
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
    
    def confirmar_salvar_cliente(self, e):
        """Mostra confirmação antes de salvar"""
        nome = self.nome_field.value
        tipo = self.tipo_cliente_radio.value
        
        if not nome:
            self.cliente_status.value = "❌ Nome é obrigatório"
            self.cliente_status.color = ft.Colors.RED
            self.page.update()
            return
        
        # Mensagem de confirmação
        if self.cliente_selecionado:
            mensagem = f"Deseja atualizar o cliente '{nome}'?"
            titulo = "Confirmar Atualização"
        else:
            mensagem = f"Deseja cadastrar o cliente '{nome}' como {tipo}?"
            titulo = "Confirmar Cadastro"
        
        def confirmar(ev):
            dialogo.open = False
            self.page.update()
            self.salvar_cliente(e)
        
        def cancelar(ev):
            dialogo.open = False
            self.page.update()
        
        dialogo = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(mensagem),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.FilledButton("Confirmar", on_click=confirmar),
            ],
        )
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def salvar_cliente(self, e):
        """Salva ou atualiza um cliente"""
        nome = self.nome_field.value
        telefone = self.telefone_field.value
        tipo_cliente = self.tipo_cliente_radio.value
        
        # Validações baseadas no tipo
        if tipo_cliente == "Terceirizado":
            # Terceirizado: Nome e WhatsApp obrigatórios
            if not nome or not telefone:
                self.cliente_status.value = "❌ Nome e WhatsApp são obrigatórios"
                self.cliente_status.color = ft.Colors.RED
                self.page.update()
                return
            
            # Validar WhatsApp
            tel_valido, tel_msg = validar_telefone(telefone)
            if not tel_valido:
                self.cliente_status.value = f"❌ {tel_msg}"
                self.cliente_status.color = ft.Colors.RED
                self.page.update()
                return
            
            # Dados do Terceirizado
            empresa = self.empresa_field.value
            regiao = self.regiao_field.value
            
        else:
            # Cliente Final: Nome e Telefone obrigatórios
            if not nome or not telefone:
                self.cliente_status.value = "❌ Nome e Telefone são obrigatórios"
                self.cliente_status.color = ft.Colors.RED
                self.page.update()
                return
            
            # Validar telefone
            tel_valido, tel_msg = validar_telefone(telefone)
            if not tel_valido:
                self.cliente_status.value = f"❌ {tel_msg}"
                self.cliente_status.color = ft.Colors.RED
                self.page.update()
                return
            
            # Validar email (se preenchido)
            email = self.email_field.value
            if email:
                email_valido, email_msg = validar_email(email)
                if not email_valido:
                    self.cliente_status.value = f"❌ {email_msg}"
                    self.cliente_status.color = ft.Colors.RED
                    self.page.update()
                    return
            
            # Validar documento (se preenchido)
            documento = self.documento_field.value
            if documento:
                doc_valido, doc_msg = validar_documento(documento)
                if not doc_valido:
                    self.cliente_status.value = f"❌ {doc_msg}"
                    self.cliente_status.color = ft.Colors.RED
                    self.page.update()
                    return
        
        try:
            if self.cliente_selecionado:
                # Atualizar cliente existente
                if tipo_cliente == "Terceirizado":
                    self.db.atualizar_cliente(
                        self.cliente_selecionado['id'],
                        tipo_cliente=tipo_cliente,
                        nome=nome,
                        telefone=telefone,
                        setor=self.empresa_field.value or None,  # Usar setor para empresa
                        regiao=self.regiao_field.value or None,
                        email=None,
                        documento=None,
                        endereco=None,
                    )
                else:
                    self.db.atualizar_cliente(
                        self.cliente_selecionado['id'],
                        tipo_cliente=tipo_cliente,
                        nome=nome,
                        telefone=telefone,
                        email=self.email_field.value or None,
                        documento=self.documento_field.value or None,
                        setor=self.setor_field.value or None,
                        endereco=self.endereco_field.value or None,
                        regiao=None,
                    )
                self.cliente_status.value = f"✅ Cliente '{nome}' atualizado!"
            else:
                # Inserir novo cliente
                if tipo_cliente == "Terceirizado":
                    self.db.inserir_cliente(
                        nome,
                        telefone,
                        email=None,
                        endereco=None,
                        documento=None,
                        setor=self.empresa_field.value or None,  # Usar setor para empresa
                        tipo_cliente=tipo_cliente,
                        regiao=self.regiao_field.value or None,
                    )
                else:
                    self.db.inserir_cliente(
                        nome,
                        telefone,
                        self.email_field.value or None,
                        self.endereco_field.value or None,
                        self.documento_field.value or None,
                        self.setor_field.value or None,
                        tipo_cliente,
                        None,
                    )
                self.cliente_status.value = f"✅ Cliente '{nome}' cadastrado!"
            
            self.cliente_status.color = ft.Colors.GREEN
            self.limpar_form_cliente()
            self.carregar_clientes()
            self.page.update()
        except Exception as ex:
            self.cliente_status.value = f"❌ Erro: {str(ex)}"
            self.cliente_status.color = ft.Colors.RED
            self.page.update()
    
    def limpar_form(self, e):
        """Limpa o formulário"""
        self.limpar_form_cliente()
        self.page.update()
    
    def limpar_form_cliente(self):
        """Limpa os campos do formulário"""
        self.nome_field.value = ""
        self.telefone_field.value = ""
        self.email_field.value = ""
        self.documento_field.value = ""
        self.setor_field.value = ""
        self.endereco_field.value = ""
        self.empresa_field.value = ""
        self.regiao_field.value = ""
        self.tipo_cliente_radio.value = "Cliente Final"
        self.tipo_cliente_atual = "Cliente Final"
        self.cliente_selecionado = None
        self.cliente_status.value = ""
        
        # Resetar visibilidade dos campos
        self.on_tipo_cliente_change(None)
    
    def _render_linha_cliente(self, cliente: dict, reload_callback=None) -> ft.DataRow:
        """
        Recebe um dict de cliente e retorna um ft.DataRow completo com 6 células:
        id, tipo (com ícone), nome, telefone, info_extra, ações.
        reload_callback é chamado após exclusão bem-sucedida.
        Se None, usa self.carregar_clientes como padrão.
        """
        _reload = reload_callback if reload_callback is not None else self.carregar_clientes

        def confirmar_editar(e, c=cliente):
            self.criar_dialogo_confirmacao(
                titulo="Confirmar Edição",
                mensagem=f"Deseja editar o cliente '{c['nome']}'?",
                on_confirmar=lambda ev: (
                    setattr(self.page.dialog, 'open', False),
                    self.page.update(),
                    self.editar_cliente(c),
                ),
            )

        def confirmar_excluir(e, c=cliente):
            def _excluir(ev):
                self.page.dialog.open = False
                self.page.update()
                if self.db.deletar_cliente(c['id']):
                    self.cliente_status.value = f"✅ Cliente '{c['nome']}' excluído!"
                    self.cliente_status.color = ft.Colors.GREEN
                else:
                    self.cliente_status.value = "❌ Cliente possui equipamentos vinculados"
                    self.cliente_status.color = ft.Colors.RED
                _reload()
                self.page.update()

            self.criar_dialogo_confirmacao(
                titulo="⚠️ Confirmar Exclusão",
                mensagem=f"Tem certeza que deseja excluir o cliente '{c['nome']}'?\n\nEsta ação não pode ser desfeita.",
                on_confirmar=_excluir,
                texto_confirmar="Excluir",
                estilo_confirmar=ft.ButtonStyle(bgcolor=ft.Colors.RED),
            )

        tipo = cliente.get('tipo_cliente', 'Cliente Final')
        if tipo == "Terceirizado":
            tipo_icon = "🏢"
            info_extra = cliente.get('regiao', '-')
        else:
            tipo_icon = "👤"
            info_extra = cliente.get('setor', '-')

        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(cliente['id']))),
                ft.DataCell(ft.Text(f"{tipo_icon} {tipo}", size=12)),
                ft.DataCell(ft.Text(cliente['nome'])),
                ft.DataCell(ft.Text(cliente['telefone'])),
                ft.DataCell(ft.Text(info_extra)),
                ft.DataCell(
                    self.criar_linha_tabela_acoes([
                        ("✏️", "Editar", confirmar_editar),
                        ("🗑️", "Excluir", confirmar_excluir),
                    ])
                ),
            ],
        )

    def carregar_clientes(self):
        """Carrega todos os clientes na tabela"""
        clientes = self.db.buscar_clientes()
        self.clientes_table.rows.clear()

        for c in clientes:
            self.clientes_table.rows.append(
                self._render_linha_cliente(c, reload_callback=self.carregar_clientes)
            )

        if hasattr(self, 'page'):
            self.page.update()
    
    def editar_cliente(self, cliente):
        """Carrega dados do cliente para edição"""
        self.cliente_selecionado = cliente
        tipo = cliente.get('tipo_cliente', 'Cliente Final')
        
        # Definir tipo
        self.tipo_cliente_radio.value = tipo
        self.tipo_cliente_atual = tipo
        
        # Campos comuns
        self.nome_field.value = cliente['nome']
        self.telefone_field.value = cliente['telefone']
        
        if tipo == "Terceirizado":
            # Carregar campos de Terceirizado
            self.empresa_field.value = cliente.get('setor', '') or ''
            self.regiao_field.value = cliente.get('regiao', '') or ''
        else:
            # Carregar campos de Cliente Final
            self.email_field.value = cliente.get('email', '') or ''
            self.documento_field.value = cliente.get('documento', '') or ''
            self.setor_field.value = cliente.get('setor', '') or ''
            self.endereco_field.value = cliente.get('endereco', '') or ''
        
        # Atualizar visibilidade dos campos
        self.on_tipo_cliente_change(None)
        
        self.cliente_status.value = f"✏️ Editando: {cliente['nome']}"
        self.cliente_status.color = ft.Colors.BLUE
        self.page.update()
    
    def buscar_clientes(self):
        """Busca clientes pelo termo"""
        termo = self.cliente_search.value or ""
        clientes = self.db.buscar_clientes(termo)
        self.clientes_table.rows.clear()

        for c in clientes:
            self.clientes_table.rows.append(
                self._render_linha_cliente(c, reload_callback=self.buscar_clientes)
            )

        self.page.update()
