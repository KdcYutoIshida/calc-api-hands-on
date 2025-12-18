# 機能要件（API）

## 概要
- Azure Functions で 2 つの HTTP API を提供する。
- ブラウザでURLを入力すると結果が画面に表示されればよい（text/plain で数値を返却）。

## エンドポイント
- GET /api/multiply
- GET /api/divide

## クエリパラメータ
- A, B（大文字）
- 型: 整数（例: -10, 0, 25）。先頭の +/- は許可。小数・指数表記は不可。
- 必須: A, B ともに必須。

## 振る舞い
- multiply: 結果は整数の積。
- divide: 通常の除算。結果は必要に応じて小数を含む（浮動小数点の文字列表現）。
- 入力検証:
  - A または B が欠落/整数変換不可 → 400 Bad Request
  - B=0（割り算のゼロ除算） → 400 Bad Request

## レスポンス
- 成功時: 200 OK
  - Content-Type: text/plain; charset=utf-8
  - Body: 結果の数値文字列のみ（例: "15", "2.5"）
- エラー時: 400 Bad Request
  - Content-Type: text/plain; charset=utf-8
  - Body: 簡潔な日本語のエラーメッセージ（例: "パラメータA,Bは整数で指定してください", "Bに0は指定できません"）

## 例
- GET /api/multiply?A=3&B=5 → 200 "15"
- GET /api/divide?A=10&B=4 → 200 "2.5"
- GET /api/divide?A=10&B=0 → 400 "Bに0は指定できません"
- GET /api/multiply?A=1.2&B=3 → 400 "パラメータA,Bは整数で指定してください"

## 非対象（本APIの範囲外）
- JSON応答、POST/PUT/PATCH/DELETEメソッド、APIバージョニング（/v1 など）は採用しない。
- 小数の丸め・桁数指定などの厳密な数値表現ルールは設けない（PoCのため簡易な表現で可）。
