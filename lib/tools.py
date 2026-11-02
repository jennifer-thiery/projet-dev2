from os import name, system


def ct() -> None:
    system("cls " if name == "nt" else "clear")
