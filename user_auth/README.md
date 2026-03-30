# salesforce-connect-sample（ユーザー名/パスワード認証）

Salesforce の取引先（Account）オブジェクトをユーザー名/パスワード認証で操作するサンプルです。

## oauth との違い

| 項目                 | oauth（JWT Bearer Flow） | user_auth（ユーザー名/パスワード）             |
| -------------------- | ------------------------ | ---------------------------------------------- |
| 認証方式             | 秘密鍵による JWT 署名    | ユーザー名 + パスワード + セキュリティトークン |
| パスワード管理       | 不要                     | 必要                                           |
| セキュリティトークン | 不要                     | 必要（信頼済み IP 登録で不要にできる）         |
| 証明書管理           | 必要（有効期限あり）     | 不要                                           |
| 推奨用途             | 本番・k8s など           | 開発・検証環境                                 |

## ディレクトリ構成

```
user_auth/
├── common/
│   └── utils.py            # SOQL エスケープユーティリティ
├── integrations/crm/salesforce/
│   ├── client.py           # Salesforce 接続基底クラス
│   ├── const.py            # 定数・環境変数
│   ├── models/
│   │   ├── account.py      # 取引先モデル
│   │   ├── bulk.py         # 一括操作結果モデル
│   │   ├── credentials.py  # 認証情報モデル
│   │   └── metadata.py     # SObject メタデータモデル
│   └── repositories/
│       └── account.py      # 取引先 CRUD 操作
├── main.py                 # 実行サンプル
├── .env                    # 接続情報（gitignore済み）
└── .env.example            # 接続情報テンプレート
```

## セットアップ

### 1. セキュリティトークンを取得する

セキュリティトークンは、Salesforce がパスワード認証時に**知らない IP からのアクセスに要求する追加の認証コード**です。

**取得手順：**

1. Salesforce にブラウザでログイン
2. 右上のアバター → **設定**
3. 左メニュー「私の個人情報」→ **「私のセキュリティトークンのリセット」**
4. 登録メールアドレスに届いたトークンを控える

> **画面に項目が表示されない場合**
> 以下の URL を直接開くとリセットできます。
>
> ```
> https://<your-instance>.salesforce.com/_ui/system/security/ResetApiTokenEdit
> ```
>
> 接続元の IP がすでに「信頼済み IP 範囲」に登録されている場合、セキュリティトークンのリセット項目自体が非表示になることがあります。

> **セキュリティトークンを不要にする方法**
> 接続元の IP を Salesforce の「信頼済み IP 範囲」に登録すれば不要になります。
> k8s など固定 IP で接続する場合はこちらの方が運用しやすいです。
>
> Setup → **Network Access** → 信頼済み IP 範囲に接続元 IP を追加

### 2. 環境変数を設定する

```bash
cp .env.example .env
```

`.env` を編集して接続情報を入力します。

```
SF_USERNAME=your-email@example.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
SF_DOMAIN=login  # サンドボックスの場合は test
```

### 3. 依存パッケージのインストール

```bash
uv sync
```

## 実行

```bash
uv run python main.py
```

## Kubernetes から利用する場合の注意点

### 1. 環境変数は Secret で管理する

`SF_PASSWORD` や `SF_SECURITY_TOKEN` を ConfigMap に入れてはいけません。必ず **Secret** リソースで管理します。

```bash
kubectl create secret generic salesforce-credentials \
  --from-literal=username=your-email@example.com \
  --from-literal=password=your_password \
  --from-literal=security_token=your_security_token
```

```yaml
env:
  - name: SF_USERNAME
    valueFrom:
      secretKeyRef:
        name: salesforce-credentials
        key: username
  - name: SF_PASSWORD
    valueFrom:
      secretKeyRef:
        name: salesforce-credentials
        key: password
  - name: SF_SECURITY_TOKEN
    valueFrom:
      secretKeyRef:
        name: salesforce-credentials
        key: security_token
```

### 2. 信頼済み IP 範囲を登録してセキュリティトークンを不要にする

k8s の Pod Egress IP を Salesforce の信頼済み IP 範囲に登録することで、`SF_SECURITY_TOKEN` が不要になりシークレット管理がシンプルになります。

> Setup → **Network Access** → 信頼済み IP 範囲に Pod の Egress IP を追加

### 3. Egress の通信を許可する

NetworkPolicy で Salesforce への HTTPS アウトバウンド通信（ポート 443）を許可してください。
接続先は `.salesforce.com` および `.force.com` ドメインです。

### 4. アクセストークンの有効期限に注意する

Salesforce のアクセストークンはデフォルト **2時間** で失効します。
長時間稼働する Pod では、リクエストのたびに再認証する設計を推奨します。
