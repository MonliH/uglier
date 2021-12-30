from rope.base.project import Project
from rope.base.libutils import analyze_modules
from rope.refactor.rename import Rename
from rope.base.exceptions import RefactoringError

import ast
import logging

logger = logging.getLogger("uglier")
logger.setLevel(logging.WARNING)


def coords_to_index(line: int, col: int, s: str):
    """Convert column and line number of string to index."""
    return sum(len(line) + 1 for line in s.splitlines()[: line - 1]) + col


def make_new(old_id: str):
    """Create a new variable name."""
    return "new_" + old_id


project = Project("./test/")
analysis = analyze_modules(project)
builtins = set(dir(__builtins__))

for file in project.get_files():
    changes = []
    changed_vars = set()

    while True:
        file_s = file.read()
        file_ast = ast.parse(file_s)
        did_something = False
        for node in ast.walk(file_ast):
            if isinstance(node, ast.Name):
                if node.id not in builtins and node.id not in changed_vars:
                    did_something = True
                    idx = coords_to_index(node.lineno, node.col_offset, file_s)
                    new_id = make_new(node.id)
                    try:
                        change = Rename(project, file, idx).get_changes(new_id)
                        project.do(change)
                    except RefactoringError as e:
                        logger.log(logging.WARNING, str(e))
                    changed_vars.add(new_id)
                    break

        if not did_something:
            break
