CREATE TABLE IF NOT EXISTS usd_rates
(
    usd_rate_id serial         NOT NULL,
    date        date           NOT NULL UNIQUE,
    rate        decimal(10, 4) NOT NULL
);
