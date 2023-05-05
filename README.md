# scrapy_sample

Scrapyを使ってスクレイピングするサンプルプロジェクト。対象は[MAMANにITブログ](https://blog.mamansoft.net/)。

## 準備

```console
python -m venv .venv
.venv/Scripts/activate.ps1
pip install -r requirements.txt
```

## 実行

```console
scrapy crawl blog -O result.json
```

`result.json`に結果が、`full`配下には画像が出力される。
