"""
Formulário de consultas avançadas e relatórios - Versão Flet
"""

import flet as ft
from datetime import datetime
import csv
import os
from gui.styles import get_colors, get_fonts, PADDING
from database import Database


class ConsultaForm(ft.UserControl):
    """Formulário de consultas avançadas"""
    
    def __init__(self, page: ft.Page, db: Database):
        super().__init__()
        self.page = page
        self.db = db
        
        self._criar_interface()

    def _criar_interface(self):
        """Cria a interface do formulário"""
        
        # Título
        self.title = ft.Text(
            "🔍 Consultas e Relatórios",
            size=get_fonts()['title']['size'],
            weight=get_fonts()['title']['weight'],
            color=get_colors()['text']
        )

        # Abas de consulta
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="📦 Por Equipamento",
                    content=self._criar_aba_equipamento()
                ),
                ft.Tab(
                    text="👤 Por Cliente",
                    content=self._criar_aba_cliente()
                ),
                ft.Tab(
                    text="📊 Relatórios",
                    content=self._criar_aba_relatorios()
                )
            ]
        )

        self.controls = [self.title, self.tabs]

    def _criar_aba_equipamento(self):
        """Cria aba de busca por equipamento"""
        
        # Campo de busca
        self.equip_search = ft.TextField(
            hint_text="Digite o número de série...",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_submit=self._buscar_equipamento
        )
        
        # Botão de busca
        self.btn_buscar_equip = ft.ElevatedButton(
            "🔍 Buscar",
            icon=ft.icons.SEARCH,
            on_click=self._buscar_equipamento,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.BLUE}
            )
        )

        # Resultado
        self.equip_result = ft.Column([], expand=True)

        # Layout da aba
        layout = ft.Column([
            ft.Text("Buscar Equipamento por Número de Série", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([self.equip_search, self.btn_buscar_equip]),
            ft.Divider(height=20),
            self.equip_result
        ], expand=True)

        return layout

    def _criar_aba_cliente(self):
        """Cria aba de busca por cliente"""
        
        # Campo de busca
        self.cliente_search = ft.TextField(
            hint_text="Digite nome, telefone ou documento...",
            border=ft.InputBorder.OUTLINE,
            filled=True,
            dense=True,
            on_submit=self._buscar_cliente
        )
        
        # Botão de busca
        self.btn_buscar_cliente = ft.ElevatedButton(
            "🔍 Buscar",
            icon=ft.icons.SEARCH,
            on_click=self._buscar_cliente,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.BLUE}
            )
        )

        # Resultado
        self.cliente_result = ft.Column([], expand=True)

        # Layout da aba
        layout = ft.Column([
            ft.Text("Buscar Cliente e seus Equipamentos", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([self.cliente_search, self.btn_buscar_cliente]),
            ft.Divider(height=20),
            self.cliente_result
        ], expand=True)

        return layout

    def _criar_aba_relatorios(self):
        """Cria aba de relatórios"""
        
        # Estatísticas gerais
        self.stats_label = ft.Text("Carregando estatísticas...", size=14)
        self._atualizar_estatisticas()

        # Botões de exportação
        export_buttons = ft.Row([
            ft.ElevatedButton(
                "📄 Exportar Clientes (CSV)",
                icon=ft.icons.FILE_DOWNLOAD,
                on_click=self._exportar_clientes,
                style=ft.ButtonStyle(
                    color={"": ft.colors.WHITE},
                    bgcolor={"": ft.colors.GREEN}
                )
            ),
            ft.ElevatedButton(
                "📄 Exportar Equipamentos (CSV)",
                icon=ft.icons.FILE_DOWNLOAD,
                on_click=self._exportar_equipamentos,
                style=ft.ButtonStyle(
                    color={"": ft.colors.WHITE},
                    bgcolor={"": ft.colors.GREEN}
                )
            ),
            ft.ElevatedButton(
                "📄 Exportar Histórico (CSV)",
                icon=ft.icons.FILE_DOWNLOAD,
                on_click=self._exportar_historico,
                style=ft.ButtonStyle(
                    color={"": ft.colors.WHITE},
                    bgcolor={"": ft.colors.GREEN}
                )
            )
        ])

        # Botão de atualização
        atualizar_btn = ft.ElevatedButton(
            "🔄 Atualizar Estatísticas",
            icon=ft.icons.REFRESH,
            on_click=self._atualizar_estatisticas,
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK87},
                bgcolor={"": ft.colors.GREY}
            )
        )

        # Status
        self.relatorio_status = ft.Text("", size=12)

        # Layout da aba
        layout = ft.Column([
            ft.Text("Relatórios e Estatísticas", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20),
            ft.Container(
                content=self.stats_label,
                padding=15,
                border=ft.border.all(1, ft.colors.GREY_300),
                bgcolor=ft.colors.GREY_100
            ),
            ft.Divider(height=20),
            ft.Text("Exportar Dados", size=16, weight=ft.FontWeight.BOLD),
            export_buttons,
            self.relatorio_status,
            ft.Divider(height=20),
            atualizar_btn
        ], expand=True)

        return layout

    def _buscar_equipamento(self, e):
        """Busca equipamento por número de série"""
        termo = self.equip_search.value.strip()
        
        if not termo:
            self.equip_result.controls = [
                ft.Text("Digite um número de série para buscar", color=ft.colors.GREY)
            ]
            self.update()
            return

        # Busca equipamento
        equip = self.db.buscar_equipamento_por_serie(termo)
        
        if not equip:
            self.equip_result.controls = [
                ft.Text(f"❌ Equipamento '{termo}' não encontrado", color=ft.colors.RED)
            ]
            self.update()
            return

        # Informações do equipamento
        info_text = f"""
📦 EQUIPAMENTO ENCONTRADO

Número de Série: {equip['numero_serie']}
Tipo: {equip['tipo']}
Marca: {equip['marca'] or '-'}
Modelo: {equip['modelo'] or '-'}
Status Atual: {equip['status_atual']}
Data de Registro: {equip['data_registro']}
Valor Estimado: R$ {equip['valor_estimado'] or '0.00'}
Data Garantia: {equip['data_garantia'] or '-'}
        """.strip()

        info_card = ft.Container(
            content=ft.Text(info_text, selectable=True),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            bgcolor=ft.colors.GREY_100
        )

        # Cliente atual
        hist_ativo = self.db.buscar_historico_ativo_equipamento(equip['id'])
        cliente_card = None
        if hist_ativo and hist_ativo['cliente_nome']:
            cliente_card = ft.Container(
                content=ft.Text(f"👤 Cliente Atual: {hist_ativo['cliente_nome']} - {hist_ativo['cliente_telefone']}", weight=ft.FontWeight.BOLD),
                padding=10,
                bgcolor=ft.colors.BLUE,
                border_radius=5
            )

        # Histórico completo
        historico = self.db.buscar_historico_equipamento(equip['id'])
        
        hist_table = ft.DataTable(
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
            hist_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(status)),
                ft.DataCell(ft.Text(h['data_inicio'])),
                ft.DataCell(ft.Text(h['data_fim'] or '-')),
                ft.DataCell(ft.Text(h['acao'])),
                ft.DataCell(ft.Text(h['cliente_nome'] or '-')),
                ft.DataCell(ft.Text(h['usuario_responsavel']))
            ]))

        hist_section = ft.Column([
            ft.Text("📜 Histórico Completo", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            ft.Column([hist_table], scroll=ft.ScrollMode.AUTO, height=300)
        ])

        # Monta resultado
        self.equip_result.controls = [info_card]
        if cliente_card:
            self.equip_result.controls.append(cliente_card)
        self.equip_result.controls.append(hist_section)

        self.update()

    def _buscar_cliente(self, e):
        """Busca cliente e seus equipamentos"""
        termo = self.cliente_search.value.strip()
        
        if not termo:
            self.cliente_result.controls = [
                ft.Text("Digite um termo para buscar", color=ft.colors.GREY)
            ]
            self.update()
            return

        # Busca clientes
        clientes = self.db.buscar_clientes(termo)
        
        if not clientes:
            self.cliente_result.controls = [
                ft.Text(f"❌ Nenhum cliente encontrado com '{termo}'", color=ft.colors.RED)
            ]
            self.update()
            return

        # Se encontrou múltiplos, mostra lista para seleção
        if len(clientes) > 1:
            self._mostrar_lista_clientes(clientes)
        else:
            self._mostrar_detalhes_cliente(clientes[0])

    def _mostrar_lista_clientes(self, clientes):
        """Mostra lista de clientes encontrados"""
        
        title = ft.Text(f"✓ {len(clientes)} clientes encontrados. Selecione um:", size=16, weight=ft.FontWeight.BOLD)
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Telefone")),
                ft.DataColumn(ft.Text("Setor"))
            ],
            rows=[]
        )

        for c in clientes:
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(c['id']))),
                ft.DataCell(ft.Text(c['nome'])),
                ft.DataCell(ft.Text(c['telefone'])),
                ft.DataCell(ft.Text(c['setor'] or '-'))
            ]))

        def ver_detalhes(e):
            # Obter índice selecionado
            selected_index = table.selected_index
            if selected_index is not None and 0 <= selected_index < len(table.rows):
                cliente_id = int(table.rows[selected_index].cells[0].content.value)
                cliente = self.db.buscar_cliente_por_id(cliente_id)
                self._mostrar_detalhes_cliente(cliente)

        btn_detalhes = ft.ElevatedButton(
            "👁️ Ver Detalhes do Cliente Selecionado",
            icon=ft.icons.VISIBILITY,
            on_click=ver_detalhes,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.BLUE}
            )
        )

        self.cliente_result.controls = [title, ft.Divider(height=10), table, btn_detalhes]
        self.update()

    def _mostrar_detalhes_cliente(self, cliente):
        """Mostra detalhes completos do cliente"""
        
        # Informações do cliente
        info_text = f"""
👤 CLIENTE ENCONTRADO

Nome: {cliente['nome']}
Telefone: {cliente['telefone']}
Email: {cliente['email'] or '-'}
Documento: {cliente['documento'] or '-'}
Setor: {cliente['setor'] or '-'}
Endereço: {cliente['endereco'] or '-'}
Data de Cadastro: {cliente['data_cadastro']}
        """.strip()

        info_card = ft.Container(
            content=ft.Text(info_text, selectable=True),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            bgcolor=ft.colors.GREY_100
        )

        # Equipamentos ativos
        equipamentos_ativos = self.db.buscar_equipamentos_cliente_ativo(cliente['id'])
        
        ativos_section = None
        if equipamentos_ativos:
            ativos_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Série")),
                    ft.DataColumn(ft.Text("Tipo")),
                    ft.DataColumn(ft.Text("Marca")),
                    ft.DataColumn(ft.Text("Modelo")),
                    ft.DataColumn(ft.Text("Desde"))
                ],
                rows=[]
            )

            for e in equipamentos_ativos:
                ativos_table.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(e['numero_serie'])),
                    ft.DataCell(ft.Text(e['tipo'])),
                    ft.DataCell(ft.Text(e['marca'] or '-')),
                    ft.DataCell(ft.Text(e['modelo'] or '-')),
                    ft.DataCell(ft.Text(e['data_inicio'][:16]))
                ]))

            ativos_section = ft.Column([
                ft.Text(f"📦 Equipamentos Ativos ({len(equipamentos_ativos)})", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                ft.Divider(height=10),
                ft.Column([ativos_table], scroll=ft.ScrollMode.AUTO, height=200)
            ])

        # Histórico completo
        historico = self.db.buscar_historico_cliente(cliente['id'])
        
        hist_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Equipamento")),
                ft.DataColumn(ft.Text("Ação")),
                ft.DataColumn(ft.Text("Data Início")),
                ft.DataColumn(ft.Text("Data Fim"))
            ],
            rows=[]
        )

        for h in historico:
            status = "🟢" if h['data_fim'] is None else "⚪"
            hist_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(status)),
                ft.DataCell(ft.Text(f"{h['equipamento_tipo']} ({h['equipamento_numero_serie']})")),
                ft.DataCell(ft.Text(h['acao'])),
                ft.DataCell(ft.Text(h['data_inicio'])),
                ft.DataCell(ft.Text(h['data_fim'] or '-'))
            ]))

        hist_section = ft.Column([
            ft.Text("📜 Histórico Completo de Equipamentos", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            ft.Column([hist_table], scroll=ft.ScrollMode.AUTO, height=300)
        ])

        # Monta resultado
        self.cliente_result.controls = [info_card]
        if ativos_section:
            self.cliente_result.controls.append(ativos_section)
        self.cliente_result.controls.append(hist_section)

        self.update()

    def _atualizar_estatisticas(self, e=None):
        """Atualiza as estatísticas exibidas"""
        stats = self.db.get_estatisticas()
        
        stats_text = f"""
📊 ESTATÍSTICAS GERAIS

Total de Clientes: {stats['total_clientes']}
Total de Equipamentos: {stats['total_equipamentos']}

Equipamentos por Status:
"""
        for status, total in stats['por_status'].items():
            stats_text += f"  • {status}: {total}\n"

        self.stats_label.value = stats_text.strip()
        self.update()

    def _exportar_clientes(self, e):
        """Exporta clientes para CSV"""
        try:
            clientes = self.db.buscar_clientes()
            
            filename = f"clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'nome', 'telefone', 'email', 'endereco', 'documento', 'setor', 'data_cadastro']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for c in clientes:
                    writer.writerow({
                        'id': c['id'],
                        'nome': c['nome'],
                        'telefone': c['telefone'],
                        'email': c['email'],
                        'endereco': c['endereco'],
                        'documento': c['documento'],
                        'setor': c['setor'],
                        'data_cadastro': c['data_cadastro']
                    })
            
            self._show_status(f"Clientes exportados para {filename}", "success")
        except Exception as ex:
            self._show_status(f"Erro ao exportar clientes: {str(ex)}", "error")

    def _exportar_equipamentos(self, e):
        """Exporta equipamentos para CSV"""
        try:
            equipamentos = self.db.buscar_equipamentos()
            
            filename = f"equipamentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'numero_serie', 'tipo', 'marca', 'modelo', 'status_atual',
                    'data_registro', 'data_garantia', 'valor_estimado', 'observacoes',
                    'cliente_atual_id', 'cliente_atual_nome'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for e in equipamentos:
                    writer.writerow({
                        'id': e['id'],
                        'numero_serie': e['numero_serie'],
                        'tipo': e['tipo'],
                        'marca': e['marca'],
                        'modelo': e['modelo'],
                        'status_atual': e['status_atual'],
                        'data_registro': e['data_registro'],
                        'data_garantia': e['data_garantia'],
                        'valor_estimado': e['valor_estimado'],
                        'observacoes': e['observacoes'],
                        'cliente_atual_id': e['cliente_atual_id'],
                        'cliente_atual_nome': e['cliente_atual_nome']
                    })
            
            self._show_status(f"Equipamentos exportados para {filename}", "success")
        except Exception as ex:
            self._show_status(f"Erro ao exportar equipamentos: {str(ex)}", "error")

    def _exportar_historico(self, e):
        """Exporta histórico para CSV"""
        try:
            historico = self.db.buscar_historico_completo()
            
            filename = f"historico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'equipamento_id', 'equipamento_tipo', 'equipamento_numero_serie',
                    'acao', 'data_inicio', 'data_fim', 'usuario_responsavel',
                    'cliente_id', 'cliente_nome', 'observacoes'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for h in historico:
                    writer.writerow({
                        'id': h['id'],
                        'equipamento_id': h['equipamento_id'],
                        'equipamento_tipo': h['equipamento_tipo'],
                        'equipamento_numero_serie': h['equipamento_numero_serie'],
                        'acao': h['acao'],
                        'data_inicio': h['data_inicio'],
                        'data_fim': h['data_fim'],
                        'usuario_responsavel': h['usuario_responsavel'],
                        'cliente_id': h['cliente_id'],
                        'cliente_nome': h['cliente_nome'],
                        'observacoes': h['observacoes']
                    })
            
            self._show_status(f"Histórico exportado para {filename}", "success")
        except Exception as ex:
            self._show_status(f"Erro ao exportar histórico: {str(ex)}", "error")

    def _show_status(self, message, level="info"):
        """Mostra mensagem de status"""
        # Atualiza o status na aba de relatórios
        colors = get_colors()
        if level == "error":
            self.relatorio_status.color = colors['danger']
            self.relatorio_status.weight = ft.FontWeight.BOLD
        elif level == "success":
            self.relatorio_status.color = colors['success']
        elif level == "warning":
            self.relatorio_status.color = colors['warning']
        else:
            self.relatorio_status.color = colors['text']
            self.relatorio_status.weight = ft.FontWeight.NORMAL

        self.relatorio_status.value = message
        self.update()