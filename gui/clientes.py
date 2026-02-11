"""
Aba Clientes - Gestão de clientes
"""
import flet as ft
from gui.base import BaseTab


class ClientesTab(BaseTab):
    """Aba de gestão de clientes"""
    
    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        self.cliente_selecionado = None
        
        # Campos do formulário
        self.nome_field = None
        self.telefone_field = None
        self.email_field = None
        self.documento_field = None
        self.setor_field = None
        self.endereco_field = None
        self.cliente_status = None
        self.clientes_table = None
        self.cliente_search = None
    
    def build(self):
        """Constrói a interface de clientes"""
        # Criar campos
        self.criar_campos()
        
        # Criar tabela
        self.criar_tabela()
        
        # Layout
        formulario = self.criar_formulario()
        lista = self.criar_lista()
        
        # Carregar clientes inicialmente
        self.carregar_clientes()
        
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
        self.nome_field = ft.TextField(
            label="Nome Completo *",
            hint_text="Digite o nome do cliente",
            width=400,
        )
        
        self.telefone_field = ft.TextField(
            label="Telefone *",
            hint_text="(11) 98765-4321",
            width=400,
        )
        
        self.email_field = ft.TextField(
            label="Email",
            hint_text="cliente@email.com",
            width=400,
        )
        
        self.documento_field = ft.TextField(
            label="CPF/CNPJ",
            hint_text="000.000.000-00",
            width=400,
        )
        
        self.setor_field = ft.TextField(
            label="Setor/Departamento",
            hint_text="Ex: TI, RH, Vendas",
            width=400,
        )
        
        self.endereco_field = ft.TextField(
            label="Endereço",
            hint_text="Rua, número, bairro, cidade",
            width=400,
            multiline=True,
            min_lines=2,
            max_lines=3,
        )
        
        self.cliente_status = ft.Text("", size=14)
        
        self.cliente_search = ft.TextField(
            label="Buscar cliente",
            hint_text="Nome, telefone ou documento...",
            width=400,
            on_submit=lambda e: self.buscar_clientes(),
        )
    
    def criar_tabela(self):
        """Cria a tabela de clientes"""
        self.clientes_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Telefone", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Setor", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
        )
    
    def criar_formulario(self):
        """Cria o formulário de cadastro"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Cadastro de Cliente", size=18, weight=ft.FontWeight.BOLD),
                    self.nome_field,
                    self.telefone_field,
                    self.email_field,
                    self.documento_field,
                    self.setor_field,
                    self.endereco_field,
                    self.cliente_status,
                    ft.Row(
                        [
                            ft.FilledButton("💾 Salvar", on_click=self.salvar_cliente),
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
        """Cria a lista de clientes"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Clientes Cadastrados", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.cliente_search,
                            ft.FilledButton("🔍 Buscar", on_click=lambda e: self.buscar_clientes()),
                            ft.FilledButton("🔄 Todos", on_click=lambda e: self.carregar_clientes()),
                        ],
                        spacing=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [self.clientes_table],
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
    
    def salvar_cliente(self, e):
        """Salva ou atualiza um cliente"""
        nome = self.nome_field.value
        telefone = self.telefone_field.value
        
        if not nome or not telefone:
            self.cliente_status.value = "❌ Nome e telefone são obrigatórios"
            self.cliente_status.color = ft.Colors.RED
            self.page.update()
            return
        
        try:
            if self.cliente_selecionado:
                self.db.atualizar_cliente(
                    self.cliente_selecionado['id'],
                    nome=nome,
                    telefone=telefone,
                    email=self.email_field.value or None,
                    documento=self.documento_field.value or None,
                    setor=self.setor_field.value or None,
                    endereco=self.endereco_field.value or None,
                )
                self.cliente_status.value = f"✅ Cliente '{nome}' atualizado!"
            else:
                self.db.inserir_cliente(
                    nome,
                    telefone,
                    self.email_field.value or None,
                    self.endereco_field.value or None,
                    self.documento_field.value or None,
                    self.setor_field.value or None,
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
        self.cliente_selecionado = None
        self.cliente_status.value = ""
    
    def carregar_clientes(self):
        """Carrega todos os clientes na tabela"""
        clientes = self.db.buscar_clientes()
        self.clientes_table.rows.clear()
        
        for c in clientes:
            def editar_cliente(e, cliente=c):
                self.cliente_selecionado = cliente
                self.nome_field.value = cliente['nome']
                self.telefone_field.value = cliente['telefone']
                self.email_field.value = cliente['email'] or ""
                self.documento_field.value = cliente['documento'] or ""
                self.setor_field.value = cliente['setor'] or ""
                self.endereco_field.value = cliente['endereco'] or ""
                self.cliente_status.value = f"✏️ Editando: {cliente['nome']}"
                self.cliente_status.color = ft.Colors.BLUE
                self.page.update()
            
            def excluir_cliente(e, cliente=c):
                if self.db.deletar_cliente(cliente['id']):
                    self.cliente_status.value = f"✅ Cliente '{cliente['nome']}' excluído!"
                    self.cliente_status.color = ft.Colors.GREEN
                else:
                    self.cliente_status.value = "❌ Cliente possui equipamentos vinculados"
                    self.cliente_status.color = ft.Colors.RED
                self.carregar_clientes()
                self.page.update()
            
            self.clientes_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c['id']))),
                        ft.DataCell(ft.Text(c['nome'])),
                        ft.DataCell(ft.Text(c['telefone'])),
                        ft.DataCell(ft.Text(c['setor'] or '-')),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton("✏️", on_click=editar_cliente, tooltip="Editar"),
                                    ft.TextButton("🗑️", on_click=excluir_cliente, tooltip="Excluir"),
                                ],
                                spacing=5,
                            )
                        ),
                    ],
                )
            )
        
        if hasattr(self, 'page'):
            self.page.update()
    
    def buscar_clientes(self):
        """Busca clientes pelo termo"""
        termo = self.cliente_search.value or ""
        clientes = self.db.buscar_clientes(termo)
        self.clientes_table.rows.clear()
        
        for c in clientes:
            def editar_cliente(e, cliente=c):
                self.cliente_selecionado = cliente
                self.nome_field.value = cliente['nome']
                self.telefone_field.value = cliente['telefone']
                self.email_field.value = cliente['email'] or ""
                self.documento_field.value = cliente['documento'] or ""
                self.setor_field.value = cliente['setor'] or ""
                self.endereco_field.value = cliente['endereco'] or ""
                self.cliente_status.value = f"✏️ Editando: {cliente['nome']}"
                self.cliente_status.color = ft.Colors.BLUE
                self.page.update()
            
            def excluir_cliente(e, cliente=c):
                if self.db.deletar_cliente(cliente['id']):
                    self.cliente_status.value = f"✅ Cliente '{cliente['nome']}' excluído!"
                    self.cliente_status.color = ft.Colors.GREEN
                else:
                    self.cliente_status.value = "❌ Cliente possui equipamentos vinculados"
                    self.cliente_status.color = ft.Colors.RED
                self.buscar_clientes()
                self.page.update()
            
            self.clientes_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c['id']))),
                        ft.DataCell(ft.Text(c['nome'])),
                        ft.DataCell(ft.Text(c['telefone'])),
                        ft.DataCell(ft.Text(c['setor'] or '-')),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton("✏️", on_click=editar_cliente, tooltip="Editar"),
                                    ft.TextButton("🗑️", on_click=excluir_cliente, tooltip="Excluir"),
                                ],
                                spacing=5,
                            )
                        ),
                    ],
                )
            )
        
        self.page.update()
