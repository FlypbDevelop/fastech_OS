"""
Classe base para as abas do sistema
"""
import flet as ft


class BaseTab:
    """Classe base para todas as abas"""
    
    def __init__(self, page: ft.Page, db, config):
        self.page = page
        self.db = db
        self.config = config
    
    def get_adaptive_color(self, dark_color, light_color):
        """Retorna cor adaptativa baseada no tema atual"""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            return light_color
        return dark_color
    
    def get_bg_color(self):
        """Retorna cor de fundo adaptativa"""
        return self.get_adaptive_color(ft.Colors.BLUE_GREY_900, ft.Colors.GREY_100)
    
    def get_text_color(self):
        """Retorna cor de texto adaptativa"""
        return self.get_adaptive_color(ft.Colors.WHITE, ft.Colors.BLACK)
    
    def get_secondary_text_color(self):
        """Retorna cor de texto secundário adaptativa"""
        return self.get_adaptive_color(ft.Colors.GREY_400, ft.Colors.GREY_700)
    
    def build(self):
        """Método abstrato que deve ser implementado pelas subclasses"""
        raise NotImplementedError("Subclasses devem implementar o método build()")
