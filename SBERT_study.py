from sentence_transformers import SentenceTransformer

# SBERT 모델을 사용하여 단어를 임베딩하는 함수
def get_word_embeddings(keywords):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(keywords)  # 주어진 단어 리스트를 임베딩 벡터로 변환
    return embeddings