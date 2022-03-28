
import requests

# https://api.github.com/users/Kalandor01/repos?per_page=100&page=1
# https://api.github.com/repos/Kalandor01/Portfolio/languages

def get_repos(uname="Kalandor01", git_token=""):
    # get projects
    project_pages = ""
    r = ""
    user_exists = True
    in_limit = True
    page_num = 1
    while in_limit == True and r != "[]":
        # get page
        if git_token!="":
            r = (requests.get(f"https://api.github.com/users/{uname}/repos?per_page=100&page={page_num}", headers={"Authorization": git_token})).text
        else:
            r = (requests.get(f"https://api.github.com/users/{uname}/repos?per_page=100&page={page_num}")).text
        if r.find('"message":"Not Found"') != -1:
            input(f"\n{uname} user doesn't exist!")
            user_exists = False
            in_limit = False
        else:
            # api limit
            if r.find("API rate limit exceeded for") != -1:
                input(f'\nAPI rate limit exceeded! Couldn\'t get the rest of the pages! (Try again in 1 hour{", or with a git token" if git_token=="" else ""}.)')
                in_limit = False
            else:
                project_pages += r
                print(f"Retrived page {page_num}.")
                page_num += 1
    if user_exists:
        # write out repos
        print(f"\n{uname}'s repos:\n")
        projects = project_pages.split("\",\"full_name\":\"")
        for x in range(len(projects) - 1):
            project_names = projects[x+1].split("\",\"")[0].split("/")[1]
            if project_names != uname:
                # get language
                if in_limit:
                    if git_token!="":
                        rl = (requests.get(f"https://api.github.com/repos/{uname}/{project_names}/languages", headers={"Authorization": git_token})).text
                    else:
                        rl = (requests.get(f"https://api.github.com/repos/{uname}/{project_names}/languages")).text
                    # api limit
                    if rl.find("API rate limit exceeded for") != -1:
                        input(f'\nAPI rate limit exceeded! (Try again in 1 hour{", or with a git token" if git_token=="" else ""}.)\n')
                        lang = "ERROR"
                        in_limit = False
                    else:
                        try:
                            lang = rl.split("{\"")[1].split("\":")[0]
                        except IndexError:
                            lang = "NONE"
                else:
                    lang = "ERROR"
                print(f"{project_names}({lang})")
        input("\nDone!")


def fetch_repos():
    # get name
    uname = input("GitHub username: ")
    if uname == "":
        uname = "Kalandor01"
    # token?
    is_token = input('Use personal git token(Y/N)? (paste token into "token.txt"): ')
    if is_token.upper() == "Y":
        # check token
        try:
            tok = open("token.txt", "r")
        except FileNotFoundError:
            print('"token.txt" not dound!')
        else:
            git_token = tok.readline().replace("\n", "")
            tok.close()
            if len(git_token) < 5:
                print("The git token is not this short!")
            else:
                get_repos(uname, git_token)
    else:
        get_repos(uname)


fetch_repos()
