import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

received_mail = input("受信したメールの内容を入力してください : \n")

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {
            "role":"user",
            "content":f"""以下のメールに対して返信メールを作成してください。

            【ルール】
            ・件名から始める
            ・丁寧な敬語を使う
            ・簡潔にまとめる
            ・署名はFinにする

            【受信メール】
            {received_mail}"""

        }
    ]
)

print("\n 【生成された返信メール】")
print(message.content[0].text)