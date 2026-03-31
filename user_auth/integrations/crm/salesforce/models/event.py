from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Event(BaseModel):
    """行動（イベント）レコード。取得・作成・更新で共用する。

    - 取得時: Id・Subject 等が設定される
    - 作成時: Id を除いて渡す（repository 側で除外）
    - 更新時: Id を含め、変更フィールドのみ渡す
    - extra="allow" により、モデルに定義していないフィールドも扱うことができる
    """

    model_config = ConfigDict(extra="allow")

    Id: Optional[str] = Field(default=None, description="行動 ID")
    WhatId: Optional[str] = Field(default=None, description="関連レコード ID（取引先など）")
    WhoId: Optional[str] = Field(default=None, description="関連する取引先責任者・リード ID")
    Subject: Optional[str] = Field(default=None, description="件名", examples=["打ち合わせ"])
    StartDateTime: Optional[str] = Field(
        default=None,
        description="開始日時（ISO 8601形式）",
        examples=["2025-12-31T10:00:00.000+0900"],
    )
    EndDateTime: Optional[str] = Field(
        default=None,
        description="終了日時（ISO 8601形式）",
        examples=["2025-12-31T11:00:00.000+0900"],
    )
    IsAllDayEvent: Optional[bool] = Field(default=None, description="終日イベントかどうか")
    Location: Optional[str] = Field(
        default=None, description="場所", examples=["会議室A"]
    )
    Description: Optional[str] = Field(default=None, description="説明")
    OwnerId: Optional[str] = Field(default=None, description="所有者 ID")
