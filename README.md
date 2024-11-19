# Email Notification Microservice

This microservice sends emails and logs activity in a SQLite database.

## Communications Contract

**Endpoint:** `/send-email`  
**Method:** `POST`  
**Content-Type:** `application/json`  

Request fields:  
- `email` (string, required): Recipient's email address.  
- `message` (string, required): Email content.  

Response fields:  
- `status` (string): `success` or `failure`.  
- `message` (string): Details of the result.  
- `error` (string, optional): Error details if the email failed to send.  

Error Codes:  
- `400`: Missing required fields.  
- `500`: Internal server error.  

## Programmatically Request and Receive Data

Send a `POST` request with a JSON payload to the `/send-email` endpoint.

```python
# Example Request
import requests

url = "http://127.0.0.1:5000/send-email"
payload = {
    "email": "recipient@example.com",
    "message": "This is a test email."
}
response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"Status: {data['status']}")
    print(f"Message: {data['message']}")
else:
    error = response.json()
    print(f"Error: {error['error']}")

# Example Request Payload
# {
#     "email": "recipient@example.com",
#     "message": "This is a test email."
# }

# Example Success Response
# {
#     "status": "success",
#     "message": "Email successfully sent to recipient@example.com"
# }

# Example Error Response
# {
#     "status": "failure",
#     "error": "Missing required fields: ['email']"
# }
