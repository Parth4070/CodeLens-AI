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
            "functions" : self._extract_functions(tree, source_code),
            "classes": self._extract_classes(tree, source_code),
        }

    def _extract_imports(self, tree: ast.AST) -> list[dict]:
        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "name": alias.asname,
                    })

            elif isinstance(node, ast.ImportFrom):

                module = node.module or ""

                for alias in node.names:
                    imports.append({
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname,
                    })

        return imports

    def _extract_functions(
        self,
        tree: ast.AST,
        source_code: str
    ) -> list[dict]:

        functions = []

        for node in ast.iter_child_nodes(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                functions.append(
                    self._extract_function(
                        node,
                        source_code
                    )
                )

        return functions

    def _extract_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        source_code: str
    ) -> dict:

        return {
            "name": node.name,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "docstring": ast.get_docstring(node),
            "code": ast.get_source_segment(
                source_code,
                node
            ),
        }
    
    def _extract_classes(
        self,
        tree: ast.AST,
        source_code: str
    ) -> list[dict]:

        classes = []

        for node in ast.iter_child_nodes(tree):

            if not isinstance(node, ast.ClassDef):
                continue

            methods = []

            for child in node.body:

                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    methods.append(
                        self._extract_function(
                            child,
                            source_code
                        )
                    )

            classes.append({
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "docstring": ast.get_docstring(node),
                "methods": methods,
                "code": ast.get_source_segment(
                    source_code,
                    node
                ),
            })

        return classes