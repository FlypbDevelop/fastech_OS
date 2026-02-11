"""
Aba Configurações - Configurações do sistema
NOTA: Este é um arquivo stub. O código completo será migrado do app.py
"""
import flet as ft
from gui.base_tab import BaseTab


class ConfiguracoesTab(BaseTab):
    """Aba de configurações do sistema"""
    
    def __init__(self, page, db, config, criar_configuracoes_original):
        super().__init__(page, db, config)
        # Temporariamente usa a função original do app.py
        self._criar_original = criar_configuracoes_original
    
    def build(self):
        """Constrói a interface de configurações"""
        # Temporariamente delega para a função original
        return self._criar_original()
