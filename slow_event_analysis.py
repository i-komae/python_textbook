#!/usr/bin/env python3

import argparse
import csv
import gzip
import os
import time

import matplotlib.pyplot as plt
from tqdm import tqdm

NANOSECONDS_PER_SECOND = 1_000_000_000


def collect_event_files(input_dir):
    """入力ディレクトリの下にあるイベントファイルを日付順に集めます。"""
    file_paths = []

    for year_name in sorted(os.listdir(input_dir)):
        year_path = os.path.join(input_dir, year_name)
        if not os.path.isdir(year_path):
            continue

        for month_name in sorted(os.listdir(year_path)):
            month_path = os.path.join(year_path, month_name)
            if not os.path.isdir(month_path):
                continue

            for file_name in sorted(os.listdir(month_path)):
                if not file_name.startswith("events_"):
                    continue
                if not file_name.endswith(".txt.gz"):
                    continue
                file_paths.append(os.path.join(month_path, file_name))

    return file_paths


def hhmmss_to_seconds(hhmmss):
    """HHMMSS を、その日の 0 時からの秒に直します。"""
    hour = int(hhmmss[0:2])
    minute = int(hhmmss[2:4])
    second = int(hhmmss[4:6])
    return hour * 3600 + minute * 60 + second


def read_events_in_one_file(file_path):
    """1 つのファイルを読み、各イベントを辞書で持ちます。"""
    events = []

    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue

            # 文字列を空白で分割してリストを作成します
            columns = line.strip().split()
            if len(columns) != 8:
                continue

            hhmmss = columns[4]
            ns = int(columns[5])

            # 各フィールドに名前をつける「辞書(dict)」というデータ構造を利用してイベントを定義します

            event = {
                "file": file_path,
                "event_id": int(columns[0]),
                "detector_id": int(columns[6]),
                "hhmmss": hhmmss,
                "ns": ns,
                "elapsed_ns": hhmmss_to_seconds(hhmmss) * NANOSECONDS_PER_SECOND + ns,
            }
            events.append(event)

    # 比較の基準となる関数を定義して sort に渡します
    def get_elapsed_ns(event_dict):
        return event_dict["elapsed_ns"]

    events.sort(key=get_elapsed_ns)
    return events


def find_pairs_in_one_file(events, dt_ns):
    """1 つのファイルの中で、時間差が小さい 2 事象を探します。"""
    pairs = []

    for i in range(len(events)):
        first_event = events[i]

        for j in range(i + 1, len(events)):
            second_event = events[j]
            difference_ns = second_event["elapsed_ns"] - first_event["elapsed_ns"]

            if first_event["detector_id"] == second_event["detector_id"]:
                continue

            if difference_ns > dt_ns:
                continue

            if first_event["detector_id"] < second_event["detector_id"]:
                event1 = first_event
                event2 = second_event
            else:
                event1 = second_event
                event2 = first_event

            pair = {
                "file": event1["file"],
                "event_id1": event1["event_id"],
                "event_id2": event2["event_id"],
                "detector_id1": event1["detector_id"],
                "detector_id2": event2["detector_id"],
                "hhmmss_1": event1["hhmmss"],
                "ns_1": event1["ns"],
                "hhmmss_2": event2["hhmmss"],
                "ns_2": event2["ns"],
                "signed_dt_ns": event2["elapsed_ns"] - event1["elapsed_ns"],
                "mean_time_s": (event1["elapsed_ns"] + event2["elapsed_ns"]) / 2.0 / NANOSECONDS_PER_SECOND,
            }
            pairs.append(pair)

    return pairs


def make_gap_values(pairs):
    """隣り合う同時観測ペアどうしの平均時刻差を秒で作ります。"""
    gap_values = []

    for i in range(1, len(pairs)):
        gap_s = pairs[i]["mean_time_s"] - pairs[i - 1]["mean_time_s"]
        gap_values.append(gap_s)

    return gap_values


