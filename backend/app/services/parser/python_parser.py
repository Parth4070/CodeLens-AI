import ast 
from pathlib import Path

from app.services.parser.base_parser import BaseParser

class PythonParser(BaseParser):
    def parse(self, file_path: Path) -> dict:
        source_code = file_path.read_text(encoding="utf-8")

        tree = ast.parse(source_code, filename=str(file_path))
        
        return {
            "file_path": str(file_path),
            "language" : "python",
            "imports": self._extract_imports(tree),
            "functions" : self._extract_functions(tree),
            "classes": self._extract_classes(tree),
        }

    def _extract_imports(self, tree):
        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for alias in node.names:
                    imports.append(
                        f"{module}.{alias.name}"
                    )

        return imports
    
    def _extract_functions(self, tree):
        functions = []

        for node in ast.iter_child_nodes(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                functions.append(node.name)

        return functions

    
    def _extract_classes(self, tree):
        classes = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                methods = []

                for child in node.body:

                    if isinstance(
                        child,
                        (ast.FunctionDef, ast.AsyncFunctionDef)
                    ):
                        methods.append(child.name)

                classes.append({
                    "name": node.name,
                    "methods": methods,
                })

        return classes