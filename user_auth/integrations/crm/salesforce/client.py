"""Salesforce接続管理モジュール（ユーザー名/パスワード認証）"""

from simple_salesforce import Salesforce

from integrations.crm.salesforce.const import (
    SF_USERNAME,
    SF_PASSWORD,
    SF_SECURITY_TOKEN,
    SF_DOMAIN,
)


class SalesforceClient:
    """Salesforce への接続を管理する基底クラス。

    継承したクラスは self.sf を通じて Salesforce API を利用できる。
    """

    def __init__(self) -> None:
        self.sf = Salesforce(
            username=SF_USERNAME,
            password=SF_PASSWORD,
            security_token=SF_SECURITY_TOKEN,
            domain=SF_DOMAIN,
        )
