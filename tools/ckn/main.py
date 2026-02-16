import sys
import datetime
import os
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

IGNORE_DIRS = {
    ".git", ".obsidian", ".idea", ".vscode", "__pycache__",
    "assets", "images", "node_modules", "dist", "build", "ckn", "ckn.egg-info", "tools",
}

# ==========================================
# TEMPLATES
# ==========================================

TPL_STANDARD = """---
title: "{title}"
date: {date}
category: "{category}"
tags: []
status: draft
---

# {title}

## 1. Summary
## 2. Content
## 3. Related
- [[Link]]
"""

TPL_CODING = """---
title: "{title}"
date: {date}
category: "{category}"
tags: [dev, implementation]
status: draft
---

# {title}

## 1. Context / Problem
## 2. Solution
""" + """```python
# Fixed code here
pass
""" + """```

## 3. Root Cause
## 4. References
- [StackOverflow / Docs](url)
"""

TPL_THEORY = """---
title: "{title}"
date: {date}
category: "{category}"
tags: [theory, deep-learning]
paper_link: 
status: draft
---

# {title}

## 1. Abstract / TL;DR
## 2. Main Contents
## 3. Key Takeaways
1. 
2. 

## 4. Future Work / Questions
- 
"""

TEMPLATES = {
    "1": ("Standard (Generic)", TPL_STANDARD),
    "2": ("Coding (Dev/Bugfix)", TPL_CODING),
    "3": ("Theory (Math/Paper)", TPL_THEORY),
}

# ==========================================
# FUNCTIONS
# ==========================================

def scan_directories(root_path: Path):
    """
    root_path 以下のディレクトリを再帰的にスキャンし、
    Pathオブジェクトのリストを返します（ルートからの相対パス）。
    """
    valid_dirs = []
    
    # os.walkを使用している理由: 
    # dirs[:] によるインプレース変更で、不要なディレクトリの深掘りを効率的に防げるため
    for current, dirs, _ in os.walk(root_path):
        # 除外ディレクトリをリストから削除
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        
        current_path = Path(current)
        rel_path = current_path.relative_to(root_path)
        
        if rel_path == Path('.'):
            continue
        
        valid_dirs.append(rel_path)
    
    return sorted(valid_dirs)

def get_safe_filename(title: str) -> str:
    """ファイル名として安全な文字列に変換"""
    safe = title.strip().replace(" ", "-")
    safe = safe.replace("/", "-").replace("\\", "-")
    safe = safe.replace(":", "").replace("*", "").replace("?", "")
    return safe

def main():
    # リポジトリ存在確認
    if not REPO_ROOT.exists():
        print(f"Error: Repository root not found at: {REPO_ROOT}")
        sys.exit(1)

    print(f"\n=== Create Knowledge Note (Pathlib Edition) ===")
    print(f"Target Repo: {REPO_ROOT}\n")
    
    # -------------------------------------------
    # 1. カテゴリ選択
    # -------------------------------------------
    categories = scan_directories(REPO_ROOT)
    
    if not categories:
        print("No subdirectories found.")
        sys.exit(0)

    print("--- [Step 1] Select Category ---")
    for idx, path in enumerate(categories, 1):
        # Windowsでも表示を "/" 区切りにするため as_posix() を使用
        display_name = "ROOT" if path == Path('.') else path.as_posix()
        print(f" [{idx}] {display_name}")

    selected_category_path = Path('.')
    while True:
        try:
            choice = input("Category number > ").strip()
            if not choice: continue
            
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                selected_category_path = categories[idx]
                break
            else:
                print(f"Please enter 1-{len(categories)}")
        except ValueError:
            pass

    # -------------------------------------------
    # 2. タイトル入力
    # -------------------------------------------
    print("\n--- [Step 2] Enter Title ---")
    while True:
        raw_title = input("Note title > ").strip()
        if raw_title:
            break
        print("Title cannot be empty.")

    # -------------------------------------------
    # 3. テンプレート選択
    # -------------------------------------------
    print("\n--- [Step 3] Select Template ---")
    for key, (name, _) in TEMPLATES.items():
        print(f" [{key}] {name}")
    
    selected_tpl_str = ""
    while True:
        choice = input("Template number > ").strip()
        if choice == "": choice = "1" # Default
        
        if choice in TEMPLATES:
            selected_tpl_str = TEMPLATES[choice][1]
            break
        print("Invalid template number.")

    # -------------------------------------------
    # 4. ファイル生成実行
    # -------------------------------------------
    today_str = datetime.date.today().isoformat()
    safe_title = get_safe_filename(raw_title)
    filename = f"{today_str}-{safe_title}.md"

    # pathlibの演算子 `/` でパスを結合
    target_dir = REPO_ROOT / selected_category_path
    target_file = target_dir / filename

    # Frontmatter用カテゴリ表記（Windows対策で強制的に / 区切りにする）
    cat_display = selected_category_path.as_posix()
    if cat_display == ".": cat_display = "root"

    # テンプレート適用
    file_content = selected_tpl_str.format(
        title=raw_title,
        date=today_str,
        category=cat_display
    )

    try:
        # ディレクトリ作成 (mkdir -p 相当)
        target_dir.mkdir(parents=True, exist_ok=True)

        if target_file.exists():
            print(f"\n[Warning] File already exists: {filename}")
            if input("Overwrite? (y/n): ").lower() != 'y':
                sys.exit(0)

        # ファイル書き込み (write_textを使用)
        target_file.write_text(file_content, encoding="utf-8")
        
        print(f"\nSuccessfully created:\n -> {target_file}")
        
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    main()