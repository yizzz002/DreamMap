import pandas as pd

from sklearn.decomposition import PCA

from jungian_analysis import model


def build_dream_galaxy(dreams):

    # 至少需要兩筆資料才能做 2D PCA
    if len(dreams) < 2:
        return None

    # -------------------------
    # 取出所有夢境文字
    # -------------------------
    dream_texts = [
        dream[2]
        for dream in dreams
    ]

    # -------------------------
    # 夢境 → Embedding
    # -------------------------
    embeddings = model.encode(
        dream_texts
    )

    # -------------------------
    # Embedding → 2D
    # -------------------------
    pca = PCA(
        n_components=2
    )

    coordinates = pca.fit_transform(
        embeddings
    )

    # -------------------------
    # 整理成 DataFrame
    # -------------------------
    rows = []

    for dream, coordinate in zip(
        dreams,
        coordinates
    ):

        dream_id = dream[0]
        dream_date = dream[1]
        content = dream[2]
        mood = dream[3]

        # Hover 時不要塞整篇文章
        preview = (
            content[:100] + "..."
            if len(content) > 100
            else content
        )

        rows.append({
            "id": dream_id,
            "date": dream_date,
            "content": preview,
            "mood": mood,
            "x": coordinate[0],
            "y": coordinate[1]
        })

    return pd.DataFrame(
        rows
    )