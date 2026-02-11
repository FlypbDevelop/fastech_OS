"""
Aba Equipamentos - Gestão de equipamentos
NOTA: Este é um arquivo stub. O código completo será migrado do app.py
"""
import flet as ft
from gui.base_tab import BaseTab


class EquipamentosTab(BaseTab):
    """Aba de gestão de equipamentos"""
    
    def __init__(self, page, db, config, criar_equipamentos_original):
        super().__init__(page, db, config)
        # Temporariamente usa a função original do app.py
        self._criar_original = criar_equipamentos_original
    
    def build(self):
        """Constrói a interface de equipamentos"""
        # Temporariamente delega para a função original
        return self._criar_original()
