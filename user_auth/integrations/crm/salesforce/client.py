"""Salesforce接続管理モジュール（ユーザー名/パスワード認証）"""

from simple_salesforce import Salesforce

from integrations.crm.salesforce.models.credentials import SalesforceCredentials
from integrations.crm.salesforce.models.metadata import SObjectMetadata


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
