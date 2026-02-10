"""
Formulário de registro de movimentações de equipamentos
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from gui.styles import COLORS, FONTS, PADDING
from gui.widgets import CustomButton, StatusLabel, DataTable, SearchBar
from database import Database
from models import AcaoHistorico, StatusEquipamento


class MovimentacaoForm(tk.Frame):
    """Formulário de registro de movimentações"""
    
    def __init__(self, parent, db: Database):
        super().__init__(parent, bg=COLORS['white'])
        self.db = db
        self.equipamento_selecionado = None
        self.cliente_selecionado = None
        
        self.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        self._criar_interface()
        self._carregar_movimentacoes_recentes()
    
    def _criar_interface(self):
        """Cria a interface do formulário"""
        
        # Título
        title = tk.Label(
            self,
            text="🔄 Registro de Movimentações",
            font=FONTS['title'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, PADDING['large']))
        
        # Container principal (2 colunas)
        main_container = tk.Frame(self, bg=COLORS['white'])
        main_container.pack(fill='both', expand=True)
        
        # Coluna esquerda - Formulário
        self._criar_formulario(main_container)
        
        # Coluna direita - Histórico recente
        self._criar_historico(main_container)
    
    def _criar_formulario(self, parent):
        """Cria o formulário de movimentação"""
        form_frame = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1)
        form_frame.pack(side='left', fill='both', padx=(0, PADDING['medium']), expand=True)
        
        # Padding interno
        form_content = tk.Frame(form_frame, bg=COLORS['white'])
        form_content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título do formulário
        form_title = tk.Label(
            form_content,
            text="Nova Movimentação",
            font=FONTS['subtitle'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        form_title.pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Tipo de Ação
        acao_frame = tk.Frame(form_content, bg=COLORS['white'])
        acao_frame.pack(fill='x', pady=PADDING['small'])
        
        tk.Label(
            acao_frame,
            text="Tipo de Movimentação *",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['danger']
        ).pack(anchor='w', pady=(0, 5))
        
        self.acao_combo = ttk.Combobox(
            acao_frame,
            values=AcaoHistorico.todos(),
            state='readonly',
            font=FONTS['normal'],
            width=38
        )
        self.acao_combo.pack(fill='x')
        self.acao_combo.set("Selecione o tipo...")
        self.acao_combo.bind('<<ComboboxSelected>>', self._on_acao_change)
        
        # Seleção de Equipamento
        equip_frame = tk.Frame(form_content, bg=COLORS['white'])
        equip_frame.pack(fill='x', pady=PADDING['small'])
        
        tk.Label(
            equip_frame,
            text="Equipamento *",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['danger']
        ).pack(anchor='w', pady=(0, 5))
        
        equip_select_frame = tk.Frame(equip_frame, bg=COLORS['white'])
        equip_select_frame.pack(fill='x')
        
        self.equipamento_combo = ttk.Combobox(
            equip_select_frame,
            state='readonly',
            font=FONTS['normal'],
            width=28
        )
        self.equipamento_combo.pack(side='left', fill='x', expand=True, padx=(0, PADDING['small']))
        self.equipamento_combo.bind('<<ComboboxSelected>>', self._on_equipamento_change)
        
        CustomButton(
            equip_select_frame,
            text="🔄 Atualizar",
            command=self._carregar_equipamentos_combo,
            style='default'
        ).pack(side='left')
        
        # Info do equipamento selecionado (CRIAR ANTES de carregar combo)
        self.info_equipamento = tk.Label(
            form_content,
            text="",
            font=FONTS['small'],
            bg=COLORS['bg'],
            fg=COLORS['text'],
            relief='solid',
            borderwidth=1,
            padx=PADDING['medium'],
            pady=PADDING['small']
        )
        self.info_equipamento.pack(fill='x', pady=PADDING['small'])
        self.info_equipamento.pack_forget()  # Oculto inicialmente
        
        # Agora sim, carregar equipamentos
        self._carregar_equipamentos_combo()
        
        # Seleção de Cliente (condicional)
        self.cliente_frame = tk.Frame(form_content, bg=COLORS['white'])
        self.cliente_frame.pack(fill='x', pady=PADDING['small'])
        
        self.cliente_label = tk.Label(
            self.cliente_frame,
            text="Cliente *",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['danger']
        )
        self.cliente_label.pack(anchor='w', pady=(0, 5))
        
        self.cliente_combo = ttk.Combobox(
            self.cliente_frame,
            state='readonly',
            font=FONTS['normal'],
            width=38
        )
        self.cliente_combo.pack(fill='x')
        
        self._carregar_clientes_combo()
        self.cliente_frame.pack_forget()  # Oculto inicialmente
        
        # Usuário Responsável
        usuario_frame = tk.Frame(form_content, bg=COLORS['white'])
        usuario_frame.pack(fill='x', pady=PADDING['small'])
        
        tk.Label(
            usuario_frame,
            text="Seu Nome (Responsável) *",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['danger']
        ).pack(anchor='w', pady=(0, 5))
        
        self.usuario_entry = tk.Entry(
            usuario_frame,
            font=FONTS['normal'],
            relief='solid',
            borderwidth=1
        )
        self.usuario_entry.pack(fill='x')
        self.usuario_entry.insert(0, "Técnico")  # Valor padrão
        
        # Observações
        obs_frame = tk.Frame(form_content, bg=COLORS['white'])
        obs_frame.pack(fill='x', pady=PADDING['small'])
        
        tk.Label(
            obs_frame,
            text="Observações",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(anchor='w', pady=(0, 5))
        
        self.obs_text = tk.Text(
            obs_frame,
            height=4,
            font=FONTS['normal'],
            relief='solid',
            borderwidth=1,
            wrap='word'
        )
        self.obs_text.pack(fill='x')
        
        # Status label
        self.status_label = StatusLabel(form_content)
        self.status_label.pack(pady=PADDING['medium'])
        
        # Botões
        btn_frame = tk.Frame(form_content, bg=COLORS['white'])
        btn_frame.pack(fill='x', pady=(PADDING['medium'], 0))
        
        CustomButton(
            btn_frame,
            text="✅ Registrar Movimentação",
            command=self._registrar_movimentacao,
            style='success'
        ).pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            btn_frame,
            text="🔄 Limpar",
            command=self._limpar_formulario,
            style='default'
        ).pack(side='left')
    
    def _criar_historico(self, parent):
        """Cria a lista de movimentações recentes"""
        list_frame = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1)
        list_frame.pack(side='right', fill='both', expand=True)
        
        # Padding interno
        list_content = tk.Frame(list_frame, bg=COLORS['white'])
        list_content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título da lista
        list_title = tk.Label(
            list_content,
            text="Movimentações Recentes",
            font=FONTS['subtitle'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        list_title.pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Filtros
        filter_frame = tk.Frame(list_content, bg=COLORS['white'])
        filter_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        # Filtro por ação
        tk.Label(
            filter_frame,
            text="Filtrar:",
            font=FONTS['normal'],
            bg=COLORS['white']
        ).pack(side='left', padx=(0, PADDING['small']))
        
        self.acao_filter = ttk.Combobox(
            filter_frame,
            values=['Todas'] + AcaoHistorico.todos(),
            state='readonly',
            font=FONTS['small'],
            width=15
        )
        self.acao_filter.set('Todas')
        self.acao_filter.pack(side='left', padx=(0, PADDING['small']))
        self.acao_filter.bind('<<ComboboxSelected>>', lambda e: self._carregar_movimentacoes_recentes())
        
        # Limite de registros
        tk.Label(
            filter_frame,
            text="Mostrar:",
            font=FONTS['normal'],
            bg=COLORS['white']
        ).pack(side='left', padx=(PADDING['medium'], PADDING['small']))
        
        self.limite_combo = ttk.Combobox(
            filter_frame,
            values=['10', '25', '50', '100', 'Todos'],
            state='readonly',
            font=FONTS['small'],
            width=8
        )
        self.limite_combo.set('25')
        self.limite_combo.pack(side='left')
        self.limite_combo.bind('<<ComboboxSelected>>', lambda e: self._carregar_movimentacoes_recentes())
        
        # Tabela de movimentações
        columns = ('Data', 'Ação', 'Equipamento', 'Cliente', 'Usuário')
        column_widths = (130, 100, 120, 120, 100)
        
        self.table = DataTable(list_content, columns, column_widths)
        self.table.pack(fill='both', expand=True, pady=(0, PADDING['medium']))
        
        # Botões de ação
        btn_frame = tk.Frame(list_content, bg=COLORS['white'])
        btn_frame.pack(fill='x')
        
        CustomButton(
            btn_frame,
            text="👁️ Ver Detalhes",
            command=self._ver_detalhes,
            style='primary'
        ).pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            btn_frame,
            text="🔄 Atualizar",
            command=self._carregar_movimentacoes_recentes,
            style='default'
        ).pack(side='left')
    
    def _carregar_equipamentos_combo(self):
        """Carrega equipamentos no combobox"""
        equipamentos = self.db.buscar_equipamentos()
        
        # Formato: "Série - Tipo - Status"
        self.equipamentos_dict = {}
        for e in equipamentos:
            key = f"{e['numero_serie']} - {e['tipo']} - {e['status_atual']}"
            self.equipamentos_dict[key] = e
        
        if self.equipamentos_dict:
            self.equipamento_combo['values'] = list(self.equipamentos_dict.keys())
            self.equipamento_combo.set(list(self.equipamentos_dict.keys())[0])
            self._on_equipamento_change()
        else:
            self.equipamento_combo['values'] = ['(Nenhum equipamento cadastrado)']
            self.equipamento_combo.set('(Nenhum equipamento cadastrado)')
            self.info_equipamento.pack_forget()
    
    def _carregar_clientes_combo(self):
        """Carrega clientes no combobox"""
        clientes = self.db.buscar_clientes()
        
        # Formato: "ID - Nome - Telefone"
        self.clientes_dict = {}
        for c in clientes:
            key = f"{c['id']} - {c['nome']} - {c['telefone']}"
            self.clientes_dict[key] = c['id']
        
        self.cliente_combo['values'] = list(self.clientes_dict.keys())
    
    def _on_acao_change(self, event=None):
        """Chamado quando a ação é alterada"""
        acao = self.acao_combo.get()
        
        # Mostra/oculta campo de cliente baseado na ação
        if acao in [AcaoHistorico.ENTREGA, AcaoHistorico.TRANSFERENCIA]:
            self.cliente_frame.pack(fill='x', pady=PADDING['small'])
            self.cliente_label.config(text="Cliente (Destino) *", fg=COLORS['danger'])
        elif acao == AcaoHistorico.DEVOLUCAO:
            self.cliente_frame.pack(fill='x', pady=PADDING['small'])
            self.cliente_label.config(text="Cliente (Origem)", fg=COLORS['text'])
        else:
            self.cliente_frame.pack_forget()
    
    def _on_equipamento_change(self, event=None):
        """Chamado quando o equipamento é alterado"""
        equip_key = self.equipamento_combo.get()
        
        # Verifica se há equipamentos e se a chave é válida
        if not equip_key or equip_key not in self.equipamentos_dict:
            self.info_equipamento.pack_forget()
            return
        
        equip = self.equipamentos_dict[equip_key]
        self.equipamento_selecionado = equip
        
        # Mostra informações do equipamento
        info_text = f"📦 {equip['tipo']} {equip['marca'] or ''} {equip['modelo'] or ''}\n"
        info_text += f"Status atual: {equip['status_atual']}"
        
        # Busca cliente atual se houver
        hist_ativo = self.db.buscar_historico_ativo_equipamento(equip['id'])
        if hist_ativo and hist_ativo.get('cliente_nome'):
            info_text += f" | Com: {hist_ativo['cliente_nome']}"
        
        self.info_equipamento.config(text=info_text)
        self.info_equipamento.pack(fill='x', pady=PADDING['small'])
    
    def _validar_campos(self):
        """Valida os campos do formulário"""
        acao = self.acao_combo.get()
        equip_key = self.equipamento_combo.get()
        usuario = self.usuario_entry.get().strip()
        
        # Ação obrigatória
        if not acao or acao == "Selecione o tipo...":
            self.status_label.show_error("Selecione o tipo de movimentação")
            return False
        
        # Equipamento obrigatório
        if not equip_key or equip_key not in self.equipamentos_dict:
            self.status_label.show_error("Selecione um equipamento")
            return False
        
        # Usuário obrigatório
        if not usuario:
            self.status_label.show_error("Informe seu nome")
            return False
        
        # Cliente obrigatório para algumas ações
        if acao in [AcaoHistorico.ENTREGA, AcaoHistorico.TRANSFERENCIA]:
            cliente_key = self.cliente_combo.get()
            if not cliente_key or cliente_key not in self.clientes_dict:
                self.status_label.show_error("Selecione o cliente de destino")
                return False
        
        return True
    
    def _registrar_movimentacao(self):
        """Registra uma nova movimentação"""
        if not self._validar_campos():
            return
        
        acao = self.acao_combo.get()
        equip = self.equipamento_selecionado
        usuario = self.usuario_entry.get().strip()
        obs = self.obs_text.get('1.0', 'end-1c').strip() or None
        
        # Cliente (se aplicável)
        cliente_id = None
        cliente_key = self.cliente_combo.get()
        if cliente_key in self.clientes_dict:
            cliente_id = self.clientes_dict[cliente_key]
        
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
            
            self.status_label.show_success(
                f"Movimentação registrada! {equip['numero_serie']} → {novo_status}"
            )
            
            self._limpar_formulario()
            self._carregar_movimentacoes_recentes()
            self._carregar_equipamentos_combo()  # Atualiza lista com novos status
            
        except Exception as e:
            self.status_label.show_error(f"Erro ao registrar: {str(e)}")
    
    def _determinar_status(self, acao: str, cliente_id: int = None) -> str:
        """Determina o novo status baseado na ação"""
        if acao == AcaoHistorico.ENTREGA:
            return StatusEquipamento.COM_CLIENTE
        elif acao == AcaoHistorico.DEVOLUCAO:
            return StatusEquipamento.EM_ESTOQUE
        elif acao in [AcaoHistorico.MANUTENCAO, AcaoHistorico.REPARO]:
            return StatusEquipamento.EM_MANUTENCAO
        elif acao == AcaoHistorico.TRANSFERENCIA:
            return StatusEquipamento.COM_CLIENTE
        elif acao == AcaoHistorico.BAIXA:
            return StatusEquipamento.BAIXADO
        else:
            return StatusEquipamento.EM_ESTOQUE
    
    def _limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.acao_combo.set("Selecione o tipo...")
        self.usuario_entry.delete(0, tk.END)
        self.usuario_entry.insert(0, "Técnico")
        self.obs_text.delete('1.0', 'end')
        self.cliente_frame.pack_forget()
        self.info_equipamento.pack_forget()
        self._carregar_equipamentos_combo()
    
    def _carregar_movimentacoes_recentes(self):
        """Carrega movimentações recentes na tabela"""
        # Busca todos os históricos
        self.db.cursor.execute("""
            SELECT h.*, 
                   e.numero_serie, e.tipo,
                   c.nome as cliente_nome
            FROM historico_posse h
            JOIN equipamentos e ON h.equipamento_id = e.id
            LEFT JOIN clientes c ON h.cliente_id = c.id
            ORDER BY h.data_inicio DESC
        """)
        
        historicos = [dict(row) for row in self.db.cursor.fetchall()]
        
        # Aplica filtro de ação
        acao_filtro = self.acao_filter.get()
        if acao_filtro != 'Todas':
            historicos = [h for h in historicos if h['acao'] == acao_filtro]
        
        # Aplica limite
        limite_str = self.limite_combo.get()
        if limite_str != 'Todos':
            limite = int(limite_str)
            historicos = historicos[:limite]
        
        # Popula tabela
        data = []
        for h in historicos:
            status = "🟢" if h['data_fim'] is None else "⚪"
            data.append((
                f"{status} {h['data_inicio'][:16]}",
                h['acao'],
                f"{h['numero_serie']} ({h['tipo']})",
                h['cliente_nome'] or '-',
                h['usuario_responsavel']
            ))
        
        self.table.populate(data)
    
    def _ver_detalhes(self):
        """Mostra detalhes da movimentação selecionada"""
        selected = self.table.get_selected()
        if not selected:
            self.status_label.show_error("Selecione uma movimentação para ver detalhes")
            return
        
        # Extrai informações da linha selecionada
        data_str = selected['values'][0]
        acao = selected['values'][1]
        equip_info = selected['values'][2]
        
        # Busca no banco
        self.db.cursor.execute("""
            SELECT h.*, 
                   e.numero_serie, e.tipo, e.marca, e.modelo, e.status_atual,
                   c.nome as cliente_nome, c.telefone as cliente_telefone
            FROM historico_posse h
            JOIN equipamentos e ON h.equipamento_id = e.id
            LEFT JOIN clientes c ON h.cliente_id = c.id
            WHERE h.data_inicio LIKE ? AND h.acao = ?
            ORDER BY h.id DESC
            LIMIT 1
        """, (f"%{data_str[2:18]}%", acao))
        
        hist = dict(self.db.cursor.fetchone())
        
        # Cria modal
        modal = tk.Toplevel(self)
        modal.title("Detalhes da Movimentação")
        modal.geometry("600x500")
        modal.configure(bg=COLORS['white'])
        modal.transient(self)
        modal.grab_set()
        
        # Conteúdo
        content = tk.Frame(modal, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título
        tk.Label(
            content,
            text=f"📋 Detalhes da Movimentação",
            font=FONTS['title'],
            bg=COLORS['white']
        ).pack(pady=(0, PADDING['large']))
        
        # Frame de informações
        info_frame = tk.Frame(content, bg=COLORS['bg'], relief='solid', borderwidth=1)
        info_frame.pack(fill='both', expand=True, pady=(0, PADDING['medium']))
        
        # Scroll
        canvas = tk.Canvas(info_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(info_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Informações
        info_text = f"""
