from app import app, DBConnection
from flask import jsonify
from flask import request
from datetime import datetime
import math
ROWS_PER_PAGE = 400
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

@app.route("/")
def index():
    return "<h1>Hello World!</h1>"


#i.e. http://localhost:8080/orders?order_purchase_timestamp_start=2018-01-10&order_purchase_timestamp_end=2018-10-10
@app.route('/orders', methods=["GET"])
def orders():
    date_start = request.args.get('order_purchase_timestamp_start')  # inclusive
    date_end = request.args.get('order_purchase_timestamp_end')  # exclusive
    date_format = '"%%Y-%%m-%%d"'
    sql_query = f'''
    SELECT * FROM orders WHERE  
        DATE_FORMAT(order_purchase_timestamp, {date_format}) >= DATE_FORMAT("{date_start}", {date_format}) 
        AND DATE_FORMAT(order_purchase_timestamp, {date_format}) < DATE_FORMAT("{date_end}", {date_format});'''
    res = db.query(sql_query)
    return res


@app.route('/products', methods=["GET"])
def customers():
    res = db.query("SELECT * FROM products")
    return res


@app.route('/sellers', methods=["GET"])
def sellers():
    page = request.args.get('page')
    page = 0 if not page else int(page)
    offset = page * ROWS_PER_PAGE
    print(f"Offset for the query {offset}")
    TOTAL_ROWS = 3095
    total_pages = TOTAL_ROWS // ROWS_PER_PAGE
    metadata = {"total_pages": total_pages, "current_page": page, "next_page": f"{None if page+1 >= total_pages else page+1}"}

    res = db.query(f"SELECT * FROM sellers LIMIT {offset}, {ROWS_PER_PAGE}", metadata)  # OFFSET by x, LIMIT 400 records per query result
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









