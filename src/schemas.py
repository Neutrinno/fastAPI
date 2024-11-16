from decimal import Decimal
import enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CategoriesEnum(str, enum.Enum):
    Income = "Доходы"
    Food = "Расходы на еду"
    Utilities = "Коммунальные платежи"
    Transportation = "Транспорт"
    Housing = "Жилье"
    Health = "Здоровье"
    Education = "Образование"
    Entertainment = "Развлечения и отдых"
    Clothing = "Одежда"
    Savings = "Сбережения и инвестиции"
    Miscellaneous = "Прочие расходы"

class TransactionsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    date: datetime
    amount: Decimal = Field(gt=0)
    category: CategoriesEnum = Field(default=CategoriesEnum.Miscellaneous)
    description: Optional[str] = None

class TransactionsCreate(TransactionsBase):
    pass

class TransactionsRead(TransactionsBase):
    id: int = Field(gt=0)