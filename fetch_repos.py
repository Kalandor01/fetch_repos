
import requests

# https://api.github.com/users/Kalandor01/repos?per_page=100&page=1
# https://api.github.com/repos/Kalandor01/Portfolio/languages

def get_repos(uname="Kalandor01", get_commit_num=True, git_token=""):
    all_commit_num = 0
    # get projects
    project_pages = ""
    r = ""
    user_exists = True
    in_limit = True
    page_num = 1
    repo_num = 0
    while in_limit == True and r != "[]":
        # get page
        print(f"Fetching page {page_num}...", end="", flush=True)
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
                if r != "[]":
                    project_pages += r
                    page_num += 1
                    # counting
                    repo_num_page = 0
                    pn_raw = r.split("\",\"full_name\":\"")
                    for x in range(len(pn_raw) - 1):
                        if pn_raw[x+1].split("\",\"")[0].split("/")[1] != uname:
                            repo_num_page += 1
                    repo_num += repo_num_page
                    print(f"DONE! ({repo_num_page})")
                else:
                    print("EMPTY!")
    if user_exists:
        # write out repos
        print(f"\n{uname}'s repos ({repo_num}):\n")
        projects = project_pages.split("\",\"full_name\":\"")
        for x in range(len(projects) - 1):
            project_name = projects[x+1].split("\",\"")[0].split("/")[1]
            if project_name != uname:
                # get language
                p_type = ((projects[x+1].split('"language":')[1]).split(",")[0]).replace('"', "")
                # get commit number
                if in_limit and get_commit_num:
                    if git_token!="":
                        rl = (requests.get(f"https://api.github.com/repos/{uname}/{project_name}/commits", headers={"Authorization": git_token})).text
                    else:
                        rl = (requests.get(f"https://api.github.com/repos/{uname}/{project_name}/commits")).text
                    # api limit
                    if rl.find("API rate limit exceeded for") != -1:
                        input(f'\nAPI rate limit exceeded! (Try again in 1 hour{", or with a git token" if git_token=="" else ""}.)\n')
                        comm = "ERROR"
                        in_limit = False
                    else:
                        comm = rl.count('"message":')
                        all_commit_num += comm
                else:
                    comm = "ERROR"
                if get_commit_num:
                    print(f"{project_name}({p_type}): {comm} commits")
                else:
                    print(f"{project_name}({p_type})")
        if get_commit_num:
            print(f"\nTotal commit number: {all_commit_num}\n")
        input("\nDone!")


def fetch_repos():
    # get name
    uname = input("GitHub username: ")
    if uname == "":
        uname = "Kalandor01"
    type_ans = input("Get the number of commits for each project? (This will take one request per project!)(Y/N): ")
    if type_ans.upper() == "N":
        type_commits = False
    else:
        type_commits = True
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
                get_repos(uname, type_commits, git_token)
    else:
        get_repos(uname, type_commits)


fetch_repos()
