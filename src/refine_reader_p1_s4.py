from __future__ import annotations

from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
READER_DIR = ROOT / "resources" / "新标日" / "md" / "reader" / "初级上册"


def block(text: str) -> str:
    return dedent(text).strip() + "\n\n"


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[:start_index] + replacement + text[end_index:]


def replace_lesson_range(lesson_no: int, start: str, end: str, replacement: str) -> None:
    path = READER_DIR / f"lesson-{lesson_no:02d}.md"
    text = path.read_text(encoding="utf-8")
    text = replace_between(text, start, end, replacement)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"refined lesson-{lesson_no:02d}.md")


LESSON_09_136_139 = block(
    """
    > Page 136

    ### 应用课文续：温泉

    #### 场景 1：试穿浴衣

    <ruby>小野<rt>おの</rt></ruby>：<ruby>李<rt>り</rt></ruby>さん、この <ruby>浴衣<rt>ゆかた</rt></ruby>は ちょっと <ruby>小さい<rt>ちいさい</rt></ruby>です。  
    <ruby>小野<rt>おの</rt></ruby>：それは <ruby>子供用<rt>こどもよう</rt></ruby>ですよ。これを どうぞ。  
    <ruby>李<rt>り</rt></ruby>：これは ちょうど いいです。  

    #### 场景 2：进入温泉

    <ruby>小野<rt>おの</rt></ruby>：<ruby>李<rt>り</rt></ruby>さん、<ruby>熱くない<rt>あつくない</rt></ruby>ですか。  
    <ruby>李<rt>り</rt></ruby>：いいえ、ちょうど いいです。とても <ruby>気持ちがいい<rt>きもちがいい</rt></ruby>ですね。  
    <ruby>李<rt>り</rt></ruby>：<ruby>小野<rt>おの</rt></ruby>さん、すばらしい <ruby>眺め<rt>ながめ</rt></ruby>ですね。  
    <ruby>小野<rt>おの</rt></ruby>：ええ、<ruby>本当に<rt>ほんとうに</rt></ruby>。  

    #### 场景 3：喝温泉水

    <ruby>李<rt>り</rt></ruby>：<ruby>小野<rt>おの</rt></ruby>さん、それは <ruby>何<rt>なん</rt></ruby>ですか。  
    <ruby>小野<rt>おの</rt></ruby>：ああ、これは <ruby>温泉<rt>おんせん</rt></ruby>の お<ruby>湯<rt>ゆ</rt></ruby>です。<ruby>李<rt>り</rt></ruby>さんも <ruby>飲みます<rt>のみます</rt></ruby>か。  
    <ruby>李<rt>り</rt></ruby>：ええ。……あまり おいしくないですね。  

    > 词语提示：`気持ちがいい` 表示“舒服”；`眺め` 是“景色”；`本当に` 是“真的 / 的确”。

    > Page 137

    ## 练习

    > 练习保真说明：本节按网页学习版重排。可文字化的题面尽量展开；依赖录音、图表或原页版式的题目，保留题型、例题、小题范围和训练重点。

    ### 练习 I

    #### 2. 把 `い` 形容词改成否定式 / 过去否定式

    | 组 | 例句 / 题干 | 作答目标 |
    | --- | --- | --- |
    | 例1 | この かばんは <ruby>大きい<rt>おおきい</rt></ruby>です。 | この かばんは <ruby>大きくない<rt>おおきくない</rt></ruby>です。 |
    | 1 | この お<ruby>茶<rt>ちゃ</rt></ruby>は <ruby>熱い<rt>あつい</rt></ruby>です。 | `熱くないです` |
    | 2 | パーティーは <ruby>楽しい<rt>たのしい</rt></ruby>です。 | `楽しくないです` |
    | 3 | この <ruby>料理<rt>りょうり</rt></ruby>は <ruby>辛い<rt>からい</rt></ruby>です。 | `辛くないです` |
    | 4 | <ruby>日本<rt>にほん</rt></ruby>の <ruby>食べ物<rt>たべもの</rt></ruby>は おいしいです。 | `おいしくないです` |
    | 5 | <ruby>明日<rt>あした</rt></ruby>は <ruby>忙しい<rt>いそがしい</rt></ruby>です。 | `忙しくないです` |
    | 6 | この <ruby>辞書<rt>じしょ</rt></ruby>は いいです。 | `よくないです` |
    | 例2 | <ruby>公園<rt>こうえん</rt></ruby>は <ruby>広かった<rt>ひろかった</rt></ruby>です。 | <ruby>広くなかった<rt>ひろくなかった</rt></ruby>です。 |
    | 7 | <ruby>駅<rt>えき</rt></ruby>は <ruby>遠かった<rt>とおかった</rt></ruby>です。 | `遠くなかったです` |
    | 8 | その <ruby>学校<rt>がっこう</rt></ruby>は <ruby>近かった<rt>ちかかった</rt></ruby>です。 | `近くなかったです` |
    | 9 | <ruby>天気<rt>てんき</rt></ruby>は <ruby>悪かった<rt>わるかった</rt></ruby>です。 | `悪くなかったです` |
    | 10 | <ruby>先週<rt>せんしゅう</rt></ruby>は <ruby>忙しかった<rt>いそがしかった</rt></ruby>です。 | `忙しくなかったです` |
    | 11 | <ruby>図書室<rt>としょしつ</rt></ruby>は <ruby>狭かった<rt>せまかった</rt></ruby>です。 | `狭くなかったです` |
    | 12 | <ruby>昨日<rt>きのう</rt></ruby>の <ruby>試験<rt>しけん</rt></ruby>は よかったです。 | `よくなかったです` |

    #### 3. 仿照例句回答提问

    - 例：その <ruby>靴<rt>くつ</rt></ruby>は <ruby>新しい<rt>あたらしい</rt></ruby>ですか。（はい）  
      → はい、<ruby>新しい<rt>あたらしい</rt></ruby>です。
    - 例：<ruby>昨日<rt>きのう</rt></ruby>は <ruby>暑かった<rt>あつかった</rt></ruby>ですか。（いいえ）  
      → いいえ、<ruby>暑くなかった<rt>あつくなかった</rt></ruby>です。

    练习题：

    1. この <ruby>本<rt>ほん</rt></ruby>は おもしろいですか。（はい）
    2. <ruby>昨日<rt>きのう</rt></ruby>は <ruby>寒かった<rt>さむかった</rt></ruby>ですか。（いいえ）
    3. <ruby>部屋<rt>へや</rt></ruby>は <ruby>狭い<rt>せまい</rt></ruby>ですか。（いいえ）
    4. この リンゴは <ruby>甘い<rt>あまい</rt></ruby>ですか。（いいえ）
    5. <ruby>旅行<rt>りょこう</rt></ruby>は <ruby>楽しかった<rt>たのしかった</rt></ruby>ですか。（はい）
    6. その <ruby>水<rt>みず</rt></ruby>は おいしいですか。（はい）

    > Page 138

    #### 4. 看图替换练习：`形容词 + 名词`

    > 原页是看图替换练习。网页学习版保留题型和可见输入；图片细节无法完全复原时，按“形容词 + 名词”的训练目标整理。

    - 例：<ruby>新しい<rt>あたらしい</rt></ruby> / <ruby>靴<rt>くつ</rt></ruby>  
      → これは <ruby>新しい<rt>あたらしい</rt></ruby> <ruby>靴<rt>くつ</rt></ruby>です。

    #### 5. 把括号里的形容词放到名词前

    1. <ruby>昨日<rt>きのう</rt></ruby> かばんを <ruby>買いました<rt>かいました</rt></ruby>。（<ruby>安い<rt>やすい</rt></ruby>）
    2. <ruby>昨日<rt>きのう</rt></ruby> ニュースを <ruby>聞きました<rt>ききました</rt></ruby>。（いい）
    3. <ruby>先週<rt>せんしゅう</rt></ruby> ケーキを <ruby>買いました<rt>かいました</rt></ruby>。（おいしい）
    4. <ruby>李<rt>り</rt></ruby>さんに <ruby>花<rt>はな</rt></ruby>を あげました。（かわいい）

    #### 6. 听录音回答：程度副词

    - 例：それは <ruby>高い<rt>たかい</rt></ruby> <ruby>時計<rt>とけい</rt></ruby>ですか。（はい / とても）  
      → はい、とても <ruby>高い<rt>たかい</rt></ruby> <ruby>時計<rt>とけい</rt></ruby>です。
    - 例：<ruby>昨日<rt>きのう</rt></ruby>は <ruby>暑かった<rt>あつかった</rt></ruby>ですか。（いいえ / あまり）  
      → いいえ、あまり <ruby>暑くなかった<rt>あつくなかった</rt></ruby>です。

    小题输入：

    1. はい / とても
    2. いいえ / あまり
    3. はい / とても
    4. いいえ / あまり

    #### 7. 替换会话

    - 例：<ruby>北京<rt>ペキン</rt></ruby>ダック / <ruby>食べます<rt>たべます</rt></ruby> / おいしい  
      甲：<ruby>北京<rt>ペキン</rt></ruby>ダックは <ruby>食べました<rt>たべました</rt></ruby>か。  
      乙：はい、<ruby>食べました<rt>たべました</rt></ruby>。とても おいしかったです。

    练习：

    1. <ruby>すき焼き<rt>すきやき</rt></ruby> / <ruby>食べます<rt>たべます</rt></ruby> / おいしい
    2. <ruby>歌舞伎<rt>かぶき</rt></ruby> / <ruby>見ます<rt>みます</rt></ruby> / おもしろい

    > Page 139

    ### 练习 II

    #### 1. 写反义词

    - 例：<ruby>大きい<rt>おおきい</rt></ruby> → <ruby>小さい<rt>ちいさい</rt></ruby>

    | 题号 | 词 | 目标 |
    | --- | --- | --- |
    | 1 | <ruby>熱い<rt>あつい</rt></ruby> | <ruby>冷たい<rt>つめたい</rt></ruby> |
    | 2 | <ruby>新しい<rt>あたらしい</rt></ruby> | <ruby>古い<rt>ふるい</rt></ruby> |
    | 3 | <ruby>高い<rt>たかい</rt></ruby> | <ruby>低い<rt>ひくい</rt></ruby> / <ruby>安い<rt>やすい</rt></ruby> |
    | 4 | <ruby>悪い<rt>わるい</rt></ruby> | いい |
    | 5 | <ruby>難しい<rt>むずかしい</rt></ruby> | <ruby>易しい<rt>やさしい</rt></ruby> |
    | 6 | <ruby>暑い<rt>あつい</rt></ruby> | <ruby>寒い<rt>さむい</rt></ruby> |
    | 7 | <ruby>広い<rt>ひろい</rt></ruby> | <ruby>狭い<rt>せまい</rt></ruby> |
    | 8 | <ruby>近い<rt>ちかい</rt></ruby> | <ruby>遠い<rt>とおい</rt></ruby> |

    #### 2. 填入适当的词语

    - 例：あなたの <ruby>車<rt>くるま</rt></ruby>は <ruby>新しい<rt>あたらしい</rt></ruby>ですか。  
      → いいえ、<ruby>新しくない<rt>あたらしくない</rt></ruby>です。<ruby>古い<rt>ふるい</rt></ruby>です。

    1. <ruby>日本語<rt>にほんご</rt></ruby>は <ruby>難しい<rt>むずかしい</rt></ruby>ですか。→ いいえ、（　　　）です。（　　　）です。
    2. <ruby>会社<rt>かいしゃ</rt></ruby>は <ruby>駅<rt>えき</rt></ruby>から（　　　）ですか。→ いいえ、<ruby>近くない<rt>ちかくない</rt></ruby>です。（　　　）です。
    3. <ruby>駅<rt>えき</rt></ruby>の <ruby>前<rt>まえ</rt></ruby>の <ruby>公園<rt>こうえん</rt></ruby>は（　　　）ですか。→ いいえ、（　　　）です。<ruby>狭い<rt>せまい</rt></ruby>です。
    4. あなたの うちは（　　　）ですか。→ いいえ、<ruby>大きくない<rt>おおきくない</rt></ruby>です。（　　　）です。
    5. その <ruby>時計<rt>とけい</rt></ruby>は <ruby>高かった<rt>たかかった</rt></ruby>ですか。→ いいえ、（　　　）です。（　　　）です。

    #### 3. 看图听录音回答

    - 例：<ruby>試験<rt>しけん</rt></ruby>は <ruby>易しかった<rt>やさしかった</rt></ruby>ですか。（いいえ）  
      → いいえ、<ruby>易しくなかった<rt>やさしくなかった</rt></ruby>です。

    小题输入：`1. はい` / `2. いいえ` / `3. はい` / `4. いいえ`

    #### 4. 判断正误

    - 例：この <ruby>本<rt>ほん</rt></ruby>は とても おもしろいです。（○）
    1. これは わたしの <ruby>新しい<rt>あたらしい</rt></ruby>の <ruby>辞書<rt>じしょ</rt></ruby>です。
    2. この <ruby>料理<rt>りょうり</rt></ruby>は あまり <ruby>辛い<rt>からい</rt></ruby>です。
    3. <ruby>冷たい<rt>つめたい</rt></ruby> <ruby>水<rt>みず</rt></ruby>は おいしいです。
    4. <ruby>昨日<rt>きのう</rt></ruby>は よく <ruby>天気<rt>てんき</rt></ruby>です。

    #### 5. 翻译题

    1. 四川菜很辣。
    2. 天安门是非常雄伟的建筑。
    3. 这个汤不太热。
    """
)


