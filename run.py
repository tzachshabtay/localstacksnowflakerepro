import snowflake.connector as sf

with open('/tmp/myfile.csv', 'w') as f:
    f.write('ID,NAME\n')
    f.write('1,100\n')

conn = sf.connect(
    user="test",
    password="test",
    account="test",
    database="test",
    host="snowflake.localhost.localstack.cloud",
    auto_commit=False
)

cursor = conn.cursor()

cursor.execute("PUT file:///tmp/myfile.csv @TEST.PUBLIC.MYSTAGE/path/to/stage")

cursor.execute("""
MERGE INTO TEST.PUBLIC.MYTABLE AS TARGET
USING (
    SELECT
        $1 AS ID,
        CAST($2 AS NUMBER(38,17)) AS NAME
    FROM @TEST.PUBLIC.MYSTAGE/path/to/stage
    (FILE_FORMAT => TEST.PUBLIC.MYFORMAT)
) AS NEW_ROWS
ON TARGET.ID = NEW_ROWS.ID
WHEN NOT MATCHED THEN
    INSERT (ID, NAME)
    VALUES (NEW_ROWS.ID, NEW_ROWS.NAME)
WHEN MATCHED THEN
    UPDATE SET TARGET.NAME = NEW_ROWS.NAME
""")

# query the table and print the results
cursor.execute("SELECT * FROM TEST.PUBLIC.MYTABLE")
for row in cursor.fetchall():
    print(row)

conn.rollback()
conn.close()

print("Done")