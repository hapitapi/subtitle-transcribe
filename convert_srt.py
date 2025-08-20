import sys
import json
import os
from fugashi import GenericTagger
from moviepy.video.io.VideoFileClip import VideoFileClip

# タイミング補正
START_OFFSET = 0.3
END_OFFSET = 0.27

def format_time(seconds):
    seconds = float(seconds)
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def main(json_path, srt_path):
    video_path = json_path.replace(".json", ".mp4")

    try:
        clip = VideoFileClip(video_path)
        video_duration = clip.duration
        clip.close()
    except Exception as e:
        print(f"⚠️ 動画の長さ取得エラー：{e}")
        video_duration = None

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    words = []
    for segment in data["segments"]:
        words.extend(segment.get("words", []))

    if not words:
        print("⚠️ words情報がありません。")
        return

    # ✅ あなた専用のMeCab辞書パス設定
    tagger = GenericTagger('-d /opt/homebrew/lib/mecab/dic/ipadic -r /opt/homebrew/Cellar/mecab/0.996/.bottle/etc/mecabrc')

    with open(srt_path, "w", encoding="utf-8") as f:
        index = 1
        current_text = ""
        start_time = None
        prev_end_time = None

        for word_info in words:
            word = word_info["word"].strip()
            start = word_info["start"] + START_OFFSET
            end = word_info["end"] + END_OFFSET

            if start_time is None:
                start_time = start

            if prev_end_time is not None:
                silence = start - prev_end_time
                if silence >= 0.5:
                    if current_text:
                        f.write(f"{index}\n{format_time(start_time)} --> {format_time(prev_end_time)}\n{current_text.strip()}\n\n")
                        index += 1
                        start_time = start
                        current_text = ""

            current_text += word
            prev_end_time = end

            tokens = list(tagger(current_text))
            char_count = sum(len(t.surface) for t in tokens)

            if char_count >= 20:
                cut_text = ""
                temp_count = 0
                for t in tokens:
                    cut_text += t.surface
                    temp_count += len(t.surface)
                    if temp_count > 15:
                        break

                f.write(f"{index}\n{format_time(start_time)} --> {format_time(end)}\n{cut_text.strip()}\n\n")
                index += 1
                current_text = current_text[len(cut_text):]
                if current_text:
                    start_time = start

        if current_text:
            f.write(f"{index}\n{format_time(start_time)} --> {format_time(prev_end_time)}\n{current_text.strip()}\n\n")
            index += 1

        if video_duration and prev_end_time and (video_duration - prev_end_time) > 0.1:
            f.write(f"{index}\n{format_time(prev_end_time)} --> {format_time(video_duration)}\n \n\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使い方: python convert_srt.py 入力.json 出力.srt")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
