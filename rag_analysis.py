import ollama

from jungian_analysis import analyze_dream


def generate_jungian_reflection(dream_text):

    # 1. Retrieval
    # 用 Embedding 找出最相關的榮格概念
    retrieved_concepts = analyze_dream(
        dream_text,
        top_k=3
    )

    # 2. 把搜尋到的知識整理成文字
    context_parts = []

    for i, concept in enumerate(
        retrieved_concepts,
        start=1
    ):
        context_parts.append(
            f"""
概念 {i}
名稱：{concept["name"]}
說明：{concept["description"]}
反思問題：{concept["question"]}
語意相關度：{concept["score"]:.3f}
"""
        )

    jungian_context = "\n".join(context_parts)

    # 3. Augmented Prompt
    prompt = f"""
/no_think

你是一個提供自我反思的夢境日記助理。

請直接根據以下資料回答，不需要展示思考過程。

請根據使用者的夢境，以及系統檢索出的榮格心理學相關概念，
產生一份簡潔、溫和、具有反思性的夢境分析。

重要規則：

1. 不要把夢境解釋成唯一真相。
2. 不要進行心理疾病或精神狀態診斷。
3. 使用「可能」、「或許」、「可以思考」等措辭。
4. 只能以提供給你的榮格概念作為主要理論依據。
5. 請使用繁體中文。
6. 不需要逐一重複所有資料，要把它們整合成自然的分析。
7. 整體內容要精簡，避免過長。

使用者夢境：
----------------
{dream_text}
----------------

檢索到的榮格概念：
----------------
{jungian_context}
----------------

請使用以下格式，並盡量精簡：

【🌙 夢境核心主題】
只用一句話，20～40字。

【✨ 重點摘要】
列出 3 點，每點 12～25 字，以短句呈現。

【🧠 詳細反思】
1～2 段即可，總長不要超過 180 字。

【💭 可以問自己的問題】
列出 2 個問題即可，每題簡短。

【⚠️ 提醒】
一句話即可。
"""

    # 4. Generation
    response = ollama.generate(
        model="qwen3:1.7b",
        prompt=prompt,
        options={
            "temperature": 0.4,
            "num_predict": 350
        },
        keep_alive="10m"
    )

    return {
        "reflection": response["response"],
        "concepts": retrieved_concepts
    }