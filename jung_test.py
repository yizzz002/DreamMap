from jungian_analysis import analyze_dream


dream = """
我夢到自己回到以前的學校，
一直找不到要去的教室。

走廊非常長，
我越走越緊張。

後來遇到一個以前很熟的朋友，
但是他完全沒有跟我說話。
"""


results = analyze_dream(dream)


print("\n夢境：")
print(dream)

print("\n榮格式反思結果：\n")


for result in results:

    print(result["name"])

    print(
        f"相關度：{result['score']:.2f}"
    )

    print(result["description"])

    print(
        "反思問題：",
        result["question"]
    )

    print("--------------------")