import csv

# get total users in database
def get_total_users() -> int:
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        total_users = len(list(reader))
    return total_users

def add_article_to_DB(article):
    with open("blogging_app/all_articles.csv", "a", newline="") as all_articles:
        writer = csv.writer(all_articles)
        writer.writerow([article.title, article.author, article.content, article.date_published])
    return

def username_in_DB(username: str) -> bool:
    with open("blogging_app/UsersDB.csv", ) as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        for user in reader:
            if username == user[1]:
                return True
    return False

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