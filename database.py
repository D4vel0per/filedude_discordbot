import os
from dotenv import load_dotenv
import supabase
import base64
from datetime import datetime, UTC

load_dotenv()

service_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase_url = os.getenv("SUPABASE_URL")

db = supabase.create_client(supabase_url, service_key)

def get_user(user_name):
    response = db.table("Users").select("*").eq("user_name", user_name).execute()
    return response.data[0] if response.data else None

def create_user(user_name):
    response = db.table("Users").select("*").eq("user_name", user_name).execute()
    if not response.data:
        user = {
            "file_count": 0,
            "user_name": user_name
        }
        db.table("Users").insert(user).execute()
    
    return None if response.data else get_user(user_name)

def update_file_count(user_name):
    user = get_user(user_name)
    file_count = (
        db.table("Files").select("*")
        .eq("user_name", user["user_name"])
        .execute().data
    )
    res = (
            db.table("Users").
            update({"file_count": len(file_count)})
            .eq("user_name", user["user_name"])
            .execute()
    )

    return res

def get_file(user_name, path, filename=""):
    user = get_user(user_name)
    query = (
        db.table("Files")
        .select("path, filename, text_64")
        .eq("user_name", user["user_name"])
    )
    if filename:
        query = query.eq("path", path).eq("filename", filename)
    else:
        query = query.like("path", f"{path}%")
    
    files_response = query.execute()
    
    return files_response.data or []

def write_file(user_name, path, filename, b_utf8, mode="BOTH"): # modes: "BOTH"/"UPDATE"/"CREATE"
    user = get_user(user_name)
    if not user: return

    file_json = {
        "path": path,
        "filename": filename,
        "text_64": base64.b64encode(b_utf8).decode("utf-8"),
        "user_name": user["user_name"],
        "created_at": datetime.now(UTC).isoformat()
    }

    if get_file(user_name, path, filename) and (mode == "BOTH" or mode == "UPDATE"):
        resp = update_file(file_json)
    elif mode == "BOTH" or mode == "CREATE":
        resp = insert_file(file_json)
    
    return resp.data

def insert_file(file:dict):
    print(f"Creating {file['filename']}...")

    resp = db.table("Files").insert(file).execute()
    update_file_count(file["user_name"])

    print(f"Succesfully Created.")
    return resp

def update_file(file:dict):
    print(f"Updating {file['filename']}...")

    resp = (
        db.table("Files")
        .update(file)
        .eq("user_name", file["user_name"])
        .eq("path", file["path"])
        .eq("filename", file["filename"])
        .execute()
    )

    print(f"Succesfully Updated.")
    return resp

def delete_file(user_name, path, filename=""):
    print(f"Removing {filename or path}...")
    user = get_user(user_name)
    if user and get_file(user["user_name"], path, filename):
        query = (
            db.table("Files")
            .delete()
            .eq("user_name", user["user_name"])
        )
        
        if filename:
            query = query.eq("path", path).eq("filename", filename)
        else:
            query = query.like("path", f"{path}%")

        resp = query.execute()
        update_file_count(user_name)

        return resp.data
    
    elif user and filename:
        print(f"File {filename} was not found.")

    elif user:
        print(f"Folder {path} was not found.")

    else:
        print(f"User {user_name} doesn't exist.")