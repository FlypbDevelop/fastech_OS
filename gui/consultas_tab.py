"""
Aba Consultas - Consultas e relatórios
NOTA: Este é um arquivo stub. O código completo será migrado do app.py
"""
import flet as ft
from gui.base_tab import BaseTab


class ConsultasTab(BaseTab):
    """Aba de consultas e relatórios"""
    
    def __init__(self, page, db, config, criar_consultas_original):
        super().__init__(page, db, config)
        # Temporariamente usa a função original do app.py
        self._criar_original = criar_consultas_original
    
    def build(self):
        """Constrói a interface de consultas"""
        # Temporariamente delega para a função original
        return self._criar_original()
