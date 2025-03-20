CREATE TABLE IF NOT EXISTS MYSCHEMA.MYTABLE (
    ID VARCHAR(255) PRIMARY KEY,
    NAME VARCHAR(255) NOT NULL
);

CREATE STAGE IF NOT EXISTS MYSCHEMA.MYSTAGE;

CREATE OR REPLACE FILE FORMAT MYSCHEMA.MYFORMAT
    TYPE = 'CSV'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"';