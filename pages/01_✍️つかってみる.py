import os
import streamlit as st

st.set_page_config(
    page_icon="✍️",
)

# ディレクトリ構造を探索
base_dir = 'output'
api_key_prefixes = os.listdir(base_dir)

# ドロップダウンでAPI Key prefixを選択
selected_api_key_prefix = st.selectbox('API Key prefixを選択してください', api_key_prefixes)

# 選択されたAPI Key prefixの下のディレクトリを探索
dir_titles = os.listdir(os.path.join(base_dir, selected_api_key_prefix))

# ドロップダウンでdir_titleを選択
selected_dir_title = st.selectbox('dir_titleを選択してください', dir_titles)

# 選択されたdir_titleの下のファイルを探索
model_name = 'model_name.txt'
if model_name in os.listdir(os.path.join(base_dir, selected_api_key_prefix, selected_dir_title)):
    with open(os.path.join(base_dir, selected_api_key_prefix, selected_dir_title, model_name), 'r') as f:
        model_name_content = f.read()
    st.text(f"{model_name_content} が存在します")

    # テキストエリアと生成ボタンを追加
    user_input = st.text_area("生成したい内容を箇条書きで入力してください")
    if st.button('生成する'):
        import openai

        # OpenAI APIへリクエストを送る
        response = openai.ChatCompletion.create(
            model=model_name_content,
            messages=[
                {"role": "system", "content": "あなたはプロの編集者です。\nユーザーからは書きたい内容を箇条書きで渡されるので、それをもとに読者に読ませるような魅力的な文章を生成します。"},
                {"role": "user", "content": user_input}
            ]
        )

        # レスポンスを画面に出力
        st.text(response['choices'][0]['message']['content'])

else:
    st.write(f'{model_name}が存在しません')