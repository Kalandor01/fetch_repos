import requests

# https://api.github.com/users/Kalandor01/repos?per_page=100
# https://api.github.com/repos/Kalandor01/Portfolio/languages

def get_repos(uname="Kalandor01", git_token=""):
    try:
        if git_token!="":
            r = (requests.get(f"https://api.github.com/users/{uname}/repos?per_page=100", headers={"Authorization": git_token})).text
        else:
            r = (requests.get(f"https://api.github.com/users/{uname}/repos?per_page=100")).text
    except:
        input(f"\n{uname} user doesn't exist!")
    else:
        if r.find("API rate limit exceeded for") != -1:
            input(f'\nAPI rate limit exceeded! (Try again in 1 hour{", or with a git token" if git_token=="" else ""}.)')
        else:
            print(f"\n{uname}'s repos:\n")
            projs = r.split("\",\"full_name\":\"")
            in_limit = True
            for x in range(len(projs) - 1):
                pn = projs[x+1].split("\",\"")[0].split("/")[1]
                if pn != uname:
                    if in_limit:
                        if git_token!="":
                            rl = (requests.get(f"https://api.github.com/repos/{uname}/{pn}/languages", headers={"Authorization": git_token})).text
                        else:
                            rl = (requests.get(f"https://api.github.com/repos/{uname}/{pn}/languages")).text
                        if rl.find("API rate limit exceeded for") != -1:
                            input(f'\nAPI rate limit exceeded! (Try again in 1 hour{", or with a git token" if git_token=="" else ""}.)\n')
                            lg = "ERROR"
                            in_limit = False
                        else:
                            try:
                                lg = rl.split("{\"")[1].split("\":")[0]
                            except IndexError:
                                lg = "NONE"
                    else:
                        lg = "ERROR"
                    print(f"{pn}({lg})")
        input("\nDone!")


uname = input("GitHub username: ")
if uname == "":
    uname = "Kalandor01"
is_token = input('Use personal git token(Y/N)? (paste token into "token.txt"): ')
if is_token.upper() == "Y":
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
