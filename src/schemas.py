from pydantic import BaseModel,Field
from typing import List,Optional
# ---------------------------------------------------------
# WHATSAPP DATA MODELS
# These models represent the structure of incoming messages
# ---------------------------------------------------------

class TextMessage(BaseModel):
    body: str

class Message(BaseModel):
    from_:str =Field(...,alias='from')
    id:str
    timestamp:str
    text:Optional[TextMessage]=None
    type:str

class Value(BaseModel):
    messaging_product:str
    metadata:dict
    contacts:Optional[List[dict]]=None
    messages:Optional[list[Message]]=None

class Change(BaseModel):
    value:Value
    field:str

class Entry(BaseModel):
    id:str
    changes:List[Change]

class WhatsAppWebhook(BaseModel):
    object:str
    entry:List[Entry]

# ---------------------------------------------------------
# FACEBOOK DATA MODELS