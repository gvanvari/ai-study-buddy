from .storage import sql
SCHEMA = """
CREATE TABLE IF NOT EXISTS TOPICS(
    id TEXT PRIMARY KEY,
    domain TEXT CHECK(domain IN ('appsec','dsa','sysdesign')) NOT NULL,
    name TEXT NOT NULL,
    prereq_ids TEXT_DEFAULT '',
    ease REAL DEFAULT 2.5,
    interval INTEGER DEFAULT 0,
    reps INTEGER DEFAULT 0,
    next_review DATETIME DEFAULT CURRENT_TIMESTAMP,
    difficulty INTEGER DEFAULT 2,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
);
"""

SEED_TOPICS = [
    ("appsec.jwt.aud-claim","appsec","JWT Aud Claim", "", 2),
    ("dsa.twoptr.167-two-sum-ii", "dsa", "Two Sum II (two pointers)", "",1),
    ("sd.consitent-hashing", "sysdesign", "Consistent hashing basics", "",2),
]

def init_db():
    con = sql()
    con.executescript(SCHEMA)

    cur = con.execute("SELECT COUNT(*) FROM TOPICS;")
    if cur.fetchone()[0] == 0:
        con.executeany(
            "INSERT INTO TOPICS (id, domain, name, prereq_ids, difficulty) VALUES (?,?,?,?,?);",
            SEED_TOPICS ,
        )
    con.commit()
    con.close()

def list_topics():
    con = sql()
    rows = con.execute("SELECT * from topics ORDER BY domain, name;").fetchall()
    con.close()
    return [dict(r) for r in rows]