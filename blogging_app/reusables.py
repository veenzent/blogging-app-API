import csv
from .models import Articles
from blogging_app.auth import auth_handler


UsersDB_header = ["id", "username", "first_name", "last_name", "email", "password", "bio", "website", "social_media.twitter", "social_media.facebook", "social_media.instagam", "last_updated_at", "posts", "total_posts"]

article_header = ["title", "author", "content", "date_published"]

# get total users in database
def get_total_users() -> int:
    """
    Returns the total number of users in the UsersDB.csv file.

    Parameters:
    None

    Returns:
    int: The total number of users in the UsersDB.csv file.
    """
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        total_users = len(list(reader))
    return total_users

def username_in_DB(username: str) -> bool:
    """
    Checks if the given username exists in the UsersDB.csv file.

    Parameters:
        username (str): The username to be checked.

    Returns:
        bool: True if the username exists in the database, False otherwise.
    """
    with open("blogging_app/UsersDB.csv", ) as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1]:
                print(user[1])
                return True
    return False

def authenticate_user(username: str, password: str):
    hashed_password = auth_handler.get_password_hash(password)
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1] and auth_handler.verify_password(password, hashed_password):
                return user
        return None

def email_in_DB(email: str) -> bool:
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if email == user[4]:
                return True
    return False

def get_user_signup_details(username: str) -> list:
    """
    Retrieves the signup details of a user based on their username.

    Args:
        username (str): The username of the user to retrieve signup details for.

    Returns:
        list: A list containing the signup details of the user. The list contains the following elements in order:
            - User ID (str)
            - Username (str)
            - First Name (str)
            - Last Name (str)
            - Email (str)
            - Password (str)

        Returns None if no user with the given username is found.
    """
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1]:
                signup_details = [user[0], user[1], user[2], user[3], user[4], user[5]]
                return signup_details

def add_article_to_DB(article):
    """
    Add an article to the database.

    Parameters:
        article (Article): The article object to be added.

    Returns:
        None
    """
    with open("blogging_app/all_articles.csv", "a", newline="") as all_articles:
        writer = csv.writer(all_articles)
        writer.writerow([article.title, article.author, article.content, article.date_published])
    return

def add_user_to_DB(user: list):
    """
    Adds a user to the UsersDB.csv file.

    Parameters:
    - user (list): A list containing the user information to be added to the database.

    Returns:
    - None
    """
    with open("blogging_app/UsersDB.csv", "a", newline="") as UsersDB:
        writer = csv.writer(UsersDB)
        writer.writerow(user)
    return

def find_article_by_title(title: str) -> list:
    """
    Find an article by its title in a CSV file.

    Parameters:
        title (str): The title of the article to search for.

    Returns:
        list: The article matching the given title, or None if no match is found.
    """
    with open("blogging_app/all_articles.csv", "r") as all_articles:
        reader = csv.reader(all_articles)
        next(reader)
        for article in reader:
            if title == article[0]:
                return article
            
def all_articles_cache() -> list:
    """
    Reads the contents of the 'all_articles.csv' file and returns a list of all articles.

    Parameters:
    None

    Returns:
    list: A list of all articles, where each article is represented as a list of strings.
    """
    with open("blogging_app/all_articles.csv", "r") as all_articles:
        reader = csv.reader(all_articles)
        next(reader)
        return list(reader)
    
def all_users_cache() -> list:
    """
    Reads the user data from the UsersDB.csv file and returns a list of all users.

    :return: A list of all users.
    :rtype: list
    """
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        users = list(reader)
        return users
    
def get_articles_by_author(author: str) -> list[dict[str, any]]:
    """
    Retrieves a list of articles written by a specific author.

    Parameters:
        author (str): The name of the author.

    Returns:
        list[dict[str, any]]: A list of dictionaries representing the articles written by the author. Each dictionary contains the following keys: 'title' (str), 'author' (str), 'content' (str), and 'date_published' (str).
    """
    with open("blogging_app/all_articles.csv", "r") as all_articles:
        reader = csv.reader(all_articles)
        next(reader)
        articles = []
        for article in reader:
            if author == article[1]:
                article = Articles(title=article[0], author=article[1], content=article[2], date_published=article[3])
                article =article.__dict__
                articles.append(article)
    return articles

def update_user_profile(signup_data: list, update: list):
    """
    Updates the user profile in the UsersDB.csv file.

    Args:
        signup_data (list): A list containing the user's signup data.
        update (list): A list containing the user updates to be made to their profile.

    Returns:
        None
    """
    all_users = all_users_cache()
    with open("blogging_app/UsersDB.csv", "w", newline="") as UsersDB:
        writer = csv.writer(UsersDB)
        writer.writerow(UsersDB_header)
        for user in all_users:
            if signup_data[0] == user[0]:
                writer.writerow(update)
            else:
                writer.writerow(user)
    return