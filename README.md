## あなただけのAIで、思いのままの文章を

AI技術は進化していますが、出力される文章がどこか人間らしさに欠けること、感じたことはありませんか？

そこで、あなたの過去の記事を学習素材にして、gpt-3.5-turboをカスタマイズ。まるで「あなたが書いたかのような」文章をAIが生成します。


## 環境設定

- Poetryが必要です

```sh
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="/Users/satoru/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

ref: https://python-poetry.org/docs/


## 使い方

### アプリを立ち上げる

このリポジトリをcloneしてください。

```sh
git clone writer-finetuning
```

makeコマンドでアプリが立ち上がります

```sh
cd writer-finetuning
make
```


### 💸 あなたの文体を学び取るステップ
noteにアップした記事のURLを教えてください。その内容をもとに、あなたらしい文章を書くためのデータを準備し、gpt-3.5-turboをカスタマイズします。ただしあなたのOpenAI API Keyが必要です。ローカル環境だから安全だね。

### ✍️ あなたらしい文章を、今すぐ体験
新しいモデルを使って、思いついた内容を入力。すると、まるであなたが書いたかのような文章が生成されます。
