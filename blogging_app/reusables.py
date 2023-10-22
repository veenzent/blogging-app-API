import csv
from blogging_app.models import Articles


UsersDB_header = ["id", "username", "first_name", "last_name", "email", "password", "bio", "website", "social_media.twitter", "social_media.facebook", "social_media.instagam", "last_updated_at", "posts", "total_posts"]

article_header = ["title", "author", "content", "date_published"]

# get total users in database
def get_total_users() -> int:
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        total_users = len(list(reader))
    return total_users

def username_in_DB(username: str) -> bool:
    with open("blogging_app/UsersDB.csv", ) as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1]:
                return True
    return False

def get_user_signup_details(username: str) -> list:
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1]:
                signup_details = [user[0], user[1], user[2], user[3], user[4], user[5]]
                return signup_details

def add_article_to_DB(article):
    with open("blogging_app/all_articles.csv", "a", newline="") as all_articles:
        writer = csv.writer(all_articles)
        writer.writerow([article.title, article.author, article.content, article.date_published])
    return

def add_user_to_DB(user: list):
    with open("blogging_app/UsersDB.csv", "a", newline="") as UsersDB:
        writer = csv.writer(UsersDB)
        writer.writerow(user)
    return

def find_article_by_title(title: str) -> list:
    with open("blogging_app/all_articles.csv", "r") as all_articles:
        reader = csv.reader(all_articles)
        next(reader)
        for article in reader:
            if title == article[0]:
                return article
            
def all_articles_cache() -> list:
    with open("blogging_app/all_articles.csv", "r") as all_articles:
        reader = csv.reader(all_articles)
        next(reader)
        return list(reader)
    
def all_users_cache() -> list:
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        users = list(reader)
        return users
    
def get_articles_by_author(author: str) -> list:
    with open("blogging_app/all_articles.csv", "r") as all_articles:
        reader = csv.reader(all_articles)
        next(reader)
        articles = []
        for article in reader:
            if author == article[1]:
                article = Articles(title=article[0], author=article[1], content=article[2], date_published=article[3])
                articles.append(article)
    return articles

# all_users = all_users_cache()
# print(all_users_cache())