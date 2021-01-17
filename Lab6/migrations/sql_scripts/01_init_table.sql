DO
$$
    BEGIN
        CREATE TABLE IF NOT EXISTS purchasing.pln_currencies
            (
                id                 serial          primary key,
                currency_date      timestamp       not null,
                currency_value     numeric(8, 4)   not null,
                interpolated       boolean         not null default false
            );
    END
$$;