from typing import Optional, List

from pydantic import StringConstraints, ConfigDict, BaseModel, EmailStr, validator
from datetime import datetime
from typing_extensions import Annotated
from .models import Invoice

# pydantic update from v1 to v2 where orm_mode changed to from_attributes
class UserOutput(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Postuser(UserOutput):
    email: EmailStr
    


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

# changed datatype to int
class DataToken(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    content: Annotated[str, StringConstraints(max_length=1000)]
    published: bool = True
    created_at: datetime


class CreateInvoice(BaseModel):
    order_number: str
    title: str
    cost_per_page: float
    pages_done: int
    total_amount_per_job: float
    total_amount_for_all_jobs: float
    paid_amount: float
    advance_amount: float
    remaining: float
    due_date: datetime
    job_status: bool
    order_status: bool


class InvoiceResponse(BaseModel):
    id: int
    order_number: str
    title: str
    cost_per_page: float
    pages_done: int
    total_amount_per_job: float
    total_amount_for_all_jobs: float
    paid_amount: float
    advance_amount: float
    remaining: float
    due_date: datetime
    job_status: bool
    order_status: bool
