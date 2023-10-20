import csv

# get total users in database
def get_total_users():
    with open("blogging_app/UsersDB.csv", "r") as UsersDB:
        reader = csv.reader(UsersDB)
        next(reader)
        total_users = len(list(reader))
    return total_users

