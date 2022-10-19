import sqlite3
from models.post import Post


def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content
        FROM Posts p
        ORDER BY publication_date DESC
        """)

        posts = []

        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'])

            # Add the dictionary representation of the animal to the list
            posts.append(post.__dict__)

        return posts
