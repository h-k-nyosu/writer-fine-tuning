import streamlit as st

def create_page_link(page_name, url):
    st.markdown(f"[{page_name}]({url})")

# ページ設定
st.set_page_config(
    page_title="はじめに",
    page_icon="📖",
)



# 新たな内容の追加
title = "## あなただけのAIで、思いのままの文章を"

content = """AI技術は進化していますが、出力される文章がどこか人間らしさに欠けること、感じたことはありませんか？

そこで、あなたの過去の記事を学習素材にして、gpt-3.5-turboをカスタマイズ。まるで「あなたが書いたかのような」文章をAIが生成します。

### 💸 あなたの文体を学び取るステップ
noteにアップした記事のURLを教えてください。その内容をもとに、あなたらしい文章を書くためのデータを準備し、gpt-3.5-turboをカスタマイズします。

### ✍️ あなたらしい文章を、今すぐ体験
新しいモデルを使って、思いついた内容を入力。すると、まるであなたが書いたかのような文章がすぐに生成されます。

"""

st.markdown(title, unsafe_allow_html=True)
st.image('image_1.png')
st.markdown(content, unsafe_allow_html=True)

# 各ページへのリンクの作成
