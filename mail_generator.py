import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

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
selected = next(p for p in data["patterns"] if p["id"] == pattern_id)
print(f"パターン判定：{selected['name']}\n")

# ↑↑↑自動判断ロジック↑↑↑

three_base = "千歳ベース" in instruction or "札幌ベース" in instruction or "道東ベース" in instruction

if pattern_id == "4":
    if three_base:
        prompt = "以下の指示書から情報を読み取り、配達完了メールとシャーシ切りメールの下書きを２通り生成してください。\n\n" + selected["prompt_output1"] + "\n---\n\n" + selected["prompt_output2"] + f"\n\n【指示書】\n{instruction}"
    else:
        prompt = "以下の指示書から情報を読み取り、配達完了メールと空車回送メールの下書きを２通り生成してください。\n\n" + selected["prompt_output1"] + "\n---\n\n" + selected["prompt_output3"] + f"\n\n【指示書】\n{instruction}"
else:
    prompt = selected["prompt"] + f"\n\n【指示書】\n{instruction}"



message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("\n【生成されたメール】")
print(message.content[0].text)