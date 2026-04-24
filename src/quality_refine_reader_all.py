from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
READER_DIR = ROOT / "resources" / "新标日" / "md" / "reader" / "初级上册"

PAGE_RE = re.compile(r"^> Page\s+(\d+)\s*$", re.M)

CANONICAL_TITLES = {
    1: "# 第1課 <ruby>李<rt>り</rt></ruby>さんは <ruby>中国人<rt>ちゅうごくじん</rt></ruby>です",
    2: "# 第2課 これは <ruby>本<rt>ほん</rt></ruby>です",
    3: "# 第3課 ここはデパートです",
    4: "# 第4課 <ruby>部屋<rt>へや</rt></ruby>に <ruby>机<rt>つくえ</rt></ruby>と いすが あります",
    5: "# 第5課 <ruby>森<rt>もり</rt></ruby>さんは <ruby>7時<rt>しちじ</rt></ruby>に <ruby>起きます<rt>おきます</rt></ruby>",
    6: "# 第6課 <ruby>吉田<rt>よしだ</rt></ruby>さんは <ruby>来月<rt>らいげつ</rt></ruby> <ruby>中国<rt>ちゅうごく</rt></ruby>へ <ruby>行きます<rt>いきます</rt></ruby>",
    7: "# 第7課 <ruby>李<rt>り</rt></ruby>さんは <ruby>毎日<rt>まいにち</rt></ruby> コーヒーを <ruby>飲みます<rt>のみます</rt></ruby>",
    8: "# 第8課 <ruby>李<rt>り</rt></ruby>さんは <ruby>日本語<rt>にほんご</rt></ruby>で <ruby>手紙<rt>てがみ</rt></ruby>を <ruby>書きます<rt>かきます</rt></ruby>",
    9: "# 第9課 <ruby>四川料理<rt>しせんりょうり</rt></ruby>は <ruby>辛い<rt>からい</rt></ruby>です",
    10: "# 第10課 <ruby>京都<rt>きょうと</rt></ruby>の <ruby>紅葉<rt>もみじ</rt></ruby>は <ruby>有名<rt>ゆうめい</rt></ruby>です",
    11: "# 第11課 <ruby>小野<rt>おの</rt></ruby>さんは <ruby>歌<rt>うた</rt></ruby>が <ruby>好き<rt>すき</rt></ruby>です",
    12: "# 第12課 <ruby>李<rt>り</rt></ruby>さんは <ruby>森<rt>もり</rt></ruby>さんより <ruby>若い<rt>わかい</rt></ruby>です",
    13: "# 第13課 <ruby>机<rt>つくえ</rt></ruby>の <ruby>上<rt>うえ</rt></ruby>に <ruby>本<rt>ほん</rt></ruby>が <ruby>3冊<rt>さんさつ</rt></ruby> あります",
    14: "# 第14課 <ruby>昨日<rt>きのう</rt></ruby> デパートへ <ruby>行って<rt>いって</rt></ruby>、<ruby>買い物<rt>かいもの</rt></ruby>しました",
    15: "# 第15課 <ruby>小野<rt>おの</rt></ruby>さんは <ruby>今<rt>いま</rt></ruby> <ruby>新聞<rt>しんぶん</rt></ruby>を <ruby>読んで<rt>よんで</rt></ruby>います",
    16: "# 第16課 ホテルの <ruby>部屋<rt>へや</rt></ruby>は <ruby>広くて<rt>ひろくて</rt></ruby> <ruby>明るい<rt>あかるい</rt></ruby>です",
    17: "# 第17課 わたしは <ruby>新しい<rt>あたらしい</rt></ruby> <ruby>洋服<rt>ようふく</rt></ruby>が <ruby>欲しい<rt>ほしい</rt></ruby>です",
    18: "# 第18課 <ruby>携帯電話<rt>けいたいでんわ</rt></ruby>は とても <ruby>小さく<rt>ちいさく</rt></ruby> なりました",
    19: "# 第19課 <ruby>部屋<rt>へや</rt></ruby>の かぎを <ruby>忘れないで<rt>わすれないで</rt></ruby> ください",
    20: "# 第20課 スミスさんは ピアノを <ruby>弾く<rt>ひく</rt></ruby> ことが できます",
    21: "# 第21課 わたしは <ruby>すき焼き<rt>すきやき</rt></ruby>を <ruby>食べた<rt>たべた</rt></ruby> ことが あります",
    22: "# 第22課 <ruby>森<rt>もり</rt></ruby>さんは <ruby>毎晩<rt>まいばん</rt></ruby> テレビを <ruby>見る<rt>みる</rt></ruby>",
    23: "# 第23課 <ruby>休み<rt>やすみ</rt></ruby>の <ruby>日<rt>ひ</rt></ruby>、<ruby>散歩したり<rt>さんぽしたり</rt></ruby> <ruby>買い物<rt>かいもの</rt></ruby>に <ruby>行ったり<rt>いったり</rt></ruby> します",
    24: "# 第24課 <ruby>李<rt>り</rt></ruby>さんは もうすぐ <ruby>来る<rt>くる</rt></ruby>と <ruby>思います<rt>おもいます</rt></ruby>",
}

