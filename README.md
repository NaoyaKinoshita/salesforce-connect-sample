# salesforce-connect-sample

Python で Salesforce の取引先（Account）オブジェクトを操作するサンプルです。
認証方式ごとにディレクトリを分けています。

## 認証方式

| ディレクトリ | 認証方式 | 推奨用途 |
| ------------ | -------- | -------- |
| `oauth/` | OAuth 2.0 JWT Bearer Flow（秘密鍵による JWT 署名） | 本番・k8s など |
| `user_auth/` | ユーザー名/パスワード + セキュリティトークン | 開発・検証環境 |

詳細は各ディレクトリの README を参照してください。

- [oauth/README.md](./oauth/README.md)
- [user_auth/README.md](./user_auth/README.md)

## ディレクトリ構成

```
salesforce-connect-sample/
├── oauth/                              # JWT Bearer Flow
│   ├── certs/
│   │   ├── server.key                  # 秘密鍵（gitignore済み）
│   │   └── server.crt                  # 公開鍵証明書（gitignore済み）
│   ├── common/
│   │   └── utils.py                    # JWT トークン取得ユーティリティ
│   ├── integrations/crm/salesforce/
│   │   ├── client.py                   # Salesforce 接続基底クラス
│   │   ├── const.py                    # 定数・環境変数
│   │   └── repositories/
│   │       └── account.py              # 取引先 CRUD 操作
│   ├── main.py
│   ├── .env.example
│   └── README.md
│
└── user_auth/                          # ユーザー名/パスワード認証
    ├── integrations/crm/salesforce/
    │   ├── client.py                   # Salesforce 接続基底クラス
    │   ├── const.py                    # 定数・環境変数
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

# ユーザー名/パスワード認証
cd user_auth && uv run python main.py
```
