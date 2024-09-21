from typing import List
from database import (
    get_file,
    write_file,
    delete_file
)

class Store:
    def path_args(original_path:str):
        comps = original_path.split("/")
        user_name = comps.pop(0)
        filename = comps.pop(-1)
        path = f"{user_name}/{'/'.join(comps)}/"

        return [user_name, path, filename]

    def submit (self, filename:str, text:str|bytes):
        user_name, path, filename = self.path_args(filename)
        write_file(user_name, path, filename, text.encode("utf-8"))   

    def remove (self, filename):
        user_name, path, filename = self.path_args(filename)
        delete_file(user_name, path, filename)

    def get(self, filename, only_folders=False):
        user_name, path, filename = self.path_args(filename)

        response = get_file(user_name, path, filename)

        if not response: return

        print(f"Trying to get {filename}...")
        
        is_inside_str = lambda path1, path2: (path1 in path2) and (path1 != path2)
        
        folders = { 
            content["path"] for content in response if is_inside_str(path, content["path"])
        }

        if only_folders:
            files = []
            for folder in folders:
                in_this_folder = [ 
                    {
                        "filename": file["path"] + file["filename"],
                        "text_64": file["text_64"]
                    } for file in response if folder in file["path"] == folder["path"]
                ]
                files.extend(in_this_folder)
        else:
            files = [
                {
                    "filename": file["path"] + file["filename"],
                    "text_64": file["text_64"]
                } for file in response
            ]
                    
        return {
            "files": files,
            "folders": list(folders)
        }

    def delete(self, filename, only_folders=False):
        
        response = self.get(filename, only_folders)
        user_name, path, filename = self.path_args(filename)

        if len(response) == 1:
            delete_file(user_name, path, filename)
        elif not only_folders:
            for file in response["files"]:
                delete_file(*self.path_args(file["filename"]))
        else:
            for folder in response["folders"]:
                delete_file(user_name, folder)

        return response
        