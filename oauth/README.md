# salesforce-connect-sample

Salesforce の取引先（Account）オブジェクトを OAuth 2.0 JWT Bearer Flow で操作するサンプルです。

## ディレクトリ構成

```
salesforce-connect-sample/
├── certs/
│   ├── server.key          # 秘密鍵（gitignore済み）
│   └── server.crt          # 公開鍵証明書（gitignore済み）
├── common/
│   └── utils.py            # JWT Bearer Flow によるトークン取得・SOQL エスケープ
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

### 1. 鍵ペアの生成

```bash
openssl genrsa -out certs/server.key 2048
openssl req -new -x509 -key certs/server.key -out certs/server.crt -days 3650
```

> **注意: `-days` について**
> `openssl` に無期限指定はできません。最大値に制限はありませんが、実運用では **`3650`（10年）** を推奨します。
> `36500`（100年）なども技術的には指定可能ですが、ブラウザや一部ツールで拒否される場合があります。
> **証明書の有効期限が切れると Salesforce への接続が失敗する**ため、期限切れ前に `certs/server.crt` を再生成して Salesforce の外部クライアントアプリケーションに再アップロードしてください。

証明書生成時の入力例:

| 項目                | 例               |
| ------------------- | ---------------- |
| Country Name        | ja               |
| State or Province   | [都道府県名]     |
| Locality            | [市区町村名]     |
| Organization        | [組織名]         |
| Organizational Unit | [組織単位]       |
| Common Name         | [氏名]           |
| Email Address       | [メールアドレス] |

### 2. Salesforce で外部クライアントアプリケーションを作成

Setup > **外部クライアントアプリケーション** > 新規 から以下の設定で作成します。

#### アプリケーション設定

| 項目             | 設定値                                                                                          |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| コールバック URL | `http://localhost`（※）                                                                         |
| OAuth 範囲       | `API を使用してユーザーデータを管理 (api)` `いつでも要求を実行 (refresh_token, offline_access)` |

> **※ コールバック URL について**
> JWT Bearer Flow はサーバー間通信のため、認証フロー中にコールバック URL へのリダイレクトは発生しません。
> ただし Connected App の設定上は必須項目のため、`http://localhost` などのダミー値を入力します。
> Web アプリなど Authorization Code Flow と併用する場合は、実際のリダイレクト先 URL（例: `https://your-app.example.com/oauth/callback`）に変更してください。

#### フローの有効化

| 項目                       | 設定値                            |
| -------------------------- | --------------------------------- |
| JWT ベアラーフローを有効化 | ✓（オン）                         |
| 証明書アップロード         | `certs/server.crt` をアップロード |

#### セキュリティ

| 項目                           | 設定値    |
| ------------------------------ | --------- |
| Web サーバーフローの秘密が必要 | ✓（オン） |
| 更新トークンフローの秘密が必要 | ✓（オン） |
| PKCE 拡張を要求                | ✓（オン） |

#### OAuth ポリシー

| 項目                   | 設定値                                 |
| ---------------------- | -------------------------------------- |
| 許可されているユーザー | 管理者が承認したユーザーは事前承認済み |

#### プロファイルを選択

| 項目                 | 設定値         |
| -------------------- | -------------- |
| 選択済みプロファイル | システム管理者 |

### 3. コンシューマー鍵を取得

アプリケーション保存後、**コンシューマー鍵と秘密** ボタンからコンシューマー鍵（Consumer Key）を取得します。

### 4. 環境変数を設定

```bash
cp .env.example .env
```

`.env` を編集して接続情報を入力します。

```
SF_CLIENT_ID=<コンシューマー鍵>
SF_USERNAME=<Salesforce ログインユーザー名>
SF_PRIVATE_KEY_FILE=./certs/server.key
SF_DOMAIN=login  # サンドボックスの場合は test
```

### 5. 依存パッケージのインストール

```bash
uv sync
```

## 実行

```bash
uv run python main.py
```

## Kubernetes から利用する場合の注意点

### 1. 秘密鍵は Secret で管理する

`server.key` を **Secret** リソースで管理し、ボリュームマウントで Pod に渡します。

```bash
kubectl create secret generic salesforce-certs \
  --from-file=server.key=certs/server.key
```

```yaml
# Deployment の volumes / volumeMounts 例
volumes:
  - name: salesforce-certs
    secret:
      secretName: salesforce-certs

volumeMounts:
  - name: salesforce-certs
    mountPath: /app/certs
    readOnly: true
```

`SF_PRIVATE_KEY_FILE` はコンテナ内のマウントパスに合わせます。

```yaml
env:
  - name: SF_PRIVATE_KEY_FILE
    value: /app/certs/server.key
```

### 2. 環境変数も Secret で管理する

`SF_CLIENT_ID` や `SF_USERNAME` も Secret で管理し、`envFrom` または `env.valueFrom` で注入します。

```yaml
env:
  - name: SF_CLIENT_ID
    valueFrom:
      secretKeyRef:
        name: salesforce-credentials
        key: client_id
  - name: SF_USERNAME
    valueFrom:
      secretKeyRef:
        name: salesforce-credentials
        key: username
```

### 3. Egress の通信を許可する

NetworkPolicy で Salesforce への HTTPS アウトバウンド通信（ポート 443）を許可してください。
接続先は `.salesforce.com` および `.force.com` ドメインです。

### 4. Pod の時刻同期を確認する

JWT の署名には `exp`（有効期限）クレームが含まれており、**Pod の時刻がずれていると認証エラーになります**。
k8s ノードの NTP 同期が正しく機能しているか確認してください。

### 5. アクセストークンの有効期限に注意する

Salesforce のアクセストークンはデフォルト **2時間** で失効します。
長時間稼働する Pod では、リクエストのたびにトークンを再取得する設計を推奨します。

### 6. 証明書の有効期限を監視する

`server.crt` の有効期限が切れると接続が失敗します。
有効期限をあらかじめ監視し（例: Prometheus の `x509-certificate-exporter`）、期限前に以下の対応を行ってください。

1. 鍵ペアを再生成
2. Salesforce の外部クライアントアプリケーションに新しい `server.crt` を再アップロード
3. k8s Secret を更新して Pod を再起動
