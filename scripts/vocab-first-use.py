"""
根据L01-L04手动策划的生词表，更新CSV中对应词的lesson列。
后续课文写完后可扩展此脚本。
"""
import csv
import os

CSV = r"d:\Project\GitHub\nihongo-learning\resources\jlpt-vocab-n5n4.csv"

# L01-L04 手动策划的词 → 首次出现课号
# 只列CSV中存在的词（课文补充词不在CSV中的不处理）
MANUAL = {
    # === L01: 人の世界 ===
    # 寒暄基本
    'いいえ': 1,
    # 身份职业
    '医者': 1, '課長': 1,
    # 家族
    'おじいさん': 1, 'おばあさん': 1, 'おじ': 1, 'おば': 1,
    'おじさん': 1, 'おばさん': 1,
    'お父さん': 1, 'お母さん': 1, 'お兄さん': 1, 'お姉さん': 1,
    # 其他
    '家族': 1, 'うち': 1, '皆さん': 1,

    # === L02: 物の世界 ===
    # 指示代词
    'それ': 2, 'どなた': 2, 'ええ': 2,
    # 文具办公
    'ペン': 2, 'ボールペン': 2, 'ノート': 2, 'テキスト': 2,
    # 数え方
    '一つ': 2, '二つ': 2, '三つ': 2, '四つ': 2, '五つ': 2,
    '六つ': 2, '七つ': 2, '八つ': 2, '九つ': 2,
    'いくつ': 2,
    # かばん
    'かばん': 2,

    # === L03: 場所の世界 ===
    # 場所代词
    'ここ': 3, 'そこ': 3, 'あそこ': 3, 'どこ': 3,
    'こちら': 3, 'そちら': 3, 'あちら': 3, 'どちら': 3,
    # 場所名
    'コンビニ': 3, 'スーパー': 3, 'デパート': 3,
    '映画館': 3, 'ホテル': 3, '高校': 3,
    # 数字金額
    'グラム': 3,
    # 位置
    '近く': 3,

    # === L04: 家の世界 ===
    # 方位词
    'そば': 4,
    # 家具家電
    'テーブル': 4, 'ドア': 4, 'エアコン': 4, 'シャワー': 4,
    'テレビ': 4, 'ストーブ': 4, 'アパート': 4,
    # 動物 - 犬 not in CSV? check
    # 住居
    '温泉': 4,
    # その他
    'あの': 4, 'この': 4, 'いつ': 4,
    'こっち': 4, 'あれ': 4, 'さあ': 4,
}

def main():
    # Read CSV
    with open(CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        rows = list(reader)

    # Find lesson column index
    lesson_idx = header.index('lesson')
    word_idx = 0  # 词条 column

    updated = 0
    for row in rows:
        word = row[word_idx]
        if word in MANUAL:
            old_lesson = row[lesson_idx]
            new_lesson = str(MANUAL[word])
            if old_lesson != new_lesson:
                row[lesson_idx] = new_lesson
                updated += 1

    # Write back
    with open(CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(header)
        # Sort by lesson
        rows.sort(key=lambda r: (int(r[lesson_idx]), r[-1] if len(r) > lesson_idx + 1 else '', r[0]))
        writer.writerows(rows)

    print(f"更新了 {updated} 个词的lesson标记")

    # Verify L01-L04 counts
    for l in range(1, 5):
        count = sum(1 for r in rows if r[lesson_idx] == str(l))
        print(f"  L{l:02d}: {count}词")

if __name__ == '__main__':
    main()
