"""Salesforce接続管理モジュール（JWT Bearer Flow）"""

from simple_salesforce import Salesforce

from common.utils import get_access_token
from integrations.crm.salesforce.models.credentials import SalesforceCredentials


class SalesforceClient:
    """Salesforce への接続を管理する基底クラス。

    継承したクラスは self.sf を通じて Salesforce API を利用できる。
    """

    def __init__(self, credentials: SalesforceCredentials) -> None:
        audience = f"https://{credentials.domain}.salesforce.com"
        token_endpoint = (
            f"https://{credentials.domain}.salesforce.com/services/oauth2/token"
        )
        access_token, instance_url = get_access_token(
            client_id=credentials.client_id,
            username=credentials.username,
            private_key=credentials.private_key,
            audience=audience,
            token_endpoint=token_endpoint,
        )
        self.sf = Salesforce(instance_url=instance_url, session_id=access_token)
