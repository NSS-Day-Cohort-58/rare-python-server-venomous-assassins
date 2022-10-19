import sqlite3
from models.category import Category


def get_all_categories(key, value):
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""

        if key == "_sortBy":
            if value == "label":
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