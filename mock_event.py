import requests
import json

# The URL of your local API
url = "http://127.0.0.1:8000/webhook"

# ---------------------------------------------------------
# SIMULATION: TURN 2
# The user is replying "Gaming" to the bot's previous question.
# ---------------------------------------------------------
payload = {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "123456789",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15555555555",
              "phone_number_id": "123456123"
            },
            "contacts": [{"profile": {"name": "Test User"}, "wa_id": "1234567890"}],
            "messages": [
              {
                "from": "201000000000",  # SAME USER ID (Critical for Memory)
                "id": "wamid.HBgLMTIzNDU2Nzg5MA==",
                "timestamp": "1673000000",
                "text": {
                  "body": "Gaming"  # <--- UPDATED MESSAGE
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}

# Send the request
try:
    print(f"📤 Sending User Reply: 'Gaming'...")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Connection Failed: {e}")