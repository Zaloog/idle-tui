from os import system
from textual.app import App
from textual.binding import Binding
from textual.widgets import TextArea, Footer

class TestApp(App):
    BINDINGS = [
        Binding("ctrl+j", "open_editor", "Editor")
    ]
    def compose(self):
        yield TextArea(read_only=True)
        yield Footer()

    def on_mount(self):
        textarea = self.query_one(TextArea)
        textarea.styles.border = "tall", "red"

        self.read_file()

    def action_open_editor(self):
        with self.suspend():
            system("nvim pyproject.toml")
        self.read_file()

    def read_file(self):
        with open("pyproject.toml") as file:
            content = file.read()

        self.query_one(TextArea).text = content



if __name__ == "__main__":
    app = TestApp()
    app.run()
