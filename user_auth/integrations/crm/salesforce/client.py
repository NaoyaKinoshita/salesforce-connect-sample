"""Salesforce接続管理モジュール（ユーザー名/パスワード認証）"""

from simple_salesforce import Salesforce

from integrations.crm.salesforce.models.credentials import SalesforceCredentials


class SalesforceClient:
    """Salesforce への接続を管理する基底クラス。

    継承したクラスは self.sf を通じて Salesforce API を利用できる。
    """

    def __init__(self, credentials: SalesforceCredentials) -> None:
        self.sf = Salesforce(
            username=credentials.username,
            password=credentials.password,
            security_token=credentials.security_token,
            domain=credentials.domain,
        )
