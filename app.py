from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['POST'])
def notify_transactions():
    data = request.get_json()

    required_fields = ['userId',
                       'transactionId',
                       'amount',
                       'contactInfo'
                       ]
    if not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400

    if not isinstance(data['amount'], (int, float)):
        return jsonify({'error': 'Invalid amount value. Value must be a number.'}), 400

    if data['amount'] > 0:
        data['category'] = 'Deposit'
    elif data['amount'] < 0:
        data['category'] = 'Expense'
    else:
        return jsonify({'error': 'Transaction amounts must be greater or less than 0.'})

    data['receivedAt'] = datetime.now().astimezone().isoformat()

    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
