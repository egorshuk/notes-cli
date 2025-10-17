import argparse, os, json 
from storage import log_action

FILE = "notes.json"

def load():
    if not os.path.exists(FILE): return []
    try:
        with open(FILE) as f: return json.load(f)
    except json.JSONDecodeError:
        print("corrupted notes file — resetting.")
        return []

def save(notes):
    with open(FILE, "w") as f: json.dump(notes, f, indent=2, ensure_ascii=False)

def add(note):
    data = load()
    data.append(note)
    save(data)

def list_notes():
    if args.bullet: 
        for note in load(): print(f'{args.bullet} {note}')
    elif args.enumerate:
        for i, note in enumerate(load()): print(f'{i+1}. {note}')
    else:
        for note in load(): print(note)

def remove(i):
    data = load()
    if 1 <= i <= len(data):
        data.pop(i-1)
        save(data)


parser = argparse.ArgumentParser(
    prog = "cli-notes",
    description = "A python script to save, read and remove your notes"
)
sub = parser.add_subparsers(dest = "cmd")

addp = sub.add_parser(
    "add",
    help = "add new note"
)
addp.add_argument("text", type=str)

remp = sub.add_parser(
    "remove",
    help = "delete note by index"
)
remp.add_argument("index", type=int)


listp = sub.add_parser(
    "list", 
    help = "print all of your notes in a such a way: 1. ... if you have k notes"
)

list_style = listp.add_mutually_exclusive_group()
list_style.add_argument(
    '-b',                                       # короткий флаг
    '--bullet',                                 # полный флаг 
    nargs = "?",                                # 0 или 1 аргумента на вход
    const = "-",                                # стандартный bullet
    help = 'prints notes as bullet list'        # описание
)

list_style.add_argument(
    '-e',                                       # короткий флаг
    '--enumerate',                              # полный флаг 
    action = 'store_true',                      # что он делает 
    help = 'prints notes as enumerate list'     # описание
)

args = parser.parse_args()

if __name__ == "__main__":
    if args.cmd == "add": 
        add(args.text)
        log_action(f"add note \"{args.text}\"")
    elif args.cmd == "remove": 
        remove(args.index)
        log_action(f"remove note {args.index}")
    elif args.cmd == "list": 
        list_notes()