"""Salesforce接続管理モジュール（JWT Bearer Flow）"""

from simple_salesforce import Salesforce

from common.utils import get_access_token
from integrations.crm.salesforce.models.credentials import SalesforceCredentials
from integrations.crm.salesforce.models.metadata import SObjectMetadata


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

    def _describe_sobject(self, sobject_name: str) -> SObjectMetadata:
        return SObjectMetadata.model_validate(getattr(self.sf, sobject_name).describe())

    def describe(self, sobject_name: str) -> SObjectMetadata:
        """指定した SObject のメタデータを取得する。

        Args:
            sobject_name: SObject の API 参照名。例: "Account", "Contact"

        Returns:
            フィールド定義・リレーション等を含むメタデータ
        """
        return self._describe_sobject(sobject_name)

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
        meta = self._describe_sobject(sobject_name)
        fields_by_name = {f.name: f for f in meta.fields}
        for name in field_names:
            if name not in fields_by_name:
                raise ValueError(f"{sobject_name}.{name} が見つかりません")
        return SObjectMetadata(
            name=meta.name,
            label=meta.label,
            fields=[fields_by_name[name] for name in field_names],
        )
