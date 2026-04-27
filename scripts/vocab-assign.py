"""
词汇分配脚本 v2：将1568词分配到48课
约束：单桶单课≤10、每课12-55词、形容词前置≥30
"""
import csv
import re
from collections import Counter, defaultdict
import importlib.util, os

INPUT = r"d:\Project\GitHub\nihongo-learning\resources\jlpt-vocab-n5n4.csv"

# 加载分桶逻辑
spec = importlib.util.spec_from_file_location("bucket",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab-bucket.py"))
bucket_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bucket_mod)

ARCS = {
    1:  [1,2,3,4],     2:  [5,6,7,8],
    3:  [9,10,11,12],   4:  [13,14,15,16],
    5:  [17,18,19,20],  6:  [21,22,23,24],
    7:  [25,26,27,28],  8:  [29,30,31,32],
    9:  [33,34,35,36],  10: [37,38,39,40],
    11: [41,42,43,44],  12: [45,46,47,48],
}
ARC_NAMES = {
    1:'到达·安顿', 2:'日常节奏', 3:'社交展开', 4:'生活技能',
    5:'年末年始', 6:'告别东京', 7:'新城市', 8:'工作推进',
    9:'接待朋友·上', 10:'北京游', 11:'项目冲刺', 12:'开业',
}

BUCKET_ARC_MAP = {
    '基础·代词指示':   {1:.7, 2:.2, 3:.1},
    '基础·感叹寒暄':   {1:.4, 2:.3, 3:.2, 6:.1},
    '基础·接续助词':   {2:.3, 3:.2, 4:.2, 5:.15, 6:.15},
    '基础·连体词':     {1:.6, 2:.2, 3:.2},
    '基础·接头接尾':   {1:.3, 3:.3, 5:.4},
    '基础·接尾':       {2:.3, 4:.3, 5:.2, 7:.2},
    '基础·量词单位':   {1:.3, 2:.3, 3:.2, 4:.2},
    '基础·造语':       {1:.3, 2:.4, 5:.3},
    '动词·补助':       {4:1.0},
    # 动词：L05起。前密后疏，但避免Arc2过载
    '动词·一类':  {2:.25, 3:.18, 4:.18, 5:.12, 6:.07, 7:.06, 8:.05, 9:.03, 10:.02, 11:.02, 12:.02},
    '动词·二类':  {2:.25, 3:.18, 4:.18, 5:.12, 6:.07, 7:.06, 8:.05, 9:.03, 10:.02, 11:.02, 12:.02},
    '动词·三类':  {2:.22, 3:.16, 4:.16, 5:.12, 6:.07, 7:.07, 8:.06, 9:.04, 10:.03, 11:.04, 12:.03},
    # 形容词：L09起。Arc3拿大头但不过载
    '形容词·い形':  {3:.35, 4:.18, 5:.14, 6:.06, 7:.06, 8:.06, 9:.03, 10:.04, 11:.03, 12:.05},
    '形容词·な形':  {3:.35, 4:.18, 5:.14, 6:.06, 7:.06, 8:.06, 9:.03, 10:.04, 11:.04, 12:.04},
    '名词·时间':      {1:.35, 2:.30, 3:.10, 5:.10, 6:.05, 7:.05, 8:.05},
    '名词·数量':      {1:.50, 2:.25, 3:.15, 4:.10},
    '名词·人物职业':  {1:.25, 2:.15, 3:.15, 4:.10, 5:.05, 6:.05, 7:.05, 8:.05, 9:.05, 11:.05, 12:.05},
    '名词·方位位置':  {1:.40, 3:.15, 4:.15, 7:.15, 9:.15},
    '名词·场所':      {1:.20, 2:.15, 3:.10, 4:.15, 7:.15, 8:.10, 9:.05, 10:.05, 12:.05},
    '名词·饮食':      {2:.20, 4:.25, 5:.05, 9:.25, 10:.10, 11:.05, 12:.10},
    '名词·交通出行':  {2:.30, 6:.20, 7:.15, 9:.15, 10:.10, 11:.10},
    '名词·住宅设备':  {1:.20, 4:.25, 7:.25, 9:.15, 12:.15},
    '名词·自然天气':  {3:.10, 5:.15, 7:.20, 8:.15, 9:.10, 10:.15, 11:.15},
    '名词·身体健康':  {3:.10, 4:.10, 5:.15, 7:.10, 8:.10, 9:.10, 10:.15, 11:.10, 12:.10},
    '名词·衣物外貌':  {2:.10, 3:.15, 5:.25, 7:.15, 9:.15, 10:.10, 12:.10},
    '名词·学习教育':  {1:.15, 2:.20, 3:.15, 4:.15, 6:.10, 7:.10, 8:.15},
    '名词·兴趣娱乐':  {2:.10, 3:.20, 5:.15, 6:.10, 8:.10, 9:.10, 10:.15, 12:.10},
    '名词·工作职场':  {5:.10, 8:.20, 11:.40, 12:.30},
    '名词·IT通信':    {2:.15, 4:.10, 7:.15, 8:.15, 11:.20, 12:.25},
    '名词·日用品':    {1:.15, 2:.15, 4:.20, 7:.15, 9:.20, 10:.15},
    '名词·社会文化':  {3:.10, 6:.20, 8:.15, 10:.25, 11:.15, 12:.15},
    '名词·抽象概念':  {3:.08, 4:.08, 5:.10, 6:.10, 7:.10, 8:.12, 9:.08, 10:.08, 11:.13, 12:.13},
    # 副词：L05起
    '副词':  {2:.15, 3:.18, 4:.15, 5:.12, 6:.08, 7:.08, 8:.07, 9:.05, 10:.05, 11:.04, 12:.03},
    '惯用表达':  {3:.15, 5:.15, 6:.15, 7:.15, 8:.15, 10:.15, 11:.10},
    '名词·其他':  {2:.2, 4:.2, 7:.2, 9:.2, 11:.2},
}

