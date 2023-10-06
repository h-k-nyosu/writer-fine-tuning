import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import json
import time
import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_icon="💸",
)

api_key = st.text_input('API KEYを入力してください', value=os.environ.get('OPENAI_API_KEY'))


OUTPUT_PREFIX = 'output_'
SUMMARY_PREFIX = 'summary_'

dir_name = st.text_input('ディレクトリ名を入力してください',
                         value='',
                         placeholder='デフォルトで日付が入ります(e.g. 202310061842)')

output_dir = "output"

api_key_dir = api_key[:7]

if not dir_name:
    dir_name = datetime.datetime.now().strftime('%Y%m%d%H%M')

output_path = os.path.join(output_dir, api_key_dir, dir_name)



def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
    return response

def parse_html(response):
    return BeautifulSoup(response.text, 'html.parser')

def format_content(soup):
    content = ""
    h1_tags = soup.find_all('h1')
    if len(h1_tags) > 1:
        h1_text = h1_tags[1].text.replace('\n', '').replace(' ', '')
        content += f"# {h1_text}\n"
    for tag in soup.find_all(['h2', 'h3', 'p']):
        if tag.name == 'h2':
            content += f"## {tag.text}\n"
        elif tag.name == 'h3':
            content += f"### {tag.text}\n"
        else:
            content += f"{tag.text}\n"
    return content

def fetch_and_parse(urls):
    with st.spinner('記事コンテンツを取得しています...'):
        contents = []
        for url in urls:
            response = fetch_url(url)
            soup = parse_html(response)
            content = format_content(soup)
            contents.append(content)
    return contents

def write_to_file(contents):
    with st.spinner('ファイルに書き込んでいます...'):
        for i, content in enumerate(contents):
            paragraphs = []
            paragraph = ""
            for line in content.split('\n'):
                if len(paragraph) + len(line) > 300:
                    if paragraph:
                        paragraphs.append(paragraph)
                    paragraph = line + '\n'
                else:
                    paragraph += line + '\n'
            if paragraph:
                paragraphs.append(paragraph)
            for j, paragraph in enumerate(paragraphs):
                with open(f'{output_path}/{OUTPUT_PREFIX}{i}_{j}.txt', 'w') as f:
                    f.write(paragraph)

def summarize_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text into bullet points."},
                {"role": "user", "content": text}
            ]
        )
    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
    return response['choices'][0]['message']['content']

def summarize_files(directory):
    with st.spinner('記事から要素を抽出しています...'):
        for filename in os.listdir(directory):
            if filename.startswith(OUTPUT_PREFIX):
                with open(os.path.join(directory, filename), 'r') as f:
                    content = f.read()
                    summary = summarize_text(content)
                    with open(os.path.join(directory, SUMMARY_PREFIX + filename), 'w') as f_summary:
                        f_summary.write(summary)

SYSTEM_PROMPT = """あなたはプロの編集者です。
ユーザーからは書きたい内容を箇条書きで渡されるので、それをもとに読者に読ませるような魅力的な文章を生成します。
"""

USER_PROMPT = """## ユーザーが書きたい内容
{summary_output}
"""

ASSISTANT_PROMPT = """{content}"""


def upload_file_to_openai(jsonl):
    with st.spinner('データセットをアップロードしています...'):
        return openai.File.create(
            purpose="fine-tune",
            file=jsonl
        )

def start_finetuning(file_response):
    with st.spinner('Fine tuning jobを作成しています...'):
        return openai.FineTuningJob.create(
            training_file=file_response['id'],
            model='gpt-3.5-turbo-0613',
        )

def wait_for_finetuning():
    with st.spinner('Fine tuningを実行中です...'):
        while True:
            ft_job = openai.FineTuningJob.list(limit=1)
            status = ft_job['data'][0]['status']
            print(f"現在のステータスは{status}です")
            if status == 'failed':
                st.write('Fine tuningが失敗しました。文章量が少ないので記事URLを追加してください。😢')
                break
            if status == 'succeeded':
                model_name = ft_job['data'][0]['model']
                with open(f"{output_path}/model_name.txt", 'w') as f:
                    f.write(model_name)
                st.write('完了しました。サイドバーの「文章を生成する」から利用してください。🎉')
                break
            time.sleep(10)

def create_dataset(directory):
    with st.spinner('データセットを作成しています...'):
        dataset = []
        for filename in os.listdir(directory):
            if filename.startswith(OUTPUT_PREFIX):
                with open(os.path.join(directory, filename), 'r') as f:
                    content = f.read()
                summary_filename = SUMMARY_PREFIX + filename
                with open(os.path.join(directory, summary_filename), 'r') as f_summary:
                    summary = f_summary.read()
                data = {
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": USER_PROMPT.format(summary_output=summary)},
                        {"role": "assistant", "content": ASSISTANT_PROMPT.format(content=content)}
                    ]
                }
                dataset.append(data)
        
        jsonl = '\n'.join([json.dumps(item) for item in dataset])
        return jsonl

def app():
    urls = st.text_area("noteのURLを入力してください（1行に1つ）").split('\n')
    if st.button('Submit'):
        openai.api_key = api_key
        os.makedirs(output_path, exist_ok=True)
        contents = fetch_and_parse(urls)
        write_to_file(contents)
        summarize_files(output_path)
        jsonl = create_dataset(output_path)
        
        print(jsonl[:100])
        file_response = upload_file_to_openai(jsonl)
        print(file_response)
        response = start_finetuning(file_response)
        print(response)
        wait_for_finetuning()
        

app()