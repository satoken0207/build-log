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

- `index.html` — マークアップ
- `styles.css` — デザイントークン・スタイル（ライト/ダーク両対応）
- `script.js` — 年表示・テーマ切り替えの補助

Projects セクションの内容（プロジェクト名・説明・リンク）は `index.html` 内の
`.specimen` を編集して差し替えてください。
