from sentence_transformers import SentenceTransformer, util

from jungian_knowledge import JUNGIAN_CONCEPTS


model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# 先把 Jungian concepts 轉成 embeddings
concept_texts = [
    concept["semantic_text"]
    for concept in JUNGIAN_CONCEPTS
]

concept_embeddings = model.encode(
    concept_texts,
    convert_to_tensor=True
)


def analyze_dream(dream_text, top_k=3):

    # 把夢境轉成 embedding
    dream_embedding = model.encode(
        dream_text,
        convert_to_tensor=True
    )

    # 與所有 Jungian concepts 比較
    scores = util.cos_sim(
        dream_embedding,
        concept_embeddings
    )[0]

    results = []

    for concept, score in zip(
        JUNGIAN_CONCEPTS,
        scores.tolist()
    ):

        results.append({
            "name": concept["name"],
            "description": concept["description"],
            "question": concept["question"],
            "score": score
        })

    # similarity 高 → 低
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]