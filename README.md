# Build Log

個人の趣味アプリ・実験のポートフォリオサイト（静的HTML/CSS/JS、ビルド不要）。

## ローカルで見る

`index.html` を直接ブラウザで開くか、簡易サーバーで確認できます。

```bash
python -m http.server 8080
# http://localhost:8080 を開く
```

## 公開（Cloudflare Pages / 無料）

1. Cloudflareダッシュボード → Workers & Pages → Create application → Pages タブ → Connect to Git
2. このリポジトリ（`build-log`）を選択して連携を許可
3. ビルド設定: Framework preset は `None`、Build command は空欄、Build output directory は `/`
4. Save and Deploy → 数十秒で `https://build-log.pages.dev` のようなURLが発行される
5. 以後 `main` ブランチへの push で自動デプロイされる

## 構成

- `index.html` — ポートフォリオのトップ
- `project-mihariban.html` — 見張り番の製品紹介・開発記録
- `mihariban-start.html` — 初回設定の画面ガイド
- `mihariban-use.html` — 監視・検知・設定の画面ガイド
- `mihariban-recordings.html` — 録画の再生・保存ガイド
- `mihariban-help.html` — 対応条件・トラブルシューティング
- `styles.<ハッシュ>.css` — デザイントークン・スタイル（pop / softの2配色）。
  内容が変わるとファイル名ごと変わる(理由は `tools/版印を確かめる.py` 参照)
- `script.<ハッシュ>.js` — 年表示・テーマ切り替えの補助。同上
- `_headers` — Cloudflareへのキャッシュ指定。ハッシュ付きCSS/JSは長期キャッシュ、
  それ以外(HTML等)は毎回再検証

Projects セクションの内容（プロジェクト名・説明・リンク）は `index.html` 内の
`.specimen` を編集して差し替えてください。
