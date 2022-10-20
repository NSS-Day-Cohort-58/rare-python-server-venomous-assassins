import sqlite3
from models.post import Post
from models.user import User
from models.category import Category


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
            p.content,
            u.id user_id,
            u.first_name user_first,
            u.last_name user_last,
            u.email user_email,
            u.bio user_bio,
            u.username user_username,
            u.password user_password,
            u.profile_image_url user_img,
            u.created_on user_created,
            u.active user_active,
            c.id category_id,
            c.label category_name
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        ORDER BY publication_date DESC
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'])

            user = User(row['user_id'], row['user_first'], row['user_last'], row['user_email'], row['user_bio'],
                        row['user_username'], row['user_password'], row['user_img'], row['user_created'], row['user_active'])

            category = Category(row['category_id'], row['category_name'])

            post.user = user.__dict__
            post.category = category.__dict__
            posts.append(post.__dict__)

        return posts
