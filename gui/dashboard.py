import tkinter as tk
from tkinter import ttk
from gui.styles import COLORS, FONTS, PADDING
from datetime import datetime, timedelta
import calendar

class Dashboard(tk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent, bg='#0f1419')
        self.db = db
        self.pack(fill='both', expand=True)
        self.lembretes = {}  # Dicionário para armazenar lembretes por data
        self._criar_interface()
        self._atualizar_dados()
    
    def _criar_interface(self):
        # Container principal
        main_container = tk.Frame(self, bg='#0f1419')
        main_container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Header
        self._criar_header(main_container)
        
        # Grid de cards
        self._criar_grid_cards(main_container)
    
    def _criar_header(self, parent):
        header = tk.Frame(parent, bg='#0f1419')
        header.pack(fill='x', pady=(0, 40))
        
        # Container principal do header
        header_content = tk.Frame(header, bg='#0f1419')
        header_content.pack(fill='x')
        
        # Saudação à esquerda
        agora = datetime.now()
        hora_int = agora.hour
        if hora_int < 12:
            saudacao = "Bom dia - Seja Bem vindo(a)"
        elif hora_int < 18:
            saudacao = "Boa tarde - Seja Bem vindo(a)"
        else:
            saudacao = "Boa noite - Seja Bem vindo(a)"
        
        tk.Label(
            header_content,
            text=saudacao,
            font=('Segoe UI', 18),
            bg='#0f1419',
            fg='#64748b'
        ).pack(side='left')
        
        # Container direito com calendário e hora
        right_container = tk.Frame(header_content, bg='#0f1419')
        right_container.pack(side='right')
        
        # Calendário clicável (substituindo área amarela)
        calendario_frame = tk.Frame(right_container, bg='#0f1419')
        calendario_frame.pack(side='left', padx=(0, 30))
        
        data_atual = agora.strftime("%d/%m/%Y")
        
        self.calendario_btn = tk.Button(
            calendario_frame,
            text=f"📅\n{data_atual}",
            font=('Segoe UI', 12, 'bold'),
            bg='#1e3a5f',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self._abrir_calendario,
            padx=15,
            pady=10
        )
        self.calendario_btn.pack()
        
        # Hover effect no calendário
        def on_enter(e):
            self.calendario_btn.config(bg='#2d4a5f')
        def on_leave(e):
            self.calendario_btn.config(bg='#1e3a5f')
        
        self.calendario_btn.bind("<Enter>", on_enter)
        self.calendario_btn.bind("<Leave>", on_leave)
        
        # Hora digital
        hora_str = agora.strftime("%H:%M")
        periodo = "AM" if agora.hour < 12 else "PM"
        
        hora_frame = tk.Frame(right_container, bg='#0f1419')
        hora_frame.pack(side='right')
        
        tk.Label(
            hora_frame,
            text=hora_str,
            font=('Consolas', 36, 'bold'),
            bg='#0f1419',
            fg='#00d4ff'
        ).pack(side='left')
        
        tk.Label(
            hora_frame,
            text=periodo,
            font=('Segoe UI', 18, 'bold'),
            bg='#0f1419',
            fg='#00d4ff'
        ).pack(side='left', padx=(5, 0), anchor='n', pady=(8, 0))
    
    def _abrir_calendario(self):
        """Abre pop-up do calendário com lembretes"""
        # Criar janela modal
        calendario_window = tk.Toplevel(self)
        calendario_window.title("Calendário e Lembretes")
        calendario_window.geometry("500x600")
        calendario_window.configure(bg='#1e293b')
        calendario_window.transient(self)
        calendario_window.grab_set()
        
        # Centralizar janela
        calendario_window.update_idletasks()
        x = (calendario_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (calendario_window.winfo_screenheight() // 2) - (600 // 2)
        calendario_window.geometry(f"500x600+{x}+{y}")
        
        # Header do calendário
        header = tk.Frame(calendario_window, bg='#1e293b')
        header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            header,
            text="📅 Calendário e Lembretes",
            font=('Segoe UI', 18, 'bold'),
            bg='#1e293b',
            fg='white'
        ).pack()
        
        # Calendário
        agora = datetime.now()
        self.mes_atual = agora.month
        self.ano_atual = agora.year
        
        # Navegação do mês
        nav_frame = tk.Frame(calendario_window, bg='#1e293b')
        nav_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        tk.Button(
            nav_frame,
            text="◀",
            font=('Segoe UI', 14, 'bold'),
            bg='#2563eb',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=lambda: self._navegar_mes(-1, calendario_window)
        ).pack(side='left')
        
        self.mes_label = tk.Label(
            nav_frame,
            text=f"{calendar.month_name[self.mes_atual]} {self.ano_atual}",
            font=('Segoe UI', 16, 'bold'),
            bg='#1e293b',
            fg='white'
        )
        self.mes_label.pack(side='left', expand=True)
        
        tk.Button(
            nav_frame,
            text="▶",
            font=('Segoe UI', 14, 'bold'),
            bg='#2563eb',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=lambda: self._navegar_mes(1, calendario_window)
        ).pack(side='right')
        
        # Grid do calendário
        self.calendario_frame = tk.Frame(calendario_window, bg='#1e293b')
        self.calendario_frame.pack(fill='x', padx=20, pady=10)
        
        self._criar_grid_calendario()
        
        # Área de lembretes
        lembretes_frame = tk.Frame(calendario_window, bg='#2d3748')
        lembretes_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            lembretes_frame,
            text="📝 Lembretes",
            font=('Segoe UI', 14, 'bold'),
            bg='#2d3748',
            fg='white'
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        # Lista de lembretes
        self.lembretes_text = tk.Text(
            lembretes_frame,
            height=8,
            font=('Segoe UI', 10),
            bg='#374151',
            fg='white',
            relief='flat',
            wrap='word'
        )
        self.lembretes_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Botão fechar
        tk.Button(
            calendario_window,
            text="Fechar",
            font=('Segoe UI', 12, 'bold'),
            bg='#6b7280',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=calendario_window.destroy,
            padx=20,
            pady=10
        ).pack(pady=(0, 20))
        
        self._atualizar_lembretes_display()
    
    def _navegar_mes(self, direcao, window):
        """Navega entre meses no calendário"""
        self.mes_atual += direcao
        if self.mes_atual > 12:
            self.mes_atual = 1
            self.ano_atual += 1
        elif self.mes_atual < 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        
        self.mes_label.config(text=f"{calendar.month_name[self.mes_atual]} {self.ano_atual}")
        self._criar_grid_calendario()
    
    def _criar_grid_calendario(self):
        """Cria o grid do calendário"""
        # Limpar grid anterior
        for widget in self.calendario_frame.winfo_children():
            widget.destroy()
        
        # Dias da semana
        dias_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
        for i, dia in enumerate(dias_semana):
            tk.Label(
                self.calendario_frame,
                text=dia,
                font=('Segoe UI', 10, 'bold'),
                bg='#374151',
                fg='white',
                width=6,
                height=2
            ).grid(row=0, column=i, padx=1, pady=1)
        
        # Dias do mês
        cal = calendar.monthcalendar(self.ano_atual, self.mes_atual)
        for semana_num, semana in enumerate(cal, 1):
            for dia_num, dia in enumerate(semana):
                if dia == 0:
                    continue
                
                data_str = f"{dia:02d}/{self.mes_atual:02d}/{self.ano_atual}"
                tem_lembrete = data_str in self.lembretes
                
                btn = tk.Button(
                    self.calendario_frame,
                    text=str(dia),
                    font=('Segoe UI', 10, 'bold' if tem_lembrete else 'normal'),
                    bg='#ef4444' if tem_lembrete else '#4b5563',
                    fg='white',
                    relief='flat',
                    cursor='hand2',
                    width=6,
                    height=2,
                    command=lambda d=dia: self._adicionar_lembrete(d)
                )
                btn.grid(row=semana_num, column=dia_num, padx=1, pady=1)
    
    def _adicionar_lembrete(self, dia):
        """Adiciona lembrete para um dia específico"""
        data_str = f"{dia:02d}/{self.mes_atual:02d}/{self.ano_atual}"
        
        # Janela para adicionar lembrete
        lembrete_window = tk.Toplevel(self)
        lembrete_window.title(f"Lembrete - {data_str}")
        lembrete_window.geometry("400x300")
        lembrete_window.configure(bg='#1e293b')
        lembrete_window.transient(self)
        lembrete_window.grab_set()
        
        # Centralizar
        lembrete_window.update_idletasks()
        x = (lembrete_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (lembrete_window.winfo_screenheight() // 2) - (300 // 2)
        lembrete_window.geometry(f"400x300+{x}+{y}")
        
        tk.Label(
            lembrete_window,
            text=f"📝 Lembrete para {data_str}",
            font=('Segoe UI', 14, 'bold'),
            bg='#1e293b',
            fg='white'
        ).pack(pady=20)
        
        # Campo de texto
        texto_frame = tk.Frame(lembrete_window, bg='#1e293b')
        texto_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        texto_entry = tk.Text(
            texto_frame,
            height=8,
            font=('Segoe UI', 11),
            bg='#374151',
            fg='white',
            relief='flat',
            wrap='word'
        )
        texto_entry.pack(fill='both', expand=True)
        
        # Se já existe lembrete, carregar
        if data_str in self.lembretes:
            texto_entry.insert('1.0', self.lembretes[data_str])
        
        # Botões
        btn_frame = tk.Frame(lembrete_window, bg='#1e293b')
        btn_frame.pack(fill='x', padx=20, pady=20)
        
        def salvar_lembrete():
            texto = texto_entry.get('1.0', 'end-1c').strip()
            if texto:
                self.lembretes[data_str] = texto
            elif data_str in self.lembretes:
                del self.lembretes[data_str]
            
            self._criar_grid_calendario()
            self._atualizar_lembretes_display()
            lembrete_window.destroy()
        
        tk.Button(
            btn_frame,
            text="💾 Salvar",
            font=('Segoe UI', 11, 'bold'),
            bg='#16a34a',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=salvar_lembrete,
            padx=20
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=('Segoe UI', 11),
            bg='#6b7280',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=lembrete_window.destroy,
            padx=20
        ).pack(side='left')
    
    def _atualizar_lembretes_display(self):
        """Atualiza a exibição dos lembretes"""
        if hasattr(self, 'lembretes_text'):
            self.lembretes_text.delete('1.0', 'end')
            
            if self.lembretes:
                for data, texto in sorted(self.lembretes.items()):
                    self.lembretes_text.insert('end', f"📅 {data}\n{texto}\n\n")
            else:
                self.lembretes_text.insert('end', "Nenhum lembrete cadastrado.")
    
    def _criar_grid_cards(self, parent):
        # Container do grid
        grid_container = tk.Frame(parent, bg='#0f1419')
        grid_container.pack(fill='both', expand=True)
        
        # Configurar grid 4x2
        for i in range(4):
            grid_container.grid_columnconfigure(i, weight=1, uniform="col")
        for i in range(2):
            grid_container.grid_rowconfigure(i, weight=1, uniform="row")
        
        # Criar cards com dados reais
        self.card_equipamentos = self._criar_card_equipamentos(grid_container, 0, 0)
        self.card_movimentacoes = self._criar_card_movimentacoes(grid_container, 0, 1)
        self.card_manutencao = self._criar_card_manutencao(grid_container, 0, 2)
        self.card_alertas = self._criar_card_alertas(grid_container, 0, 3)
        
        self.card_clientes = self._criar_card_clientes(grid_container, 1, 0)
        self.card_estoque = self._criar_card_estoque(grid_container, 1, 1)
        self.card_atividade = self._criar_card_atividade(grid_container, 1, 2)
        self.card_status = self._criar_card_status(grid_container, 1, 3)
    
    def _criar_card_base(self, parent, row, col, bg_color, title_line1, title_line2):
        # Frame do card com bordas arredondadas simuladas
        card_outer = tk.Frame(parent, bg='#0f1419')
        card_outer.grid(row=row, column=col, padx=12, pady=12, sticky='nsew')
        
        # Simular bordas arredondadas com múltiplas camadas
        # Camada externa (mais escura)
        outer_border = tk.Frame(card_outer, bg='#2a2a2a', relief='raised', bd=1)
        outer_border.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Camada média
        middle_border = tk.Frame(outer_border, bg='#3a3a3a', relief='raised', bd=1)
        middle_border.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Card principal
        card = tk.Frame(middle_border, bg=bg_color, relief='flat', bd=0)
        card.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Área interna
        card_inner = tk.Frame(card, bg=bg_color)
        card_inner.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(card_inner, bg=bg_color)
        title_frame.pack(fill='x', anchor='nw')
        
        tk.Label(
            title_frame,
            text=title_line1,
            font=('Segoe UI', 11, 'bold'),
            bg=bg_color,
            fg='white'
        ).pack(anchor='w')
        
        tk.Label(
            title_frame,
            text=title_line2,
            font=('Segoe UI', 9),
            bg=bg_color,
            fg='#b8c5d6'
        ).pack(anchor='w')
        
        # Área de conteúdo
        content_frame = tk.Frame(card_inner, bg=bg_color)
        content_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        return content_frame, card_inner
    
    def _criar_card_equipamentos(self, parent, row, col):
        content, card = self._criar_card_base(parent, row, col, '#1e3a5f', 'EQUIPAMENTOS', 'CADASTRADOS')
        
        icon_value_frame = tk.Frame(content, bg='#1e3a5f')
        icon_value_frame.pack(fill='x')
        
        tk.Label(
            icon_value_frame,
            text='📦',
            font=('Segoe UI', 32),
            bg='#1e3a5f'
        ).pack(side='left')
        
        self.equipamentos_valor = tk.Label(
            icon_value_frame,
            text='0',
            font=('Segoe UI', 28, 'bold'),
            bg='#1e3a5f',
            fg='#00ff88'
        )
        self.equipamentos_valor.pack(side='right')
        
        return content
    
    def _criar_card_movimentacoes(self, parent, row, col):
        content, card = self._criar_card_base(parent, row, col, '#2d4a5f', 'MOVIMENTAÇÕES', 'ESTE MÊS')
        
        icon_value_frame = tk.Frame(content, bg='#2d4a5f')
        icon_value_frame.pack(fill='x')
        
        tk.Label(
            icon_value_frame,
            text='🔄',
            font=('Segoe UI', 32),
            bg='#2d4a5f'
        ).pack(side='left')
        
        self.movimentacoes_valor = tk.Label(
            icon_value_frame,
            text='0',
            font=('Segoe UI', 28, 'bold'),
            bg='#2d4a5f',
            fg='#ffd700'
        )
        self.movimentacoes_valor.pack(side='right')
        
        return content
    
    def _criar_card_manutencao(self, parent, row, col):
        content, card = self._criar_card_base(parent, row, col, '#2d5f4a', 'EM MANUTENÇÃO', 'EQUIPAMENTOS')
        
        icon_value_frame = tk.Frame(content, bg='#2d5f4a')
        icon_value_frame.pack(fill='x')
        
        tk.Label(
            icon_value_frame,
            text='🔧',
            font=('Segoe UI', 32),
            bg='#2d5f4a'
        ).pack(side='left')
        
        self.manutencao_valor = tk.Label(
            icon_value_frame,
            text='0',
            font=('Segoe UI', 28, 'bold'),
            bg='#2d5f4a',
            fg='#ff9500'
        )
        self.manutencao_valor.pack(side='right')
        
        return content
    
    def _criar_card_alertas(self, parent, row, col):
        content, card = self._criar_card_base(parent, row, col, '#1e4a5f', 'SISTEMA', 'STATUS')
        
        icon_value_frame = tk.Frame(content, bg='#1e4a5f')
        icon_value_frame.pack(fill='x')
        
        tk.Label(
            icon_value_frame,
            text='✅',
            font=('Segoe UI', 32),
            bg='#1e4a5f'
        ).pack(side='left')
        
        self.alertas_valor = tk.Label(
            icon_value_frame,
            text='OK',
            font=('Segoe UI', 20, 'bold'),
            bg='#1e4a5f',
            fg='#00ff88'
        )
        self.alertas_valor.pack(side='right')
        
        return content
    
    def _criar_card_clientes(self, parent, row, col):
        content, card = self._criar_card_base(parent, row, col, '#2d5f3a', 'CLIENTES', 'CADASTRADOS')
        
        icon_value_frame = tk.Frame(content, bg='#2d5f3a')
        icon_value_frame.pack(fill='x')
        
        tk.Label(
            icon_value_frame,
            text='👥',
            font=('Segoe UI', 32),
            bg='#2d5f3a'
        ).pack(side='left')
        
        self.clientes_valor = tk.Label(
            icon_value_frame,
            text='0',
            font=('Segoe UI', 28, 'bold'),
            bg='#2d5f3a',
            fg='#00ff88'
        )
        self.clientes_valor.pack(side='right')
        
        return content
    
    def _criar_card_estoque(self, parent, row, col):
        content, card = self._criar_card_base(parent, row, col, '#5f3a2d', 'EM ESTOQUE', 'DISPONÍVEIS')
        
        icon_value_frame = tk.Frame(content, bg='#5f3a2d')
        icon_value_frame.pack(fill='x')
        
        tk.Label(
            icon_value_frame,
            text='📊',
            font=('Segoe UI', 32),
            bg='#5f3a2d'
        ).pack(side='left')
        
        self.estoque_valor = tk.Label(
            icon_value_frame,
            text='0',
            font=('Segoe UI', 28, 'bold'),
            bg='#5f3a2d',
            fg='#00d4ff'
        )
        self.estoque_valor.pack(side='right')
        
        return content
    
    def _criar_card_atividade(self, parent, row, col):
        content, card = self._criar_card_base(parent, row, col, '#3a4a5f', 'COM CLIENTES', 'EM USO')
        
        icon_value_frame = tk.Frame(content, bg='#3a4a5f')
        icon_value_frame.pack(fill='x')
        
        tk.Label(
            icon_value_frame,
            text='📤',
            font=('Segoe UI', 32),
            bg='#3a4a5f'
        ).pack(side='left')
        
        self.atividade_valor = tk.Label(
            icon_value_frame,
            text='0',
            font=('Segoe UI', 28, 'bold'),
            bg='#3a4a5f',
            fg='#ffd700'
        )
        self.atividade_valor.pack(side='right')
        
        return content
    
    def _criar_card_status(self, parent, row, col):
        content, card = self._criar_card_base(parent, row, col, '#5f4a2d', 'BANCO DE DADOS', 'TAMANHO')
        
        icon_value_frame = tk.Frame(content, bg='#5f4a2d')
        icon_value_frame.pack(fill='x')
        
        tk.Label(
            icon_value_frame,
            text='💾',
            font=('Segoe UI', 32),
            bg='#5f4a2d'
        ).pack(side='left')
        
        self.status_valor = tk.Label(
            icon_value_frame,
            text='0 KB',
            font=('Segoe UI', 16, 'bold'),
            bg='#5f4a2d',
            fg='#ffd700'
        )
        self.status_valor.pack(side='right')
        
        return content
    
    def _atualizar_dados(self):
        try:
            stats = self.db.get_estatisticas()
            
            self.equipamentos_valor.config(text=str(stats['total_equipamentos']))
            self.clientes_valor.config(text=str(stats['total_clientes']))
            
            em_estoque = stats['por_status'].get('Em Estoque', 0)
            com_cliente = stats['por_status'].get('Com o Cliente', 0)
            em_manutencao = stats['por_status'].get('Em Manutenção', 0)
            
            self.estoque_valor.config(text=str(em_estoque))
            self.atividade_valor.config(text=str(com_cliente))
            self.manutencao_valor.config(text=str(em_manutencao))
            
            movimentacoes_mes = self._contar_movimentacoes_mes()
            self.movimentacoes_valor.config(text=str(movimentacoes_mes))
            
            tamanho_db = self._get_db_size()
            self.status_valor.config(text=tamanho_db)
            
            if stats['total_equipamentos'] > 0:
                self.alertas_valor.config(text='OK', fg='#00ff88')
            else:
                self.alertas_valor.config(text='VAZIO', fg='#ff6b6b')
                
        except Exception as e:
            print(f"Erro ao atualizar dashboard: {e}")
            self.equipamentos_valor.config(text='--')
            self.clientes_valor.config(text='--')
            self.estoque_valor.config(text='--')
            self.atividade_valor.config(text='--')
            self.manutencao_valor.config(text='--')
            self.movimentacoes_valor.config(text='--')
            self.status_valor.config(text='--')
            self.alertas_valor.config(text='ERRO', fg='#ff6b6b')
    
    def _contar_movimentacoes_mes(self):
        try:
            cursor = self.db.conn.cursor()
            agora = datetime.now()
            inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            cursor.execute("""
                SELECT COUNT(*) FROM historico_posse 
                WHERE data_movimentacao >= ?
            """, (inicio_mes.isoformat(),))
            
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        except:
            return 0
    
    def _get_db_size(self):
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
    
    def atualizar(self):
        self._atualizar_dados()