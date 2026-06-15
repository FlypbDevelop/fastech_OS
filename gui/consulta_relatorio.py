"""
Relatórios e Exportação - Estatísticas e exportação CSV
"""
import csv
import flet as ft
from datetime import datetime


class RelatorioView:
    """View de relatórios, estatísticas e exportação"""

    def __init__(self, orc, page, db, config):
        self.orc = orc
        self.page = page
        self.db = db
        self.config = config

    def montar_view(self):
        """Monta a view de relatórios"""
        self.stats_text = ft.Text("Carregando estatísticas...", size=14)

        stats_card = ft.Container(
            content=self.stats_text,
            bgcolor=self.orc.get_adaptive_color(ft.Colors.BLUE_GREY_800, ft.Colors.GREY_200),
            padding=20,
            border_radius=10,
        )

        self.relatorio_status = ft.Text("", size=14)

        self.atualizar_estatisticas()

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
                    ft.FilledButton("🔄 Atualizar Estatísticas", on_click=lambda e: self.atualizar_estatisticas(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
        )

    def atualizar_estatisticas(self):
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

        self.db.cursor.execute("SELECT COUNT(*) FROM historico_posse")
        total_movimentacoes = self.db.cursor.fetchone()[0]

        self.db.cursor.execute("SELECT COUNT(*) FROM historico_posse WHERE data_fim IS NULL")
        movimentacoes_ativas = self.db.cursor.fetchone()[0]

        texto += f"\nTotal de Movimentações: {total_movimentacoes}\n"
        texto += f"Movimentações Ativas: {movimentacoes_ativas}\n"

        if hasattr(self, 'stats_text'):
            self.stats_text.value = texto.strip()
            if hasattr(self, 'page'):
                self.page.update()

    def exportar_clientes_csv(self):
        """Exporta clientes para CSV"""
        try:
            clientes = self.db.buscar_clientes()
            filename = f"clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Nome', 'Telefone', 'Email', 'Documento', 'Setor', 'Endereço', 'Data Cadastro'])
                for c in clientes:
                    writer.writerow([
                        c['id'], c['nome'], c['telefone'],
                        c['email'] or '', c['documento'] or '',
                        c['setor'] or '', c['endereco'] or '',
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
        try:
            equipamentos = self.db.buscar_equipamentos()
            filename = f"equipamentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Número Série', 'Tipo', 'Marca', 'Modelo', 'Status', 'Data Registro', 'Valor', 'Garantia'])
                for e in equipamentos:
                    writer.writerow([
                        e['id'], e['numero_serie'], e['tipo'],
                        e['marca'] or '', e['modelo'] or '',
                        e['status_atual'], e['data_registro'],
                        e['valor_estimado'] or '', e['data_garantia'] or ''
                    ])

            self.relatorio_status.value = f"✅ {len(equipamentos)} equipamentos exportados para {filename}"
            self.relatorio_status.color = ft.Colors.GREEN
        except Exception as e:
            self.relatorio_status.value = f"❌ Erro ao exportar: {str(e)}"
            self.relatorio_status.color = ft.Colors.RED
        self.page.update()

    def exportar_historico_csv(self):
        """Exporta histórico completo para CSV"""
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
                        h['id'], h['numero_serie'], h['tipo'],
                        h['marca'] or '', h['modelo'] or '',
                        h['cliente_nome'] or '', h['cliente_telefone'] or '',
                        h['acao'], h['data_inicio'], h['data_fim'] or '',
                        h['usuario_responsavel'], h['observacoes'] or ''
                    ])

            self.relatorio_status.value = f"✅ {len(historico)} registros exportados para {filename}"
            self.relatorio_status.color = ft.Colors.GREEN
        except Exception as e:
            self.relatorio_status.value = f"❌ Erro ao exportar: {str(e)}"
            self.relatorio_status.color = ft.Colors.RED
        self.page.update()
