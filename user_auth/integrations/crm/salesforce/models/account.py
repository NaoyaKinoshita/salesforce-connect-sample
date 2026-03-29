from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Account(BaseModel):
    """取引先レコード。取得・作成・更新で共用する。

    - 取得時: Id・Name が設定される
    - 作成時: Id を除いて渡す（repository 側で除外）
    - 更新時: Id と変更フィールドのみ渡す
    - extra="allow" により、modelに定義していないフィールドも扱うことができる
    """

    model_config = ConfigDict(extra="allow")

    Id: Optional[str] = Field(default=None, description="取引先ID")
    Name: Optional[str] = Field(default=None, description="取引先名")
    Phone: Optional[str] = Field(
        default=None, description="電話番号", examples=["03-1234-5678"]
    )
    BillingCity: Optional[str] = Field(
        default=None, description="請求先市区町村", examples=["渋谷区"]
    )
    BillingState: Optional[str] = Field(
        default=None, description="請求先都道府県", examples=["東京都"]
    )
