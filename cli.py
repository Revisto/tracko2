import click
from models import Files, Rich, Questionary, Auth, CLI, Requests

@click.group()
def main():
    pass


@main.command()
def setup(**kwargs):
    if Auth().is_user_logged_in():
        Rich().rich_print(":thumbs_up: Hip Hip Hooray, Everything Is Set Up!")
        return True
    answer = Questionary().ask_selection_question("🔎 Oh, You Are Not Logged In, You Want To ", ["Create A New Account.", "Log-in To My Account."])
    if "Log-in" in answer:
        return CLI().login_cli()
    else:
        return CLI().signup_cli()

@main.command()
def signout(**kwargs):
    if Auth().is_user_logged_in():
        Files().remove_api_key()
        Rich().rich_print("🥺 You Now Logged-Out! Hope To See You Soon...")
    else:
        Rich().rich_print("😧 You Were Not Logged-In!")

@main.command()
def all_shelves(**kwargs):
    return CLI().shelves()

@main.command()
def shelf(**kwargs):
    selected_shelf = CLI().choose_a_shelf()
    if selected_shelf is not False:
        CLI().shelves(selected_shelf)

@main.command()
def add(**kwargs):
    CLI().add_series_to_shelf()

@main.command()
def move(**kwargs):
    CLI().move_series()

if __name__ == '__main__':
    main()