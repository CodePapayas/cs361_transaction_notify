from flask import Flask, request, jsonify
from datetime import datetime
from email_svc import send_email

app = Flask(__name__)


@app.route('/', methods=['POST'])
def notify_transactions():
    data = request.get_json()

    required_fields = ['userId', 'transactionId', 'amount', 'contactInfo']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:

        if 'contactInfo' not in data:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}',
                'note': 'Unable to send notification email due to missing contactInfo'
            }), 400

        subject = "Transaction Notification Failed - Missing Information"
        body = f"""
        Hello,

        We were unable to process your recent transaction notification due to missing information.

        **Transaction Details Provided:**
        {data}

        **Missing Information:**
        {missing_fields}

        Please ensure all required fields are included in your next request.

        Thank you,
        Transaction Notification Service
        """
        if 'contactInfo' in data:
            send_email(data['contactInfo'], subject, body)

        return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400

    if not isinstance(data['amount'], (int, float)):
        return jsonify({'error': 'Invalid amount value. Value must be a number.'}), 400

    if data['amount'] > 0:
        data['category'] = 'Deposit'
    elif data['amount'] < 0:
        data['category'] = 'Expense'
    else:
        return jsonify({'error': 'Transaction amounts must be greater or less than 0.'}), 400

    data['receivedAt'] = datetime.now().astimezone().strftime("%B %d, %Y %I:%M %p %Z")

    subject = "Transaction Notification"
    body = f"""
    Hello,

    A {data['category'].lower()} has posted to your account. Please review the included details.

    Transaction Details:
    - User ID: {data['userId']}
    - Transaction ID: {data['transactionId']}
    - Amount: {data['amount']}
    - Category: {data['category']}
    - Received At: {data['receivedAt']}

    Thank you,
    Transaction Notification Service
    """
    send_email(data['contactInfo'], subject, body)

    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
