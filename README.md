```markdown
# Email Notification Microservice

This microservice sends emails and logs activity in a SQLite database.

## Requirements

- Python 3.8 or higher
- The following Python packages:
  - `flask`
  - `requests`
  - `python-dotenv`

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install flask requests python-dotenv
   ```

3. Create a `.env` file in the root of the project to store your environment variables:
   ```plaintext
   SMTP_USER=your_email@example.com
   SMTP_PASSWORD=your_smtp_password
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   ```

4. Ensure the SQLite database `email_logs.db` exists. If not, create it using the schema provided in the repository:
   ```sql
   CREATE TABLE email_logs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       timestamp TEXT NOT NULL,
       recipient TEXT NOT NULL,
       status TEXT NOT NULL,
       message TEXT,
       error TEXT
   );
   ```

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
 {
     "email": "recipient@example.com",
     "message": "This is a test email."
 }

# Example Success Response
 {
     "status": "success",
     "message": "Email successfully sent to recipient@example.com"
 }

# Example Error Response
 {
     "status": "failure",
     "error": "Missing required fields: ['email']"
 }
```
## UML Sequence Graph

                       ┌─┐                                                                                    ,.-^^-._              
                       ║"│                                                                                   |-.____.-|             
                       └┬┘                                                                                   |        |             
                       ┌┼┐                                                                                   |        |             
                        │              ┌───────────────────────────────┐          ┌───────────┐              |        |             
                       ┌┴┐             │Email Notification Microservice│          │SMTP Server│              '-.____.-'             
                     Client            └───────────────┬───────────────┘          └─────┬─────┘           SQLite Database           
                        │      POST /send-email        │                                │                        │                  
                        │─────────────────────────────>│                                │                        │                  
                        │                              │                                │                        │                  
                        │                              │────┐                           │                        │                  
                        │                              │    │ Validate Request          │                        │                  
                        │                              │<───┘                           │                        │                  
                        │                              │                                │                        │                  
                        │                              │                                │                        │                  
          ╔══════╤══════╪══════════════════════════════╪════════════════════════════════╪════════════════════════╪═════════════════╗
          ║ ALT  │  Valid Request                      │                                │                        │                 ║
          ╟──────┘      │                              │                                │                        │                 ║
          ║             │                              │          Send Email            │                        │                 ║
          ║             │                              │───────────────────────────────>│                        │                 ║
          ║             │                              │                                │                        │                 ║
          ║             │                              │        Acknowledgement         │                        │                 ║
          ║             │                              │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                        │                 ║
          ║             │                              │                                │                        │                 ║
          ║             │                              │                   Log Email Activity                    │                 ║
          ║             │                              │────────────────────────────────────────────────────────>│                 ║
          ╠═════════════╪══════════════════════════════╪════════════════════════════════╪════════════════════════╪═════════════════╣
          ║ [Invalid Request]                          │                                │                        │                 ║
          ║             │       400 Bad Request        │                                │                        │                 ║
          ║             │<─────────────────────────────│                                │                        │                 ║
          ╚═════════════╪══════════════════════════════╪════════════════════════════════╪════════════════════════╪═════════════════╝
                        │                              │                                │                        │                  
                        │    Response (200 or 500)     │                                │                        │                  
                        │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                                │                        │                  
                     Client            ┌───────────────┴───────────────┐          ┌─────┴─────┐           SQLite Database           
                       ┌─┐             │Email Notification Microservice│          │SMTP Server│               ,.-^^-._              
                       ║"│             └───────────────────────────────┘          └───────────┘              |-.____.-|             
                       └┬┘                                                                                   |        |             
                       ┌┼┐                                                                                   |        |             
                        │                                                                                    |        |             
                       ┌┴┐                                                                                   '-.____.-'             
