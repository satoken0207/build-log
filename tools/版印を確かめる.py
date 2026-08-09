# -*- coding: utf-8 -*-
"""**HTML が指している版印が、いまの中身と合っているかを確かめる。**

■ **なぜ要るか。付け忘れると、前に来た人だけが崩れたページを見る**

  2026-08-09、利用者が公開ページを見たら細長く崩れていた。
  **公開側は正しい物を配っていた。**HTML も CSS もバイト単位で一致していた。

  原因は、利用者のブラウザが**前に見たときの古い `styles.css` を持ったまま、**
  **新しい HTML に当てていた**こと。Ctrl+F5 で直った。

  **見る側は「古いのを持っている」と気づけない。**
  そして**前に来たことのある人だけ**に起きるので、初めて見る人には見えない。
  作った側が自分で見ても、たいてい直っている。**いちばん見つけにくい壊れ方。**

■ **なぜ中身のハッシュか。記録の番号ではないのか**

  記録の番号だと、**HTML だけ直した回でも印が変わる。**
  そのたびに全訪問者が CSS と JS を読み直す。崩れはしないが、毎回無駄が出る。

  **中身のハッシュなら、変わった回だけ変わる。**

■ **なぜ道具で自動で書き換えないのか**

  **HP に組み立ての段が無い。**入れると、増える仕掛けのほうが大きくなる。
  **手で書いて、この見張りで守る。**忘れた瞬間に落ちる。

■ **使い方**

    python tools/版印を確かめる.py

  合っていれば 0、ずれていれば 1 を返す。**ずれている場所を全部並べる。**
"""
import glob
import hashlib
import os
import re
import sys

ここ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# **見張る対象。** 増えたらここへ足す。
対象 = {
    "styles.css": r'href="styles\.css(?:\?v=([0-9a-f]+))?"',
    "script.js": r'src="script\.js(?:\?v=([0-9a-f]+))?"',
}


def 中身の印(path: str) -> str:
    """**中身から出す。**先頭8桁で足りる（衝突は事実上起きない）。"""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]


def main() -> int:
    os.chdir(ここ)

    正しい = {}
    for name in 対象:
        if not os.path.exists(name):
            print(f"  **{name} が無い。**この見張りを直すこと")
            return 1
        正しい[name] = 中身の印(name)

    pages = sorted(glob.glob("*.html"))

    # **1つも見ずに通らないこと。**置き場所が変われば「ずれ0」で緑になる。
    if len(pages) < 5:
        print(f"  **ページを {len(pages)} 枚しか見ていない。**置き場所が変わった")
        return 1

    ずれ = []
    見た = 0

    for page in pages:
        with open(page, encoding="utf-8") as f:
            html = f.read()

        for name, pattern in 対象.items():
            for m in re.finditer(pattern, html):
                見た += 1
                印 = m.group(1)

                if 印 is None:
                    ずれ.append(f"{page}: {name} に版印が無い")
                elif 印 != 正しい[name]:
                    ずれ.append(
                        f"{page}: {name} の版印が {印}。いまの中身は {正しい[name]}")

    print(f"  見たページ {len(pages)} 枚 / 読み込み {見た} 件")
    for name, v in 正しい.items():
        print(f"    {name}  いまの中身  {v}")
    print()

    if not ずれ:
        print("  ずれ 0 件")
        return 0

    print(f"  **ずれ {len(ずれ)} 件**")
    for s in ずれ:
        print(f"    {s}")
    print()
    print("  **CSS か JS を直したら、全ページの版印を新しい値へ書き換えること。**")
    print("  忘れると、前に来たことのある人だけが崩れたページを見ます。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
