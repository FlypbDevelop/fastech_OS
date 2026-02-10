"""
Estilos e configurações visuais para a interface
"""

import json
import os

# Carrega tema da configuração
def _carregar_tema():
    """Carrega tema das configurações"""
    tema = 'claro'  # Padrão
    
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                tema = config.get('tema', 'claro')
        except:
            pass
    
    return tema

TEMA_ATUAL = _carregar_tema()

# Cores do tema claro
COLORS_LIGHT = {
    'primary': '#2563eb',      # Azul principal
    'primary_dark': '#1e40af', # Azul escuro
    'success': '#16a34a',      # Verde sucesso
    'danger': '#dc2626',       # Vermelho erro
    'warning': '#ea580c',      # Laranja aviso
    'bg': '#f8fafc',          # Fundo claro
    'bg_dark': '#e2e8f0',     # Fundo escuro
    'text': '#1e293b',        # Texto principal
    'text_light': '#64748b',  # Texto secundário
    'border': '#cbd5e1',      # Bordas
    'white': '#ffffff',       # Branco
}

# Cores do tema escuro
COLORS_DARK = {
    'primary': '#3b82f6',      # Azul mais claro
    'primary_dark': '#2563eb', # Azul médio
    'success': '#22c55e',      # Verde mais claro
    'danger': '#ef4444',       # Vermelho mais claro
    'warning': '#f97316',      # Laranja mais claro
    'bg': '#1e293b',          # Fundo escuro
    'bg_dark': '#0f172a',     # Fundo mais escuro
    'text': '#f1f5f9',        # Texto claro
    'text_light': '#94a3b8',  # Texto secundário
    'border': '#334155',      # Bordas
    'white': '#1e293b',       # "Branco" = fundo escuro
}

# Seleciona cores baseado no tema
COLORS = COLORS_DARK if TEMA_ATUAL == 'escuro' else COLORS_LIGHT

# Fontes
FONTS = {
    'title': ('Segoe UI', 16, 'bold'),
    'subtitle': ('Segoe UI', 12, 'bold'),
    'normal': ('Segoe UI', 10),
    'small': ('Segoe UI', 9),
    'button': ('Segoe UI', 10, 'bold'),
}

# Configurações de widgets
BUTTON_STYLE = {
    'font': FONTS['button'],
    'relief': 'flat',
    'cursor': 'hand2',
    'padx': 20,
    'pady': 8,
}

ENTRY_STYLE = {
    'font': FONTS['normal'],
    'relief': 'solid',
    'borderwidth': 1,
}

LABEL_STYLE = {
    'font': FONTS['normal'],
    'bg': COLORS['white'],
}

TITLE_STYLE = {
    'font': FONTS['title'],
    'bg': COLORS['white'],
    'fg': COLORS['text'],
}

# Padding padrão
PADDING = {
    'small': 5,
    'medium': 10,
    'large': 20,
}
