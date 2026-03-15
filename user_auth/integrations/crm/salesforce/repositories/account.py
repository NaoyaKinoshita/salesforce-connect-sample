from integrations.crm.salesforce.client import SalesforceClient


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
        safe_name = name.replace("'", "\\'")
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
