"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from collections import defaultdict

from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    r = get_redis_conn()
    order_ids = r.lrange("orders", 0, limit - 1)
    print(limit)

    orders = []
    order_ids = r.zrevrange("orders", 0, limit - 1)

    return [
            r.hgetall(f"order:{order_id}")
            for order_id in order_ids
        ]  


def get_highest_spending_users():
    """Get report of highest spending users"""
    r = get_redis_conn()
    keys = r.keys("order:*")
    orders = []

    for key in keys:
        # Skip item hashes
        if ":item:" in key:
            continue
        data = r.hgetall(key)
        if not data:
            continue
        orders.append(data)

    expenses_by_user = defaultdict(float)

    for order in orders:
        expenses_by_user[int(order['user_id'])] += float(order['total_amount'])

    highest_spending_users = sorted(
        expenses_by_user.items(),
        key=lambda item: item[1],
        reverse=True
    )
    result = []

    for user_id, total in highest_spending_users[:10]:
        result.append(
            f"<li>{user_id}: {total:.2f}$</li>"
        )

    return "".join(result)



def get_best_sellers():
    """Get report of best selling products"""

    r = get_redis_conn()

    keys = r.keys("product:*:sold")

    quantities_by_product = {}

    for key in keys:
        value = r.get(key)

        if value is None:
            continue

        product_id = int(key.split(":")[1])
        quantities_by_product[product_id] = int(value)

    best_sellers = sorted(
        quantities_by_product.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return "".join(
        f"<li>Produit {pid}: {qty} vendu(s)</li>"
        for pid, qty in best_sellers[:10]
    )