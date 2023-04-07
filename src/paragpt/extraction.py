import pathlib as pt

def read_text(file: pt.Path)->str:
    with open(file, "r") as f:
        content = f.read()
    return content