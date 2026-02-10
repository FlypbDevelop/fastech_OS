"""
Formulário de consultas avançadas e relatórios
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
import csv
from gui.styles import COLORS, FONTS, PADDING
from gui.widgets import CustomButton, StatusLabel, DataTable, SearchBar
from database import Database


class ConsultaForm(tk.Frame):
    """Formulário de consultas avançadas"""
    
    def __init__(self, parent, db: Database):
        super().__init__(parent, bg=COLORS['white'])
        self.db = db
        
        self.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        self._criar_interface()
    
    def _criar_interface(self):
        """Cria a interface do formulário"""
        
        # Título
        title = tk.Label(
            self,
            text="🔍 Consultas e Relatórios",
            font=FONTS['title'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, PADDING['large']))
        
        # Notebook com abas de consulta
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        
        # Aba 1: Busca por Equipamento
        self._criar_aba_equipamento()
        
        # Aba 2: Busca por Cliente
        self._criar_aba_cliente()
        
        # Aba 3: Relatórios
        self._criar_aba_relatorios()
    
    def _criar_aba_equipamento(self):
        """Cria aba de busca por equipamento"""
        frame = tk.Frame(self.notebook, bg=COLORS['white'])
        self.notebook.add(frame, text='📦 Por Equipamento')
        
        # Padding
        content = tk.Frame(frame, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título
        tk.Label(
            content,
            text="Buscar Equipamento por Número de Série",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Busca
        search_frame = tk.Frame(content, bg=COLORS['white'])
        search_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        self.equip_search = SearchBar(
            search_frame,
            placeholder="Digite o número de série...",
            on_search=self._buscar_equipamento
        )
        self.equip_search.pack(fill='x')
        
        # Resultado
        self.equip_result_frame = tk.Frame(content, bg=COLORS['white'])
        self.equip_result_frame.pack(fill='both', expand=True)
        
        # Mensagem inicial
        tk.Label(
            self.equip_result_frame,
            text="Digite um número de série e clique em Buscar",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['text_light']
        ).pack(expand=True)
    
    def _criar_aba_cliente(self):
        """Cria aba de busca por cliente"""
        frame = tk.Frame(self.notebook, bg=COLORS['white'])
        self.notebook.add(frame, text='👤 Por Cliente')
        
        # Padding
        content = tk.Frame(frame, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título
        tk.Label(
            content,
            text="Buscar Cliente e seus Equipamentos",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Busca
        search_frame = tk.Frame(content, bg=COLORS['white'])
        search_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        self.cliente_search = SearchBar(
            search_frame,
            placeholder="Digite nome, telefone ou documento...",
            on_search=self._buscar_cliente
        )
        self.cliente_search.pack(fill='x')
        
        # Resultado
        self.cliente_result_frame = tk.Frame(content, bg=COLORS['white'])
        self.cliente_result_frame.pack(fill='both', expand=True)
        
        # Mensagem inicial
        tk.Label(
            self.cliente_result_frame,
            text="Digite nome, telefone ou documento e clique em Buscar",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['text_light']
        ).pack(expand=True)
    
    def _criar_aba_relatorios(self):
        """Cria aba de relatórios"""
        frame = tk.Frame(self.notebook, bg=COLORS['white'])
        self.notebook.add(frame, text='📊 Relatórios')
        
        # Padding
        content = tk.Frame(frame, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título
        tk.Label(
            content,
            text="Relatórios e Estatísticas",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, PADDING['large']))
        
        # Estatísticas gerais
        stats_frame = tk.Frame(content, bg=COLORS['bg'], relief='solid', borderwidth=1)
        stats_frame.pack(fill='x', pady=(0, PADDING['large']))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Carregando estatísticas...",
            font=FONTS['normal'],
            bg=COLORS['bg'],
            fg=COLORS['text'],
            justify='left',
            padx=PADDING['large'],
            pady=PADDING['large']
        )
        self.stats_label.pack(fill='x')
        
        self._atualizar_estatisticas()
        
        # Botões de relatório
        tk.Label(
            content,
            text="Exportar Dados",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(PADDING['large'], PADDING['medium']))
        
        btn_frame = tk.Frame(content, bg=COLORS['white'])
        btn_frame.pack(fill='x')
        
        CustomButton(
            btn_frame,
            text="📄 Exportar Clientes (CSV)",
            command=self._exportar_clientes,
            style='primary'
        ).pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            btn_frame,
            text="📄 Exportar Equipamentos (CSV)",
            command=self._exportar_equipamentos,
            style='primary'
        ).pack(side='left', padx=PADDING['small'])
        
        CustomButton(
            btn_frame,
            text="📄 Exportar Histórico (CSV)",
            command=self._exportar_historico,
            style='primary'
        ).pack(side='left', padx=PADDING['small'])
        
        # Status
        self.relatorio_status = StatusLabel(content)
        self.relatorio_status.pack(pady=PADDING['large'])
        
        # Botão atualizar estatísticas
        CustomButton(
            content,
            text="🔄 Atualizar Estatísticas",
            command=self._atualizar_estatisticas,
            style='default'
        ).pack(pady=PADDING['medium'])
    
    def _buscar_equipamento(self):
        """Busca equipamento por número de série"""
        termo = self.equip_search.get().strip()
        
        if not termo:
            messagebox.showwarning("Atenção", "Digite um número de série para buscar")
            return
        
        # Limpa resultado anterior
        for widget in self.equip_result_frame.winfo_children():
            widget.destroy()
        
        # Busca equipamento
        equip = self.db.buscar_equipamento_por_serie(termo)
        
        if not equip:
            tk.Label(
                self.equip_result_frame,
                text=f"❌ Equipamento '{termo}' não encontrado",
                font=FONTS['normal'],
                bg=COLORS['white'],
                fg=COLORS['danger']
            ).pack(expand=True)
            return
        
        # Cria frame de resultado
        result = tk.Frame(self.equip_result_frame, bg=COLORS['white'])
        result.pack(fill='both', expand=True)
        
        # Informações do equipamento
        info_frame = tk.Frame(result, bg=COLORS['bg'], relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
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
        """
        
        tk.Label(
            info_frame,
            text=info_text.strip(),
            font=FONTS['normal'],
            bg=COLORS['bg'],
            fg=COLORS['text'],
            justify='left',
            padx=PADDING['large'],
            pady=PADDING['large']
        ).pack(fill='x')
        
        # Cliente atual
        hist_ativo = self.db.buscar_historico_ativo_equipamento(equip['id'])
        if hist_ativo and hist_ativo['cliente_nome']:
            cliente_frame = tk.Frame(result, bg=COLORS['primary'], relief='solid', borderwidth=1)
            cliente_frame.pack(fill='x', pady=(0, PADDING['medium']))
            
            tk.Label(
                cliente_frame,
                text=f"👤 Cliente Atual: {hist_ativo['cliente_nome']} - {hist_ativo['cliente_telefone']}",
                font=FONTS['subtitle'],
                bg=COLORS['primary'],
                fg=COLORS['white'],
                padx=PADDING['large'],
                pady=PADDING['medium']
            ).pack(fill='x')
        
        # Histórico completo
        tk.Label(
            result,
            text="📜 Histórico Completo",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(PADDING['medium'], PADDING['small']))
        
        historico = self.db.buscar_historico_equipamento(equip['id'])
        
        columns = ('Status', 'Data Início', 'Data Fim', 'Ação', 'Cliente', 'Usuário')
        column_widths = (50, 130, 130, 100, 150, 100)
        
        hist_table = DataTable(result, columns, column_widths)
        hist_table.pack(fill='both', expand=True)
        
        data = []
        for h in historico:
            status = "🟢" if h['data_fim'] is None else "⚪"
            data.append((
                status,
                h['data_inicio'],
                h['data_fim'] or '-',
                h['acao'],
                h['cliente_nome'] or '-',
                h['usuario_responsavel']
            ))
        
        hist_table.populate(data)
    
    def _buscar_cliente(self):
        """Busca cliente e seus equipamentos"""
        termo = self.cliente_search.get().strip()
        
        if not termo:
            messagebox.showwarning("Atenção", "Digite um termo para buscar")
            return
        
        # Limpa resultado anterior
        for widget in self.cliente_result_frame.winfo_children():
            widget.destroy()
        
        # Busca clientes
        clientes = self.db.buscar_clientes(termo)
        
        if not clientes:
            tk.Label(
                self.cliente_result_frame,
                text=f"❌ Nenhum cliente encontrado com '{termo}'",
                font=FONTS['normal'],
                bg=COLORS['white'],
                fg=COLORS['danger']
            ).pack(expand=True)
            return
        
        # Se encontrou múltiplos, mostra lista para seleção
        if len(clientes) > 1:
            self._mostrar_lista_clientes(clientes)
        else:
            self._mostrar_detalhes_cliente(clientes[0])
    
    def _mostrar_lista_clientes(self, clientes):
        """Mostra lista de clientes encontrados"""
        result = tk.Frame(self.cliente_result_frame, bg=COLORS['white'])
        result.pack(fill='both', expand=True)
        
        tk.Label(
            result,
            text=f"✓ {len(clientes)} clientes encontrados. Selecione um:",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(0, PADDING['medium']))
        
        columns = ('ID', 'Nome', 'Telefone', 'Setor')
        column_widths = (50, 250, 150, 120)
        
        table = DataTable(result, columns, column_widths)
        table.pack(fill='both', expand=True, pady=(0, PADDING['medium']))
        
        data = []
        for c in clientes:
            data.append((
                c['id'],
                c['nome'],
                c['telefone'],
                c['setor'] or '-'
            ))
        
        table.populate(data)
        
        # Botão para ver detalhes
        def ver_detalhes():
            selected = table.get_selected()
            if selected:
                cliente_id = selected['values'][0]
                cliente = self.db.buscar_cliente_por_id(cliente_id)
                self._mostrar_detalhes_cliente(cliente)
        
        CustomButton(
            result,
            text="👁️ Ver Detalhes do Cliente Selecionado",
            command=ver_detalhes,
            style='primary'
        ).pack()
    
    def _mostrar_detalhes_cliente(self, cliente):
        """Mostra detalhes completos do cliente"""
        # Limpa frame
        for widget in self.cliente_result_frame.winfo_children():
            widget.destroy()
        
        result = tk.Frame(self.cliente_result_frame, bg=COLORS['white'])
        result.pack(fill='both', expand=True)
        
        # Informações do cliente
        info_frame = tk.Frame(result, bg=COLORS['bg'], relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        info_text = f"""
👤 CLIENTE ENCONTRADO

Nome: {cliente['nome']}
Telefone: {cliente['telefone']}
Email: {cliente['email'] or '-'}
Documento: {cliente['documento'] or '-'}
Setor: {cliente['setor'] or '-'}
Endereço: {cliente['endereco'] or '-'}
Data de Cadastro: {cliente['data_cadastro']}
        """
        
        tk.Label(
            info_frame,
            text=info_text.strip(),
            font=FONTS['normal'],
            bg=COLORS['bg'],
            fg=COLORS['text'],
            justify='left',
            padx=PADDING['large'],
            pady=PADDING['large']
        ).pack(fill='x')
        
        # Equipamentos ativos
        equipamentos_ativos = self.db.buscar_equipamentos_cliente_ativo(cliente['id'])
        
        if equipamentos_ativos:
            tk.Label(
                result,
                text=f"📦 Equipamentos Ativos ({len(equipamentos_ativos)})",
                font=FONTS['subtitle'],
                bg=COLORS['white'],
                fg=COLORS['success']
            ).pack(anchor='w', pady=(PADDING['medium'], PADDING['small']))
            
            columns = ('Série', 'Tipo', 'Marca', 'Modelo', 'Desde')
            column_widths = (150, 100, 100, 120, 130)
            
            ativos_table = DataTable(result, columns, column_widths)
            ativos_table.pack(fill='x', pady=(0, PADDING['medium']))
            
            data = []
            for e in equipamentos_ativos:
                data.append((
                    e['numero_serie'],
                    e['tipo'],
                    e['marca'] or '-',
                    e['modelo'] or '-',
                    e['data_inicio'][:16]
                ))
            
            ativos_table.populate(data)
        
        # Histórico completo
        tk.Label(
            result,
            text="📜 Histórico Completo de Equipamentos",
            font=FONTS['subtitle'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(PADDING['medium'], PADDING['small']))
        
        historico = self.db.buscar_historico_cliente(cliente['id'])
        
        if historico:
            columns = ('Status', 'Equipamento', 'Ação', 'Data Início', 'Data Fim')
            column_widths = (50, 200, 100, 130, 130)
            
            hist_table = DataTable(result, columns, column_widths)
            hist_table.pack(fill='both', expand=True)
            
            data = []
            for h in historico:
                status = "🟢" if h['data_fim'] is None else "⚪"
                equip_info = f"{h['numero_serie']} ({h['tipo']})"
                data.append((
                    status,
                    equip_info,
                    h['acao'],
                    h['data_inicio'],
                    h['data_fim'] or '-'
                ))
            
            hist_table.populate(data)
        else:
            tk.Label(
                result,
                text="Nenhum histórico de equipamentos",
                font=FONTS['normal'],
                bg=COLORS['white'],
                fg=COLORS['text_light']
            ).pack(pady=PADDING['large'])
    
    def _atualizar_estatisticas(self):
        """Atualiza estatísticas gerais"""
        stats = self.db.get_estatisticas()
        
        texto = f"""
📊 ESTATÍSTICAS GERAIS

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
        
        self.stats_label.config(text=texto.strip())
    
    def _exportar_clientes(self):
        """Exporta clientes para CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not filename:
            return
        
        try:
            clientes = self.db.buscar_clientes()
            
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
            
            self.relatorio_status.show_success(f"✓ {len(clientes)} clientes exportados para {filename}")
        
        except Exception as e:
            self.relatorio_status.show_error(f"Erro ao exportar: {str(e)}")
    
    def _exportar_equipamentos(self):
        """Exporta equipamentos para CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"equipamentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not filename:
            return
        
        try:
            equipamentos = self.db.buscar_equipamentos()
            
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
            
            self.relatorio_status.show_success(f"✓ {len(equipamentos)} equipamentos exportados para {filename}")
        
        except Exception as e:
            self.relatorio_status.show_error(f"Erro ao exportar: {str(e)}")
    
    def _exportar_historico(self):
        """Exporta histórico completo para CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"historico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not filename:
            return
        
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
            
            self.relatorio_status.show_success(f"✓ {len(historico)} registros exportados para {filename}")
        
        except Exception as e:
            self.relatorio_status.show_error(f"Erro ao exportar: {str(e)}")
