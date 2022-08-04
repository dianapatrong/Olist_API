from app import app, DBConnection
from flask import jsonify
from flask import request


@app.route("/")
def index():
    return "<h1>Hello World!</h1>"


@app.route('/orders')
def orders():
    res = db.query("SELECT * FROM orders LIMIT 1")
    return res


@app.route('/products')
def customers():
    res = db.query("SELECT * FROM products LIMIT 1")
    return res


@app.route('/sellers')
def sellers():
    res = db.query("SELECT * FROM sellers LIMIT 1")
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
    db = DBConnection()
    serve(app, host="0.0.0.0", port=8080)









