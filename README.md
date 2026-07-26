# Build Log

個人の趣味アプリ・実験のポートフォリオサイト（静的HTML/CSS/JS、ビルド不要）。

## ローカルで見る

`index.html` を直接ブラウザで開くか、簡易サーバーで確認できます。

```bash
python -m http.server 8080
# http://localhost:8080 を開く
```

## 公開（GitHub Pages / 無料）

1. GitHubで空のリポジトリを作成する（Public、README/ .gitignore は追加しない）
2. このディレクトリをそのリポジトリに push する
3. リポジトリの Settings → Pages → Source を「Deploy from a branch」、Branch を `main` / `/(root)` に設定
4. 数分後に `https://<username>.github.io/<repo>/` で公開される

## 構成

- `index.html` — マークアップ
- `styles.css` — デザイントークン・スタイル（ライト/ダーク両対応）
- `script.js` — 年表示・テーマ切り替えの補助

Projects セクションの内容（プロジェクト名・説明・リンク）は `index.html` 内の
`.specimen` を編集して差し替えてください。
