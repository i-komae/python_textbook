# Pythonによるデータ解析と高速化

このディレクトリには、LaTeX で書かれたテキスト原稿と、その出力 PDF を置いています。

## PDF

- [main.pdf](./main.pdf)

上の PDF が、カレントディレクトリに置いてある最新版の通読用ファイルです。

## 入手方法

このリポジトリは GitHub から取得できます。

```sh
git clone https://github.com/i-komae/python_textbook.git
cd python_textbook
```

ブラウザから ZIP を落としてもよいですが、更新を追いやすいので通常は `git clone` の方が扱いやすいです。

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
│   ├── 00_intro.tex
│   ├── ...
│   ├── 10_assignment.tex
│   ├── 90_ssh.tex
│   ├── 91_git.tex
│   └── 92_regex.tex
├── assets/
├── scripts/
└── build/
```

課題で参照する配布ファイルは、現在はリポジトリ直下に置いています。`events_data.zip` を展開すると `events_data/` ディレクトリができ、`slow_event_analysis.py` からそのディレクトリを入力として読みます。

## 章構成

- 本文: `00_intro.tex` から `10_assignment.tex`
- 付録: `90_ssh.tex`, `91_git.tex`, `92_regex.tex`

## コンパイル

通常は、次のように `make` を使います。

```sh
make
```

補助ファイルと生成された PDF を消して作り直したいときは、次を使います。

```sh
make distclean
make
```

内部では、次の `latexmk` コマンドを使っています。

```sh
TEXMFCACHE=build/texmf-cache TEXMFVAR=build/texmf-var \
latexmk -f -gg -pv -lualatex -synctex=1 -interaction=nonstopmode \
  -file-line-error -output-directory=build main.tex
```

## 補足

- 課題用のスクリプトとデータは、リポジトリ直下の `slow_event_analysis.py` と `events_data.zip` です。
- Git 管理やシェル操作の説明は、付録や前半章にも含まれています。
