import snowflake.connector as sf
import json

conn = sf.connect(
    user="test",
    password="test",
    account="test",
    database="test",
    host="snowflake.localhost.localstack.cloud",
    schema="MYSCHEMA",
    auto_commit=False
)

cursor = conn.cursor()

cursor.execute("""
SELECT
    LOWER(REGEXP_REPLACE(COL1, 'PREFIX_', '')) AS COL1,
FROM
    MYSCHEMA.MYTABLE;
""")

conn.rollback()
conn.close()

print("Done")