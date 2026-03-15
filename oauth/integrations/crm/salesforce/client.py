"""Salesforce接続管理モジュール（JWT Bearer Flow）"""

from simple_salesforce import Salesforce

from common.utils import get_access_token
from integrations.crm.salesforce.const import (
    SF_CLIENT_ID,
    SF_USERNAME,
    SF_PRIVATE_KEY_FILE,
    SF_TOKEN_ENDPOINT,
    SF_AUDIENCE,
)


class SalesforceClient:
    """Salesforce への接続を管理する基底クラス。

    継承したクラスは self.sf を通じて Salesforce API を利用できる。
    """

    def __init__(self) -> None:
        access_token, instance_url = get_access_token(
            client_id=SF_CLIENT_ID,
            username=SF_USERNAME,
            private_key_file=SF_PRIVATE_KEY_FILE,
            audience=SF_AUDIENCE,
            token_endpoint=SF_TOKEN_ENDPOINT,
        )
        self.sf = Salesforce(instance_url=instance_url, session_id=access_token)
