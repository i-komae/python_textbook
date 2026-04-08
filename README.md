# Pythonによるデータ解析と高速化

このディレクトリには、LaTeX で書かれたテキスト原稿と、その出力 PDF を置いています。

## PDF

- [main.pdf](./main.pdf)

上の PDF が、カレントディレクトリに置いてある最新版の通読用ファイルです。

## 主なファイル

- `main.tex`: 全体をまとめる親ファイル
- `chapters/`: 各章の本文
- `assets/`: 図や補助ファイル
- `build/`: LaTeX のビルド生成物

## 章構成

- 本文: `00_intro.tex` から `10_assignment.tex`
- 付録: `90_ssh.tex`, `91_git.tex`

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

- 課題用のスクリプトとデータとして `slow_event_analysis.py` と `events_data.zip` を同じディレクトリに置いています。
- Git 管理やシェル操作の説明は、付録や前半章にも含まれています。
