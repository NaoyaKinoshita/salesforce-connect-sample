from pydantic import BaseModel, Field


class PicklistValue(BaseModel):
    value: str = Field(description="選択リスト値")
    label: str = Field(description="表示ラベル")
    active: bool = Field(description="有効フラグ")
    default_value: bool = Field(alias="defaultValue", description="デフォルト値フラグ")


class FieldMetadata(BaseModel):
    name: str = Field(description="API 参照名")
    label: str = Field(description="表示ラベル")
    type: str = Field(description="フィールド型")
    picklist_values: list[PicklistValue] = Field(
        alias="picklistValues",
        default_factory=list,
        description="選択リスト値（picklist のみ）",
    )


class SObjectMetadata(BaseModel):
    name: str = Field(description="API 参照名")
    label: str = Field(description="表示ラベル")
    fields: list[FieldMetadata] = Field(
        default_factory=list, description="フィールド定義一覧"
    )
