import argparse
import ast
import os
from typing import Dict, List, Optional, Set, Tuple
import unicodedata
from os import path
from collections import defaultdict
import random
import builtins
import logging

logger = logging.getLogger("uglier")


with open(path.join(path.dirname(__file__), "characters.txt"), "r") as f:
    CHARACTERS = defaultdict(list)
    for character in f.read():
        normalised = unicodedata.normalize("NFKC", character)
        CHARACTERS[normalised].append(character)

CHARACTERS.default_factory = None
SORTED_MATCH = sorted(CHARACTERS.keys(), key=len, reverse=True)
BUILTINS = set(dir(builtins))


def random_casing(s: str) -> str:
    return "".join(random.choice([str.lower, str.upper])(c) for c in s)


class Patcher(ast.NodeTransformer):
    def __init__(self, opts: argparse.Namespace):
        # Map old ident names to new NORMALIZED ident names (with random underscores)
        self.mapping: Dict[str, str] = {}

        # Set of all mapped ident names (non-normalized)
        self.mapped_idents: Set[str] = set()

        self.opts = opts

    def visit_Name(self, node):
        new_name = self.modify_name(node.id)
        return ast.Name(id=new_name, ctx=node.ctx)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        new_node = super().generic_visit(node)

        new_name = self.modify_name(new_node.name)
        new_node.name = new_name

        for i in range(len(new_node.args.args)):
            pos_arg_name = new_node.args.args[i].arg
            new_node.args.args[i].arg = self.modify_name(pos_arg_name)

        return new_node

    def modify_name(self, name: str) -> str:
        if name in self.mapping:
            new_name, normalised = self.generate_ident(False, self.mapping[name])
        else:
            new_name, normalised = self.generate_ident(True, name)
        self.mapping[name] = normalised
        self.mapped_idents.add(new_name)
        return new_name

    def generate_ident(
        self,
        modify_name: bool,
        original: Optional[str] = None,
    ) -> Tuple[str, str]:
        if original is not None:
            quacked = original
            new = quacked
            if modify_name and quacked not in BUILTINS:
                new = ""
                for char in quacked:
                    if random.random() < 0.01:
                        new += "quack"
                    new += char
                new = random_casing(new)

            for match in SORTED_MATCH:
                random_alternative = random.choice(CHARACTERS[match])
                new = new.replace(match, random_alternative)

            final = new
            if modify_name and new not in BUILTINS:
                final = ""
                for char in new:
                    if random.random() < 0.07:
                        final += "_" * random.randint(2, 4)
                    final += char

                while final in self.mapped_idents or final in self.mapping:
                    final += "_"

            return (final, unicodedata.normalize("NFKC", final))
        else:
            ident = "_"
            while (ident in self.mapping) or (ident in self.mapped_idents):
                ident += "_"

            return (ident, ident)

    def patch_paths(self, paths: List[str]):
        for file in paths:
            if path.isdir(file):
                for root, dirs, files in os.walk(file):
                    for file in files:
                        self.patch_file(path.join(root, file))
            else:
                self.patch_file(file)

    def patch_file(self, file: str):
        if path.splitext(file)[-1] != ".py":
            logger.log(logging.INFO, f"Skipping non-python file: {file}")
            return

        with open(file, "r") as f:
            file_ast = ast.parse(f.read())

        new_ast = self.visit(file_ast)
        new_ast = ast.fix_missing_locations(new_ast)

        print(ast.unparse(new_ast))
