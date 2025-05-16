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
with source1 as (select COL1 from MYSCHEMA.MYTABLE),
source2 as (select COL1 from MYSCHEMA.MYTABLE2)
select * from source1 full outer join source2 on source1.COL1 = source2.COL1
               order by source1.COL1 limit 5;
""")

conn.rollback()
conn.close()

print("Done")