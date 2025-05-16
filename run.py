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

source_data = [
    {"COL1": "A", "COL2": "2023-01-01", "COL3": "X"},
]

cursor.execute("""
WITH Source AS (
    SELECT
        VALUE:COL1::STRING AS COL1,
        VALUE:COL2::DATE AS COL2,
        VALUE:COL3::STRING AS COL3
    FROM TABLE(FLATTEN(INPUT => PARSE_JSON(%s)))
)
SELECT
    COALESCE(cm.COL1, '') AS COL1,
    COALESCE(TO_CHAR(cm.COL2, 'YYYYMMDD')::INT, 0) AS COL2,
    COALESCE(cm.COL3, '') AS COL3
FROM
    Source cm
LEFT JOIN MYSCHEMA.MYTABLE pm
    ON cm.COL1 = pm.COL1
    AND cm.COL2 = pm.COL2
    AND cm.COL3 = pm.COL3
LEFT JOIN MYSCHEMA.MYTABLE2 mc
    ON cm.COL1 = mc.COL1
    AND cm.COL2 = mc.COL2
    AND cm.COL3 = mc.COL3
GROUP BY
    cm.COL1,
    cm.COL2,
    cm.COL3
HAVING
    COUNT(pm.COL4) = 10
    AND COUNT(mc.COL4) = 0;
""", (json.dumps(source_data),))

conn.rollback()
conn.close()

print("Done")