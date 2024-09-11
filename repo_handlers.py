from github import Github, Auth
from github.GithubException import UnknownObjectException

def connect(): # Add DEV or PROD mode handling
    with open("GITHUB-env.txt", "r") as file:
        g = Github(auth=Auth.Token(file.read()))
        repo = g.get_repo("D4vel0per/filedude_userfiles")
    return Store(repo)

class Store:
    def __init__(self, repo):
        self.main = repo
    def submit (self, filename, text):
        print(f"Creating {filename}...")
        try:
            self.main.get_contents(f"D4v/{filename}")
            print(f"Already exists. Skipping...")
        except UnknownObjectException:
            self.main.create_file(f"D4v/{filename}", f"Creating {filename}", text)
            print("Succesfully Created.")

    def remove (self, filename):
        print(f"Removing {filename}...")
        try:
            contents = self.main.get_contents(f"D4v/{filename}")
            self.main.delete_file(f"D4v/{filename}", f"Deleting {filename}", contents.sha)
        except UnknownObjectException:
            print(f"File {filename} wasn't found")

    def update(self, filename, new_text=None):
        print(f"Updating {filename}...")
        try:
            contents = self.main.get_contents(f"D4v/{filename}")
            if new_text:
                self.main.update_file(f"D4v/{filename}", f"Updating {filename}", new_text, sha=contents.sha)
        except UnknownObjectException:
            print(f"File {filename} wasn't found")