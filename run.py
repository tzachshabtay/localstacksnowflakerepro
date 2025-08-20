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
with source1 as (
    select
        COL1,
        COL2,
        COL3
    from
        MYSCHEMA.MYTABLE
    where
        COL2 = '2023-01-01'
    ),
source2 as (
    select
        record_content:col1 AS COL1,
        record_content:col2 AS COL2,
        record_content:col3 AS COL3
    from
        MYSCHEMA.MYTABLE2
    where
        CAST(record_content:col2 AS DECIMAL(38, 0)) = 20230101
)
select
    COALESCE(s.COL1, d.COL1) as id,
    s.COL3 AS source_col,
    d.COL3 as dest_col
from
    source1 as s
full outer join
    source2 as d
on
    s.COL1 = d.COL1
where
    s.COL1 IS DISTINCT FROM d.COL1 OR
    s.COL3 IS DISTINCT FROM d.COL3
               limit 100;
""")

conn.rollback()
conn.close()

print("Done")