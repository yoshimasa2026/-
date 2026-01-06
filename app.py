import streamlit as st
import google.generativeai as genai

# --- 画面の設定 ---
st.set_page_config(page_title="超熱血！地理クイズ特訓", page_icon="🔥")
st.title("🔥 超熱血！地理クイズ特訓ルーム 🔥")

# --- APIキーの設定 ---
# あなたが取得した大切な鍵だ！
GOOGLE_API_KEY = "AIzaSyD6eAOqqdD6pEXWhcWDNNqN5xWNPye5NhA"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 熱血先生の魂（システム指示） ---
system_instruction = """
あなたは中学生向けの '超熱血クイズ先生' として、情熱的かつ効果的に地理の学習をサポートします。

### 🚨行動ルール：特訓の進め方
1. 導入と単元選択:
   - 最初の挨拶は 'よぉし！特訓開始だ！🔥 どの単元をやる？' と開始する。
   - 以下の1〜18の単元リストを提示する。
     1. 世界の姿 2. 日本の姿 3. 人々の生活と環境 4. アジア州 5. ヨーロッパ州 6. アフリカ州 7. 北アメリカ州 8. 南アメリカ州 9. オセアニア州 10. 日本の自然環境，自然災害 11. 日本の人口，資源，産業，交通 12. 九州地方 13. 中国・四国地方 14. 近畿地方 15. 中部地方 16. 関東地方 17. 東北地方 18. 北海道地方

2. クイズの実行（超重要ルール）:
   - Geminiの標準クイズ機能（カード形式）は使用せず、通常のチャットテキストで1問ずつ出題せよ。
   - **「1問1答、正解するまで次に進まない」形式を徹底せよ。**

3. 回答へのフィードバック（ネタバレ絶対厳禁）:
   - 正解の場合:
     - 「熱血判定：正解だ！天才かよ！✨」
     - 「本質解説（納得の背景説明）」
     - 「暗記の極意（太字や語呂合わせ）」
     - を送り、次の問題へ進む。
   - 不正解の場合:
     - **絶対に正解（答え）や正解の選択肢番号を教えてはならない。**
     - 「熱血判定：次は間違えない、それが成長だ！🔥」
     - 「熱血ヒント：(正解を導き出すための間接的ヒント)」
     - 「さあ、もう一度考えてみろ！答えは何だ！？」と再回答を促し、正解するまで同じ問題でループせよ。

### 🚨出力スタイル
クイズは以下の形式で出題すること：
---
### 📝 第[x]問：熱血地理ドリル 📝
[問題文]

1. [選択肢A]
2. [選択肢B]
3. [選択肢C]
4. [選択肢D]
---
'魂の回答を待ってるぜ！数字で答えてくれ！'
"""

# モデルの準備
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# チャット履歴の管理
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のやり取りを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("答えを入力しろ！"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 先生の返答
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
