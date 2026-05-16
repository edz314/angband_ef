"""
src/ui/tui_app.py
Main Textual Application for rendering the game world and UI.
"""
from textual.app import App, ComposeResult
from textual.widgets import Static, Footer
from textual.containers import Container, Horizontal
from textual.binding import Binding
from typing import List, Dict

class MapView(Static):
    """Custom widget to render the ASCII map grid."""
    
    def __init__(self, grid: List[List[str]], player_pos: tuple):
        super().__init__()
        self.grid = grid
        self.player_pos = player_pos
        
    def on_mount(self) -> None:
        self.refresh()

    def render(self) -> str:
        """Render the map to ASCII."""
        output = []
        # Simple Fog of War: Only show tiles near player or previously visited (simplified here)
        for y, row in enumerate(self.grid):
            line = ""
            for x, tile in enumerate(row):
                if (x, y) == self.player_pos:
                    line += "@" # Player
                else:
                    # Simple visibility check (Manhattan distance < 5)
                    dist = abs(x - self.player_pos[0]) + abs(y - self.player_pos[1])
                    if dist <= 4:
                        line += tile
                    elif dist <= 7:
                        line += "·" # Distant/Unexplored hint
                    else:
                        line += " " # Unseen
            output.append(line)
        return "\n".join(output)

class StatusPanel(Static):
    """Displays Player Stats."""
    
    def __init__(self, player_data: Dict):
        super().__init__()
        self.player = player_data
        
    def render(self) -> str:
        stats = [
            f"[bold]READING ROGUE[/bold]",
            "-------------------",
            f"HP: {self.player['hp']}/{self.player['max_hp']}",
            f"STA: {self.player['stamina']}/{self.player['max_stamina']}",
            f"Pleasure: {self.player['pleasure']}/100",
            f"AP: {self.player['ap']}",
            "-------------------",
            f"District: {self.player.get('district', 'Unknown')}"
        ]
        return "\n".join(stats)

class GameApp(App):
    """Main Game Loop and UI Controller."""
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("w|up", "move_up", "Up"),
        Binding("s|down", "move_down", "Down"),
        Binding("a|left", "move_left", "Left"),
        Binding("d|right", "move_right", "Right"),
    ]

    def __init__(self, initial_grid: List[List[str]], player_state: Dict):
        super().__init__()
        self.grid = initial_grid
        self.player_pos = (10, 5) # Initial spawn point (example)
        self.player_state = player_state
        
    def compose(self) -> ComposeResult:
        yield Container(
            StatusPanel(self.player_state),
            MapView(self.grid, self.player_pos),
            Footer()
        )

    def action_move_up(self):
        self._move_player(0, -1)
        
    def action_move_down(self):
        self._move_player(0, 1)
        
    def action_move_left(self):
        self._move_player(-1, 0)
        
    def action_move_right(self):
        self._move_player(1, 0)

    def _move_player(self, dx: int, dy: int):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Bounds check
        if not (0 <= new_y < len(self.grid) and 0 <= new_x < len(self.grid[0])):
            return

        target_tile = self.grid[new_y][new_x]
        
        # Collision logic
        if target_tile == '#':
            self.notify("Blocked by wall.")
            return
            
        # Hazard Logic (Example)
        if target_tile in ['~', 'G']:
            self.player_state['hp'] -= 5
            self.notify(f"Stepped on hazard! -5 HP")
            
        # Update Position
        self.player_pos = (new_x, new_y)
        
        # Refresh UI
        self.refresh()

if __name__ == "__main__":
    # Placeholder for testing TUI in isolation
    pass
        # Hazard Logic (Example)
        if target_tile in ['~', 'G']:
            self.player_state['hp'] -= 5
            self.notify(f"Stepped on hazard! -5 HP")
            
        # Update Position
        self.player_pos = (new_x, new_y)
        
        # Refresh UI
        self.refresh()

if __name__ == "__main__":
    # Placeholder for testing TUI in isolation
    pass