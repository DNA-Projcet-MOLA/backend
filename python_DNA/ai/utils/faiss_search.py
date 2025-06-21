import json
from django.conf import settings
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def load_problems():
    with open(settings.PROBLEM_JSON_PATH, encoding='utf-8') as f:
        return json.load(f)

def build_embeddings(problems):
    corpus = [p['question'] + ' ' + str(p.get('latex', '')) for p in problems]
    embs = model.encode(corpus, convert_to_numpy=True)
    faiss.normalize_L2(embs)
    return embs

def get_similar_problem_idxs(query, top_k=3):
    problems = load_problems()
    embs = build_embeddings(problems)
    query_emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_emb)
    d = embs.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embs)
    D, I = index.search(query_emb, top_k)
    return [int(i) for i in I[0]]