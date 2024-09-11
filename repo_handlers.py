from github import Github, Auth
from github.GithubException import UnknownObjectException

with open("GITHUB-env.txt", "r") as file:
    g = Github(auth=Auth.Token(file.read()))
    repo = g.get_repo("D4vel0per/filedude_userfiles")

def submit (filename, text):
    print(f"Creating {filename}...")
    try:
        repo.get_contents(f"D4v/{filename}")
        print(f"Already exists. Skipping...")
    except UnknownObjectException:
        repo.create_file(f"D4v/{filename}", f"Creating {filename}", text)
        print("Succesfully Created.")

def remove (filename):
    print(f"Removing {filename}...")
    try:
        contents = repo.get_contents(f"D4v/{filename}")
        repo.delete_file(f"D4v/{filename}", f"Deleting {filename}", contents.sha)
    except UnknownObjectException:
        print(f"File {filename} wasn't found")

def update(filename, new_text=None):
    print(f"Updating {filename}...")
    try:
        contents = repo.get_contents(f"D4v/{filename}")
        if new_text:
            repo.update_file(f"D4v/{filename}", f"Updating {filename}", new_text, sha=contents.sha)
    except UnknownObjectException:
        print(f"File {filename} wasn't found")


remove("alo.txt")