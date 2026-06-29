import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

print("=== 業務メール自動生成ツール ===\n")

instruction = input("指示書の内容を入力してください : \n")

print("\n報告タイプを選んでください")
print("1: 出発報告")
print("2: 到着報告")
report_type = input("番号を入力:")

if report_type =="1":
    departure_time = input("出発時間(例:07:30):")
    departure_temp = input("出発時温度(例:+3):")
    seal = input("封印番号(なければそのままenter):")

    prompt = f"""以下の指示書から情報を読み取り、出発報告メールを作成してください。

    【指示書】
    {instruction}

    【追加情報】
    出発時間:{departure_time}
    出発時温度:{departure_temp}
    封印:{seal if seal else "なし"}

    【出力フォーマット】
    件名：配達集荷用　車番 [車番]

    本文：
    [場所]集荷完了

    積み荷：[積み荷]
    設定温度：[設定温度]℃

    出発地：[出発地]
    出発時間：{departure_time}
    出発時温度：{departure_temp}℃
    封印番号：{seal if seal else "なし"}

異常：なし"""

elif report_type =="2":
    arrival_time = input("到着時間（例：14：30）：")
    arrival_temp = input("到着時温度（例：+3）：")
    seal = input("封印番号（なければそのままEnter）：")
    issues = input("異常（なければそのままEnter）：")

    prompt = f"""以下の指示書から情報を読み取り、到着報告メールを作成してください。

    【指示書】
    {instruction}

    【追加情報】
    到着時間：{arrival_time}
    到着時温度：{arrival_temp}
    封印：{seal if seal else "なし"}
    異常：{issues if issues else "なし"}

    【出力フォーマット】
    件名：配達集荷用　車番 [車番]

    本文：
    [場所]切り

    積み荷：[積み荷]
    設定温度：[設定温度]℃

    到着地：[到着地]
    到着時間：{arrival_time}
    到着時温度：{arrival_temp}℃
    封印番号：{seal if seal else "なし"}

    異常：{issues if issues else "なし"}"""

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("\n【生成されたメール】")
print(message.content[0].text)