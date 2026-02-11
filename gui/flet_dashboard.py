import flet as ft
from datetime import datetime
import random
import asyncio


class FletDashboard(ft.Container):
    def __init__(self):
        super().__init__()
        self.cards = []
        
    def create_card(self, title_line1, title_line2, value, icon, color):
        """Create a dashboard card with rounded corners and animated icon"""
        # Animated icon container
        animated_icon = ft.Container(
            content=ft.Icon(
                icon,
                size=40,
                color=color
            ),
            animate_scale=ft.animation.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
            scale=ft.transform.Scale(1.0)
        )
        
        # Value text
        value_text = ft.Text(
            value,
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE
        )
        
        # Title texts
        title1 = ft.Text(title_line1, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        title2 = ft.Text(title_line2, size=12, color=ft.colors.GREY_400)
        
        # Card content
        content = ft.Column(
            [
                ft.Row([title1], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([title2], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=15, color="transparent"),
                ft.Row(
                    [
                        animated_icon,
                        ft.Container(width=10),  # Spacer
                        ft.Column([value_text], alignment=ft.MainAxisAlignment.END, spacing=0)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            spacing=5
        )
        
        # Create the card container with rounded corners
        card = ft.Container(
            content=content,
            width=200,
            height=150,
            padding=20,
            bgcolor=color + "20",  # Lighter background with transparency
            border_radius=15,  # Rounded corners
            border=ft.border.all(1, color + "40"),  # Subtle border
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[color + "10", color + "30"]
            ),
            ink=True,  # Enable ripple effect on click
            on_click=lambda e: self.animate_card(animated_icon),
            tooltip=f"Clique para animar o card de {title_line1.lower()}"
        )
        
        return card
    
    def animate_card(self, icon_container):
        """Animate the icon when card is clicked"""
        # Scale animation
        icon_container.scale = ft.transform.Scale(1.2)
        icon_container.update()
        
        # Wait a bit then return to original size
        self.page.run_task(lambda: self.reset_animation(icon_container))
    
    async def reset_animation(self, icon_container):
        """Reset the animation after a delay"""
        await asyncio.sleep(0.3)  # Wait 300ms
        icon_container.scale = ft.transform.Scale(1.0)
        icon_container.update()
    
    def build(self):
        return self.create_dashboard_content()
    
    def create_dashboard_content(self):
        # Header with greeting and date/time
        now = datetime.now()
        hour = now.hour
        
        if hour < 12:
            greeting = "Bom dia - Seja Bem vindo(a)"
        elif hour < 18:
            greeting = "Boa tarde - Seja Bem vindo(a)"
        else:
            greeting = "Boa noite - Seja Bem vindo(a)"
        
        # Create header
        header = ft.Row(
            [
                ft.Text(greeting, size=18, color=ft.colors.GREY_500),
                ft.VerticalDivider(width=50),
                ft.Column([
                    ft.Text(now.strftime("%d/%m/%Y"), size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(now.strftime("%H:%M"), size=24, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN)
                ])
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        # Create dashboard cards
        cards_row1 = ft.Row(
            [
                self.create_card("EQUIPAMENTOS", "CADASTRADOS", "0", ft.icons.DESKTOP_WINDOWS, ft.colors.BLUE),
                self.create_card("MOVIMENTAÇÕES", "HOJE", "0", ft.icons.SWAP_HORIZ, ft.colors.GREEN),
                self.create_card("MANUTENÇÃO", "PENDENTE", "0", ft.icons.BUILD, ft.colors.ORANGE),
                self.create_card("ALERTAS", "ATIVOS", "0", ft.icons.NOTIFICATION_IMPORTANT, ft.colors.RED),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=20
        )
        
        cards_row2 = ft.Row(
            [
                self.create_card("CLIENTES", "CADASTRADOS", "0", ft.icons.PEOPLE, ft.colors.PURPLE),
                self.create_card("ESTOQUE", "TOTAL", "0", ft.icons.INVENTORY_2, ft.colors.INDIGO),
                self.create_card("ATIVIDADE", "RECENTE", "0", ft.icons.SHOW_CHART, ft.colors.TEAL),
                self.create_card("STATUS", "GERAL", "0", ft.icons.INFO, ft.colors.AMBER),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=20
        )
        
        # Main layout
        main_layout = ft.Column(
            [
                header,
                ft.Divider(height=40, color="transparent"),
                cards_row1,
                ft.Divider(height=20, color="transparent"),
                cards_row2
            ],
            expand=True
        )
        
        return main_layout


def main(page: ft.Page):
    page.title = "Dashboard Moderno com Flet"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 40
    
    # Create and add the dashboard
    dashboard = FletDashboard()
    page.add(dashboard)
    
    # Update the page reference for animations after adding to page
    dashboard.page = page


if __name__ == "__main__":
    ft.app(target=main, port=8555)