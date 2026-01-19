import pandas as pd
import faiss
import os
from sentence_transformers import SentenceTransformer
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# -------- Paths --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "awadhi_dataset.csv")

df = pd.read_csv(DATA_PATH)

# -------- Model --------
model = SentenceTransformer("all-MiniLM-L6-v2")

questions = df.iloc[:, 0].astype(str).tolist()
answers = df.iloc[:, 1].astype(str).tolist()

embeddings = model.encode(questions, convert_to_numpy=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# -------- Roman → Devanagari --------
def normalize_query(query: str) -> str:
    # अगर English / Roman है
    if query.isascii():
        try:
            return transliterate(query, sanscript.ITRANS, sanscript.DEVANAGARI)
        except:
            return query
    return query

# -------- Retrieval --------
def retrieve_context(query, k=1):
    normalized_query = normalize_query(query)

    q_emb = model.encode([normalized_query])
    _, I = index.search(q_emb, k)

    return answers[I[0][0]]
