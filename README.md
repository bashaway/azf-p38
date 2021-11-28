![workflow status](https://github.com/bashaway/azf-p38/actions/workflows/main.yml/badge.svg)

# azf-p38

## github actions

うまいことライブラリのダウンロードができなかった場合に、デプロイログに以下のようなメッセージが出力される場合がある。
このときは、ライブラリが利用できず実行エラーが発生するため、再度デプロイする必要がある。

```
Collecting PyMuPDF==1.16.14
  WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ReadTimeoutError("HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out. (read timeout=15)")': /packages/6e/6a/1294187941deddf7faefefdb012ba1ff85caca3017fce883fbfcaf8e6d73/PyMuPDF-1.16.14-cp38-cp38-manylinux2010_x86_64.whl
  Downloading PyMuPDF-1.16.14-cp38-cp38-manylinux2010_x86_64.whl (5.7 MB)
```

