import anthropic                            # Anthropicのライブラリを読み込む
from dotenv import load_dotenv              # .envファイルを読み込むライブラリ

load_dotenv()                               # .envからAPIキーを読み込む

client = anthropic.Anthropic()              # Claudeに繋がる窓口を作る

message = client.messages.create(           # Claudeにメッセージを送る
    model="claude-haiku-4-5-20251001",      # 使うモデルを指定
    max_tokens=1024,                        # 返事の最大文字数
    messages=[
        {"role": "user", "content": "あなたは私にとってのなんですか？"}     # 送るメッセージ
    ]
)

print(message.content[0].text)              # 返ってきた返事を表示