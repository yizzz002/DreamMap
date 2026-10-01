from rag_analysis import generate_jungian_reflection


dream = """
我夢到自己回到以前的學校。

我一直在找一間教室，
但是走廊好像沒有盡頭。

我越來越著急，
後來看到一個以前很熟的朋友，
但是他看到我之後直接走掉了。
"""


result = generate_jungian_reflection(
    dream
)


print("\n==============================")
print("🌙 Dream")
print("==============================")

print(dream)


print("\n==============================")
print("🔎 Retrieved Concepts")
print("==============================")

for concept in result["concepts"]:

    print(
        concept["name"],
        f"{concept['score']:.3f}"
    )


print("\n==============================")
print("🧠 Jungian RAG Reflection")
print("==============================")

print(
    result["reflection"]
)