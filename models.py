import questionary
import rich
from rich.console import Console
class Questionary:
    def ask_for_text(self, question):
        answer = questionary.text(question).ask()
        return answer

    def ask_for_password(self, question):
        answer = questionary.password(question).ask()
        return answer

    def ask_for_confirmation(self, question):
        answer = questionary.confirm(question).ask()
        return answer

    def ask_selection_question(self, question, choices: list):
        answer = questionary.select(question, choices=choices,).ask()
        return answer

    def ask_checkbox_question(self, question, choices: list):
        answer = questionary.checkbox(question, choices=choices).ask()
        return answer


class Rich:
    def rich_print(self, text):
        rich.print(text)


    def table(self, columns:list, rows:list):
        console = Console()
        table = rich.table.Table(show_header=True, header_style="bold magenta")
        for column in columns:
            table.add_column(column)
        for row in rows:
            table.add_row(
                *row
            )
        console.print(table)
