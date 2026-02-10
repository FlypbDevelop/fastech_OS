import flet as ft
from core.game import Game
from core.board import Board
from core.player import Player


class ConnectFourApp:
    def __init__(self):
        self.game = Game()
        self.buttons = []
        self.info_text = None
        self.restart_button = None
        
    def create_board_view(self, page: ft.Page):
        """Create the game board UI"""
        # Create the board grid
        board_grid = ft.GridView(
            expand=True,
            runs_count=7,
            max_extent=60,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )
        
        # Create 42 buttons for the board (7x6)
        self.buttons = []
        for row in range(6):
            row_buttons = []
            for col in range(7):
                btn = ft.ElevatedButton(
                    text="",
                    width=50,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        padding=ft.padding.all(0)
                    ),
                    data={"row": row, "col": col}
                )
                btn.on_click = lambda e, r=row, c=col: self.drop_piece(e, r, c)
                board_grid.controls.append(btn)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        # Info text showing current player or winner
        self.info_text = ft.Text(
            value=f"Jogador {self.game.current_player.symbol}'s vez",
            size=20,
            weight=ft.FontWeight.BOLD
        )
        
        # Restart button
        self.restart_button = ft.ElevatedButton(
            text="Reiniciar Jogo",
            on_click=self.restart_game
        )
        
        # Main layout
        main_column = ft.Column(
            controls=[
                self.info_text,
                board_grid,
                self.restart_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        return main_column
    
    def drop_piece(self, e, row, col):
        """Handle piece dropping when a column button is clicked"""
        # Find the lowest available row in the selected column
        placed_row = self.game.board.get_lowest_empty_row(col)
        if placed_row != -1:
            # Place the piece
            self.game.board.place_piece(placed_row, col, self.game.current_player.symbol)
            
            # Update the button appearance
            color = "#FF0000" if self.game.current_player.symbol == "X" else "#FFFF00"
            self.buttons[placed_row][col].bgcolor = color
            self.buttons[placed_row][col].update()
            
            # Check for win or draw
            if self.game.check_winner(placed_row, col):
                self.info_text.value = f"Jogador {self.game.current_player.symbol} venceu!"
                self.info_text.update()
                self.disable_board()
            elif self.game.is_draw():
                self.info_text.value = "Empate!"
                self.info_text.update()
                self.disable_board()
            else:
                # Switch players
                self.game.switch_player()
                self.info_text.value = f"Jogador {self.game.current_player.symbol}'s vez"
                self.info_text.update()
    
    def disable_board(self):
        """Disable all buttons on the board"""
        for row in self.buttons:
            for btn in row:
                btn.disabled = True
                btn.update()
    
    def restart_game(self, e):
        """Restart the game"""
        self.game.reset()
        
        # Reset the board UI
        for row in range(6):
            for col in range(7):
                self.buttons[row][col].bgcolor = None
                self.buttons[row][col].disabled = False
                self.buttons[row][col].update()
        
        # Reset info text
        self.info_text.value = f"Jogador {self.game.current_player.symbol}'s vez"
        self.info_text.update()
    
    def main_view(self, page: ft.Page):
        """Main view setup"""
        page.title = "Conecta Quatro"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.padding = 20
        
        return self.create_board_view(page)


def main(page: ft.Page):
    app = ConnectFourApp()
    return app.main_view(page)


if __name__ == "__main__":
    ft.app(target=main)