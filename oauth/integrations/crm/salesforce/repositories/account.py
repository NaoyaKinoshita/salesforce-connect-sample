from integrations.crm.salesforce.client import SalesforceClient
from common.utils import escape_soql


class AccountRepository(SalesforceClient):
    def find_all(self, limit: int = 100) -> list[dict]:
        """取引先を一覧取得する。"""
        query = f"SELECT Id, Name, Phone, BillingCity, BillingState FROM Account LIMIT {limit}"
        result = self.sf.query(query)
        return result["records"]

    def find_by_id(self, account_id: str) -> dict:
        """ID で取引先を1件取得する。"""
        return self.sf.Account.get(account_id)

    def search_by_name(self, name: str) -> list[dict]:
        """名前の部分一致で取引先を検索する。"""
        safe_name = escape_soql(name)
        query = (
            f"SELECT Id, Name, Phone, BillingCity, BillingState "
            f"FROM Account WHERE Name LIKE '%{safe_name}%'"
        )
        result = self.sf.query(query)
        return result["records"]

    def create(self, data: dict) -> str:
        """取引先を新規作成し、作成された ID を返す。

        Args:
            data: 設定するフィールドの辞書。例: {"Name": "株式会社サンプル"}

        Returns:
            作成された取引先の ID
        """
        result = self.sf.Account.create(data)
        if not result.get("id"):
            raise RuntimeError(f"取引先の作成に失敗しました: {result}")
        return result["id"]

    def update(self, account_id: str, data: dict) -> None:
        """取引先を更新する。

        Args:
            account_id: 更新対象の取引先 ID
            data: 更新するフィールドの辞書。例: {"Phone": "03-1234-5678"}
        """
        self.sf.Account.update(account_id, data)

    def delete(self, account_id: str) -> None:
        """取引先を削除する。

        Args:
            account_id: 削除対象の取引先 ID
        """
        self.sf.Account.delete(account_id)

    # ------------------------------------------------------------------ #
    # 一括操作                                                             #
    # ------------------------------------------------------------------ #

    def bulk_create(self, records: list[dict]) -> list[dict]:
        """取引先を一括作成する。

        Args:
            records: 作成するレコードのリスト。例: [{"Name": "会社A"}, ...]

        Returns:
            各レコードの処理結果（id, success, errors）のリスト
        """
        return self.sf.bulk.Account.insert(records)

    def bulk_update(self, records: list[dict]) -> list[dict]:
        """取引先を一括更新する。

        Args:
            records: 更新するレコードのリスト。各要素に Id が必須。
                     例: [{"Id": "001...", "Phone": "03-0000-0000"}, ...]

        Returns:
            各レコードの処理結果（id, success, errors）のリスト
        """
        return self.sf.bulk.Account.update(records)

    def bulk_upsert(self, records: list[dict], external_id_field: str) -> list[dict]:
        """取引先を一括 upsert する。

        Args:
            records: upsert するレコードのリスト
            external_id_field: 外部 ID フィールドの API 参照名。例: "ExternalId__c"

        Returns:
            各レコードの処理結果（id, success, errors）のリスト
        """
        return self.sf.bulk.Account.upsert(records, external_id_field)

    def bulk_delete(self, account_ids: list[str]) -> list[dict]:
        """取引先を一括削除する。

        Args:
            account_ids: 削除対象の取引先 ID のリスト

        Returns:
            各レコードの処理結果（id, success, errors）のリスト
        """
        return self.sf.bulk.Account.delete([{"Id": i} for i in account_ids])
