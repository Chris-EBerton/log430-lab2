"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param
from queries.read_order import get_highest_spending_users, get_best_sellers

def show_highest_spending_users():
    """ Show report of highest spending users """
    users_html = get_highest_spending_users()

    return get_template(f"""
            <h2>Les plus gros acheteurs</h2>
            <ul>
                {users_html}
            </ul>
        """)
def show_best_sellers():
    """ Show report of best selling products """

    sellers_html = get_best_sellers()

    return get_template(f"""
        <h2>Les articles les plus vendus</h2>
        <ul>
            {sellers_html}
        </ul>
    """)