🔄 AÇÃO: {hist['acao']}
📅 Data/Hora: {hist['data_inicio']}
{'📅 Finalizado: ' + hist['data_fim'] if hist['data_fim'] else '🟢 ATIVO'}

📦 EQUIPAMENTO:
   Série: {hist['numero_serie']}
   Tipo: {hist['tipo']}
   Marca/Modelo: {hist['marca'] or '-'} {hist['modelo'] or '-'}
   Status Atual: {hist['status_atual']}

👤 CLIENTE:
   Nome: {hist['cliente_nome'] or 'Nenhum'}
   Telefone: {hist['cliente_telefone'] or '-'}

👨‍💼 RESPONSÁVEL:
   {hist['usuario_responsavel']}

📝 OBSERVAÇÕES:
   {hist['observacoes'] or 'Nenhuma'}
        """
        
        tk.Label(
            scrollable_frame,
            text=info_text.strip(),
            font=FONTS['normal'],
            bg=COLORS['bg'],
            fg=COLORS['text'],
            justify='left',
            padx=PADDING['large'],
            pady=PADDING['large']
        ).pack(fill='both', expand=True)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botão fechar
        CustomButton(
            content,
            text="Fechar",
            command=modal.destroy,
            style='default'
        ).pack(pady=PADDING['medium'])
