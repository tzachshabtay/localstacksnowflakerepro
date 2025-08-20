    WITH my_cte AS (
    SELECT
        col1,
        col2,
        col3,
        col4
    FROM MYSCHEMA.MYTABLE
    WHERE
        col2 = '2023-01-01'
    ),

    eod_my_cte AS (
    SELECT
        col1,
        col2,
        col3,
        col4
    FROM MYSCHEMA.MYTABLE
    WHERE
        col2 = '2023-01-01'
    )

    SELECT
        l.col1 AS L_COL1,
        e.col1 AS E_COL1,
        EQUAL_NULL(l.col2, e.col2) AS EQ_COL2,
        l.col3 AS L_COL3,
        e.col3 AS E_COL3,
        EQUAL_NULL(l.col3, e.col3) AS EQ_COL3,
        l.col4 AS L_COL4,
        e.col4 AS E_COL4,
        EQUAL_NULL(l.col4, e.col4) AS EQ_COL4,
            MOD(EQ_COL2::numeric+1, 2) +
            MOD(EQ_COL3::numeric+1, 2) +
            MOD(EQ_COL4::numeric+1, 2) AS total_diffs
    FROM
        my_cte l
    FULL OUTER JOIN
        eod_my_cte e
    ON
        l.col2 = e.col2
    WHERE
        total_diffs > 0
    ORDER BY
        total_diffs DESC
    LIMIT 100;