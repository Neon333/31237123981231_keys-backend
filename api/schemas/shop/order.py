from pydantic import BaseModel


class OrderCreated(BaseModel):
    id: str
    payment_form_html: str
