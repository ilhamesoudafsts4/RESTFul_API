import psycopg2
from datetime import datetime

def get_comments_from_db(subfeddit, limit=25):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="mysecretpassword"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.text, c.created_at
    FROM comment c
    JOIN subfeddit s ON c.subfeddit_id = s.id
    WHERE s.title = %s
    ORDER BY c.created_at DESC
    LIMIT %s
    """, (subfeddit, limit))

    rows = cur.fetchall()
    comments = []
    for row in rows:
        comment_id, text, created_at = row
        # convert created_at to datetime if int
        if isinstance(created_at, int):
            created_at = datetime.fromtimestamp(created_at)

        comments.append({
            "id": comment_id,
            "text": text,
            "created_at": created_at
        })

    cur.close()
    conn.close()
    return comments
