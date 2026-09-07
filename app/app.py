from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "appuser"),
        password=os.getenv("MYSQL_PASSWORD", "apppassword"),
        database=os.getenv("MYSQL_DATABASE", "devopsdb")
    )


@app.route("/")
def home():
    return jsonify({
        "application": "DevOps 2-Tier Application",
        "status": "running",
        "version": "1.1"
    })


@app.route("/health")
def health():
    try:
        connection = get_db_connection()
        connection.close()

        return jsonify({
            "status": "healthy",
            "database": "connected",
            "service": "Flask + MySQL"
        }), 200

    except Exception as error:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
