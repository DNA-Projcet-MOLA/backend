import os
import json
import pandas as pd
import ace_tools_open as tools  # ✅ 올바른 모듈

# ======== 1. 원본 JSON 파일에서 문제 설명 추출 (문항(텍스트)만) ========
base_dir = r"C:\python_DNA\data_file"
extracted_questions = []

if os.path.exists(base_dir):
    for folder in os.listdir(base_dir):
        if folder.startswith("VL"):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith(".json"):
                        json_path = os.path.join(folder_path, file)
                        try:
                            with open(json_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                for section in data.get("learning_data_info", []):
                                    if section.get("class_name") == "문항(텍스트)":
                                        for info in section.get("class_info_list", []):
                                            text = info.get("text_description", "").strip()
                                            if text:
                                                extracted_questions.append(text)
                        except Exception as e:
                            print(f"Error reading {json_path}: {e}")
else:
    print(f"Directory not found: {base_dir}")

# ======== 2. 텍스트 파일로 저장 (원본) ========
raw_txt_path = r"C:\python_DNA\extracted_questions.txt"
with open(raw_txt_path, 'w', encoding='utf-8') as f:
    for line in extracted_questions:
        f.write(line + '\n')




# # ======== 3. 간단한 정제 기준으로 불필요한 문장 제거 ========
# exact_removal_lines = [
#     "다음을 계산하시오", "다음 계산하시오", "계산하시오"
# ]

# removal_keywords = [
#     "이것을 구하시오", "적절한 것을 고르시오",
#     "옳은 것을 고르시오", "바르게 나타낸 것",
#     "맞는 것을", "보기에서", "보기", "에 알맞은",
#     "보기에", "적절한", "고르시오"
# ]

# cleaned_questions = []
# for line in extracted_questions:
#     if len(line.strip()) < 8:
#         continue
#     if line.strip() in exact_removal_lines:
#         continue
#     if any(kw in line for kw in removal_keywords):
#         continue
#     cleaned_questions.append(line.strip())

# # ======== 4. 정제된 텍스트 파일로 저장 ========
# clean_txt_path = r"C:\python_DNA\extracted_questions_cleaned.txt"
# with open(clean_txt_path, 'w', encoding='utf-8') as f:
#     for line in cleaned_questions:
#         f.write(line + '\n')

# # ======== 5. 화면에 미리보기 ========
# df = pd.DataFrame(cleaned_questions, columns=["문제 설명"])
# tools.display_dataframe_to_user(name="정제된 문제 설명", dataframe=df)
