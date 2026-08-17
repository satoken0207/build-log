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

■ **なぜファイル名にハッシュを埋めるのか。`?v=` クエリではだめなのか**

  2026-08-17まではクエリ文字列(`styles.css?v=ハッシュ`)で運用していたが、
  **Cloudflareのエッジキャッシュはこのクエリを見ていなかった。**
  `?v=` を変えて再配置しても、エッジは同じパス(`/styles.css`)への
  古いキャッシュをそのまま返し続けた。ブラウザのキャッシュは効いていたので
  自分では気づけず、原因を切り分けるのに時間がかかった。

  **ファイル名自体にハッシュを埋めれば(`styles.<ハッシュ>.css`)、
  内容が変わるたびに別パスになる。** パスが違えばどんなキャッシュ層でも
  取り違えようがない。古いファイル名はそのまま残しておいて構わない
  (二度と参照されなくなるだけで、害はない)。

■ **なぜ中身のハッシュか。連番ではないのか**

  連番だと、**HTML だけ直した回でも版が変わる。**
  そのたびに全訪問者が CSS と JS を読み直す。崩れはしないが、毎回無駄が出る。

  **中身のハッシュなら、変わった回だけファイル名が変わる。**

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

# **見張る対象。** ファイル名のパターンと、HTML側の参照パターン。増えたらここへ足す。
対象 = {
    "styles.css": {
        "ファイル": re.compile(r"^styles\.([0-9a-f]{8})\.css$"),
        "参照": re.compile(r'href="styles\.([0-9a-f]{8})\.css"'),
    },
    "script.js": {
        "ファイル": re.compile(r"^script\.([0-9a-f]{8})\.js$"),
        "参照": re.compile(r'src="script\.([0-9a-f]{8})\.js"'),
    },
}


def 中身の印(path: str) -> str:
    """**中身から出す。**先頭8桁で足りる(衝突は事実上起きない)。"""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]


def main() -> int:
    os.chdir(ここ)

    ずれ = []
    正しい = {}

    for name, pat in 対象.items():
        候補 = sorted(
            f for f in os.listdir(ここ) if pat["ファイル"].match(f)
        )
        if not 候補:
            print(f"  **{name} 形式のファイルが無い。**この見張りを直すこと")
            return 1

        # 複数残っていて構わない(古い版は参照されなくなるだけ)。
        # ただし「今の中身」と一致するものが少なくとも1つ必要。
        いまの中身 = 中身の印(候補[-1]) if len(候補) == 1 else None
        一致するもの = None
        for f in 候補:
            埋め込み = pat["ファイル"].match(f).group(1)
            if 埋め込み == 中身の印(f):
                一致するもの = f
                break
        if 一致するもの is None:
            print(f"  **{name}: ファイル名のハッシュと中身が一致するものが無い。**")
            for f in 候補:
                print(f"    {f}  ファイル名の印 {pat['ファイル'].match(f).group(1)}"
                      f"  中身の印 {中身の印(f)}")
            return 1
        正しい[name] = pat["ファイル"].match(一致するもの).group(1)

    pages = sorted(glob.glob("*.html"))

    # **1つも見ずに通らないこと。**置き場所が変われば「ずれ0」で緑になる。
    if len(pages) < 5:
        print(f"  **ページを {len(pages)} 枚しか見ていない。**置き場所が変わった")
        return 1

    見た = 0

    for page in pages:
        with open(page, encoding="utf-8") as f:
            html = f.read()

        for name, pat in 対象.items():
            マッチ = list(pat["参照"].finditer(html))
            if not マッチ:
                ずれ.append(f"{page}: {name} への参照が無い")
                continue
            for m in マッチ:
                見た += 1
                印 = m.group(1)
                if 印 != 正しい[name]:
                    ずれ.append(
                        f"{page}: {name} の参照が {印}。いまの中身は {正しい[name]}")

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
    print("  **CSS か JS を直したら、新しいファイル名(styles.<ハッシュ>.css)に")
    print("  リネームして、全ページの参照を書き換えること。**")
    print("  忘れると、前に来たことのある人だけが崩れたページを見ます。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
