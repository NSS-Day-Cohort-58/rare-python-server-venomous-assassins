import sqlite3
import json

from models import Subscription

def get_all_subscriptions():
    """gets all subscriptions"""
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM Subscriptions s
        """)

        subscriptions = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            sub = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])

            subscriptions.append(sub.__dict__)

    return subscriptions

def create_subscription(new_sub):
    """creates new subscription in subscriptions table"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( follower_id, author_id, created_on )
        VALUES
            ( ?, ?, ?);
        """, (new_sub['follower_id'], new_sub['author_id'], new_sub['created_on'], ))

        id = db_cursor.lastrowid

        new_sub['id'] = id

    return json.dumps(new_sub)


def delete_subscription(id):
    """deletes a subscription"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Subscriptions
        WHERE id = ?
        """, (id, ))