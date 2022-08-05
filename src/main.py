from app import app, DBConnection
from flask import jsonify
from flask import request
from datetime import datetime
import math
from pagination import Pagination
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

ROWS_PER_PAGE = 400
TOTAL_ROWS = 3095
TABLE_INFO = {
    "sellers": {"ROWS_PER_PAGE": 400, "TOTAL_ROWS": 3095},
    "orders": {"ROWS_PER_PAGE": 2000, "TOTAL_ROWS": 99441}
}

@app.route("/")
def index():
    return "<h1>Hello World!</h1>"


#i.e. http://localhost:8080/orders?order_purchase_timestamp_start=2018-01-10&order_purchase_timestamp_end=2018-10-10
@app.route('/orders', methods=["GET"])
def orders():
    ROWS_PER_PAGE = 2000
    TOTAL_ROWS = 99441
    total_pages = TOTAL_ROWS // ROWS_PER_PAGE
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

# i.e. http://localhost:8080/sellers?page=0
@app.route('/sellers', methods=["GET"])
def sellers():
    table_info = TABLE_INFO["sellers"]

    page_number = request.args.get('page')
    page_number = 1 if not page_number else int(page_number)  # Return page 1 by default

    try:
        p = Pagination(rows=table_info["TOTAL_ROWS"], per_page=table_info["ROWS_PER_PAGE"], current_page=page_number)
        print(f"Offset for the query {p.row_offset}")
        response = db.query(f"SELECT * FROM sellers LIMIT {p.row_offset}, {p.rows_per_page}", p.get_metadata())

    except ValueError as e:
        response = {"message": f"{e}"}
        response = jsonify(response)
        response.status_code = 500

    return response


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









