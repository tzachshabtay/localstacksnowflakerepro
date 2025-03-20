import snowflake.connector as sf

with open('/tmp/myfile.csv', 'w') as f:
    f.write('ID,NAME\n')
    f.write('1,20210101\n')

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

cursor.execute("PUT file:///tmp/myfile.csv @MYSCHEMA.MYSTAGE/path/to/stage")

cursor.execute("""
MERGE INTO MYSCHEMA.MYTABLE AS TARGET
USING (
    SELECT
        $1 AS ID,
        $2 AS NAME
    FROM @MYSCHEMA.MYSTAGE/path/to/stage
    (FILE_FORMAT => MYSCHEMA.MYFORMAT)
) AS NEW_ROWS
ON TARGET.ID = NEW_ROWS.ID
WHEN NOT MATCHED THEN
    INSERT (ID, NAME)
    VALUES (NEW_ROWS.ID, NEW_ROWS.NAME)
""")

conn.rollback()
conn.close()

print("Done")