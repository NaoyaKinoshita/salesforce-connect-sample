from pydantic import BaseModel, Field


class SalesforceCredentials(BaseModel):
    """Salesforce 接続に必要な認証情報。"""

    username: str = Field(description="Salesforce ユーザー名")
    password: str = Field(description="Salesforce パスワード")
    security_token: str = Field(description="Salesforce セキュリティトークン")
    domain: str = Field(
        default="login", description="ログインドメイン（本番: login / Sandbox: test）"
    )

    @classmethod
    def from_env(cls) -> "SalesforceCredentials":
        """環境変数（const 経由）から SalesforceCredentials を生成する。"""
        from integrations.crm.salesforce.const import (
            SF_DOMAIN,
            SF_PASSWORD,
            SF_SECURITY_TOKEN,
            SF_USERNAME,
        )

        return cls(
            username=SF_USERNAME,
            password=SF_PASSWORD,
            security_token=SF_SECURITY_TOKEN,
            domain=SF_DOMAIN,
        )
