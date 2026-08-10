from langchain_core.documents import Document

class CodeChunker:
    """
    Converts parsed code into langhchain documents.
    """
    def create_documents(self, parsed_code:dict) -> list[Document]:
        documents = []
        
        file_path = parsed_code.get("file_path")
        language = parsed_code.get("language")

        #imports
        if parsed_code["imports"]:
            import_lines = []

            for item in parsed_code["imports"]:
                module = item["module"]
                name = item["name"]

                if name:
                    import_lines.append(f"from {module} import {name}")
                else:
                    import_lines.append(f"import {module}")
                
            
            documents.append(Document(
                page_content="\n".join(import_lines),
                meta_data={
                    "file_path": file_path,
                    "language": language,
                    "chunk_type": "imports"
                }
            ))

        
        #classes
        for class_info in parsed_code["classes"]:
            method_names = [method["name"] for method in class_info["methods"]]
            
            content = (
                f"Class: {class_info['name']}\n"
                f"Methods: {', '.join(method_names)}\n"
            )

            if class_info["docstring"]:
                content += f"Description:\n{class_info['docstring']}\n"

            documents.append(Document(
                page_content=content,
                metadata={
                    "file_path": file_path,
                    "language": language,
                    "chunk_type": "class",
                    "class_name": class_info["name"],
                    "start_line": class_info["start_line"],
                    "end_line": class_info["end_line"]
                }
            ))
        
        #class methods
        for method in class_info["methods"]:
            content = (
                    f"Class: {class_info['name']}\n"
                    f"Method: {method['name']}\n\n"
                    f"{method['code']}"
                )

            if method["docstring"]:
                content += (
                    f"\n\nDescription:\n"
                    f"{method['docstring']}"
                )

            documents.append(
            Document(
                        page_content=content,
                        metadata={
                            "file_path": file_path,
                            "language": language,
                            "chunk_type": "method",
                            "class_name": class_info["name"],
                            "function_name": method["name"],
                            "start_line": method["start_line"],
                            "end_line": method["end_line"],
                        },
                    )
                )
        
        for function in parsed_code["functions"]:

            content = (
                f"Function: {function['name']}\n\n"
                f"{function['code']}"
            )

            if function["docstring"]:
                content += (
                    f"\n\nDescription:\n"
                    f"{function['docstring']}"
                )

            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "file_path": file_path,
                        "language": language,
                        "chunk_type": "function",
                        "function_name": function["name"],
                        "start_line": function["start_line"],
                        "end_line": function["end_line"],
                    },
                )
            )

            return documents
