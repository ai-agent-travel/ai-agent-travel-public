from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator

class Message(BaseModel):
    role: str
    content: str
    selector: List[str] = Field(default_factory=list, description="あなたの質問に対する回答選択肢を入力してください。")

    @validator("selector", pre=True, always=True)
    def default_selector(cls, v):
        return v or []

class Messages(BaseModel):
    message: Message = Field(..., description="ヒアリング用メッセージ 必ずメッセージを入力してください。")
    is_done: bool = Field(default=False, description="ヒアリング終了フラグ")