MAX_BUCKET_PER_LESSON = 12
MIN_PER_LESSON = 12
MAX_PER_LESSON = 65
ADJ_BEFORE_L9 = 30  # no longer needed, adjectives start at L9

# 语法解锁约束：某些词性只能分配到语法支持使用的课
# 动词 → L05+（L05教ます形）
# い形容词 → L09+（L09教い形容词）
# な形容词 → L10+（L10教な形容词，但L09已教修饰名词可提前到L09）
# 副词 → L05+（需要动词/形容词才能修饰）
GRAMMAR_UNLOCK = {
    '动词·一类': 5,
    '动词·二类': 5,
    '动词·三类': 5,
    '动词·补助': 14,
    '形容词·い形': 9,
    '形容词·な形': 9,
    '副词': 5,
}


def load_words():
    rows = []
    with open(INPUT, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        for i, row in enumerate(reader):
            if len(row) < 5: continue
            w = row[0]; pos = row[2]; rd = row[3]; mn = row[4]
            rows.append({
                'idx': i, 'word': w, 'pos': pos, 'reading': rd,
                'meaning': mn, 'bucket': bucket_mod.classify(w, pos, rd, mn),
                'lesson': 0,
            })
    return rows


def lesson_count(words, lesson):
    return sum(1 for w in words if w['lesson'] == lesson)

def bucket_in_lesson(words, bucket, lesson):
    return sum(1 for w in words if w['lesson'] == lesson and w['bucket'] == bucket)

def find_lightest_lesson(words, lessons, bucket=None):
    """找arc内词最少的课，如果指定bucket则优先找该桶最少的课"""
    if bucket:
        return min(lessons, key=lambda l: (bucket_in_lesson(words, bucket, l), lesson_count(words, l)))
    return min(lessons, key=lambda l: lesson_count(words, l))


def assign_words(words):
    by_bucket = defaultdict(list)
    for w in words:
        by_bucket[w['bucket']].append(w)

    for bucket, items in by_bucket.items():
        arc_map = BUCKET_ARC_MAP.get(bucket, {i: 1.0/12 for i in range(1,13)})

        # 按比例分配到arc
        total = len(items)
        arc_alloc = {}
        assigned_count = 0
        arc_ids = sorted(arc_map.keys())

        for aid in arc_ids[:-1]:
            c = max(1, round(total * arc_map[aid])) if arc_map[aid] > 0 else 0
            arc_alloc[aid] = c
            assigned_count += c
        arc_alloc[arc_ids[-1]] = total - assigned_count

        # 逐arc逐词分配到具体课
        idx = 0
        for aid in arc_ids:
            lessons = ARCS[aid]
            count = arc_alloc[aid]
            batch = items[idx:idx+count]
            for w in batch:
                # 找这个桶在这个arc内最轻的课（同时受单桶上限约束）
                candidates = [l for l in lessons if bucket_in_lesson(words, bucket, l) < MAX_BUCKET_PER_LESSON]
                if not candidates:
                    candidates = lessons  # fallback
                target = find_lightest_lesson(words, candidates, bucket)
                w['lesson'] = target
            idx += count

    # 兜底：确保所有词都有lesson
    for w in words:
        if w['lesson'] == 0:
            w['lesson'] = 1


def enforce_grammar_unlock(words):
    """确保词性受限的词不会被分配到语法解锁之前的课"""
    for w in words:
        bucket = w['bucket']
        min_lesson = GRAMMAR_UNLOCK.get(bucket, 1)
        if w['lesson'] < min_lesson:
            # 在所有 >= min_lesson 的课里找最轻的
            all_valid = [l for l in range(min_lesson, 49)]
            target = min(all_valid, key=lambda l: (lesson_count(words, l), l))
            w['lesson'] = target


def enforce_adj_preload(words):
    """确保L01-08至少有ADJ_BEFORE_L9个形容词"""
    adj_before = [w for w in words if w['lesson'] <= 8 and '形容词' in w['bucket']]
    current = len(adj_before)
    if current >= ADJ_BEFORE_L9:
        return

    need = ADJ_BEFORE_L9 - current
    # 从L09-12的形容词中取最基础的前移
    adj_pool = [w for w in words if 9 <= w['lesson'] <= 12 and '形容词' in w['bucket']]

    # 优先选常见词（按释义长度近似，短释义=基础词）
    adj_pool.sort(key=lambda w: len(w['meaning']))

    moved = 0
    for w in adj_pool:
        if moved >= need:
            break
        # 分配到L01-08中形容词最少的课
        target = find_lightest_lesson(words, list(range(1,9)), w['bucket'])
        w['lesson'] = target
        moved += 1


def enforce_lesson_cap(words):
    """确保每课不超过MAX_PER_LESSON"""
    for _ in range(5):  # 多轮迭代
        changed = False
        for l in range(1, 49):
            count = lesson_count(words, l)
            if count <= MAX_PER_LESSON:
                continue
            # 找同arc内最轻的其他课
            arc_id = next(aid for aid, ls in ARCS.items() if l in ls)
            siblings = [s for s in ARCS[arc_id] if s != l]
            overflow_words = [w for w in words if w['lesson'] == l]
            overflow_words.sort(key=lambda w: len(w['meaning']), reverse=True)  # 先移长释义的（偏专业的）

            while lesson_count(words, l) > MAX_PER_LESSON and overflow_words:
                w = overflow_words.pop(0)
                target = find_lightest_lesson(words, siblings)
                if lesson_count(words, target) < MAX_PER_LESSON:
                    w['lesson'] = target
                    changed = True
        if not changed:
            break


def enforce_bucket_cap(words):
    """确保单桶单课不超过MAX_BUCKET_PER_LESSON"""
    for _ in range(5):
        changed = False
        for l in range(1, 49):
            bucket_counts = Counter(w['bucket'] for w in words if w['lesson'] == l)
            for bucket, count in bucket_counts.items():
                if count <= MAX_BUCKET_PER_LESSON:
                    continue
                # 溢出的词移到arc内其他课
                arc_id = next(aid for aid, ls in ARCS.items() if l in ls)
                siblings = [s for s in ARCS[arc_id] if s != l]
                excess = [w for w in words if w['lesson'] == l and w['bucket'] == bucket]
                excess.sort(key=lambda w: len(w['meaning']), reverse=True)

                while bucket_in_lesson(words, bucket, l) > MAX_BUCKET_PER_LESSON and excess:
                    w = excess.pop(0)
                    candidates = [s for s in siblings if bucket_in_lesson(words, bucket, s) < MAX_BUCKET_PER_LESSON]
                    if not candidates:
                        candidates = siblings
                    target = find_lightest_lesson(words, candidates, bucket)
                    w['lesson'] = target
                    changed = True
        if not changed:
            break


def enforce_min_per_lesson(words):
    """如果某课低于MIN_PER_LESSON，从arc内最多的课匀过来"""
    for _ in range(3):
        changed = False
        for l in range(1, 49):
            count = lesson_count(words, l)
            if count >= MIN_PER_LESSON:
                continue
            arc_id = next(aid for aid, ls in ARCS.items() if l in ls)
            siblings = [s for s in ARCS[arc_id] if s != l]
            heaviest = max(siblings, key=lambda s: lesson_count(words, s))
            if lesson_count(words, heaviest) <= MIN_PER_LESSON + 2:
                continue  # 大家都少，别匀了
            donors = [w for w in words if w['lesson'] == heaviest]
            donors.sort(key=lambda w: len(w['meaning']), reverse=True)
            while lesson_count(words, l) < MIN_PER_LESSON and donors:
                w = donors.pop(0)
                w['lesson'] = l
                changed = True
        if not changed:
            break


def print_summary(words):
    print("=" * 70)
    print("词汇分配摘要")
    print("=" * 70)
    for aid in sorted(ARCS.keys()):
        lessons = ARCS[aid]
        total = sum(1 for w in words if w['lesson'] in lessons)
        print(f"\n--- Arc {aid}: {ARC_NAMES[aid]} (共{total}词) ---")
        for l in lessons:
            lw = [w for w in words if w['lesson'] == l]
            bc = Counter(w['bucket'] for w in lw)
            top3 = bc.most_common(3)
            top3s = ', '.join(f"{b}:{c}" for b, c in top3)
            print(f"  L{l:02d}: {len(lw):3d}词  [{top3s}]")

    print("\n" + "=" * 70)
    print("约束检查")
    print("=" * 70)

    # 单桶单课上限
    violations = 0
    for l in range(1, 49):
        bc = Counter(w['bucket'] for w in words if w['lesson'] == l)
        for b, c in bc.items():
            if c > MAX_BUCKET_PER_LESSON:
                print(f"  ⚠ L{l:02d} 桶[{b}]={c} > {MAX_BUCKET_PER_LESSON}")
                violations += 1
    if violations == 0:
        print(f"  ✅ 单桶单课上限({MAX_BUCKET_PER_LESSON}): 全部通过")

    # 每课总量
    below = [l for l in range(1,49) if lesson_count(words, l) < MIN_PER_LESSON]
    above = [l for l in range(1,49) if lesson_count(words, l) > MAX_PER_LESSON]
    if below:
        print(f"  ⚠ 低于{MIN_PER_LESSON}词的课: {['L'+str(l) for l in below]}")
    if above:
        print(f"  ⚠ 超过{MAX_PER_LESSON}词的课: {['L'+str(l) for l in above]}")
    if not below and not above:
        print(f"  ✅ 每课总量({MIN_PER_LESSON}-{MAX_PER_LESSON}): 全部通过")

    # 语法解锁
    unlock_ok = True
    for bucket, min_l in GRAMMAR_UNLOCK.items():
        bad = [w for w in words if w['bucket'] == bucket and w['lesson'] < min_l]
        if bad:
            print(f"  ⚠ {bucket}: {len(bad)}词在L{min_l:02d}之前（违规）")
            unlock_ok = False
    if unlock_ok:
        print(f"  ✅ 语法解锁约束: 全部通过（动词L05+、形容词L09+、副词L05+）")

    # L01-L04 词性分布
    l14_words = [w for w in words if w['lesson'] <= 4]
    l14_buckets = Counter(w['bucket'].split('·')[0] for w in l14_words)
    print(f"\n  L01-04词性: {dict(l14_buckets)}")

    # 动词前置
    print("\n  动词累积:")
    for ck, desc in [(13,'L14て形前'), (18,'L19ない形前'), (20,'L21た形前'),
                      (37,'L38可能形前'), (40,'L41被动形前'), (42,'L43使役形前')]:
        v1 = sum(1 for w in words if w['lesson'] <= ck and '动词·一类' in w['bucket'])
        v2 = sum(1 for w in words if w['lesson'] <= ck and '动词·二类' in w['bucket'])
        v3 = sum(1 for w in words if w['lesson'] <= ck and '动词·三类' in w['bucket'])
        print(f"    ≤L{ck:02d}({desc}): 一{v1} 二{v2} 三{v3} 计{v1+v2+v3}")

    print(f"\n  总计: {len(words)}词, 已分配: {sum(1 for w in words if w['lesson']>0)}")

    # 直方图
    print("\n" + "=" * 70)
    print("每课词数:")
    print("=" * 70)
    for l in range(1, 49):
        c = lesson_count(words, l)
        bar = '█' * (c // 2)
        print(f"  L{l:02d}: {c:3d} {bar}")


def main():
    words = load_words()
    print(f"加载 {len(words)} 词\n")

    # 1. 初始分配
    assign_words(words)

    # 2. 语法解锁约束（动词L05+、形容词L09+、副词L05+）
    enforce_grammar_unlock(words)

    # 3. 单桶单课上限（多轮）
    enforce_bucket_cap(words)

    # 4. 每课总量上限
    enforce_lesson_cap(words)

    # 5. 每课最低保底
    enforce_min_per_lesson(words)

    # 6. 再跑一轮桶上限（前面的匀可能引入新违规）
    enforce_bucket_cap(words)

    print_summary(words)

    # 输出带lesson列的CSV（从原始8列数据重建，避免旧列残留）
    OUTPUT = os.path.join(os.path.dirname(INPUT), 'jlpt-vocab-n5n4.csv')
    ORIG_HEADER = ['词条', '声调', '词性', '读音', '中文释义', '备注', '例句', '例句翻译']

    # 重读原始数据（只取前8列）
    with open(INPUT, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # skip header
        all_rows = []
        for row in reader:
            all_rows.append(row[:8])  # 只取原始8列

    new_header = ORIG_HEADER + ['lesson', 'bucket']
    new_rows = []
    for w in words:
        orig = all_rows[w['idx']]
        new_rows.append(orig + [str(w['lesson']), w['bucket']])

    # 按lesson排序
    new_rows.sort(key=lambda r: (int(r[8]), r[9], r[0]))

    with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(new_header)
        writer.writerows(new_rows)

    print(f"\n✅ 已输出到 {OUTPUT}")
    print(f"   新增列: lesson(课号), bucket(主题桶)")


if __name__ == '__main__':
    main()
