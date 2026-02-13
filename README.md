# subtitle-transcribe

音声・動画から自動で字幕ファイル（SRT）を生成する Python スクリプトです。  
OpenAI Whisper を使って音声認識を行い、MeCab を利用して自然な日本語の区切りに整形します。  
PowerDirector などの動画編集ソフトにそのまま取り込める形式の SRT を出力します。

---

## 特徴
- 音声や動画ファイルから自動で文字起こし
- MeCab を利用した自然な日本語の文章分割
- PowerDirector 対応の SRT 形式で出力
- 複数の SRT を結合して1つにまとめる機能もあり

---

## 必要環境
- Python 3.9 以上  
- FFmpeg（Whisper が使用）  
- MeCab（日本語分かち書き用）

---

## インストール方法
 このリポジトリをクローン  
   ```bash
   git clone https://github.com/hapitapi/subtitle-transcribe.git
   cd subtitle-transcribe

使い方

1.MP4→JSON変換
Whisperを用いて動画ファイルからJSONを生成します。
　```bash
python convert_json.py sample.mp4

2.JSON→SR変換
Whisperで生成したJSONをSRTに変換します。
　```bash
python convert_srt.py sample.json sample.srt

2.複数SRTを結合
複数の字幕ファイルをまとめて1つにします。
　```bash
python merge_srt.py input1.srt input2.srt merged_output.srt
