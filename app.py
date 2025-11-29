import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# OpenAI APIキーの設定と.envファイルに記載したキーの読み込み
from dotenv import load_dotenv
load_dotenv()

# APIキーチェック
import os
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI APIキーが設定されていません。")
    st.stop()

# Streamlitアプリのタイトル
st.title("質問回答Webアプリ")

#Webアプリの概要や操作方法をユーザーに明示するためのテキストを表示
st.markdown("""
# 質問回答Webアプリへようこそ。
このアプリでは、医者、弁護士、エンジニアの専門家として質問に回答します。質問内容を入力し、専門家の種類を選択してください。
""")

# 入力フォーム
text_input = st.text_area("テキストを入力してください") 

#テキスト以外が入力された場合の処理
if not text_input:
    st.error("テキストを入力してください。")
    st.stop()

#ラジオボタンでLLMに振る舞わせる専門家の種類を選択できるようにします
expert_type = st.radio(
    "回答に使用する専門家の種類を選択してください",
    ('医者', '弁護士', 'エンジニア')
)

# 専門家の種類に応じたプロンプトの前置き
if expert_type == '医者':
    prompt_prefix = "あなたは医者です。以下の質問に専門的な知識で答えてください。"
elif expert_type == '弁護士':
    prompt_prefix = "あなたは弁護士です。以下の質問に法律の専門知識で答えてください。"
else:
    prompt_prefix = "あなたはエンジニアです。以下の質問に技術的な知識で答えてください。"

# 実行ボタンでのみAI処理を実行
if st.button("実行"):
    user_input_with_prefix = prompt_prefix + "\n" + text_input
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True)
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=user_input_with_prefix)
    ]
    with st.spinner("AIが回答中です..."):
        try:
            response = llm.invoke(messages)
            st.write("LLMの回答:")
            st.write(response.content)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# 注意書き
st.markdown("""
**注意:** このアプリは情報提供のみを目的としており、専門的な助言を提供するものではありません。重要な決定を下す前に、必ず資格のある専門家に相談してください。
""")

