import sys
import re
import os

def read_srt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip().split("\n\n")

def write_srt(path, blocks):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocks).strip() + "\n")  # 最後は改行1つで終了

def parse_time(time):
    h, m, s_ms = time.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def format_time(seconds):
    ms = int((seconds % 1) * 1000)
    total = int(seconds)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def merge_srt_files(input_paths, output_path):
    merged_blocks = []
    offset = 0.0
    index = 1

    for path in input_paths:
        if not os.path.exists(path):
            print(f"ファイルが見つかりません: {path}")
            continue

        blocks = read_srt(path)

        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) < 3:
                continue  # 空の字幕や不正なブロックは無視

            time_line = lines[1]
            try:
                start, end = re.findall(r"(\d+:\d+:\d+,\d+)", time_line)
            except:
                continue

            start_sec = parse_time(start) + offset
            end_sec = parse_time(end) + offset
            if end_sec <= start_sec:
                continue  # 時間がおかしい字幕は除外

            new_time = f"{format_time(start_sec)} --> {format_time(end_sec)}"
            text = "\n".join(lines[2:]).strip()
            if not text:
                continue  # 空字幕スキップ

            merged_blocks.append(f"{index}\n{new_time}\n{text}")
            index += 1

        # 最後の時間を次の字幕のオフセットに使う
        if blocks:
            last_block = blocks[-1].split("\n")
            if len(last_block) >= 2:
                try:
                    _, end = re.findall(r"(\d+:\d+:\d+,\d+)", last_block[1])
                    offset = parse_time(end)
                except:
                    pass

    write_srt(output_path, merged_blocks)
    print(f"PowerDirector対応 SRT結合完了: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使い方: merge_srt.py input1.srt input2.srt ... output.srt")
        sys.exit(1)
    *input_paths, output_path = sys.argv[1:]
    merge_srt_files(input_paths, output_path)
