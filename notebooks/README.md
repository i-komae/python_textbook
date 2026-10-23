# 章末課題の解説Notebook

各Notebookは、本文の課題を「考え方、実装、結果の確認」の順に解説します。本文の小規模入力から始め、期待値、境界条件、保存ファイルの読み戻しを確認できます。それぞれ単独で実行できるため、前のNotebookの実行状態を引き継ぐ必要はありません。

## 起動する

Python 3.12以降を用意し、リポジトリ直下で次を実行してください。シェルの実習はmacOSまたはLinux（WindowsではWSL）を対象としています。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r notebooks/requirements.txt
python -m jupyterlab notebooks
```

uvを利用する場合は、次の方法でも起動できます。

```sh
uv venv --python 3.12
uv pip install -r notebooks/requirements.txt
uv run --no-project --python .venv/bin/python python -m jupyterlab notebooks
```

Notebookを開き、コードセルを上からShift+Enterで実行してください。セルの下に出た値や図を、前後の説明と比べます。最後にカーネルを再起動して全セルを上から実行すると、前の実行状態に依存していないことを確かめられます。ファイルを作る問では、その直前の「保存先を用意する」セルでPythonの版と出力先を確認できます。図、CSV、仮想環境、実習用スクリプトなどは `notebooks/_outputs/<Notebook名>/` に作成され、再実行時には同名の実習用生成物を置き換えます。

## 本文との対応

番号は本文の章番号ではなく、課題Notebookの実行順を示します。

| Notebook | 対応する本文 | 解説する内容 |
| --- | --- | --- |
| [01_shell.ipynb](01_shell.ipynb) | シェル | 作業場所、USGSの取得条件、内容の調査、3形式の圧縮と全バイト照合、URLを解説します。 |
| [02_setup.ipynb](02_setup.ipynb) | 実行環境・付録「実行環境の補足」 | 動いているPythonを確認し、venv、uv、pyenvの順に違いを確かめます。 |
| [03_basics.ipynb](03_basics.ipynb) | 基本構文 | 1件の取り出しから、反復、欠損判定、平均関数、時刻差、端末の引数へ進みます。 |
| [04_io.ipynb](04_io.ipynb) | 入出力 | CSVの要約、JSONとPickleの読み戻し、不正値の記録を解説します。 |
| [05_numpy.ipynb](05_numpy.ipynb) | NumPy | 4個の時刻で差分を確かめ、課題の6個の時刻、axis、区間集計、地域比較へ進みます。 |
| [06_pandas.ipynb](06_pandas.ipynb) | pandas | 欠損、条件抽出、群集計、結合、チャンク集計、Parquetを解説します。 |
| [07_polars.ipynb](07_polars.ipynb) | Polars | 列式、群平均、実行計画、結合、pivot、pandasとの照合を解説します。 |
| [08_matplotlib.ipynb](08_matplotlib.ipynb) | Matplotlib | 散布図、カラーバー、対数ビン、保存、Cartopyを解説します。 |
| [09_scipy.ipynb](09_scipy.ipynb) | SciPy | 指数分布、重み付きフィット、残差、AIC、切断分布、Gutenberg–Richter関係を解説します。 |
| [10_astropy.ipynb](10_astropy.ipynb) | Astropy | 単位、秒境界、UTCとTAI、ECSVとFITS、座標変換を解説します。 |
| [11_modules.ipynb](11_modules.ipynb) | 自作モジュール | src構成、公開API、2件のテスト、docstring、2種類のインストールを解説します。 |
| [12_performance.ipynb](12_performance.ipynb) | 高速化 | 5回の時間測定、計算量、ビュー、逐次集計、メモリ、プロファイルを解説します。 |
| [13_assignment.ipynb](13_assignment.ipynb) | 総合課題 | 整数時刻、時間窓探索、配布コードとの比較、3日と全500日の検証、作図とフィットを解説します。 |

## 実データと発展課題を実行する

通常の全セル実行では、本文に示された人工データとリポジトリ内の配布データを使い、外部への通信は行いません。

- USGSの取得は01の端末用コマンドを使います。取得日時、検索条件、countの応答を保存し、取得上限とイベントIDの重複を確認してください。人工データは実カタログと別名で保存します。
- 05と09で `REAL_CSV` に取得済みカタログのパスを設定すると、地域比較と実際の発生間隔の解析を実行できます。実データについては種別、マグニチュード尺度、対象範囲、モデルの仮定も記録してください。
- 08の地図はCartopyと海岸線データを用意してから `RUN_CARTOPY = True` とします。導入用コマンドと、初回の海岸線データ取得についてはNotebook内に記載しています。
- 02のpyenvによる2系統のPythonの比較と、対話シェルの有効化・解除は端末で行います。Notebookにはコマンドと判定方法を記載しています。セル内で起動した別シェルの変更はカーネルへ引き継がれません。
- 13は通常、最初の3日分を処理します。`RUN_FULL = True` で全500日を再計算できます。配布コードの基準測定は二重ループを含むため、計算機によって時間がかかります。

## 全Notebookを検証する

リポジトリ直下で実行します。Notebookごとに新しいカーネルを起動し、そのNotebookがあるフォルダーを現在位置として実行します。エラーや期待値との不一致があれば終了します。

```sh
python scripts/check_notebooks.py
python scripts/check_notebooks.py --full
```

`--full` は総合課題の全500日も検証します。実行結果をNotebookへ保存する場合は `--save` を加えます。特定のNotebookだけを再検証する場合はパスを指定できます。

`--save` では、保存するテキスト出力内の環境固有のパスを `[教材フォルダー]`、`[Python本体]`、`[ホーム]`、`[一時フォルダー]` へ置き換えます。計算結果と図は保持します。手元でセルを実行すると、その環境の実際のパスが表示されます。

```sh
python scripts/check_notebooks.py notebooks/10_astropy.ipynb
```

検証用の一時ファイルは `build/notebook-validation/` に保存します。通常の検証では、実カタログの取得、Cartopyの描画、端末でのpyenv切り替えは実行しません。

2026年10月24日に、Python 3.12.14で全13冊を新しいカーネルから実行し、期待値と保存ファイルを確認しました。Notebookのあるフォルダーを現在位置として実行しています。総合課題は最初の3日で66組、全500日で12,033組となり、配布データの基準値に一致しました。主なライブラリはNumPy 2.5.4、pandas 3.0.6、Polars 2.0.0、Matplotlib 3.11.2、SciPy 1.18.1、Astropy 8.0.2、PyArrow 26.0.0です。
