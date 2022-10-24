
import json
import sqlite3

from models.postTag import PostTag
from models.tag import Tag


def get_all_post_tags(query_params): ##might not need this function but leaving here just in case
    with sqlite3.connect("./db.sqlite3") as conn: 

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        where_clause = ""

        if len(query_params) != 0: #query param found in url
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

            if qs_key == "post_id":
                where_clause = f"WHERE pt.post_id = {qs_value}"



        db_cursor.execute(f"""
        SELECT 
            pt.*,
            t.label
        FROM PostTags pt
        JOIN Tags t
        ON t.id = pt.tag_id
        {where_clause}
        """)

        post_tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post_tag = PostTag(row["id"], row["post_id"], row["tag_id"])

            tag = Tag(row["tag_id"], row["label"])

            post_tag.tag = tag.__dict__

            post_tags.append(post_tag.__dict__)

    return post_tags



def create_post_tag(new_post_tag):
    with sqlite3.connect("./db.sqlite3") as conn: 

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostTags
            (post_id, tag_id)
        VALUES
            (?, ?);
        """, (new_post_tag["post_id"], new_post_tag["tag_id"], ))

        id = db_cursor.lastrowid

        new_post_tag["id"] = id

    return json.dumps(new_post_tag)
