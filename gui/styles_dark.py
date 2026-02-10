"""
Estilos para tema escuro
"""

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

# Fontes (mesmas do tema claro)
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
    'bg': COLORS_DARK['bg_dark'],
    'fg': COLORS_DARK['text'],
    'insertbackground': COLORS_DARK['text'],
}

LABEL_STYLE = {
    'font': FONTS['normal'],
    'bg': COLORS_DARK['white'],
    'fg': COLORS_DARK['text'],
}

TITLE_STYLE = {
    'font': FONTS['title'],
    'bg': COLORS_DARK['white'],
    'fg': COLORS_DARK['text'],
}

# Padding padrão (mesmo do tema claro)
PADDING = {
    'small': 5,
    'medium': 10,
    'large': 20,
}
