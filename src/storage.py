from datetime import datetime 

def log_action(action):
    with open("log.txt", "a") as f: 
        f.write(f"[{datetime.now()}] {action}\n")