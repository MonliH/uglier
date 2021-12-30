import ast
from typing import Dict, Optional
import unicodedata
from os import path

with open(path.join(path.basename(__file__), "characters.txt"), "r") as f:
    CHARACTERS = f.read()


class Patcher:
    def __init__(self):
        self.mapping: Dict[str, str] = {}

    def generate_ident(self, resoloves_to: Optional[str] = None):
        pass

    def patch_file(self, file: str):
        with open(file, "r") as f:
            file_ast = ast.parse(f.read())
        for node in ast.walk(file_ast):
            print(node)
