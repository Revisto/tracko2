import click
from models import Files, Rich, Questionary, Auth

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
        return Auth().login_cli()
    else:
        return Auth().signup_cli()

@main.command()
def signout(**kwargs):
    if Auth().is_user_logged_in():
        Files().remove_api_key()
        Rich().rich_print("🥺 You Now Logged-Out! Hope To See You Soon...")
    else:
        Rich().rich_print("😧 You Were Not Logged-In!")



if __name__ == '__main__':
    main()