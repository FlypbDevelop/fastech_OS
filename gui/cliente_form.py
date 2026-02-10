"""
Formulário de cadastro e edição de clientes
"""

import tkinter as tk
from tkinter import messagebox
from gui.styles import COLORS, FONTS, PADDING
from gui.widgets import CustomButton, LabeledEntry, StatusLabel, DataTable, SearchBar
from database import Database
from utils.validators import (
    validar_telefone, validar_email, validar_documento,
    formatar_telefone, formatar_cpf, formatar_cnpj
)


class ClienteForm(tk.Frame):
    """Formulário completo de gestão de clientes"""
    
    def __init__(self, parent, db: Database):
        super().__init__(parent, bg=COLORS['white'])
        self.db = db
        self.cliente_selecionado = None
        
        self.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        self._criar_interface()
        self._carregar_clientes()
    
    def _criar_interface(self):
        """Cria a interface do formulário"""
        
        # Título
        title = tk.Label(
            self,
            text="📋 Gestão de Clientes",
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
            text="Cadastro de Cliente",
            font=FONTS['subtitle'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        form_title.pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Campos do formulário
        self.nome_entry = LabeledEntry(
            form_content,
            "Nome Completo",
            placeholder="Digite o nome do cliente",
            required=True,
            width=40
        )
        self.nome_entry.pack(fill='x', pady=PADDING['small'])
        
        self.telefone_entry = LabeledEntry(
            form_content,
            "Telefone",
            placeholder="(11) 98765-4321",
            required=True,
            width=40
        )
        self.telefone_entry.pack(fill='x', pady=PADDING['small'])
        
        self.email_entry = LabeledEntry(
            form_content,
            "Email",
            placeholder="cliente@email.com",
            width=40
        )
        self.email_entry.pack(fill='x', pady=PADDING['small'])
        
        self.documento_entry = LabeledEntry(
            form_content,
            "CPF/CNPJ",
            placeholder="000.000.000-00",
            width=40
        )
        self.documento_entry.pack(fill='x', pady=PADDING['small'])
        
        self.setor_entry = LabeledEntry(
            form_content,
            "Setor/Departamento",
            placeholder="Ex: TI, RH, Vendas",
            width=40
        )
        self.setor_entry.pack(fill='x', pady=PADDING['small'])
        
        self.endereco_entry = LabeledEntry(
            form_content,
            "Endereço",
            placeholder="Rua, número, bairro, cidade",
            width=40
        )
        self.endereco_entry.pack(fill='x', pady=PADDING['small'])
        
        # Status label
        self.status_label = StatusLabel(form_content)
        self.status_label.pack(pady=PADDING['medium'])
        
        # Botões
        btn_frame = tk.Frame(form_content, bg=COLORS['white'])
        btn_frame.pack(fill='x', pady=(PADDING['medium'], 0))
        
        self.btn_salvar = CustomButton(
            btn_frame,
            text="💾 Salvar Cliente",
            command=self._salvar_cliente,
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
        """Cria a lista de clientes"""
        list_frame = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1)
        list_frame.pack(side='right', fill='both', expand=True)
        
        # Padding interno
        list_content = tk.Frame(list_frame, bg=COLORS['white'])
        list_content.pack(fill='both', expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Título da lista
        list_title = tk.Label(
            list_content,
            text="Clientes Cadastrados",
            font=FONTS['subtitle'],
            bg=COLORS['white'],
            fg=COLORS['text']
        )
        list_title.pack(anchor='w', pady=(0, PADDING['medium']))
        
        # Barra de busca
        self.search_bar = SearchBar(
            list_content,
            placeholder="Buscar por nome, telefone ou documento...",
            on_search=self._buscar_clientes
        )
        self.search_bar.pack(fill='x', pady=(0, PADDING['medium']))
        
        # Tabela de clientes
        columns = ('ID', 'Nome', 'Telefone', 'Setor')
        column_widths = (50, 200, 150, 100)
        
        self.table = DataTable(list_content, columns, column_widths)
        self.table.pack(fill='both', expand=True, pady=(0, PADDING['medium']))
        
        # Bind duplo clique para editar
        self.table.tree.bind('<Double-1>', lambda e: self._editar_cliente())
        
        # Botões de ação
        btn_frame = tk.Frame(list_content, bg=COLORS['white'])
        btn_frame.pack(fill='x')
        
        CustomButton(
            btn_frame,
            text="✏️ Editar",
            command=self._editar_cliente,
            style='primary'
        ).pack(side='left', padx=(0, PADDING['small']))
        
        CustomButton(
            btn_frame,
            text="🗑️ Excluir",
            command=self._excluir_cliente,
            style='danger'
        ).pack(side='left', padx=PADDING['small'])
        
        CustomButton(
            btn_frame,
            text="🔄 Atualizar",
            command=self._carregar_clientes,
            style='default'
        ).pack(side='left', padx=PADDING['small'])
    
    def _validar_campos(self):
        """Valida os campos do formulário"""
        nome = self.nome_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        email = self.email_entry.get().strip()
        documento = self.documento_entry.get().strip()
        
        # Nome obrigatório
        if not nome:
            self.status_label.show_error("Nome é obrigatório")
            return False
        
        # Telefone obrigatório e válido
        if not telefone:
            self.status_label.show_error("Telefone é obrigatório")
            return False
        
        valido, msg = validar_telefone(telefone)
        if not valido:
            self.status_label.show_error(msg)
            return False
        
        # Email opcional mas deve ser válido
        if email:
            valido, msg = validar_email(email)
            if not valido:
                self.status_label.show_error(msg)
                return False
        
        # Documento opcional mas deve ser válido
        if documento:
            valido, msg = validar_documento(documento)
            if not valido:
                self.status_label.show_error(msg)
                return False
        
        return True
    
    def _salvar_cliente(self):
        """Salva ou atualiza um cliente"""
        if not self._validar_campos():
            return
        
        nome = self.nome_entry.get().strip()
        telefone = formatar_telefone(self.telefone_entry.get().strip())
        email = self.email_entry.get().strip() or None
        documento = self.documento_entry.get().strip()
        setor = self.setor_entry.get().strip() or None
        endereco = self.endereco_entry.get().strip() or None
        
        # Formata documento se preenchido
        if documento:
            if len(documento.replace('.', '').replace('-', '').replace('/', '')) == 11:
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
                self.status_label.show_success(f"Cliente '{nome}' atualizado com sucesso!")
            else:
                # Inserir novo cliente
                cliente_id = self.db.inserir_cliente(
                    nome, telefone, email, endereco, documento, setor
                )
                self.status_label.show_success(f"Cliente '{nome}' cadastrado com sucesso! (ID: {cliente_id})")
            
            self._limpar_formulario()
            self._carregar_clientes()
            
        except ValueError as e:
            self.status_label.show_error(str(e))
    
    def _limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.nome_entry.clear()
        self.telefone_entry.clear()
        self.email_entry.clear()
        self.documento_entry.clear()
        self.setor_entry.clear()
        self.endereco_entry.clear()
        self.cliente_selecionado = None
        self.btn_cancelar.pack_forget()
        self.btn_salvar.config(text="💾 Salvar Cliente")
    
    def _cancelar_edicao(self):
        """Cancela a edição"""
        self._limpar_formulario()
        self.status_label.show_info("Edição cancelada")
    
    def _carregar_clientes(self):
        """Carrega todos os clientes na tabela"""
        clientes = self.db.buscar_clientes()
        
        data = []
        for c in clientes:
            data.append((
                c['id'],
                c['nome'],
                c['telefone'],
                c['setor'] or '-'
            ))
        
        self.table.populate(data)
    
    def _buscar_clientes(self):
        """Busca clientes pelo termo"""
        termo = self.search_bar.get()
        clientes = self.db.buscar_clientes(termo)
        
        data = []
        for c in clientes:
            data.append((
                c['id'],
                c['nome'],
                c['telefone'],
                c['setor'] or '-'
            ))
        
        self.table.populate(data)
        
        if not data:
            self.status_label.show_info("Nenhum cliente encontrado")
    
    def _editar_cliente(self):
        """Carrega dados do cliente selecionado para edição"""
        selected = self.table.get_selected()
        if not selected:
            self.status_label.show_error("Selecione um cliente para editar")
            return
        
        cliente_id = selected['values'][0]
        cliente = self.db.buscar_cliente_por_id(cliente_id)
        
        if cliente:
            self.cliente_selecionado = cliente
            
            # Preenche o formulário
            self.nome_entry.set(cliente['nome'])
            self.telefone_entry.set(cliente['telefone'])
            self.email_entry.set(cliente['email'] or "")
            self.documento_entry.set(cliente['documento'] or "")
            self.setor_entry.set(cliente['setor'] or "")
            self.endereco_entry.set(cliente['endereco'] or "")
            
            # Mostra botão cancelar e muda texto do salvar
            self.btn_cancelar.pack(side='left', padx=PADDING['small'])
            self.btn_salvar.config(text="💾 Atualizar Cliente")
            
            self.status_label.show_info(f"Editando: {cliente['nome']}")
    
    def _excluir_cliente(self):
        """Exclui o cliente selecionado"""
        selected = self.table.get_selected()
        if not selected:
            self.status_label.show_error("Selecione um cliente para excluir")
            return
        
        cliente_id = selected['values'][0]
        cliente_nome = selected['values'][1]
        
        # Confirmação
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir o cliente '{cliente_nome}'?\n\n"
            "ATENÇÃO: Não é possível excluir clientes com equipamentos ativos."
        )
        
        if resposta:
            sucesso = self.db.deletar_cliente(cliente_id)
            
            if sucesso:
                self.status_label.show_success(f"Cliente '{cliente_nome}' excluído com sucesso!")
                self._carregar_clientes()
            else:
                self.status_label.show_error(
                    "Não é possível excluir este cliente. "
                    "Ele possui equipamentos vinculados."
                )
