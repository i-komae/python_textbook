# Pythonによるデータ解析と高速化

このディレクトリには、LaTeX で書かれたテキスト原稿と、その出力 PDF を置いています。

## PDF

- [main.pdf](./main.pdf)

上の PDF が、カレントディレクトリに置いてある最新版の通読用ファイルです。

## 入手方法

このリポジトリは GitHub から取得できます。

```sh
git clone git@github.com:i-komae/python_textbook.git
cd python_textbook
```

ブラウザから ZIP を落としてもよいですが、更新を追いやすいので通常は `git clone` の方が扱いやすいです。この README では、後で push や private repository の取得へ移りやすいように、HTTPS より SSH を推奨しています。

## 主なファイル

- `main.tex`: 全体をまとめる親ファイル
- `chapters/`: 各章の本文
- `assets/`: 図や補助ファイル
- `build/`: LaTeX のビルド生成物
- `slow_event_analysis.py`: 課題で使う配布スクリプト
- `events_data.zip`: 課題で使う配布データ

## ディレクトリ構造

主要部分だけ書くと、配置は次のようになっています。

```text
python_textbook/
├── README.md
├── Makefile
├── main.tex
├── main.pdf
├── slow_event_analysis.py
├── events_data.zip
├── chapters/
│   ├── intro.tex
│   ├── ...
│   ├── assignment.tex
│   ├── appendix_ssh.tex
│   ├── appendix_git.tex
│   └── appendix_regex.tex
├── assets/
├── scripts/
└── build/
```

課題で参照する配布ファイルは、現在はリポジトリ直下に置いています。`events_data.zip` を展開すると `events_data/` ディレクトリができ、`slow_event_analysis.py` からそのディレクトリを入力として読みます。

## 章構成

- 本文: `intro.tex` から `assignment.tex`
- 付録: `appendix_ssh.tex`, `appendix_git.tex`, `appendix_regex.tex`, `appendix_shell_scripting.tex`

## コンパイル

通常は、次のように `make` を使います。

```sh
make
```

`make` は差分があるときだけビルドし、目次や相互参照のために追加のコンパイルが必要な場合は `latexmk` が自動的に必要回数だけ再実行します。ビルド後は、Skim が入っていれば Skim で、入っていなければ既定の PDF アプリで `main.pdf` を開きます。

強制的に全体を作り直したいときは、次を使います。

```sh
make all
```

補助ファイルと生成された PDF を消して作り直したいときは、次を使います。

```sh
make distclean
make
```

通常の `make` では、内部で次の `latexmk` コマンドを使っています。

```sh
TEXMFCACHE=build/texmf-cache TEXMFVAR=build/texmf-var \
latexmk -f -lualatex -synctex=1 -interaction=nonstopmode \
  -file-line-error -output-directory=build main.tex
```

`make all` では、これに `-gg` を付けて強制再コンパイルします。

## 補足

- 課題用のスクリプトとデータは、リポジトリ直下の `slow_event_analysis.py` と `events_data.zip` です。
- Git 管理やシェル操作の説明は、付録や前半章にも含まれています。
