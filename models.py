import questionary


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