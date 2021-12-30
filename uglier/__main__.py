from typing import Tuple
from rope.base.project import Project
from rope.base.libutils import analyze_modules
import ast

from rope.refactor.extract import ExtractVariable
from rope.refactor.rename import Rename


def coords_to_index(line: int, col: int, s: str):
    """Convert column and line number of string to index."""
    return sum(len(line) + 1 for line in s.splitlines()[: line - 1]) + col


project = Project("./test/")
analysis = analyze_modules(project)
for file in project.get_files():
    print(dir(file))
    # project.do(changes)
    file_s = file.read()
    file_ast = ast.parse(file_s)
    for node in ast.walk(file_ast):
        if isinstance(node, ast.Name):
            idx = coords_to_index(node.lineno, node.col_offset, file_s)
            print(node.id, file_s[idx : idx + len(node.id)])
            changes = ExtractVariable(
                project, file, idx, idx + len(node.id)
            ).get_changes(f"new_{node.id}")
