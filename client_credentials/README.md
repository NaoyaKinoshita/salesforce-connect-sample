# salesforce-connect-sample（Client Credentials Flow）

Salesforce の取引先（Account）オブジェクトを OAuth 2.0 Client Credentials Flow で操作するサンプルです。

## 他の認証方式との違い

| 項目 | oauth（JWT Bearer） | client_credentials | user_auth（パスワード） |
| ---- | ------------------- | ------------------ | ----------------------- |
| 認証方式 | 秘密鍵による JWT 署名 | client_id + client_secret | ユーザー名 + パスワード |
| パスワード管理 | 不要 | 不要 | 必要 |
| 証明書管理 | 必要（有効期限あり） | 不要 | 不要 |
| 実行ユーザーの設定 | 不要 | 必要（Connected App に設定） | 不要 |
| 推奨用途 | 本番・k8s など | 本番・k8s など | 開発・検証環境 |

## ディレクトリ構成

```
client_credentials/
├── common/
│   └── utils.py            # strtobool ユーティリティ
├── integrations/crm/salesforce/
│   ├── client.py           # Salesforce 接続基底クラス
│   ├── const.py            # 定数・環境変数
│   └── repositories/
│       └── account.py      # 取引先 CRUD 操作
├── main.py                 # 実行サンプル
├── .env                    # 接続情報（gitignore済み）
└── .env.example            # 接続情報テンプレート
```

## セットアップ

### 1. Salesforce で Connected App の設定を確認する

Setup > **外部クライアントアプリケーション** > 対象アプリを選択し、以下を確認・設定します。

#### フローの有効化

| 項目 | 設定値 |
| ---- | ------ |
| クライアントログイン情報フローを有効化 | ✓（オン） |

#### 実行ユーザーを設定する

Client Credentials Flow は**ユーザーコンテキストなし**でアクセスするため、Connected App に「実行ユーザー」の紐付けが必要です。

1. アプリの詳細画面で **「クライアントログイン情報を管理」** をクリック
2. **実行ユーザー** に API アクセス権限を持つユーザーを設定

> 実行ユーザーの権限がそのままアクセス権限になるため、**必要最小限の権限を持つ専用ユーザー**を用意することを推奨します。

### 2. コンシューマー鍵と秘密を取得する

アプリの詳細画面で **「コンシューマー鍵と秘密」** ボタンをクリックし、以下の値を取得します。

- **コンシューマー鍵** → `SF_CLIENT_ID`
- **コンシューマーの秘密** → `SF_CLIENT_SECRET`

### 3. 環境変数を設定する

```bash
cp .env.example .env
```

`.env` を編集して接続情報を入力します。

#### My Domain を使用しない場合（2021年以前の旧 Org など）

```
SF_CLIENT_ID=<コンシューマー鍵>
SF_CLIENT_SECRET=<コンシューマーの秘密>
SF_MY_DOMAIN=false
SF_DOMAIN=login  # サンドボックスの場合は test
```

#### My Domain を使用する場合（新規 Org・Spring '21 以降）

```
SF_CLIENT_ID=<コンシューマー鍵>
SF_CLIENT_SECRET=<コンシューマーの秘密>
SF_MY_DOMAIN=true
SF_INSTANCE_URL=https://<your-domain>.my.salesforce.com
```

> **`SF_MY_DOMAIN` について**
> `SF_MY_DOMAIN=false` の場合は `login.salesforce.com`（サンドボックスは `test.salesforce.com`）をトークンエンドポイントとして使用します。
> `SF_MY_DOMAIN=true` の場合は `SF_INSTANCE_URL` をトークンエンドポイントとして使用します。
> My Domain が有効な Org で `false` を設定すると `request not supported on this domain` エラーになります。
>
> My Domain の有効化状況は Setup → **My Domain** で確認できます。
>
> `SF_MY_DOMAIN` に設定できる値: `true` / `false` / `1` / `0` / `yes` / `no`

### 4. 依存パッケージのインストール

```bash
uv sync
```

## 実行

```bash
uv run python main.py
```

## Kubernetes から利用する場合の注意点

### 1. 環境変数は Secret で管理する

`SF_CLIENT_SECRET` を ConfigMap に入れてはいけません。必ず **Secret** リソースで管理します。

```bash
kubectl create secret generic salesforce-credentials \
  --from-literal=client_id=your_consumer_key \
  --from-literal=client_secret=your_consumer_secret
```

```yaml
env:
  - name: SF_CLIENT_ID
    valueFrom:
      secretKeyRef:
        name: salesforce-credentials
        key: client_id
  - name: SF_CLIENT_SECRET
    valueFrom:
      secretKeyRef:
        name: salesforce-credentials
        key: client_secret
```

### 2. Egress の通信を許可する

NetworkPolicy で Salesforce への HTTPS アウトバウンド通信（ポート 443）を許可してください。
接続先は `.salesforce.com` および `.force.com` ドメインです。

### 3. アクセストークンについて

Salesforce のアクセストークンはデフォルト **2時間** で失効します。

本実装では `AccountRepository()` のインスタンス化のたびに `__init__` でトークンを取得するため、**毎回新しいトークンが発行され、有効期限切れは発生しません**。

ただし、リクエストのたびに認証 API を呼び出すコストがかかります。パフォーマンスが求められる場合は、トークンをキャッシュして有効期限が近づいたタイミングで再取得する設計を検討してください。
