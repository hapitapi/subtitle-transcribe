import sys
import whisper
import os

def transcribe_to_json(input_file, output_file):
    model = whisper.load_model("large")  
    result = model.transcribe(
        input_file,
        language="ja",
        word_timestamps=True, 
        fp16=False
    )

    # JSONとして保存
    with open(output_file, "w", encoding="utf-8") as f:
        import json
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使い方: python convert_json.py 入力ファイル名.mp4 出力ファイル名.json")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"入力ファイルが見つかりません: {input_path}")
        sys.exit(1)

    transcribe_to_json(input_path, output_path)
