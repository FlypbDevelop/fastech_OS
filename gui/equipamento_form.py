"""
Formulário de cadastro e edição de equipamentos
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from gui.styles import COLORS, FONTS, PADDING
from gui.widgets import CustomButton, LabeledEntry, StatusLabel, DataTable, SearchBar
from database import Database
from models import TipoEquipamento, StatusEquipamento, AcaoHistorico
from utils.validators import validar_numero_serie


class EquipamentoForm(tk.Frame):
    """Formulário completo de gestão de equipamentos"""
    
    def __init__(self, parent, db: Database):
        super().__init__(parent, bg=COLORS['white'])
        self.db = db
        self.equipamento_selecionado = None
        self.modal_cliente = None
        
        self.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        self._criar_interface()
        self._carregar_equipamentos()
    
    def _criar_interface(self):
        """Cria a interface do formulário"""
        
        # Título
        title = tk.Label(
            self,
            text="📦 Gestão de Equipamentos",
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
        
        # Coluna direita - Lista
        self._criar_lista(main_container)
    
    def _criar_formulario(self, parent):
        """Cria o formulário de cadastro"""
        form_frame = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1)
        form_frame.pack(side='left', fill='both', padx=(0, PADDING['medium']), expand=True)
        
        # Padding interno
        form_content = tk.Frame(form_frame, bg=COLORS['white'])
        form_content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título do formulário
        form_title = tk.Label(
            form_content,
            text="Cadastro de Equipamento",
            font=FONTS['subtitle'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        form_title.pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Número de Série
        self.numero_serie_entry = LabeledEntry(
            form_content,
            "Número de Série",
            placeholder="Ex: NB-2024-001",
            required=True,
            width=40
        )
        self.numero_serie_entry.pack(fill='x', pady=PADDING['small'])
        
        # Tipo (Dropdown)
        tipo_frame = tk.Frame(form_content, bg=COLORS['white'])
        tipo_frame.pack(fill='x', pady=PADDING['small'])
        
        tk.Label(
            tipo_frame,
            text="Tipo de Equipamento *",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['danger']
        ).pack(anchor='w', pady=(0, 5))
        
        self.tipo_combo = ttk.Combobox(
            tipo_frame,
            values=TipoEquipamento.todos(),
            state='readonly',
            font=FONTS['normal'],
            width=38
        )
        self.tipo_combo.pack(fill='x')
        self.tipo_combo.set("Selecione o tipo...")
        
        # Marca e Modelo (mesma linha)
        marca_modelo_frame = tk.Frame(form_content, bg=COLORS['white'])
        marca_modelo_frame.pack(fill='x', pady=PADDING['small'])
        
        self.marca_entry = LabeledEntry(
            marca_modelo_frame,
            "Marca",
            placeholder="Ex: Dell, HP, Samsung",
            width=18
        )
        self.marca_entry.pack(side='left', fill='x', expand=True, padx=(0, PADDING['small']))
        
        self.modelo_entry = LabeledEntry(
            marca_modelo_frame,
            "Modelo",
            placeholder="Ex: Latitude 5420",
            width=18
        )
        self.modelo_entry.pack(side='left', fill='x', expand=True)
        
        # Cliente (Dropdown + Botão Novo)
        cliente_frame = tk.Frame(form_content, bg=COLORS['white'])
        cliente_frame.pack(fill='x', pady=PADDING['small'])
        
        tk.Label(
            cliente_frame,
            text="Cliente (opcional - deixe vazio para 'Em Estoque')",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(anchor='w', pady=(0, 5))
        
        cliente_select_frame = tk.Frame(cliente_frame, bg=COLORS['white'])
        cliente_select_frame.pack(fill='x')
        
        self.cliente_combo = ttk.Combobox(
            cliente_select_frame,
            state='readonly',
            font=FONTS['normal'],
            width=28
        )
        self.cliente_combo.pack(side='left', fill='x', expand=True, padx=(0, PADDING['small']))
        self._carregar_clientes_combo()
        
        CustomButton(
            cliente_select_frame,
            text="➕ Novo Cliente",
            command=self._abrir_modal_cliente,
            style='primary'
        ).pack(side='left')
        
        # Status (Dropdown)
        status_frame = tk.Frame(form_content, bg=COLORS['white'])
        status_frame.pack(fill='x', pady=PADDING['small'])
        
        tk.Label(
            status_frame,
            text="Status Inicial",
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['text']
        ).pack(anchor='w', pady=(0, 5))
        
        self.status_combo = ttk.Combobox(
            status_frame,
            values=StatusEquipamento.todos(),
            state='readonly',
            font=FONTS['normal'],
            width=38
        )
        self.status_combo.pack(fill='x')
        self.status_combo.set(StatusEquipamento.EM_ESTOQUE)
        
        # Valor Estimado e Data Garantia (mesma linha)
        valor_garantia_frame = tk.Frame(form_content, bg=COLORS['white'])
        valor_garantia_frame.pack(fill='x', pady=PADDING['small'])
        
        self.valor_entry = LabeledEntry(
            valor_garantia_frame,
            "Valor Estimado (R$)",
            placeholder="0.00",
            width=18
        )
        self.valor_entry.pack(side='left', fill='x', expand=True, padx=(0, PADDING['small']))
        
        self.garantia_entry = LabeledEntry(
            valor_garantia_frame,
            "Data Garantia",
            placeholder="AAAA-MM-DD",
            width=18
        )
        self.garantia_entry.pack(side='left', fill='x', expand=True)
        
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
            height=3,
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
        
        self.btn_salvar = CustomButton(
            btn_frame,
            text="💾 Salvar Equipamento",
            command=self._salvar_equipamento,
            style='success'
        )
        self.btn_salvar.pack(side='left', padx=(0, PADDING['small']))
        
        self.btn_limpar = CustomButton(
            btn_frame,
            text="🔄 Limpar",
            command=self._limpar_formulario,
            style='default'
        )
        self.btn_limpar.pack(side='left', padx=PADDING['small'])
        
        self.btn_cancelar = CustomButton(
            btn_frame,
            text="✖ Cancelar Edição",
            command=self._cancelar_edicao,
            style='danger'
        )
        self.btn_cancelar.pack(side='left', padx=PADDING['small'])
        self.btn_cancelar.pack_forget()  # Oculto inicialmente
    
    def _criar_lista(self, parent):
        """Cria a lista de equipamentos"""
        list_frame = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1)
        list_frame.pack(side='right', fill='both', expand=True)
        
        # Padding interno
        list_content = tk.Frame(list_frame, bg=COLORS['white'])
        list_content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título da lista
        list_title = tk.Label(
            list_content,
            text="Equipamentos Cadastrados",
            font=FONTS['subtitle'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        list_title.pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Barra de busca
        self.search_bar = SearchBar(
            list_content,
            placeholder="Buscar por número de série, tipo ou marca...",
            on_search=self._buscar_equipamentos
        )
        self.search_bar.pack(fill='x', pady=(0, PADDING['medium']))
        
        # Filtro por status
        filter_frame = tk.Frame(list_content, bg=COLORS['white'])
        filter_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        tk.Label(
            filter_frame,
            text="Filtrar por status:",
            font=FONTS['normal'],
            bg=COLORS['white']
        ).pack(side='left', padx=(0, PADDING['small']))
        
        self.status_filter = ttk.Combobox(
            filter_frame,
            values=['Todos'] + StatusEquipamento.todos(),
            state='readonly',
            font=FONTS['small'],
            width=20
        )
        self.status_filter.set('Todos')
        self.status_filter.pack(side='left')
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self._carregar_equipamentos())
        
        # Tabela de equipamentos
        columns = ('ID', 'Série', 'Tipo', 'Marca', 'Status')
        column_widths = (40, 150, 120, 100, 120)
        
        self.table = DataTable(list_content, columns, column_widths)
        self.table.pack(fill='both', expand=True, pady=(0, PADDING['medium']))
        
        # Bind duplo clique para editar
        self.table.tree.bind('<Double-1>', lambda e: self._editar_equipamento())
        
        # Botões de ação
        btn_frame = tk.Frame(list_content, bg=COLORS['white'])
        btn_frame.pack(fill='x')
        
        CustomButton(
            btn_frame,
            text="✏️ Editar",
            command=self._editar_equipamento,
            style='primary'
        ).pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            btn_frame,
            text="👁️ Ver Histórico",
            command=self._ver_historico,
            style='primary'
        ).pack(side='left', padx=PADDING['small'])
        
        CustomButton(
            btn_frame,
            text="🔄 Atualizar",
            command=self._carregar_equipamentos,
            style='default'
        ).pack(side='left', padx=PADDING['small'])
    
    def _carregar_clientes_combo(self):
        """Carrega clientes no combobox"""
        clientes = self.db.buscar_clientes()
        
        # Formato: "ID - Nome - Telefone"
        self.clientes_dict = {f"{c['id']} - {c['nome']} - {c['telefone']}": c['id'] for c in clientes}
        
        valores = ['(Sem cliente - Em Estoque)'] + list(self.clientes_dict.keys())
        self.cliente_combo['values'] = valores
        self.cliente_combo.set('(Sem cliente - Em Estoque)')
    
    def _validar_campos(self):
        """Valida os campos do formulário"""
        numero_serie = self.numero_serie_entry.get().strip()
        tipo = self.tipo_combo.get()
        
        # Número de série obrigatório
        valido, msg = validar_numero_serie(numero_serie)
        if not valido:
            self.status_label.show_error(msg)
            return False
        
        # Tipo obrigatório
        if not tipo or tipo == "Selecione o tipo...":
            self.status_label.show_error("Tipo de equipamento é obrigatório")
            return False
        
        return True
    
    def _salvar_equipamento(self):
        """Salva ou atualiza um equipamento"""
        if not self._validar_campos():
            return
        
        numero_serie = self.numero_serie_entry.get().strip()
        tipo = self.tipo_combo.get()
        marca = self.marca_entry.get().strip() or None
        modelo = self.modelo_entry.get().strip() or None
        status = self.status_combo.get()
        
        # Valor estimado
        valor_str = self.valor_entry.get().strip()
        valor = float(valor_str.replace(',', '.')) if valor_str else None
        
        # Data garantia
        garantia = self.garantia_entry.get().strip() or None
        
        # Observações
        obs = self.obs_text.get('1.0', 'end-1c').strip() or None
        
        # Cliente selecionado
        cliente_sel = self.cliente_combo.get()
        cliente_id = None
        if cliente_sel != '(Sem cliente - Em Estoque)':
            cliente_id = self.clientes_dict.get(cliente_sel)
        
        try:
            if self.equipamento_selecionado:
                # Atualizar equipamento existente
                self.db.atualizar_equipamento(
                    self.equipamento_selecionado['id'],
                    numero_serie=numero_serie,
                    tipo=tipo,
                    marca=marca,
                    modelo=modelo,
                    status_atual=status,
                    data_garantia=garantia,
                    valor_estimado=valor,
                    observacoes=obs
                )
                self.status_label.show_success(f"Equipamento '{numero_serie}' atualizado!")
            else:
                # Inserir novo equipamento
                equip_id = self.db.inserir_equipamento(
                    numero_serie, tipo, marca, modelo, status, garantia, valor, obs
                )
                
                # Registrar no histórico
                acao = AcaoHistorico.CADASTRO
                if cliente_id:
                    acao = AcaoHistorico.ENTREGA
                    status = StatusEquipamento.COM_CLIENTE
                    self.db.atualizar_status_equipamento(equip_id, status)
                
                self.db.inserir_historico(
                    equip_id,
                    acao,
                    "Sistema",
                    cliente_id,
                    observacoes=f"Cadastro inicial: {obs}" if obs else "Cadastro inicial"
                )
                
                self.status_label.show_success(f"Equipamento '{numero_serie}' cadastrado! (ID: {equip_id})")
            
            self._limpar_formulario()
            self._carregar_equipamentos()
            
        except ValueError as e:
            self.status_label.show_error(str(e))
    
    def _limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.numero_serie_entry.clear()
        self.tipo_combo.set("Selecione o tipo...")
        self.marca_entry.clear()
        self.modelo_entry.clear()
        self.cliente_combo.set('(Sem cliente - Em Estoque)')
        self.status_combo.set(StatusEquipamento.EM_ESTOQUE)
        self.valor_entry.clear()
        self.garantia_entry.clear()
        self.obs_text.delete('1.0', 'end')
        self.equipamento_selecionado = None
        self.btn_cancelar.pack_forget()
        self.btn_salvar.config(text="💾 Salvar Equipamento")
    
    def _cancelar_edicao(self):
        """Cancela a edição"""
        self._limpar_formulario()
        self.status_label.show_info("Edição cancelada")
    
    def _carregar_equipamentos(self):
        """Carrega todos os equipamentos na tabela"""
        status_filtro = self.status_filter.get()
        status = None if status_filtro == 'Todos' else status_filtro
        
        equipamentos = self.db.buscar_equipamentos(status=status)
        
        data = []
        for e in equipamentos:
            data.append((
                e['id'],
                e['numero_serie'],
                e['tipo'],
                e['marca'] or '-',
                e['status_atual']
            ))
        
        self.table.populate(data)
    
    def _buscar_equipamentos(self):
        """Busca equipamentos pelo termo"""
        termo = self.search_bar.get()
        status_filtro = self.status_filter.get()
        status = None if status_filtro == 'Todos' else status_filtro
        
        equipamentos = self.db.buscar_equipamentos(termo, status)
        
        data = []
        for e in equipamentos:
            data.append((
                e['id'],
                e['numero_serie'],
                e['tipo'],
                e['marca'] or '-',
                e['status_atual']
            ))
        
        self.table.populate(data)
        
        if not data:
            self.status_label.show_info("Nenhum equipamento encontrado")
    
    def _editar_equipamento(self):
        """Carrega dados do equipamento selecionado para edição"""
        selected = self.table.get_selected()
        if not selected:
            self.status_label.show_error("Selecione um equipamento para editar")
            return
        
        equip_id = selected['values'][0]
        equip = self.db.buscar_equipamento_por_id(equip_id)
        
        if equip:
            self.equipamento_selecionado = equip
            
            # Preenche o formulário
            self.numero_serie_entry.set(equip['numero_serie'])
            self.tipo_combo.set(equip['tipo'])
            self.marca_entry.set(equip['marca'] or "")
            self.modelo_entry.set(equip['modelo'] or "")
            self.status_combo.set(equip['status_atual'])
            self.valor_entry.set(str(equip['valor_estimado']) if equip['valor_estimado'] else "")
            self.garantia_entry.set(equip['data_garantia'] or "")
            
            if equip['observacoes']:
                self.obs_text.delete('1.0', 'end')
                self.obs_text.insert('1.0', equip['observacoes'])
            
            # Mostra botão cancelar e muda texto do salvar
            self.btn_cancelar.pack(side='left', padx=PADDING['small'])
            self.btn_salvar.config(text="💾 Atualizar Equipamento")
            
            self.status_label.show_info(f"Editando: {equip['numero_serie']}")
    
    def _ver_historico(self):
        """Mostra o histórico do equipamento selecionado"""
        selected = self.table.get_selected()
        if not selected:
            self.status_label.show_error("Selecione um equipamento para ver o histórico")
            return
        
        equip_id = selected['values'][0]
        equip = self.db.buscar_equipamento_por_id(equip_id)
        historico = self.db.buscar_historico_equipamento(equip_id)
        
        # Cria janela modal
        modal = tk.Toplevel(self)
        modal.title(f"Histórico - {equip['numero_serie']}")
        modal.geometry("700x500")
        modal.configure(bg=COLORS['white'])
        
        # Centraliza
        modal.transient(self)
        modal.grab_set()
        
        # Título
        tk.Label(
            modal,
            text=f"📜 Histórico Completo",
            font=FONTS['title'],
            bg=COLORS['white']
        ).pack(pady=PADDING['large'])
        
        # Info do equipamento
        info_frame = tk.Frame(modal, bg=COLORS['bg'], relief='solid', borderwidth=1)
        info_frame.pack(fill='x', padx=PADDING['large'], pady=(0, PADDING['medium']))
        
        tk.Label(
            info_frame,
            text=f"{equip['tipo']} {equip['marca']} {equip['modelo']}",
            font=FONTS['subtitle'],
            bg=COLORS['bg']
        ).pack(pady=PADDING['small'])
        
        tk.Label(
            info_frame,
            text=f"Série: {equip['numero_serie']} | Status: {equip['status_atual']}",
            font=FONTS['normal'],
            bg=COLORS['bg']
        ).pack(pady=PADDING['small'])
        
        # Tabela de histórico
        columns = ('Data', 'Ação', 'Cliente', 'Usuário')
        column_widths = (150, 120, 200, 120)
        
        hist_table = DataTable(modal, columns, column_widths)
        hist_table.pack(fill='both', expand=True, padx=PADDING['large'], pady=(0, PADDING['medium']))
        
        data = []
        for h in historico:
            status = "🟢" if h['data_fim'] is None else "⚪"
            data.append((
                f"{status} {h['data_inicio']}",
                h['acao'],
                h['cliente_nome'] or '-',
                h['usuario_responsavel']
            ))
        
        hist_table.populate(data)
        
        # Botão fechar
        CustomButton(
            modal,
            text="Fechar",
            command=modal.destroy,
            style='default'
        ).pack(pady=PADDING['medium'])
    
    def _abrir_modal_cliente(self):
        """Abre modal para cadastro rápido de cliente"""
        from gui.widgets import LabeledEntry
        
        # Cria janela modal
        self.modal_cliente = tk.Toplevel(self)
        self.modal_cliente.title("Cadastro Rápido de Cliente")
        self.modal_cliente.geometry("500x400")
        self.modal_cliente.configure(bg=COLORS['white'])
        
        # Centraliza
        self.modal_cliente.transient(self)
        self.modal_cliente.grab_set()
        
        # Conteúdo
        content = tk.Frame(self.modal_cliente, bg=COLORS['white'])
        content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        tk.Label(
            content,
            text="➕ Novo Cliente",
            font=FONTS['title'],
            bg=COLORS['white']
        ).pack(pady=(0, PADDING['large']))
        
        # Campos
        self.modal_nome = LabeledEntry(content, "Nome Completo", required=True, width=40)
        self.modal_nome.pack(fill='x', pady=PADDING['small'])
        
        self.modal_telefone = LabeledEntry(content, "Telefone", required=True, width=40)
        self.modal_telefone.pack(fill='x', pady=PADDING['small'])
        
        self.modal_email = LabeledEntry(content, "Email", width=40)
        self.modal_email.pack(fill='x', pady=PADDING['small'])
        
        self.modal_status = StatusLabel(content)
        self.modal_status.pack(pady=PADDING['medium'])
        
        # Botões
        btn_frame = tk.Frame(content, bg=COLORS['white'])
        btn_frame.pack(fill='x', pady=PADDING['medium'])
        
        CustomButton(
            btn_frame,
            text="💾 Salvar",
            command=self._salvar_cliente_modal,
            style='success'
        ).pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            btn_frame,
            text="Cancelar",
            command=self.modal_cliente.destroy,
            style='default'
        ).pack(side='left')
    
    def _salvar_cliente_modal(self):
        """Salva cliente do modal"""
        from utils.validators import validar_telefone, validar_email, formatar_telefone
        
        nome = self.modal_nome.get().strip()
        telefone = self.modal_telefone.get().strip()
        email = self.modal_email.get().strip() or None
        
        # Validações
        if not nome:
            self.modal_status.show_error("Nome é obrigatório")
            return
        
        valido, msg = validar_telefone(telefone)
        if not valido:
            self.modal_status.show_error(msg)
            return
        
        if email:
            valido, msg = validar_email(email)
            if not valido:
                self.modal_status.show_error(msg)
                return
        
        try:
            telefone = formatar_telefone(telefone)
            cliente_id = self.db.inserir_cliente(nome, telefone, email)
            
            self.modal_status.show_success(f"Cliente '{nome}' cadastrado!")
            
            # Recarrega combo e seleciona o novo cliente
            self._carregar_clientes_combo()
            
            # Seleciona o cliente recém-criado
            for key in self.clientes_dict:
                if self.clientes_dict[key] == cliente_id:
                    self.cliente_combo.set(key)
                    break
            
            # Fecha modal após 1 segundo
            self.modal_cliente.after(1000, self.modal_cliente.destroy)
            
        except ValueError as e:
            self.modal_status.show_error(str(e))
