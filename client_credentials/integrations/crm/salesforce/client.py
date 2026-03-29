"""Salesforce接続管理モジュール（Client Credentials Flow）"""

import requests
from simple_salesforce import Salesforce

from integrations.crm.salesforce.models.credentials import SalesforceCredentials
from integrations.crm.salesforce.models.metadata import SObjectMetadata


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

    def describe(self, sobject_name: str) -> SObjectMetadata:
        """指定した SObject のメタデータを取得する。

        Args:
            sobject_name: SObject の API 参照名。例: "Account", "Contact"

        Returns:
            フィールド定義・リレーション等を含むメタデータ
        """
        return SObjectMetadata.model_validate(getattr(self.sf, sobject_name).describe())

    def describe_specified_fields(
        self, sobject_name: str, field_names: list[str]
    ) -> SObjectMetadata:
        """指定した SObject の特定フィールドのメタデータを取得する。

        Args:
            sobject_name: SObject の API 参照名。例: "Account"
            field_names: 取得するフィールドの API 参照名のリスト。例: ["Name", "Industry"]

        Returns:
            指定したフィールドのみを含む SObjectMetadata

        Raises:
            ValueError: 指定したフィールドが存在しない場合
        """
        meta = self.describe(sobject_name)
        fields_by_name = {f.name: f for f in meta.fields}
        for name in field_names:
            if name not in fields_by_name:
                raise ValueError(f"{sobject_name}.{name} が見つかりません")
        return SObjectMetadata(
            name=meta.name,
            label=meta.label,
            fields=[fields_by_name[name] for name in field_names],
        )
