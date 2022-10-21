import sqlite3
from models.category import Category
import json


def get_all_categories(query_params):
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""

        if len(query_params) != 0: #query param found in url
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

            if qs_key == "_sortBy":
                if qs_value == "label":
                    sort_by = "ORDER BY c.label"

        db_cursor.execute(f"""
        SELECT 
            c.*
        FROM Categories c
        {sort_by}
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset: 
            category = Category(row["id"], row["label"])

            categories.append(category.__dict__)

    return categories


def create_category(new_category):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            ( label )
        VALUES
            ( ? );
        """, (new_category['label'],))

        id = db_cursor.lastrowid

        new_category['id'] = id

    return json.dumps(new_category)