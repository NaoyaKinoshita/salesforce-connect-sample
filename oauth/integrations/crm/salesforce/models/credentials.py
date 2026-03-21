from pydantic import BaseModel, Field


class SalesforceCredentials(BaseModel):
    """Salesforce 接続に必要な認証情報。"""

    client_id: str = Field(description="Connected App のコンシューマキー")
    username: str = Field(description="Salesforce ユーザー名")
    private_key: str = Field(description="JWT 署名用 RSA 秘密鍵（PEM 形式）")
    domain: str = Field(
        default="login", description="ログインドメイン（本番: login / Sandbox: test）"
    )

    @classmethod
    def from_env(cls) -> "SalesforceCredentials":
        """環境変数（const 経由）から SalesforceCredentials を生成する。"""
        from integrations.crm.salesforce.const import (
            SF_CLIENT_ID,
            SF_DOMAIN,
            SF_PRIVATE_KEY_FILE,
            SF_USERNAME,
        )

        with open(SF_PRIVATE_KEY_FILE) as f:
            private_key = f.read()

        return cls(
            client_id=SF_CLIENT_ID,
            username=SF_USERNAME,
            private_key=private_key,
            domain=SF_DOMAIN,
        )
