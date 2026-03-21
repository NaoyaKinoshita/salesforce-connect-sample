from pydantic import BaseModel, Field


class SalesforceCredentials(BaseModel):
    """Salesforce 接続に必要な認証情報。"""

    client_id: str = Field(description="Connected App のコンシューマキー")
    client_secret: str = Field(description="Connected App のコンシューマシークレット")
    token_endpoint: str = Field(description="OAuth2 トークンエンドポイント URL")

    @classmethod
    def from_env(cls) -> "SalesforceCredentials":
        """環境変数（const 経由）から SalesforceCredentials を生成する。"""
        from integrations.crm.salesforce.const import (
            SF_CLIENT_ID,
            SF_CLIENT_SECRET,
            SF_TOKEN_ENDPOINT,
        )

        return cls(
            client_id=SF_CLIENT_ID,
            client_secret=SF_CLIENT_SECRET,
            token_endpoint=SF_TOKEN_ENDPOINT,
        )
