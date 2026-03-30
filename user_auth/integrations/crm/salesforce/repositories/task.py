from integrations.crm.salesforce.client import SalesforceClient
from integrations.crm.salesforce.models.metadata import SObjectMetadata
from integrations.crm.salesforce.models.task import Task
from common.utils import escape_soql


class TaskRepository(SalesforceClient):
    sobject_name = "Task"

    def describe(self) -> SObjectMetadata:
        """Task SObject のメタデータを取得する。"""
        return super().describe(self.sobject_name)

    def describe_specified_fields(self, field_names: list[str]) -> SObjectMetadata:
        """Task SObject の特定フィールドのメタデータを取得する。"""
        return super().describe_specified_fields(self.sobject_name, field_names)

    def find_by_account(self, account_id: str, limit: int = 100) -> list[Task]:
        """取引先に紐づく行動を一覧取得する。"""
        safe_id = escape_soql(account_id)
        query = (
            f"SELECT Id, WhatId, Subject, Status, Priority, ActivityDate, Description "
            f"FROM Task WHERE WhatId = '{safe_id}' LIMIT {limit}"
        )
        result = self.sf.query(query)
        return [Task.model_validate(r) for r in result["records"]]

    def find_by_id(self, task_id: str) -> Task:
        """ID で行動を1件取得する。"""
        return Task.model_validate(self.sf.Task.get(task_id))

    def create(self, data: Task) -> str:
        """行動を新規作成し、作成された ID を返す。

        Args:
            data: 作成するフィールドの値

        Returns:
            作成された行動の ID
        """
        result = self.sf.Task.create(data.model_dump(exclude_none=True, exclude={"Id"}))
        if not result.get("id"):
            raise RuntimeError(f"行動の作成に失敗しました: {result}")
        return result["id"]

    def update(self, data: Task) -> None:
        """行動を更新する。

        Args:
            data: 更新するフィールドの値（Id を含めること）

        Raises:
            ValueError: Id が指定されていない場合
        """
        if not data.Id:
            raise ValueError("update には Id が必要です")
        self.sf.Task.update(data.Id, data.model_dump(exclude_none=True, exclude={"Id"}))

    def delete(self, task_id: str) -> None:
        """行動を削除する。

        Args:
            task_id: 削除対象の行動 ID
        """
        self.sf.Task.delete(task_id)
