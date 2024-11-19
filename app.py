from flask import Flask, request, jsonify
from email_svc import send_email
from email_logger import log_email_activity

app = Flask(__name__)


@app.route('/send-email', methods=['POST'])
def send_email_service():
    data = request.get_json()
    required_fields = ['email', 'message']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        error_message = f"Missing required fields: {missing_fields}"
        log_email_activity(data.get('email', 'N/A'), 'failure', error=error_message)
        return jsonify({'error': error_message}), 400

    email = data['email']
    message = data['message']

    if "@" not in email or "." not in email.split("@")[-1]:
        error_message = "Invalid email format"
        log_email_activity(email, 'failure', error=error_message)
        return jsonify({'error': error_message}), 400

    try:
        response = send_email(email, "Notification", message)
        if response["status"] == "error":
            log_email_activity(email, 'failure', message, response["message"])
            return jsonify(response), 500
        log_email_activity(email, 'success', message)
        return jsonify(response), 200
    except Exception as e:
        log_email_activity(email, 'failure', message, str(e))
        return jsonify({
            'status': 'failure',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
