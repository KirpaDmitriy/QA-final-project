from flask import Flask, json

app = Flask(__name__)


@app.route('/vk_id/<user>', methods=['GET'])
def refresh(user):
    return json.dumps({"vk_id": "123456"}), 200


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
