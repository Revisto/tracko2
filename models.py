import questionary
import rich
from rich.console import Console
import os.path
import pathlib
import requests
from os import remove
import socket


def is_internet_connected(func):
    def is_internet_connected_(*args, **kwargs):
        if General().is_internet_connected() is False:
            Rich().rich_print("🌐 It Seems Like You're Not Connected To The Internet. Please Try Again Later...")
            return False
        return func(*args, **kwargs)
    return is_internet_connected_

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
        answer = questionary.select(question, choices=choices).ask()
        return answer

    def ask_checkbox_question(self, question, choices: list):
        answer = questionary.checkbox(question, choices=choices).ask()
        return answer

class Requests:
    def __init__(self):
        self.base_url = "http://127.0.0.1:1287"
        self.login_request_url = f"{self.base_url}/api/login"
        self.signup_request_url = f"{self.base_url}/api/signup"
        self.is_username_unique_request_url = f"{self.base_url}/api/is_username_unique"


    @is_internet_connected
    def login_request(self, username, password):
        login_request = requests.post(self.login_request_url, data={'username': username, 'password': password})
        login_request_json = login_request.json()
        if login_request.status_code == 200 and login_request_json["logged_in"] is True:
            Files().write_api_key_text(login_request_json["api_key"])
            return True
        return False

    @is_internet_connected
    def signup_request(self, username, password):
        signup_request = requests.post(self.signup_request_url, data={'username': username, 'password': password})
        signup_request_json = signup_request.json()
        if signup_request.status_code == 200 and signup_request_json["logged_in"] is True:
            Files().write_api_key_text(signup_request_json["api_key"])
            return True
        return False

    @is_internet_connected
    def is_username_unique(self, username):
        request = requests.post(self.is_username_unique_request_url, data={'username': username})
        request_json = request.json()
        if request.status_code == 200 and request_json["is_it_unique"] is True:
            return True
        return False
class Auth:
    def is_user_logged_in(self):
        if Files().does_it_exist(api_key_path):
            return True
        return False

class CLI:

    @is_internet_connected
    def login_cli(self):
        Rich().rich_print("📒 Alright, Alright, Alright. Let's Log-In to your account.")
        username = Questionary().ask_for_text("👤 Please Enter Your Username: ")
        password = Questionary().ask_for_password("🔑 Please Enter Your Password: ")
        console = Console()   
        with console.status("[bold green]Loggin in...") as status:
            if Requests().login_request(username, password):
                Rich().rich_print("🦄 Yoo hoo, You Are Logged-In Now.")
                return True
            else:
                Rich().rich_print("😔 Awwww, Log-In Failed.")
                return False

    @is_internet_connected
    def signup_cli(self):
        Rich().rich_print("📒 Alright, Alright, Alright. Let's Create an account for you.")
        
        username = Questionary().ask_for_text("👤 Please Enter Your Username: ")
        while Requests().is_username_unique(username) is False:
            username = Questionary().ask_for_text(f"👤 '{username}' Is Already Taken, Please Enter Your Username: ")

        password = Questionary().ask_for_password("🔑 Please Enter Your Password: ")
        password_confirmation = Questionary().ask_for_password("🔑 Please Enter Your Password Again: ")
        if password_confirmation != password:
            Rich().rich_print("😮 Oh. The Passwords Are Not The Same, Quitting...")
            return False
        console = Console()   
        with console.status("[bold green]Signing-Up...") as status:
            if Requests().signup_request(username, password):
                Rich().rich_print("🦄 Yoo hoo, Your Account Is Created And You Are Logged-In Now.")
            else:
                Rich().rich_print("😔 Awwww, Sign-Up Failed.")

class Rich:
    def rich_print(self, text, style="magenta"):
        console = Console()
        console.print(text, style=style)


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


class Files:
    def write_api_key_text(self, key):
        with open(api_key_path, "w") as file:
            file.write(str(key))
            file.close()
        return True

    def current_path(self):
        return pathlib.Path(__file__).parent.absolute()

    def does_it_exist(self, path):
        return os.path.isfile(path)
    
    def read_file(self, path):
        if Files().does_it_exist(path) is True:
            file = open(path, "r")
            return file.read()
        return False

    def remove_api_key(self):
        remove(api_key_path)


class General:
    def is_internet_connected(self):
        try:
            socket.create_connection(("1.1.1.1", 53))
            return True
        except OSError:
            pass
        return False

api_key_path = f"{Files().current_path()}/.tracko_api_key"