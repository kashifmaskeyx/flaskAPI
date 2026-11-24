# errors.py
# Error handling
from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        response = {"error": error.name, "message": error.description}
        return jsonify(response), error.code