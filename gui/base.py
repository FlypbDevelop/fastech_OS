"""
Classe base para as abas do sistema
"""
import flet as ft


class BaseTab:
    """Classe base para todas as abas"""

    # Design tokens
    BORDER_RADIUS = 10
    SPACING = 10
    PADDING = 20
    BODY_SIZE = 14
    TITLE_SIZE = 18
    SMALL_SIZE = 12
    CAPTION_SIZE = 10
    H1_SIZE = 32
    H2_SIZE = 24
    H3_SIZE = 18
    PRIMARY_COLOR = ft.Colors.BLUE_700
    SECONDARY_COLOR = ft.Colors.BLUE_400
    ACCENT_COLOR = ft.Colors.AMBER_600

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

    def criar_dialogo_confirmacao(
        self,
        titulo: str,
        mensagem: str,
        on_confirmar,
        on_cancelar=None,
        texto_confirmar: str = "Confirmar",
        texto_cancelar: str = "Cancelar",
        estilo_confirmar=None,
    ) -> ft.AlertDialog:
        """
        Cria, abre e retorna um ft.AlertDialog padronizado.
        Atribui a self.page.dialog, define open=True e chama self.page.update().
        Se on_cancelar não for fornecido, usa callback padrão que fecha o diálogo.
        """
        def _fechar_dialogo(e):
            self.page.dialog.open = False
            self.page.update()

        _on_cancelar = on_cancelar if on_cancelar is not None else _fechar_dialogo

        dialogo = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(mensagem),
            actions=[
                ft.TextButton(texto_cancelar, on_click=_on_cancelar),
                ft.FilledButton(
                    texto_confirmar,
                    on_click=on_confirmar,
                    style=estilo_confirmar,
                ),
            ],
        )

        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

        return dialogo

    def criar_container_secao(
        self,
        content,
        padding=None,
        border_radius=None,
        bgcolor=None,
    ) -> ft.Container:
        """
        Retorna ft.Container com defaults derivados dos design tokens.
        padding default: self.PADDING
        border_radius default: self.BORDER_RADIUS
        bgcolor default: self.get_bg_color()
        """
        return ft.Container(
            content=content,
            padding=padding if padding is not None else self.PADDING,
            border_radius=border_radius if border_radius is not None else self.BORDER_RADIUS,
            bgcolor=bgcolor if bgcolor is not None else self.get_bg_color(),
        )

    def criar_linha_tabela_acoes(
        self,
        acoes: list,
    ) -> ft.Row:
        """
        Retorna ft.Row com um ft.TextButton por tupla em acoes.
        Cada botão usa icone como texto, tooltip como tooltip e callback como on_click.
        """
        botoes = [
            ft.TextButton(content=ft.Text(icone), tooltip=tooltip, on_click=callback)
            for icone, tooltip, callback in acoes
        ]
        return ft.Row(controls=botoes)

    def build(self):
        """Método abstrato que deve ser implementado pelas subclasses"""
        raise NotImplementedError("Subclasses devem implementar o método build()")
