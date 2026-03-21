"""Salesforce接続管理モジュール（Client Credentials Flow）"""

import requests
from simple_salesforce import Salesforce

from integrations.crm.salesforce.models.credentials import SalesforceCredentials


class SalesforceClient:
    """Salesforce への接続を管理する基底クラス。

    継承したクラスは self.sf を通じて Salesforce API を利用できる。
    """

    def __init__(self, credentials: SalesforceCredentials) -> None:
        response = requests.post(
            credentials.token_endpoint,
            data={
                "grant_type": "client_credentials",
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
            },
            timeout=30,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(
                f"Salesforce 認証エラー: {response.status_code} {response.text}"
            ) from e

        try:
            token_data = response.json()
        except ValueError as e:
            raise RuntimeError("Salesforce 認証レスポンスのパースに失敗しました") from e

        try:
            self.sf = Salesforce(
                instance_url=token_data["instance_url"],
                session_id=token_data["access_token"],
            )
        except KeyError as e:
            raise RuntimeError(
                f"Salesforce 認証レスポンスに必要なキーが存在しません: {e}"
            ) from e
