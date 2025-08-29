from pathlib import Path
from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, CenterMiddle
from textual.widgets import Footer

from idle_tui.widgets.characters import Character


class IdleApp(App):
    CSS_PATH = Path("assets/app.tcss")
    BINDINGS = [
        Binding("1", "shoot_p2", "Shoot P2"),
        Binding("2", "shoot_p1", "Shoot P1"),
        Binding("r", "reset", "Reset"),
        Binding("q", "app.quit", "Quit"),
    ]

    def compose(self):
        with Horizontal():
            with CenterMiddle(id="field_you"):
                yield Character(id="p1")
            with CenterMiddle(id="field_opponent"):
                yield Character(id="p2")
        yield Footer(show_command_palette=False)

    def action_shoot_p1(self):
        player = self.query_one("#p2", Character)
        target = player.find_opponent()
        if player.dead:
            player.im_dead()
            return
        if target:
            player.fire(target)

    def action_shoot_p2(self):
        player = self.query_one("#p1", Character)
        target = player.find_opponent()
        if player.dead:
            player.im_dead()
            return
        if target:
            player.fire(target)

    def action_reset(self):
        for player in self.query(Character):
            player.damage = 0
