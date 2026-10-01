from sentence_transformers import util

# 直接共用目前 Jungian Analysis 已載入的 Embedding model
from jungian_analysis import model


def search_similar_dreams(query, dreams, top_k=3):

    # 沒有夢境就直接回傳空結果
    if not dreams:
        return []

    # 搜尋文字 → Embedding
    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    # 取出每一篇夢境內容
    dream_texts = [
        dream[2]
        for dream in dreams
    ]

    # 所有夢境 → Embedding
    dream_embeddings = model.encode(
        dream_texts,
        convert_to_tensor=True
    )

    # 計算語意相似度
    scores = util.cos_sim(
        query_embedding,
        dream_embeddings
    )[0]

    results = []

    for dream, score in zip(
        dreams,
        scores.tolist()
    ):

        results.append({
            "id": dream[0],
            "date": dream[1],
            "content": dream[2],
            "mood": dream[3],
            "score": score
        })

    # 相似度由高到低排序
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]