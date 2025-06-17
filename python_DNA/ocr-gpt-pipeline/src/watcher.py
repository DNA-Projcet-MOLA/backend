import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tqdm import tqdm

from src.ocr_latex import img2latex
from src.ocr_text import img2text
from src.gpt_struct import struct_problem_with_gpt

import json
import time

IMAGES_DIR = "images/"
RESULTS_PATH = "results/problems.json"

class ImageHandler(FileSystemEventHandler):
    def __init__(self):
        os.makedirs("results", exist_ok=True)
        # 기존 데이터셋 로드
        if os.path.exists(RESULTS_PATH):
            with open(RESULTS_PATH, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = []

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"New image detected: {event.src_path}")
            self.process_image(event.src_path)
            self.save_results()

    def process_image(self, image_path):
        print(f"[Step 1] 텍스트 OCR 수행")
        text = img2text(image_path)
        print(f"[Step 2] 수식(Latex-OCR) 수행")
        latex = img2latex(image_path)
        print(f"[Step 3] GPT 구조화")
        info = struct_problem_with_gpt(text, latex, image_path)
        print(f"→ 구조화 결과: {info['question'][:50]}...")
        self.data.append(info)

    def save_results(self):
        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"저장 완료: {RESULTS_PATH}")

def run_watcher():
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, IMAGES_DIR, recursive=False)
    observer.start()
    print(f"이미지 폴더 감시 시작: {IMAGES_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()