import sqlite3

from models.tag import Tag

def get_all_tags():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM tags t
        ORDER BY label
        """)

        # Initialize an empty list to hold all metal representations
        tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an metal instance from the current row.
            # Note that the database fields are specified in
            # exact metal of the parameters defined in the
            # metal class above.
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    return tags