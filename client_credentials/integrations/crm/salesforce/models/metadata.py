from typing import Optional

from pydantic import BaseModel, Field


class PicklistValue(BaseModel):
    value: str = Field(description="選択リスト値")
    label: str = Field(description="表示ラベル")
    active: bool = Field(description="有効フラグ")
    default_value: bool = Field(alias="defaultValue", description="デフォルト値フラグ")
    valid_for: Optional[str] = Field(
        alias="validFor",
        default=None,
        description="連動選択用ビットマスク（Base64）",
    )


class FieldMetadata(BaseModel):
    name: str = Field(description="API 参照名")
    label: str = Field(description="表示ラベル")
    type: str = Field(description="フィールド型")
    controller_name: Optional[str] = Field(
        alias="controllerName",
        default=None,
        description="連動選択の親フィールド API 参照名",
    )
    picklist_values: list[PicklistValue] = Field(
        alias="picklistValues",
        default_factory=list,
        description="選択リスト値（picklist / multipicklist）",
    )


class SObjectMetadata(BaseModel):
    name: str = Field(description="API 参照名")
    label: str = Field(description="表示ラベル")
    fields: list[FieldMetadata] = Field(
        default_factory=list, description="フィールド定義一覧"
    )
