from app.models.retrieval import RetrievedChunk

class ContextBuilder:
    def build(self, chunks: list[RetrievedChunk]) -> str:
        context_parts = []

        for index, chunk in enumerate(chunks, start = 1):
            location = chunk.file_path

            if chunk.start_line and chunk.end_line:
                location += (f":{chunk.start_line}"
                            f"-{chunk.end_line}")
            
            symbol = ""
            if chunk.class_name:
                symbol += chunk.class_name
            
            if chunk.function_name:
                if symbol:
                    symbol += "."
                symbol += chunk.function_name
            
            context_parts.append(
                f"""
                --- SOURCE {index} ---
                File: {location}
                Symbol: {symbol}
                Type: {chunk.chunk_type}

                {chunk.content}
                """
            )
        
        return "\n".join(context_parts)