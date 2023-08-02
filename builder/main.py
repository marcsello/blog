import os

from .output import LocalDirOutput


def main():
    print("init output")
    o = LocalDirOutput("_output")
    print("copy public")
    o.add_folder("public", ".")
    print("read posts")
    posts = []

