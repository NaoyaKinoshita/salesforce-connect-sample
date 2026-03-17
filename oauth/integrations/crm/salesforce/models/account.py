from pydantic import BaseModel, ConfigDict


class Account(BaseModel):
    """取引先レコード。取得・作成・更新で共用する。

    - 取得時: Id・Name が設定される
    - 作成時: Id を除いて渡す（repository 側で除外）
    - 更新時: Id を除いて変更フィールドのみ渡す
    - extra="allow" により CompanyCode__c 等のカスタムフィールドも扱える
    """

    model_config = ConfigDict(extra="allow")

    Id: str | None = None
    Name: str | None = None
    Phone: str | None = None
    BillingCity: str | None = None
    BillingState: str | None = None


class BulkResult(BaseModel):
    """Bulk API の処理結果"""

    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    success: bool
    errors: list = []
