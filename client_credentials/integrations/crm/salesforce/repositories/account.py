from integrations.crm.salesforce.client import SalesforceClient
from integrations.crm.salesforce.models.account import Account
from integrations.crm.salesforce.models.bulk import BulkResult
from common.utils import escape_soql


class AccountRepository(SalesforceClient):
    def find_all(self, limit: int = 100) -> list[Account]:
        """取引先を一覧取得する。"""
        query = f"SELECT Id, Name, Phone, BillingCity, BillingState FROM Account LIMIT {limit}"
        result = self.sf.query(query)
        return [Account.model_validate(r) for r in result["records"]]

    def find_by_id(self, account_id: str) -> Account:
        """ID で取引先を1件取得する。"""
        return Account.model_validate(self.sf.Account.get(account_id))

    def search_by_name(self, name: str) -> list[Account]:
        """名前の部分一致で取引先を検索する。"""
        safe_name = escape_soql(name)
        query = (
            f"SELECT Id, Name, Phone, BillingCity, BillingState "
            f"FROM Account WHERE Name LIKE '%{safe_name}%'"
        )
        result = self.sf.query(query)
        return [Account.model_validate(r) for r in result["records"]]

    def create(self, data: Account) -> str:
        """取引先を新規作成し、作成された ID を返す。

        Args:
            data: 作成するフィールドの値

        Returns:
            作成された取引先の ID
        """
        result = self.sf.Account.create(data.model_dump(exclude_none=True, exclude={"Id"}))
        if not result.get("id"):
            raise RuntimeError(f"取引先の作成に失敗しました: {result}")
        return result["id"]

    def update(self, data: Account) -> None:
        """取引先を更新する。

        Args:
            data: 更新するフィールドの値（Id を含めること）
        """
        self.sf.Account.update(data.Id, data.model_dump(exclude_none=True, exclude={"Id"}))

    def delete(self, account_id: str) -> None:
        """取引先を削除する。

        Args:
            account_id: 削除対象の取引先 ID
        """
        self.sf.Account.delete(account_id)

    # ------------------------------------------------------------------ #
    # 一括操作                                                             #
    # ------------------------------------------------------------------ #

    def bulk_create(self, records: list[Account]) -> list[BulkResult]:
        """取引先を一括作成する。

        Args:
            records: 作成するレコードのリスト

        Returns:
            各レコードの処理結果のリスト
        """
        raw = self.sf.bulk.Account.insert(
            [r.model_dump(exclude_none=True, exclude={"Id"}) for r in records]
        )
        return [BulkResult.model_validate(r) for r in raw]

    def bulk_update(self, records: list[Account]) -> list[BulkResult]:
        """取引先を一括更新する。

        Args:
            records: 更新するレコードのリスト（各レコードに Id を含めること）

        Returns:
            各レコードの処理結果のリスト
        """
        raw = self.sf.bulk.Account.update(
            [r.model_dump(exclude_none=True) for r in records]
        )
        return [BulkResult.model_validate(r) for r in raw]

    def bulk_upsert(
        self, records: list[Account], external_id_field: str
    ) -> list[BulkResult]:
        """取引先を一括 upsert する。

        Args:
            records: upsert するレコードのリスト
            external_id_field: 外部 ID フィールドの API 参照名。例: "ExternalId__c"

        Returns:
            各レコードの処理結果のリスト
        """
        raw = self.sf.bulk.Account.upsert(
            [r.model_dump(exclude_none=True, exclude={"Id"}) for r in records],
            external_id_field,
        )
        return [BulkResult.model_validate(r) for r in raw]

    def bulk_delete(self, account_ids: list[str]) -> list[BulkResult]:
        """取引先を一括削除する。

        Args:
            account_ids: 削除対象の取引先 ID のリスト

        Returns:
            各レコードの処理結果のリスト
        """
        raw = self.sf.bulk.Account.delete([{"Id": i} for i in account_ids])
        return [BulkResult.model_validate(r) for r in raw]
