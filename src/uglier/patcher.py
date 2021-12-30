import argparse
import ast
import os
from typing import Dict, List, Set, Tuple
import unicodedata
from os import path
from collections import defaultdict
import random
import builtins
import logging

logger = logging.getLogger("uglier")


character_list = "𝕺𝔒𝓘𝕴ℓ𝔩𝕝𝔄𝕬ℬ𝓑𝔹𝕭ℭ𝕮𝔇𝕯Ǳǲ𝕰𝔈𝔉𝕱𝔊𝕳ℌⅡⅢĲⅣⅨ𝕵𝔍𝕶𝔎𝕷𝔏Ǉǈ𝕸𝔐𝕹𝔑Ǌǋ𝕻𝔓𝕼𝔔ℜ𝕽𝕾𝔖𝕿𝔗𝓤𝕌𝖁𝔙ⅥⅦⅧ𝖂𝔚𝔛𝓧ⅪⅫ𝔜𝖄𝖅ℨ𝕒𝒶𝒷𝓫𝒸𝓬𝔡ǳ𝔢𝔰𝕤𝖘𝒻𝓯ﬀﬃﬂᵍ𝓰𝔥𝒾𝓲ⅱⅲĳⅳⅸ𝒿𝖐ǉ𝓂𝕟ǌᵒ𝓅𝔮𝓇ﬆ𝑡𝓊𝓋ⅵⅶⅷ𝔀𝕩ⅺⅻ𝔶𝔷"
CHARACTERS = defaultdict(list)
for character in character_list:
    normalised = unicodedata.normalize("NFKC", character)
    CHARACTERS[normalised].append(character)

CHARACTERS.default_factory = None
SORTED_MATCH = sorted(CHARACTERS.keys(), key=len, reverse=True)
BUILTINS = set(dir(builtins))

latin = "ABEMHOPCTXaeopcyx"
cryllic = "АВЕМНОРСТХаеорсух"
latin_to_cyrillic = dict(zip(latin, cryllic))
cryllic_to_latin = dict(zip(cryllic, latin))


def random_casing(s: str) -> str:
    return "".join(random.choice([str.lower, str.upper])(c) for c in s)


class Patcher(ast.NodeTransformer):
    def __init__(self, opts: argparse.Namespace):
        # Map old ident names to new ident names
        self.mapping: Dict[str, str] = {}

        # Set of all mapped ident names (non-normalized)
        self.mapped_idents: Set[str] = set()
        self.opts = opts

        # Map old function names to new function names (normalized)
        self.function_names: Dict[str, str] = {}
        self.function_id = random.choice(latin) * 4
        self.mapped_idents.add(self.function_id)

    def visit_Name(self, node):
        new_name = self.modify_name(node.id)
        if isinstance(node.ctx, ast.Store):
            new_name = new_name
        return ast.Name(id=new_name, ctx=node.ctx)

    def visit_Attribute(self, node: ast.Attribute):
        return ast.Attribute(
            value=self.generic_visit(node.value),
            attr=self.modify_name(node.attr),
            ctx=node.ctx,
        )

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return self.visit_FunctionDef(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        new_node = super().generic_visit(node)

        new_fn_name = self.random_name(new_node.name)
        self.function_names[new_node.name] = new_fn_name
        self.mapped_idents.add(new_fn_name)
        new_node.name = new_fn_name

        return new_node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.function_id = random.choice(latin) * 4
        self.mapped_idents.add(self.function_id)
        new_node = super().generic_visit(node)

        new_fn_name = (
            self.random_name(new_node.name)
            if self.safe_to_modify(new_node.name)
            else self.generate_ident(new_node.name)
        )
        self.function_names[new_node.name] = new_fn_name
        self.mapped_idents.add(new_fn_name)
        new_node.name = new_fn_name

        for i in range(len(new_node.args.args)):
            pos_arg_name = new_node.args.args[i].arg
            new_node.args.args[i].arg = self.modify_name(pos_arg_name)

        if new_node.args.kwonlyargs is not None:
            for i in range(len(new_node.args.kwonlyargs)):
                pos_arg_name = new_node.args.kwonlyargs[i].arg
                new_node.args.kwonlyargs[i].arg = self.modify_name(pos_arg_name)

        return new_node

    def random_name(self, old: str) -> str:
        new = "".join(i for i in old.upper().replace("_", "") if not i.isdigit())
        while new in self.mapped_idents:
            new += "_"
        return new

    def modify_name(self, name: str, cryllic: bool = True) -> str:
        new_name = self.generate_ident(name, cryllic)
        self.mapping[name] = new_name
        self.mapped_idents.add(new_name)

        return new_name

    @staticmethod
    def safe_to_modify(original: str) -> bool:
        return (original not in BUILTINS) and not (
            (original[0:2] == "__" and original[-2:] == "__")
            if len(original) > 4
            else False
        )

    def generate_ident(
        self,
        original: str,
        cryllic: bool = True,
    ) -> Tuple[str, str]:
        safe_to_modify = self.safe_to_modify(original)

        if not safe_to_modify or not cryllic:
            new = original
            for match in SORTED_MATCH:
                random_alternative = random.choice(CHARACTERS[match])
                new = new.replace(match, random_alternative)
            final = new
        else:
            if original in self.mapping:
                final = self.mapping[original]
            elif original in self.function_names:
                new = self.function_names[original]
                for match in SORTED_MATCH:
                    random_alternative = random.choice(CHARACTERS[match])
                    new = new.replace(match, random_alternative)
                final = new
            else:
                while True:
                    final = "".join(
                        random.choice([latin_to_cyrillic[c], c])
                        for c in self.function_id
                    )
                    iters = 0
                    while (final in self.mapped_idents) and (
                        iters < len(self.function_id) ** 2 * 2
                    ):
                        final = "".join(
                            random.choice([latin_to_cyrillic[c], c])
                            for c in self.function_id
                        )
                        iters += 1

                    if final not in self.mapped_idents:
                        return final

                    self.function_id += self.function_id[0]

        return final

    def patch_paths(self, paths: List[str]):
        for file in paths:
            if path.isdir(file):
                for root, _, files in os.walk(file):
                    for file in files:
                        self.patch_file(path.join(root, file))
            else:
                self.patch_file(file)

    def patch_file(self, file: str):
        if path.splitext(file)[-1] != ".py":
            logger.log(logging.INFO, f"Skipping non-python file: {file}")
            return

        with open(file, "r") as f:
            try:
                file_ast = ast.parse(f.read())
            except SyntaxError as e:
                logger.log(
                    logging.ERROR, f"Failed to parse file (syntax error): {file}: {e}"
                )
                return

        new_ast = self.visit(file_ast)
        new_ast = ast.fix_missing_locations(new_ast)

        split_file = ast.unparse(new_ast).splitlines()
        new_file = ""
        for line in split_file:
            new_file += line
            new_file += "\n" * random.randint(1, 3)

        if self.opts.yolo:
            logger.log(logging.INFO, f"Patched {file}")
            with open(file, "w") as f:
                f.write(new_file)
        else:
            print(f"--- {file} ---")
            print(new_file)
