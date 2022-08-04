from app import app, DBConnection
from flask import jsonify
from flask import request


@app.route("/")
def index():
    return "<h1>Hello World!</h1>"


@app.route('/sellers')
def sellers():
    db = DBConnection()
    res = db.query("SELECT * FROM sellers_dataset LIMIT 1")

    return res


@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "message": f"Endpoint {request.url} not found",
    }
    res = jsonify(message)
    res.status_code = 404

    return res


# 7:30 PM -9:00
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)









