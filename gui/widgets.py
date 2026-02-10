"""
Widgets customizados reutilizáveis
"""

import tkinter as tk
from tkinter import ttk
from gui.styles import COLORS, FONTS, BUTTON_STYLE, ENTRY_STYLE


class CustomButton(tk.Button):
    """Botão customizado com estilo"""
    
    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        # Define cores baseado no estilo
        if style == 'primary':
            bg = COLORS['primary']
            fg = COLORS['white']
            active_bg = COLORS['primary_dark']
        elif style == 'success':
            bg = COLORS['success']
            fg = COLORS['white']
            active_bg = '#15803d'
        elif style == 'danger':
            bg = COLORS['danger']
            fg = COLORS['white']
            active_bg = '#b91c1c'
        else:
            bg = COLORS['bg_dark']
            fg = COLORS['text']
            active_bg = COLORS['border']
        
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=COLORS['white'],
            **BUTTON_STYLE,
            **kwargs
        )


class CustomEntry(tk.Entry):
    """Entry customizado com placeholder"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(
            parent,
            **ENTRY_STYLE,
            **kwargs
        )
        
        self.placeholder = placeholder
        self.placeholder_active = False
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=COLORS['text_light'])
            self.placeholder_active = True
            
            self.bind('<FocusIn>', self._on_focus_in)
            self.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.config(fg=COLORS['text'])
            self.placeholder_active = False
    
    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=COLORS['text_light'])
            self.placeholder_active = True
    
    def get_value(self):
        """Retorna o valor real (sem placeholder)"""
        if self.placeholder_active:
            return ""
        return self.get()


class LabeledEntry(tk.Frame):
    """Frame com label e entry"""
    
    def __init__(self, parent, label_text, placeholder="", required=False, **kwargs):
        super().__init__(parent, bg=COLORS['white'])
        
        # Label
        label = tk.Label(
            self,
            text=label_text + (" *" if required else ""),
            font=FONTS['normal'],
            bg=COLORS['white'],
            fg=COLORS['text'] if not required else COLORS['danger']
        )
        label.pack(anchor='w', pady=(0, 5))
        
        # Entry
        self.entry = CustomEntry(self, placeholder=placeholder, **kwargs)
        self.entry.pack(fill='x')
    
    def get(self):
        return self.entry.get_value()
    
    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.entry.placeholder_active = False
        self.entry.config(fg=COLORS['text'])
    
    def clear(self):
        self.entry.delete(0, tk.END)
        if self.entry.placeholder:
            self.entry.insert(0, self.entry.placeholder)
            self.entry.config(fg=COLORS['text_light'])
            self.entry.placeholder_active = True


class SearchBar(tk.Frame):
    """Barra de busca com ícone"""
    
    def __init__(self, parent, placeholder="Buscar...", on_search=None, **kwargs):
        super().__init__(parent, bg=COLORS['white'])
        
        # Entry de busca
        self.entry = CustomEntry(self, placeholder=placeholder, width=40)
        self.entry.pack(side='left', padx=(0, 10))
        
        # Botão de busca
        self.btn_search = CustomButton(
            self,
            text="🔍 Buscar",
            command=on_search,
            style='primary'
        )
        self.btn_search.pack(side='left')
        
        # Bind Enter key
        self.entry.bind('<Return>', lambda e: on_search() if on_search else None)
    
    def get(self):
        return self.entry.get_value()
    
    def clear(self):
        self.entry.delete(0, tk.END)


class StatusLabel(tk.Label):
    """Label para mensagens de status"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            text="",
            font=FONTS['normal'],
            bg=COLORS['white'],
            **kwargs
        )
    
    def show_success(self, message):
        self.config(text=f"✓ {message}", fg=COLORS['success'])
        self.after(3000, lambda: self.config(text=""))
    
    def show_error(self, message):
        self.config(text=f"✗ {message}", fg=COLORS['danger'])
        self.after(5000, lambda: self.config(text=""))
    
    def show_info(self, message):
        self.config(text=f"ℹ {message}", fg=COLORS['primary'])
        self.after(3000, lambda: self.config(text=""))


class DataTable(tk.Frame):
    """Tabela de dados com Treeview"""
    
    def __init__(self, parent, columns, column_widths=None, **kwargs):
        super().__init__(parent, bg=COLORS['white'])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        self.tree.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.tree.yview)
        
        # Configurar colunas
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            width = column_widths[i] if column_widths and i < len(column_widths) else 100
            self.tree.column(col, width=width)
        
        # Estilo zebrado
        self.tree.tag_configure('oddrow', background=COLORS['bg'])
        self.tree.tag_configure('evenrow', background=COLORS['white'])
    
    def insert_row(self, values, tags=None):
        """Insere uma linha na tabela"""
        return self.tree.insert('', 'end', values=values, tags=tags)
    
    def clear(self):
        """Limpa todas as linhas"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_selected(self):
        """Retorna o item selecionado"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])
        return None
    
    def populate(self, data):
        """Popula a tabela com dados"""
        self.clear()
        for i, row in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.insert_row(row, tags=(tag,))
