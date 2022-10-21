from cProfile import label
import sqlite3
from models.post import Post
from models.user import User
from models.category import Category
import json


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

def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            p.*,
            c.*
        FROM Posts p
        JOIN Categories c 
        ON c.id = p.category_id
        WHERE p.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['image_url'], data['content'])

        category = Category(data['id'], data['label'])

        post.category = category.__dict__

        return post.__dict__

#def update_post(id, updated_post):
    #add code here for update





def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content )
        VALUES
            ( ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], ))

        id = db_cursor.lastrowid

        new_post['id'] = id

    return json.dumps(new_post)


def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
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
        WHERE p.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                    data['publication_date'], data['image_url'], data['content'])

        user = User(data['user_id'], data['user_first'], data['user_last'], data['user_email'], data['user_bio'],
                    data['user_username'], data['user_password'], data['user_img'], data['user_created'], data['user_active'])

        category = Category(data['category_id'], data['category_name'])

        post.user = user.__dict__
        post.category = category.__dict__

        return post.__dict__
