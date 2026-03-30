# salesforce-connect-sample

Python で Salesforce の取引先（Account）オブジェクトを操作するサンプルです。
認証方式ごとにディレクトリを分けています。

## 認証方式

| ディレクトリ | 認証方式 | 推奨用途 |
| ------------ | -------- | -------- |
| `oauth/` | OAuth 2.0 JWT Bearer Flow（秘密鍵による JWT 署名） | 本番・k8s など |
| `client_credentials/` | OAuth 2.0 Client Credentials Flow（client_id + client_secret） | 本番・k8s など |
| `user_auth/` | ユーザー名/パスワード + セキュリティトークン | 開発・検証環境 |

詳細は各ディレクトリの README を参照してください。

- [oauth/README.md](./oauth/README.md)
- [client_credentials/README.md](./client_credentials/README.md)
- [user_auth/README.md](./user_auth/README.md)

## ディレクトリ構成

```
salesforce-connect-sample/
├── oauth/                              # JWT Bearer Flow
│   ├── certs/
│   │   ├── server.key                  # 秘密鍵（gitignore済み）
│   │   └── server.crt                  # 公開鍵証明書（gitignore済み）
│   ├── common/
│   │   └── utils.py                    # JWT トークン取得・SOQL エスケープユーティリティ
│   ├── integrations/crm/salesforce/
│   │   ├── client.py                   # Salesforce 接続基底クラス
│   │   ├── const.py                    # 定数・環境変数
│   │   ├── models/
│   │   │   ├── account.py              # 取引先モデル
│   │   │   ├── bulk.py                 # 一括操作結果モデル
│   │   │   ├── credentials.py          # 認証情報モデル
│   │   │   └── metadata.py             # SObject メタデータモデル
│   │   └── repositories/
│   │       └── account.py              # 取引先 CRUD 操作
│   ├── main.py
│   ├── .env.example
│   └── README.md
│
├── client_credentials/                 # Client Credentials Flow
│   ├── common/
│   │   └── utils.py                    # SOQL エスケープ・strtobool ユーティリティ
│   ├── integrations/crm/salesforce/
│   │   ├── client.py                   # Salesforce 接続基底クラス
│   │   ├── const.py                    # 定数・環境変数
│   │   ├── models/
│   │   │   ├── account.py              # 取引先モデル
│   │   │   ├── bulk.py                 # 一括操作結果モデル
│   │   │   ├── credentials.py          # 認証情報モデル
│   │   │   └── metadata.py             # SObject メタデータモデル
│   │   └── repositories/
│   │       └── account.py              # 取引先 CRUD 操作
│   ├── main.py
│   ├── .env.example
│   └── README.md
│
└── user_auth/                          # ユーザー名/パスワード認証
    ├── common/
    │   └── utils.py                    # SOQL エスケープユーティリティ
    ├── integrations/crm/salesforce/
    │   ├── client.py                   # Salesforce 接続基底クラス
    │   ├── const.py                    # 定数・環境変数
    │   ├── models/
    │   │   ├── account.py              # 取引先モデル
    │   │   ├── bulk.py                 # 一括操作結果モデル
    │   │   ├── credentials.py          # 認証情報モデル
    │   │   └── metadata.py             # SObject メタデータモデル
    │   └── repositories/
    │       └── account.py              # 取引先 CRUD 操作
    ├── main.py
    ├── .env.example
    └── README.md
```

## 実行

```bash
# JWT Bearer Flow
cd oauth && uv run python main.py

# Client Credentials Flow
cd client_credentials && uv run python main.py

# ユーザー名/パスワード認証
cd user_auth && uv run python main.py
```
