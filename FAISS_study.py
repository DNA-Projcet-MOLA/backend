# FAISS_study.py

import faiss
import numpy as np

def load_faiss_index(word_embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    word_embeddings: (N, d) ndarray
    반환: d 차원의 FAISS IndexFlatL2 인스턴스 with embeddings added
    """
    emb = word_embeddings
    # 1차원 벡터일 경우 (d,) → (1, d)
    if emb.ndim == 1:
        emb = emb.reshape(1, -1)
    d = emb.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(emb)  # (N, d) 추가
    return index

def find_similar_words(keywords: list[str], word_embeddings: np.ndarray, k: int = 5) -> list[list[str]]:
    """
    각 키워드 임베딩에 대해 상위 k개의 유사 키워드 인덱스를 리턴 후
    원본 keywords 리스트에서 대응하는 단어로 매핑하여 반환.
    """
    index = load_faiss_index(word_embeddings)
    query = word_embeddings
    if query.ndim == 1:
        query = query.reshape(1, -1)
    # search
    D, I = index.search(query, k)
    # I.shape == (N, k)
    result: list[list[str]] = []
    for row in I:
        result.append([keywords[i] for i in row])
    return result
