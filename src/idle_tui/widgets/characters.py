from __future__ import annotations
import random
from typing import TYPE_CHECKING
from uuid import uuid1

if TYPE_CHECKING:
    from idle_tui.app import IdleApp

from textual.reactive import reactive
from textual.geometry import Offset
from textual.widgets import Label
from textual.containers import CenterMiddle, Horizontal


class Character(Label):
    app: "IdleApp"
    max_hp: reactive[int] = reactive(20)
    damage: reactive[int] = reactive(0)

    def on_mount(self):
        self.styles.background = "blue"
        self.update(
            f" {self.id}"
            "\n ( )"
            "\n-| |-"
            "\n / \\ "
            f"\n{max(self.max_hp - self.damage, 0)}/{self.max_hp}"
        )

    def find_opponent(self):
        for field in self.query_ancestor(Horizontal).query_children(CenterMiddle):
            if not field.id == self.parent.id:
                opponents = field.query_children(Character)
                for opponent in opponents:
                    return opponent

    def fire(self, opponent: Character):
        self.app.mount(Projectile(self, opponent))

    def inflict_damage(self, amount: int):
        self.app.mount(Damage(target=self, damage=amount))
        self.damage += amount

    def watch_damage(self):
        if self.damage >= self.max_hp:
            match self.parent.id:
                case _ if "you" in self.parent.id:
                    self.update(f" {self.id}\n _(xx)|-|\\_\n{0}/{self.max_hp}")
                case _:
                    self.update(f" {self.id}\n _/|-|(xx)_\n{0}/{self.max_hp}")
        else:
            self.update(
                f" {self.id}"
                "\n ( )"
                "\n-| |-"
                "\n / \\ "
                f"\n{self.max_hp - self.damage}/{self.max_hp}"
            )

    @property
    def screen_offset(self):
        return self.screen.get_offset(self)

    @property
    def dead(self):
        return self.damage >= self.max_hp

    def im_dead(self):
        self.notify(
            title="This is not `The Walking Dead`",
            message="I am [red]dead[/] I cant shoot!",
            timeout=1.5,
            severity="error",
        )


class Projectile(Label):
    app: "IdleApp"
    DEFAULT_CSS = """
    Projectile {
        layer:above;
        background:green;

    }
    """

    def __init__(
        self, start_char: Character, target_char: Character, *args, **kwargs
    ) -> None:
        self.start = self.app.screen.get_offset(start_char)
        self.target_char = target_char
        self.target = self.app.screen.get_offset(target_char)
        super().__init__(*args, **kwargs)

    def on_mount(self):
        if self.start.x < self.target.x:
            self.update(">>-->")
        else:
            self.update("<--<<")

        self.offset = self.start
        self.styles.layer = f"{uuid1()}"
        layers = [layer for layer in self.screen.styles.layers]
        layers.append(self.styles.layer)
        self.screen.styles.layers = tuple(layer for layer in layers)
        self.fly()

    def fly(self):
        self.animate(
            attribute="offset",
            value=self.target,
            duration=0.5,
            easing="linear",
            on_complete=self.hit_target,
        )

    def hit_target(self):
        self.remove()
        layers = [
            layer for layer in self.screen.styles.layers if layer != self.styles.layer
        ]
        self.screen.styles.layers = tuple(layers)
        self.target_char.inflict_damage(3)


class Damage(Label):
    app: "IdleApp"
    DEFAULT_CSS = """
    Damage {
        layer:above;
        background:red;

    }
    """

    def __init__(self, target: Character, damage: int, *args, **kwargs) -> None:
        self.target = target
        self.damage = damage
        super().__init__(*args, **kwargs)

    def on_mount(self):
        self.styles.layer = f"{uuid1()}"
        layers = [layer for layer in self.screen.styles.layers]
        layers.append(self.styles.layer)
        self.screen.styles.layers = tuple(layer for layer in layers)
        self.update(f"{self.damage}")
        self.random_width = random.choice(list(range(self.target.region.width)))
        self.offset = Offset(
            self.target.screen_offset.x + self.random_width, self.target.screen_offset.y
        )
        self.fly_up()

    def fly_up(self):
        self.animate(
            attribute="offset",
            value=Offset(
                self.target.screen_offset.x + self.random_width,
                self.target.screen_offset.y - 5,
            ),
            duration=1,
            on_complete=self.fizzle,
        )

    def fizzle(self):
        layers = [
            layer for layer in self.screen.styles.layers if layer != self.styles.layer
        ]
        self.screen.styles.layers = tuple(layers)
        self.remove()
