"""
Aba Consultas - Consultas e relatórios
"""
import flet as ft
from gui.base import BaseTab
from datetime import datetime


class ConsultasTab(BaseTab):
    """Aba de consultas e relatórios"""
    
    def __init__(self, page, db, config):
        super().__init__(page, db, config)
        self.consulta_view = "equipamento"
        self._init_campos()

    def _init_campos(self):
        """Inicializa campos de busca para reutilização entre navegações"""
        self.equip_search_field = ft.TextField(
            label="Número de Série",
            hint_text="Digite o número de série...",
            expand=True,
            on_submit=lambda e: self.buscar_equipamento_consulta(),
        )
        self.equip_result_container = ft.Container(
            content=ft.Text(
                "Digite um número de série e clique em Buscar",
                size=14,
                color=ft.Colors.GREY_400,
            ),
            expand=True,
        )
        self.cliente_search_field = ft.TextField(
            label="Buscar Cliente",
            hint_text="Digite nome, telefone ou documento...",
            expand=True,
            on_submit=lambda e: self.buscar_cliente_consulta(),
        )
        self.cliente_result_container = ft.Container(
            content=ft.Text(
                "Digite nome, telefone ou documento e clique em Buscar",
                size=14,
                color=ft.Colors.GREY_400,
            ),
            expand=True,
        )
    
    def build(self):
        """Constrói a interface de consultas"""
        # Container para conteúdo dinâmico
        self.consulta_content_container = ft.Container(expand=True)
        
        # Sub-navegação
        subnav = ft.Container(
            content=ft.Row(
                [
                    ft.FilledButton("📦 Por Equipamento", on_click=self.ir_para_equipamento, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                    ft.FilledButton("👤 Por Cliente", on_click=self.ir_para_cliente, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                    ft.FilledButton("📊 Relatórios", on_click=self.ir_para_relatorios, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                ],
                spacing=10,
            ),
            padding=15,
            bgcolor=self.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
        )
        
        # Inicializar com primeira view
        self.consulta_content_container.content = self._montar_view_equipamento()
        
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
    
    def ir_para_equipamento(self, e):
        """Navega para busca por equipamento"""
        self.consulta_view = "equipamento"
        self.consulta_content_container.content = self._montar_view_equipamento()
        self.page.update()
    
    def ir_para_cliente(self, e):
        """Navega para busca por cliente"""
        self.consulta_view = "cliente"
        self.consulta_content_container.content = self._montar_view_cliente()
        self.page.update()
    
    def ir_para_relatorios(self, e):
        """Navega para relatórios"""
        self.consulta_view = "relatorios"
        self.consulta_content_container.content = self.criar_consulta_relatorios()
        self.page.update()
    
    def _montar_view_equipamento(self):
        """Monta o layout de busca por equipamento reutilizando campos existentes"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Buscar Equipamento por Número de Série", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.equip_search_field,
                            ft.FilledButton("🔍 Buscar", on_click=lambda e: self.buscar_equipamento_consulta(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
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

    def criar_consulta_equipamento(self):
        """Cria a view de busca por equipamento (mantido para compatibilidade)"""
        return self._montar_view_equipamento()
    
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
        result_content = [info_card]
        
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
    
    def _montar_view_cliente(self):
        """Monta o layout de busca por cliente reutilizando campos existentes"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Buscar Cliente e seus Equipamentos", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.cliente_search_field,
                            ft.FilledButton("🔍 Buscar", on_click=lambda e: self.buscar_cliente_consulta(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
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

    def criar_consulta_cliente(self):
        """Cria a view de busca por cliente (mantido para compatibilidade)"""
        return self._montar_view_cliente()
    
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
                            ft.FilledButton("📄 Exportar Clientes (CSV)", on_click=lambda e: self.exportar_clientes_csv(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                            ft.FilledButton("📄 Exportar Equipamentos (CSV)", on_click=lambda e: self.exportar_equipamentos_csv(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                            ft.FilledButton("📄 Exportar Histórico (CSV)", on_click=lambda e: self.exportar_historico_csv(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                        ],
                        spacing=10,
                    ),
                    self.relatorio_status,
                    ft.FilledButton("🔄 Atualizar Estatísticas", on_click=lambda e: self.atualizar_estatisticas_consulta(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
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
