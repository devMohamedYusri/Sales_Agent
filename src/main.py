from fastapi import FastAPI
from src.schemas import WhatsAppWebhook
from src.services.sales_brain import generate_response

app=FastAPI(
    title="AI Sales Agent",
    description="An AI-powered sales agent that assists with customer inquiries and sales processes.",
    version="0.1.0"
)

@app.get('/')
async def health_check():
    return {'status':"ok",
            'message':"AI Sales Agent is running"}

# Core message Receiver Endpoint
@app.post('/webhook')
async def receive_whatsapp_message(payload:WhatsAppWebhook):
    """
    Docstring for receive_whatsapp_message
    receives incoming WhatsApp messages via webhook
    display them for now
    :param payload: Description
    :type payload: WhatsAppWebhook
    """

    try:
        body=payload.entry[0].changes[0].value
        if body.messages:
            incoming_message=body.messages[0]
            if incoming_message.type =='text':
                message=incoming_message.text.body
                sender_id=incoming_message.from_

                # TODO: This is where we will send data to the AI sales agent for processing
                response = await generate_response(message=message, sender_id=sender_id)

                print(f"📤 SENDING BACK: {response}")
                return {"status":"processed",
                        "response":response}
            return {"status":"ignored",
                    "reason":"non-text message"}
        
    except Exception as e:
        print(f"Error processing message: {e}")
