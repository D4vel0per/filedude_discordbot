from typing import List
from github import Github, Auth, ContentFile
from github.GithubException import UnknownObjectException
from dotenv import load_dotenv
import os

load_dotenv()

def connect(mode:str="DEV"): # Add DEV or PROD mode handling
    if mode == "DEV":
        token = os.getenv("GITHUB_STORING_DEV_TOKEN")
    else:
        token = os.getenv("GITHUB_STORING_PROD_TOKEN")
    g = Github(auth=Auth.Token(token))
    repo = g.get_repo("D4vel0per/filedude_userfiles")
    return Store(repo)

class Store:
    def __init__(self, repo):
        self.main = repo
    def submit (self, filename, text):
        print(f"Creating {filename}...")
        try:
            self.main.get_contents(filename)
            print(f"Already exists. Updating instead...")
            self.update(filename=filename, new_text=text)
        except UnknownObjectException:
            self.main.create_file(filename, f"Creating {filename}", text)
            print("Succesfully Created.")

    def remove (self, filename):
        print(f"Removing {filename}...")
        try:
            contents = self.main.get_contents(filename)
            self.main.delete_file(filename, f"Deleting {filename}", contents.sha)
        except UnknownObjectException:
            print(f"File {filename} wasn't found")

    def update(self, filename, new_text=None):
        print(f"Updating {filename}...")
        try:
            contents = self.main.get_contents(filename)
            if new_text:
                self.main.update_file(filename, f"Updating {filename}", new_text, sha=contents.sha)
        except UnknownObjectException:
            print(f"File {filename} wasn't found")

    def get(self, filename, recursive=True):
        print(f"Trying to get {filename}...")
        try:
            response = self.main.get_contents(filename)
            results = []
            if not isinstance(response, List):
                return [response]
            for content in response:
                results.append(content)
                if content.type == "dir" and recursive:
                    results.extend(self.get(content.path))
                    
            return results
        except UnknownObjectException as e:
            return []
        except Exception as e:
            print(type(e))
            print(e)