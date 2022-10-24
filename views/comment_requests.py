import json
import sqlite3
from models import Comment


def get_comments_by_post_id(post_id):
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
       SELECT
            c.id,
            c.post_id,
            c.author_id,
            c.content
        FROM Comments c
        WHERE c.post_id = ?
        """, (post_id, ))

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            comment = Comment(row['id'], row['post_id'],
                              row['author_id'], row['content'])

            comments.append(comment.__dict__)

    return comments


def create_comment(new_comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( post_id, author_id, content )
        VALUES
            ( ?, ?, ? );
        """, (new_comment['post_id'], new_comment['author_id'], new_comment['content']))

        id = db_cursor.lastrowid

        # Add the `id` property to the tag dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment['id'] = id

    return json.dumps(new_comment)
