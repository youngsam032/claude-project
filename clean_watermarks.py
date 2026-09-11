import os
import re

# 제로위드 특수문자 및 보이지 않는 유니코드 워터마크 패턴
ZERO_WIDTH_RE = re.compile(r'[\u200B-\u200D\u200E\u200F\uFEFF\u202A-\u202E]')

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        cleaned = ZERO_WIDTH_RE.sub('', content)
        if content != cleaned:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print(f"[정제 완료] {filepath}")
            return True
    except Exception:
        pass
    return False

def scan_workspace():
    count = 0
    for root, _, files in os.walk('.'):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith(('.md', '.py', '.r', '.R', '.csv', '.txt', '.tex')):
                path = os.path.join(root, file)
                if clean_file(path):
                    count += 1
    print(f"스캔 완료: 총 {count}개 파일에서 숨은 특수문자/워터마크 정제됨")

if __name__ == '__main__':
    scan_workspace()
