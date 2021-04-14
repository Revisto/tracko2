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
    shelf_names = []
    request_response = Requests().get_all_shelves()
    if request_response["status"] is True and request_response["unauthorized"] is False:
        for shelf_name in request_response["shelves"]:
            shelf_names.append(shelf_name)
        selected_shelf = Questionary().ask_selection_question("Which Shelf?", shelf_names)
        CLI().shelves(selected_shelf)
        return True
    if request_response["status"] is True and request_response["unauthorized"] is True:
        Rich().rich_print("🤺 Oh, It Seems Like Your Api-Key Is Not Valid, Try 'tracko signout' And Then 'tracko setup'")
        return True
    Rich().rich_print("🌐 Unknown Problem, Please Check Your Internet Connection.")

if __name__ == '__main__':
    main()