def write_pairs_csv(file_path, pairs):
    """同時観測ペアの一覧を書き出します。"""
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "file",
                "event_id1",
                "event_id2",
                "detector_id1",
                "detector_id2",
                "hhmmss_1",
                "ns_1",
                "hhmmss_2",
                "ns_2",
                "signed_dt_ns",
            ]
        )

        for pair in pairs:
            writer.writerow(
                [
                    pair["file"],
                    pair["event_id1"],
                    pair["event_id2"],
                    pair["detector_id1"],
                    pair["detector_id2"],
                    pair["hhmmss_1"],
                    pair["ns_1"],
                    pair["hhmmss_2"],
                    pair["ns_2"],
                    pair["signed_dt_ns"],
                ]
            )


def write_timing_csv(file_path, timing_rows):
    """各ファイルの読込み時間と探索時間を保存します。"""
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "n_events", "read_sec", "search_sec", "n_pairs"])

        for row in timing_rows:
            writer.writerow(row)


def write_histogram_pdf(file_path, values, title, x_label):
    """ヒストグラムを PDF で保存します。"""
    fig, ax = plt.subplots(figsize=(8, 5))

    if len(values) == 0:
        ax.text(0.5, 0.5, "no data", ha="center", va="center", transform=ax.transAxes)
    else:
        ax.hist(values, bins=40, color="#4C78A8", edgecolor="black")

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("count")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(file_path)
    plt.close(fig)


def write_graphs(output_dir, pairs, gap_values):
    """2 つの分布図を PDF で保存します。"""
    dt_values = []
    for pair in pairs:
        dt_values.append(pair["signed_dt_ns"])

    write_histogram_pdf(
        os.path.join(output_dir, "pair_dt_hist.pdf"),
        dt_values,
        "distribution of pair signed dt",
        "signed_dt_ns",
    )
    write_histogram_pdf(
        os.path.join(output_dir, "pair_mean_gap_hist.pdf"),
        gap_values,
        "distribution of pair mean timestamp gap",
        "gap_s",
    )


def analyze(input_dir, output_dir, dt_ns):
    """イベントファイルを順に読み、解析結果を保存します。"""
    os.makedirs(output_dir, exist_ok=True)

    old_path = os.path.join(output_dir, "pair_dt_ns.csv")
    if os.path.exists(old_path):
        os.remove(old_path)

    old_path = os.path.join(output_dir, "pair_mean_gap_s.csv")
    if os.path.exists(old_path):
        os.remove(old_path)

    event_files = collect_event_files(input_dir)

    all_pairs = []
    all_gap_values = []
    timing_rows = []

    total_start = time.perf_counter()

    for file_path in tqdm(event_files, desc="analyze", unit="file"):
        read_start = time.perf_counter()
        events = read_events_in_one_file(file_path)
        read_end = time.perf_counter()

        search_start = time.perf_counter()
        pairs = find_pairs_in_one_file(events, dt_ns)
        gap_values = make_gap_values(pairs)
        search_end = time.perf_counter()

        all_pairs.extend(pairs)
        all_gap_values.extend(gap_values)
        timing_rows.append(
            [
                file_path,
                len(events),
                read_end - read_start,
                search_end - search_start,
                len(pairs),
            ]
        )

    analysis_end = time.perf_counter()

    write_pairs_csv(os.path.join(output_dir, "coincidence_pairs.csv"), all_pairs)
    write_timing_csv(os.path.join(output_dir, "timing.csv"), timing_rows)

    plot_start = time.perf_counter()
    write_graphs(output_dir, all_pairs, all_gap_values)
    plot_end = time.perf_counter()

    with open(os.path.join(output_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(f"n_pairs_total {len(all_pairs)}\n")
        f.write(f"analysis_sec {analysis_end - total_start:.6f}\n")
        f.write(f"plot_sec {plot_end - plot_start:.6f}\n")
        f.write(f"total_sec {plot_end - total_start:.6f}\n")


def main():
    # コマンドライン引数をパースします
    parser = argparse.ArgumentParser(description="課題用の同時観測解析コード")
    parser.add_argument("input_dir", help="生成したイベントデータのディレクトリ")
    parser.add_argument("--outdir", default="slow_output", help="解析結果を書き出すディレクトリ")
    parser.add_argument("--dt-ns", type=int, default=250, help="同時観測とみなす時間差の上限 [ns]")
    args = parser.parse_args()

    analyze(args.input_dir, args.outdir, args.dt_ns)


# このスクリプトが直接実行されたときだけ起動するための定型句です
if __name__ == "__main__":
    main()
