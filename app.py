from flask import Flask, request, jsonify
from email_svc import send_email

app = Flask(__name__)


@app.route('/send-email', methods=['POST'])
def send_email_service():
    data = request.get_json()

    required_fields = ['email', 'message']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            'error': f'Missing required fields: {missing_fields}'
        }), 400

    email = data['email']
    message = data['message']

    try:
        send_email(email, "Notification", message)
        return jsonify({
            'status': 'success',
            'message': f'Email successfully sent to {email}'
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'status': 'failure',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
