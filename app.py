"""
FastTech Control - Aplicação Principal
Sistema de Gestão de Equipamentos com interface moderna Flet
"""

import flet as ft
from database import Database
from datetime import datetime
import calendar


class FastTechApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database()
        self.lembretes = {}
        
        # Configurações da página
        self.page.title = "FastTech Control - Sistema de Gestão"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.window_width = 1400
        self.page.window_height = 800
        
        # Criar interface
        self.criar_interface()
    
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
        
        # Barra de navegação
        nav_bar = ft.Container(
            content=ft.Row(
                [
                    ft.FilledButton("🏠 Dashboard", on_click=ir_para_dashboard),
                    ft.FilledButton("👥 Clientes", on_click=ir_para_clientes),
                    ft.FilledButton("📦 Equipamentos", on_click=ir_para_equipamentos),
                    ft.FilledButton("🔄 Movimentações", on_click=ir_para_movimentacoes),
                    ft.FilledButton("🔍 Consultas", on_click=ir_para_consultas),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
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
        # Atualizar dados
        stats = self.db.get_estatisticas()
        
        # Saudação
        now = datetime.now()
        hour = now.hour
        if hour < 12:
            greeting = "Bom dia - Seja Bem vindo(a)"
        elif hour < 18:
            greeting = "Boa tarde - Seja Bem vindo(a)"
        else:
            greeting = "Boa noite - Seja Bem vindo(a)"
        
        # Header do dashboard
        dashboard_header = ft.Container(
            content=ft.Row(
                [
                    ft.Text(greeting, size=18, color=ft.Colors.GREY_500),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("📅", size=20),
                                        ft.Text(now.strftime("%d/%m/%Y"), size=12, weight=ft.FontWeight.BOLD),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5,
                                ),
                                bgcolor=ft.Colors.BLUE_900,
                                padding=15,
                                border_radius=10,
                                on_click=lambda e: self.abrir_calendario(),
                                tooltip="Clique para abrir calendário",
                            ),
                            ft.Container(width=20),
                            ft.Column(
                                [
                                    ft.Text(now.strftime("%H:%M"), size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN),
                                    ft.Text("AM" if now.hour < 12 else "PM", size=14, color=ft.Colors.CYAN),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.Padding(left=40, right=40, top=30, bottom=20),
        )
        
        # Cards do dashboard
        em_estoque = stats['por_status'].get('Em Estoque', 0)
        com_cliente = stats['por_status'].get('Com o Cliente', 0)
        em_manutencao = stats['por_status'].get('Em Manutenção', 0)
        
        cards_row1 = ft.Row(
            [
                self.criar_card("EQUIPAMENTOS", "CADASTRADOS", str(stats['total_equipamentos']), "📦", ft.Colors.BLUE),
                self.criar_card("MOVIMENTAÇÕES", "ESTE MÊS", str(self.contar_movimentacoes_mes()), "🔄", ft.Colors.AMBER),
                self.criar_card("EM MANUTENÇÃO", "EQUIPAMENTOS", str(em_manutencao), "🔧", ft.Colors.ORANGE),
                self.criar_card("SISTEMA", "STATUS", "OK", "✅", ft.Colors.GREEN),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=20,
        )
        
        cards_row2 = ft.Row(
            [
                self.criar_card("CLIENTES", "CADASTRADOS", str(stats['total_clientes']), "👥", ft.Colors.GREEN_700),
                self.criar_card("EM ESTOQUE", "DISPONÍVEIS", str(em_estoque), "📊", ft.Colors.BROWN),
                self.criar_card("COM CLIENTES", "EM USO", str(com_cliente), "📤", ft.Colors.INDIGO),
                self.criar_card("BANCO DE DADOS", self.get_db_size(), "💾", "💾", ft.Colors.AMBER_900),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=20,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    dashboard_header,
                    ft.Container(height=20),
                    cards_row1,
                    ft.Container(height=20),
                    cards_row2,
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding(left=40, right=40, bottom=30),
            expand=True,
        )
    
    def criar_card(self, title_line1, title_line2, value, icon, color):
        """Cria um card do dashboard"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title_line1, size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(title_line2, size=9, color=ft.Colors.GREY_400),
                    ft.Container(height=15),
                    ft.Row(
                        [
                            ft.Text(icon, size=32),
                            ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=5,
            ),
            width=280,
            height=150,
            padding=20,
            bgcolor=color + "20",
            border_radius=15,
            border=ft.Border(
                left=ft.BorderSide(2, color + "40"),
                right=ft.BorderSide(2, color + "40"),
                top=ft.BorderSide(2, color + "40"),
                bottom=ft.BorderSide(2, color + "40"),
            ),
        )
    
    def criar_clientes(self):
        """Cria a aba de clientes"""
        # Estado
        self.cliente_selecionado = None
        
        # Campos do formulário
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
        
        # Status message
        self.cliente_status = ft.Text("", size=14)
        
        # Tabela de clientes
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
        
        # Busca
        self.cliente_search = ft.TextField(
            label="Buscar cliente",
            hint_text="Nome, telefone ou documento...",
            width=400,
            on_submit=lambda e: self.buscar_clientes(),
        )
        
        # Botões
        def salvar_cliente(e):
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
        
        def limpar_form(e):
            self.limpar_form_cliente()
            self.page.update()
        
        # Layout
        formulario = ft.Container(
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
                            ft.FilledButton("💾 Salvar", on_click=salvar_cliente),
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
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=10,
        )
        
        lista = ft.Container(
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
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=10,
        )
        
        # Carregar clientes inicialmente
        self.carregar_clientes()
        
        return ft.Container(
            content=ft.Row(
                [
                    formulario,
                    ft.Container(width=20),
                    lista,
                ],
                expand=True,
            ),
            padding=20,
            expand=True,
        )
    
    def limpar_form_cliente(self):
        """Limpa o formulário de cliente"""
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
                                    ft.IconButton(icon=ft.icons.EDIT_OUTLINED, on_click=editar_cliente, tooltip="Editar"),
                                    ft.IconButton(icon=ft.icons.DELETE_OUTLINED, on_click=excluir_cliente, tooltip="Excluir", icon_color=ft.Colors.RED),
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
                                    ft.IconButton(icon=ft.icons.EDIT_OUTLINED, on_click=editar_cliente, tooltip="Editar"),
                                    ft.IconButton(icon=ft.icons.DELETE_OUTLINED, on_click=excluir_cliente, tooltip="Excluir", icon_color=ft.Colors.RED),
                                ],
                                spacing=5,
                            )
                        ),
                    ],
                )
            )
        
        self.page.update()
    
    def criar_equipamentos(self):
        """Cria a aba de equipamentos"""
        return ft.Container(
            content=ft.Text("Aba de Equipamentos - Em desenvolvimento", size=20),
            padding=40,
            alignment=ft.Alignment(0, 0),
        )
    
    def criar_movimentacoes(self):
        """Cria a aba de movimentações"""
        return ft.Container(
            content=ft.Text("Aba de Movimentações - Em desenvolvimento", size=20),
            padding=40,
            alignment=ft.Alignment(0, 0),
        )
    
    def criar_consultas(self):
        """Cria a aba de consultas"""
        return ft.Container(
            content=ft.Text("Aba de Consultas - Em desenvolvimento", size=20),
            padding=40,
            alignment=ft.Alignment(0, 0),
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
