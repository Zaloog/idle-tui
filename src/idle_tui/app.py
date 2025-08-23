from pathlib import Path
from textual.app import App
from textual.events import Key
from textual.containers import Horizontal, CenterMiddle

from idle_tui.widgets.characters import Character


class IdleApp(App):
    CSS_PATH = Path("assets/app.tcss")

    def compose(self):
        with Horizontal():
            with CenterMiddle(id="field_you"):
                yield Character(id="p1")
            with CenterMiddle(id="field_opponent"):
                yield Character(id="p2")

    def on_key(self, event: Key):
        match event.key:
            case "1":
                player = self.query_one("#p1", Character)
                target = player.find_opponent()
                if target:
                    player.fire(target)
            case "2":
                player = self.query_one("#p2", Character)
                target = player.find_opponent()
                if target:
                    player.fire(target)
            case "r":
                for player in self.query(Character):
                    player.damage = 0
            case _:
                pass
