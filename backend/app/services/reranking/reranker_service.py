import os
from typing import Optional
from app.models.retrieval import RetrievedChunk
from app.utils.logger import logger


class RerankerService:
    _shared_model = None

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.getenv(
            "RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    @classmethod
    def _get_model(cls, model_name: str):
        if cls._shared_model is None:
            try:
                # Try lightweight ONNX first to keep RAM < 200MB
                from huggingface_hub import hf_hub_download
                import onnxruntime as ort
                from tokenizers import Tokenizer
                import numpy as np

                class _OnnxReranker:
                    def __init__(self, model_id: str):
                        try:
                            model_path = hf_hub_download(
                                repo_id=model_id, filename="onnx/model_quint8_avx2.onnx"
                            )
                        except Exception:
                            model_path = hf_hub_download(
                                repo_id=model_id, filename="onnx/model.onnx"
                            )

                        tokenizer_path = hf_hub_download(
                            repo_id=model_id, filename="tokenizer.json"
                        )
                        self.tokenizer = Tokenizer.from_file(tokenizer_path)
                        self.tokenizer.enable_padding()
                        self.tokenizer.enable_truncation(max_length=512)
                        self.session = ort.InferenceSession(
                            model_path, providers=["CPUExecutionProvider"]
                        )

                    def predict(self, pairs: list[tuple[str, str]]) -> list[float]:
                        if not pairs:
                            return []
                        encodings = self.tokenizer.encode_batch(pairs)
                        inputs = {
                            "input_ids": np.array([e.ids for e in encodings], dtype=np.int64),
                            "attention_mask": np.array(
                                [e.attention_mask for e in encodings], dtype=np.int64
                            ),
                            "token_type_ids": np.array(
                                [e.type_ids for e in encodings], dtype=np.int64
                            ),
                        }
                        out = self.session.run(None, inputs)[0].flatten().tolist()
                        return [float(s) for s in out]

                cls._shared_model = _OnnxReranker(model_name)
                logger.info(f"Loaded lightweight ONNX reranker: {model_name}")
            except Exception as e:
                logger.warning(f"Could not load ONNX reranker ({e}), falling back to CrossEncoder: {model_name}")
                from sentence_transformers import CrossEncoder
                cls._shared_model = CrossEncoder(model_name)

        return cls._shared_model

    def rerank(
        self, query: str, retrieved_chunks: list[RetrievedChunk], top_k: int = 5
    ) -> list[RetrievedChunk]:
        if not retrieved_chunks:
            return []

        try:
            model = self._get_model(self.model_name)
            pairs = [(query, chunk.content) for chunk in retrieved_chunks]
            scores = model.predict(pairs)

            ranked_chunks = []
            for chunk, score in zip(retrieved_chunks, scores):
                chunk.rerank_score = float(score)
                ranked_chunks.append(chunk)

            ranked_chunks.sort(key=lambda chunk: chunk.rerank_score or 0.0, reverse=True)
            return ranked_chunks[:top_k]
        except Exception as err:
            logger.error(f"Error during reranking ({err}), returning top retrieved chunks")
            return retrieved_chunks[:top_k]


