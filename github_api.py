import requests

def get_user_info(username):
    url = f"https://api.github.com/users/{username}"
    return requests.get(url).json()

def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    return requests.get(url).json()