LESSON_10_146_149 = block(
    """
    > Page 146

    ### 应用课文续：京都の美術館

    #### 场景 1：京都的红叶

    <ruby>長島<rt>ながしま</rt></ruby>：<ruby>昨日<rt>きのう</rt></ruby> <ruby>京都<rt>きょうと</rt></ruby>へ <ruby>行きました<rt>いきました</rt></ruby>。  
    <ruby>小野<rt>おの</rt></ruby>：<ruby>京都<rt>きょうと</rt></ruby>ですか。<ruby>京都<rt>きょうと</rt></ruby>の <ruby>紅葉<rt>もみじ</rt></ruby>は どうでしたか。  
    <ruby>長島<rt>ながしま</rt></ruby>：とても きれいでした。でも、<ruby>町<rt>まち</rt></ruby>は あまり <ruby>静か<rt>しずか</rt></ruby>じゃ ありませんでした。  
    <ruby>李<rt>り</rt></ruby>：えっ。  
    <ruby>長島<rt>ながしま</rt></ruby>：<ruby>今<rt>いま</rt></ruby> ちょうど <ruby>修学旅行<rt>しゅうがくりょこう</rt></ruby>の シーズンです。とても にぎやかでした。  

    #### 场景 2：平日和休息日

    <ruby>李<rt>り</rt></ruby>：この <ruby>通り<rt>とおり</rt></ruby>は <ruby>静か<rt>しずか</rt></ruby>ですね。  
    <ruby>長島<rt>ながしま</rt></ruby>：ああ、<ruby>今日<rt>きょう</rt></ruby>は <ruby>平日<rt>へいじつ</rt></ruby>ですね。でも、<ruby>休み<rt>やすみ</rt></ruby>の <ruby>日<rt>ひ</rt></ruby>は <ruby>観光客<rt>かんこうきゃく</rt></ruby>が <ruby>多い<rt>おおい</rt></ruby>です。とても にぎやかですよ。  
    <ruby>李<rt>り</rt></ruby>：そうですか。  

    #### 场景 3：美术馆还没有游客

    <ruby>李<rt>り</rt></ruby>：あれえ、だれも いませんね。  
    <ruby>小野<rt>おの</rt></ruby>：そうですね。  
    <ruby>李<rt>り</rt></ruby>：ところで、この <ruby>美術館<rt>びじゅつかん</rt></ruby>には どんな <ruby>作品<rt>さくひん</rt></ruby>が ありますか。  
    <ruby>小野<rt>おの</rt></ruby>：<ruby>世界中<rt>せかいじゅう</rt></ruby>の <ruby>有名<rt>ゆうめい</rt></ruby>な <ruby>作家<rt>さっか</rt></ruby>の <ruby>彫刻<rt>ちょうこく</rt></ruby>です。  
    <ruby>長島<rt>ながしま</rt></ruby>：<ruby>美術館<rt>びじゅつかん</rt></ruby>の <ruby>庭<rt>にわ</rt></ruby>にも いろいろ おもしろいのが ありますよ。  

    > Page 147

    ## 练习

    > 练习保真说明：本节按网页学习版重排。可文字化的题面尽量展开；依赖录音、图表或原页版式的题目，保留题型、例题、小题范围和训练重点。

    ### 练习 I

    #### 2. 二类形容词做谓语和修饰名词

    - 例：<ruby>森<rt>もり</rt></ruby>さん / <ruby>元気<rt>げんき</rt></ruby> / <ruby>人<rt>ひと</rt></ruby>  
      → <ruby>森<rt>もり</rt></ruby>さんは <ruby>元気<rt>げんき</rt></ruby>です。  
      → <ruby>森<rt>もり</rt></ruby>さんは <ruby>元気<rt>げんき</rt></ruby>な <ruby>人<rt>ひと</rt></ruby>です。

    练习：

    1. <ruby>李<rt>り</rt></ruby>さん / きれい / <ruby>人<rt>ひと</rt></ruby>
    2. <ruby>部長<rt>ぶちょう</rt></ruby> / <ruby>親切<rt>しんせつ</rt></ruby> / <ruby>方<rt>かた</rt></ruby>
    3. ここ / にぎやか / <ruby>通り<rt>とおり</rt></ruby>
    4. これ / <ruby>簡単<rt>かんたん</rt></ruby> / <ruby>試験<rt>しけん</rt></ruby>
    5. ここ / <ruby>有名<rt>ゆうめい</rt></ruby> / <ruby>所<rt>ところ</rt></ruby>
    6. これ / <ruby>便利<rt>べんり</rt></ruby> / <ruby>道具<rt>どうぐ</rt></ruby>

    #### 3. 用 `な` 形容词修饰名词

    - 例：<ruby>人形<rt>にんぎょう</rt></ruby>を <ruby>買いました<rt>かいました</rt></ruby>。（きれい）  
      → きれいな <ruby>人形<rt>にんぎょう</rt></ruby>を <ruby>買いました<rt>かいました</rt></ruby>。

    1. カメラを <ruby>買います<rt>かいます</rt></ruby>。（<ruby>簡単<rt>かんたん</rt></ruby>）
    2. <ruby>道具<rt>どうぐ</rt></ruby>を もらいました。（<ruby>便利<rt>べんり</rt></ruby>）
    3. レストランへ <ruby>行きました<rt>いきました</rt></ruby>。（<ruby>有名<rt>ゆうめい</rt></ruby>）
    4. <ruby>音楽<rt>おんがく</rt></ruby>を <ruby>聞きます<rt>ききます</rt></ruby>。（<ruby>静か<rt>しずか</rt></ruby>）

    #### 4. 回答提问

    - 例：<ruby>今日<rt>きょう</rt></ruby>は <ruby>暇<rt>ひま</rt></ruby>ですか。（はい / いいえ）  
      → はい、<ruby>暇<rt>ひま</rt></ruby>です。  
      → いいえ、<ruby>暇<rt>ひま</rt></ruby>では ありません。

    1. <ruby>東京<rt>とうきょう</rt></ruby>は にぎやかですか。（はい）
    2. <ruby>魚<rt>さかな</rt></ruby>は <ruby>嫌い<rt>きらい</rt></ruby>ですか。（いいえ）
    3. <ruby>地下鉄<rt>ちかてつ</rt></ruby>は <ruby>便利<rt>べんり</rt></ruby>ですか。（はい）
    4. この <ruby>町<rt>まち</rt></ruby>は <ruby>有名<rt>ゆうめい</rt></ruby>ですか。（いいえ）

    > Page 148

    #### 5. 替换会话：`どんな + 名词`

    - 例：あの <ruby>人<rt>ひと</rt></ruby> / <ruby>人<rt>ひと</rt></ruby> / <ruby>親切<rt>しんせつ</rt></ruby>  
      甲：あの <ruby>人<rt>ひと</rt></ruby>は どんな <ruby>人<rt>ひと</rt></ruby>ですか。  
      乙：とても <ruby>親切<rt>しんせつ</rt></ruby>な <ruby>人<rt>ひと</rt></ruby>です。

    练习：

    1. <ruby>日本<rt>にほん</rt></ruby> / <ruby>国<rt>くに</rt></ruby> / きれい
    2. <ruby>京都<rt>きょうと</rt></ruby> / <ruby>町<rt>まち</rt></ruby> / <ruby>古い<rt>ふるい</rt></ruby>
    3. これ / お<ruby>菓子<rt>かし</rt></ruby> / <ruby>甘い<rt>あまい</rt></ruby>
    4. それ / <ruby>料理<rt>りょうり</rt></ruby> / <ruby>簡単<rt>かんたん</rt></ruby>
    5. <ruby>富士山<rt>ふじさん</rt></ruby> / <ruby>山<rt>やま</rt></ruby> / <ruby>高い<rt>たかい</rt></ruby>
    6. <ruby>銀座<rt>ぎんざ</rt></ruby> / <ruby>所<rt>ところ</rt></ruby> / にぎやか

    #### 6. 听录音替换：请求更合适的东西

    - 例：<ruby>高い<rt>たかい</rt></ruby> / <ruby>安い<rt>やすい</rt></ruby>  
      甲：これは ちょっと <ruby>高い<rt>たかい</rt></ruby>です。もう <ruby>少し<rt>すこし</rt></ruby> <ruby>安い<rt>やすい</rt></ruby>のは ありませんか。

    1. <ruby>小さい<rt>ちいさい</rt></ruby> / <ruby>大きい<rt>おおきい</rt></ruby>
    2. <ruby>汚い<rt>きたない</rt></ruby> / きれい
    3. <ruby>難しい<rt>むずかしい</rt></ruby> / <ruby>簡単<rt>かんたん</rt></ruby>

    #### 7. 名词过去式和否定

    - 例：<ruby>日曜日<rt>にちようび</rt></ruby> / <ruby>雪<rt>ゆき</rt></ruby>  
      → <ruby>昨日<rt>きのう</rt></ruby>は <ruby>日曜日<rt>にちようび</rt></ruby>でした。  
      → <ruby>昨日<rt>きのう</rt></ruby>は <ruby>雪<rt>ゆき</rt></ruby>では ありませんでした。

    1. <ruby>月曜日<rt>げつようび</rt></ruby> / <ruby>晴れ<rt>はれ</rt></ruby>
    2. <ruby>金曜日<rt>きんようび</rt></ruby> / <ruby>誕生日<rt>たんじょうび</rt></ruby>
    3. <ruby>水曜日<rt>すいようび</rt></ruby> / <ruby>曇り<rt>くもり</rt></ruby>
    4. <ruby>土曜日<rt>どようび</rt></ruby> / <ruby>休み<rt>やすみ</rt></ruby>

    #### 8. 综合会话

    - 例1：<ruby>田中<rt>たなか</rt></ruby>さん / <ruby>人<rt>ひと</rt></ruby> / <ruby>親切<rt>しんせつ</rt></ruby> / ハンサム  
      甲：<ruby>田中<rt>たなか</rt></ruby>さんは どんな <ruby>人<rt>ひと</rt></ruby>ですか。  
      乙：とても <ruby>親切<rt>しんせつ</rt></ruby>な <ruby>人<rt>ひと</rt></ruby>です。そして、ハンサムです。
    - 例2：<ruby>仕事<rt>しごと</rt></ruby> / おもしろい / <ruby>暇<rt>ひま</rt></ruby>  
      甲：<ruby>仕事<rt>しごと</rt></ruby>は どうですか。  
      乙：とても おもしろいです。でも、<ruby>暇<rt>ひま</rt></ruby>では ありません。
    - 例3：<ruby>仕事<rt>しごと</rt></ruby> / <ruby>簡単<rt>かんたん</rt></ruby> / <ruby>忙しい<rt>いそがしい</rt></ruby>  
      甲：<ruby>仕事<rt>しごと</rt></ruby>は どうでしたか。  
      乙：<ruby>簡単<rt>かんたん</rt></ruby>でした。でも、ちょっと <ruby>忙しかった<rt>いそがしかった</rt></ruby>です。

    练习输入：

    1. <ruby>中国<rt>ちゅうごく</rt></ruby> / <ruby>国<rt>くに</rt></ruby> / <ruby>広い<rt>ひろい</rt></ruby> / きれい
    2. <ruby>張<rt>ちょう</rt></ruby>さん / <ruby>人<rt>ひと</rt></ruby> / おもしろい / <ruby>元気<rt>げんき</rt></ruby>
    3. それ / <ruby>料理<rt>りょうり</rt></ruby> / <ruby>簡単<rt>かんたん</rt></ruby> / おいしい
    4. <ruby>富士山<rt>ふじさん</rt></ruby> / <ruby>山<rt>やま</rt></ruby> / きれい / <ruby>有名<rt>ゆうめい</rt></ruby>
    5. <ruby>新しい<rt>あたらしい</rt></ruby> <ruby>課長<rt>かちょう</rt></ruby> / <ruby>親切<rt>しんせつ</rt></ruby> / ハンサム
    6. あなたの <ruby>故郷<rt>こきょう</rt></ruby> / きれい / <ruby>有名<rt>ゆうめい</rt></ruby>
    7. その パソコン / <ruby>便利<rt>べんり</rt></ruby> / <ruby>簡単<rt>かんたん</rt></ruby>
    8. <ruby>新しい<rt>あたらしい</rt></ruby> <ruby>家<rt>いえ</rt></ruby> / <ruby>便利<rt>べんり</rt></ruby> / <ruby>静か<rt>しずか</rt></ruby>
    9. ホテル / <ruby>静か<rt>しずか</rt></ruby> / <ruby>駅<rt>えき</rt></ruby>から <ruby>遠い<rt>とおい</rt></ruby>
    10. <ruby>昨日<rt>きのう</rt></ruby>の <ruby>天気<rt>てんき</rt></ruby> / いい / <ruby>寒い<rt>さむい</rt></ruby>
    11. あの お<ruby>店<rt>みせ</rt></ruby>の <ruby>料理<rt>りょうり</rt></ruby> / おいしい / <ruby>高い<rt>たかい</rt></ruby>
    12. <ruby>日本<rt>にほん</rt></ruby>の <ruby>生活<rt>せいかつ</rt></ruby> / <ruby>便利<rt>べんり</rt></ruby> / <ruby>忙しい<rt>いそがしい</rt></ruby>

    > Page 149

    ### 练习 II

    #### 1. 填助词

    - 例：<ruby>昨日<rt>きのう</rt></ruby> <ruby>李<rt>り</rt></ruby>さん（に）<ruby>会いました<rt>あいました</rt></ruby>。

    1. <ruby>富士山<rt>ふじさん</rt></ruby>は きれい（　）<ruby>山<rt>やま</rt></ruby>です。
    2. <ruby>公園<rt>こうえん</rt></ruby>は あまり <ruby>静か<rt>しずか</rt></ruby>で（　）ありませんでした。
    3. <ruby>万里の長城<rt>ばんりのちょうじょう</rt></ruby>は <ruby>北京<rt>ペキン</rt></ruby>（　）（　）<ruby>遠い<rt>とおい</rt></ruby>ですか。
    4. <ruby>北京<rt>ペキン</rt></ruby>の <ruby>天気<rt>てんき</rt></ruby>（　）どうでしたか。
    5. この ノート（　）<ruby>鉛筆<rt>えんぴつ</rt></ruby>を ください。
    6. <ruby>李<rt>り</rt></ruby>さん、だれ（　）その <ruby>花<rt>はな</rt></ruby>（　）もらいましたか。

    #### 2. 选择正确回答

    1. どんな <ruby>傘<rt>かさ</rt></ruby>を <ruby>買いました<rt>かいました</rt></ruby>か。
       - はい、<ruby>傘<rt>かさ</rt></ruby>を <ruby>買いました<rt>かいました</rt></ruby>。
       - きれいな <ruby>傘<rt>かさ</rt></ruby>を <ruby>買いました<rt>かいました</rt></ruby>。
       - はい、きれいの <ruby>傘<rt>かさ</rt></ruby>です。
    2. <ruby>京都<rt>きょうと</rt></ruby>の <ruby>紅葉<rt>もみじ</rt></ruby>は <ruby>有名<rt>ゆうめい</rt></ruby>ですか。
       - はい、<ruby>有名<rt>ゆうめい</rt></ruby>です。
       - いいえ、<ruby>有名<rt>ゆうめい</rt></ruby>です。
       - はい、<ruby>有名<rt>ゆうめい</rt></ruby>なです。
    3. <ruby>旅行<rt>りょこう</rt></ruby>は どうでしたか。
       - はい、<ruby>楽しかった<rt>たのしかった</rt></ruby>です。
       - いいえ、<ruby>楽しくなかった<rt>たのしくなかった</rt></ruby>です。
       - <ruby>天気<rt>てんき</rt></ruby>は よくなかったです。でも、<ruby>楽しかった<rt>たのしかった</rt></ruby>です。

    #### 3. 听录音，用 `でも` 或 `そして` 回答

    - 例：<ruby>日本<rt>にほん</rt></ruby>の <ruby>食べ物<rt>たべもの</rt></ruby>は どうですか。（おいしい / <ruby>高い<rt>たかい</rt></ruby>）  
      → とても おいしいです。でも、<ruby>高い<rt>たかい</rt></ruby>です。

    1. <ruby>大きい<rt>おおきい</rt></ruby> / にぎやか
    2. <ruby>高い<rt>たかい</rt></ruby> / きれい
    3. いい / <ruby>寒い<rt>さむい</rt></ruby>
    4. おいしい / <ruby>辛い<rt>からい</rt></ruby>
    5. ハンサム / おもしろい

    #### 4. 翻译题

    1. 京都的红叶很有名。
    2. 横滨是个什么样的城市？是一个很大的城市，而且很热闹。
    3. 京都很美。不过，不太安静。
    """
)

