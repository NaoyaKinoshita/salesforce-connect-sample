from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Task(BaseModel):
    """行動（タスク）レコード。取得・作成・更新で共用する。

    - 取得時: Id・Subject 等が設定される
    - 作成時: Id を除いて渡す（repository 側で除外）
    - 更新時: Id を含め、変更フィールドのみ渡す
    - extra="allow" により、モデルに定義していないフィールドも扱うことができる
    """

    model_config = ConfigDict(extra="allow")

    Id: Optional[str] = Field(default=None, description="行動 ID")
    WhatId: Optional[str] = Field(
        default=None, description="関連レコード ID（取引先など）"
    )
    Subject: Optional[str] = Field(default=None, description="件名", examples=["電話"])
    Status: Optional[str] = Field(
        default=None, description="状況", examples=["未着手", "進行中", "完了"]
    )
    Priority: Optional[str] = Field(
        default=None, description="優先度", examples=["高", "中", "低"]
    )
    ActivityDate: Optional[str] = Field(
        default=None, description="期日（YYYY-MM-DD）", examples=["2025-12-31"]
    )
    TaskSubtype: Optional[str] = Field(
        default=None, description="タスク種別", examples=["Call"]
    )
    Description: Optional[str] = Field(default=None, description="説明")
    OwnerId: Optional[str] = Field(default=None, description="所有者 ID")
