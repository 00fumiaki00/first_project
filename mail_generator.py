import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


def generate_and_print(prompt):
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print("\n【生成されたメール】")
    print(message.content[0].text)


print("=== 業務メール自動生成ツール ===\n")

with open("patterns.json","r",encoding="utf-8") as f:   # patterns.json を読み込んで data に入れる。with open はファイルを開いて、終わったら自動で閉じる仕組み
    data = json.load(f)


instruction = input("指示書の内容を入力してください : \n")


#　↓↓↓自動判断ロジック↓↓↓

pattern_list = "\n".join([f'id:{p["id"]} name:{p["name"]} keywords:{p["keywords"]}' for p in data["patterns"]])

detection_prompt = f"""以下の指示書を読んで、最も適切なパターンのidを数字1つだけ返してください。

【指示書】
{instruction}

【パターン一覧】
{pattern_list}


"""

detection = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=10,
    messages=[{"role":"user", "content": detection_prompt}]
)

pattern_id = detection.content[0].text.strip().splitlines()[0].strip()
print(f"[DEBUG] pattern_id = {repr(pattern_id)}")
selected = next(p for p in data["patterns"] if p["id"] == pattern_id)
print(f"パターン判定：{selected['name']}\n")

# ↑↑↑自動判断ロジック↑↑↑



# ↓↓↓集荷回数カウント↓↓↓

pickup_count = instruction.count(selected.get("repeat_keyword",""))
print(f"[DEBUG] pickup_count = {pickup_count}")

# ↑↑↑集荷回数カウント↑↑↑



# ↓↓↓条件分岐（シャーシ切りか空車回送か判断）↓↓↓
if "repeat_keyword" in selected:
    for i in range(1,pickup_count + 1):
        directive = f"\nこの指示書には集荷が全部で{pickup_count}回あります。今回は{i}回目の集荷分の出発報告だけ生成してください。"
        prompt = selected["departure_template"] + directive + f"\n\n【指示書】\n{instruction}"
        generate_and_print(prompt)
    prompt = selected["arrival_template"] + f"\n\n【指示書】\n{instruction}"
    generate_and_print(prompt)

elif "common" in selected:
    matched = False     # 最初は「まだ何も見つかってない」
    for branch in selected["branches"]:
        if any(keyword in instruction for keyword in branch.get("conditions",[])):
            prompt = selected["common"] + branch["content"] + f"\n\n【指示書】\n{instruction}"
            matched = True      # 「見つかった」に書き換える
            break
    if not matched:
        default_branch = next(b for b in selected["branches"] if b.get("default"))
        prompt = selected["common"] + default_branch["content"] + f"\n\n【指示書】\n{instruction}"
        generate_and_print(prompt)

else:
    prompt = selected["prompt"] + f"\n\n【指示書】\n{instruction}"
    generate_and_print(prompt)


# ↑↑↑条件分岐（シャーシ切りか空車回送か判断）↑↑↑
