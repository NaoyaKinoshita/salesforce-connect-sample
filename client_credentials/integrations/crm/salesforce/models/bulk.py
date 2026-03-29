from typing import Optional

from pydantic import BaseModel, Field


class BulkResult(BaseModel):
    """Bulk API の処理結果"""

    id: Optional[str] = Field(default=None, description="レコード ID")
    success: bool = Field(description="処理成否")
    errors: list[dict] = Field(default_factory=list, description="エラー詳細")