RUBY_REPLACEMENTS = {
    "<ruby>1時30分ごろ<rt>1とき30ふんごろ</rt></ruby>": "<ruby>1時30分ごろ<rt>いちじさんじゅっぷんごろ</rt></ruby>",
    "<ruby>12時半ごろ<rt>12じはんごろ</rt></ruby>": "<ruby>12時半ごろ<rt>じゅうにじはんごろ</rt></ruby>",
    "<ruby>11時半ごろ<rt>11じはんごろ</rt></ruby>": "<ruby>11時半ごろ<rt>じゅういちじはんごろ</rt></ruby>",
    "<ruby>12月25日<rt>12がつ25にち</rt></ruby>": "<ruby>12月25日<rt>じゅうにがつにじゅうごにち</rt></ruby>",
    "<ruby>9月1日<rt>9がつ1にち</rt></ruby>": "<ruby>9月1日<rt>くがつついたち</rt></ruby>",
    "<ruby>5月5日<rt>5がつ5にち</rt></ruby>": "<ruby>5月5日<rt>ごがついつか</rt></ruby>",
    "<ruby>11月3日<rt>11がつ3にち</rt></ruby>": "<ruby>11月3日<rt>じゅういちがつみっか</rt></ruby>",
    "<ruby>150円<rt>150えん</rt></ruby>": "<ruby>150円<rt>ひゃくごじゅうえん</rt></ruby>",
    "<ruby>25番<rt>25ばん</rt></ruby>": "<ruby>25番<rt>にじゅうごばん</rt></ruby>",
    "<ruby>9番<rt>9ばん</rt></ruby>": "<ruby>9番<rt>きゅうばん</rt></ruby>",
    "<ruby>1番<rt>1ばん</rt></ruby>": "<ruby>1番<rt>いちばん</rt></ruby>",
    "<ruby>2番<rt>2ばん</rt></ruby>": "<ruby>2番<rt>にばん</rt></ruby>",
    "<ruby>14番<rt>14ばん</rt></ruby>": "<ruby>14番<rt>じゅうよんばん</rt></ruby>",
    "<ruby>京都<rt>きょうと</rt></ruby>の <ruby>紅葉<rt>こうよう</rt></ruby>": "<ruby>京都<rt>きょうと</rt></ruby>の <ruby>紅葉<rt>もみじ</rt></ruby>",
    "<ruby>紅葉<rt>こうよう / もみじ</rt></ruby>": "<ruby>紅葉<rt>もみじ</rt></ruby>",
    "すき<ruby>焼き<rt>やき</rt></ruby>": "<ruby>すき焼き<rt>すきやき</rt></ruby>",
    "<ruby>額<rt>ひたい / おでこ</rt></ruby>": "<ruby>額<rt>ひたい</rt></ruby>（おでこ）",
    "<ruby>腹<rt>はら / おなか</rt></ruby>": "<ruby>腹<rt>はら</rt></ruby>（おなか）",
    "まゆ<ruby>毛<rt>げ</rt></ruby>": "<ruby>まゆ毛<rt>まゆげ</rt></ruby>",
    "めまつ<ruby>毛<rt>げ</rt></ruby>": "<ruby>まつ毛<rt>まつげ</rt></ruby>",
    "まつ<ruby>毛<rt>げ</rt></ruby>": "<ruby>まつ毛<rt>まつげ</rt></ruby>",
    "つま<ruby>先<rt>さき</rt></ruby>": "<ruby>つま先<rt>つまさき</rt></ruby>",
    "ひな<ruby>祭り<rt>まつり</rt></ruby>": "<ruby>ひな祭り<rt>ひなまつり</rt></ruby>",
    "やり<ruby>方<rt>かた</rt></ruby>": "<ruby>やり方<rt>やりかた</rt></ruby>",
}

PRACTICE_NOTE = (
    "> 练习保真说明：本节按网页学习版重排。可文字化的题面尽量展开；"
    "依赖录音、图表或原页版式的题目，保留题型、例题、小题范围和训练重点。"
)


def normalize_title(lesson_no: int, text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return text
    lines[0] = CANONICAL_TITLES[lesson_no]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def normalize_top_block_spacing(text: str) -> str:
    text = re.sub(r"(?m)^(> Pages: .+)\n(> 图像策略：)", r"\1\n\n\2", text)
    text = re.sub(r"(?m)^(> 图像策略：.+)\n(> 当前完成度：)", r"\1\n\n\2", text)
    text = re.sub(r"(?m)^(> 当前完成度：.+)\n(> Page )", r"\1\n\n\2", text)
    return text


def refine_ruby(text: str) -> str:
    for old, new in RUBY_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def refine_page_anchor_notes(text: str) -> str:
    current_page: str | None = None
    output: list[str] = []

    for line in text.splitlines():
        page_match = PAGE_RE.match(line)
        if page_match:
            current_page = page_match.group(1)
            output.append(line)
            continue

        if "本页内容已并入相邻页面重排" in line:
            page = current_page or "本"
            output.append(
                f"> 页码锚点说明：原书第 {page} 页的学习内容已经并入本课相邻模块重排；这里保留页码锚点，方便和纸书或 PDF 对照。"
            )
            continue

        output.append(line)

    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def ensure_practice_note(text: str) -> str:
    if PRACTICE_NOTE in text or "练习保真说明：" in text:
        return text
    marker = "## 练习"
    if marker not in text:
        return text
    return text.replace(marker, f"{marker}\n\n{PRACTICE_NOTE}", 1)


def refine_lesson(lesson_no: int) -> None:
    path = READER_DIR / f"lesson-{lesson_no:02d}.md"
    text = path.read_text(encoding="utf-8")
    text = normalize_title(lesson_no, text)
    text = normalize_top_block_spacing(text)
    text = refine_ruby(text)
    text = refine_page_anchor_notes(text)
    text = ensure_practice_note(text)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    for lesson_no in range(1, 25):
        refine_lesson(lesson_no)
        print(f"quality refined lesson-{lesson_no:02d}.md")


if __name__ == "__main__":
    main()
