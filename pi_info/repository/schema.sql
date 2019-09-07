CREATE TABLE IF NOT EXISTS sensor_data
(
    sensor_data_id SERIAL PRIMARY KEY,
    type1          VARCHAR(20),
    value1         DECIMAL,
    type2          VARCHAR(20),
    value2         decimal,
    status         VARCHAR(20),
    sensor_id      INTEGER,
    published_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor
(
    sensor_id     INTEGER PRIMARY KEY,
    name          VARCHAR(50),
    location      VARCHAR(50),
    code          VARCHAR(50),
    type          VARCHAR(50),
    sampling_rate INTEGER
);

CREATE TABLE IF NOT EXISTS relay
(
    relay_id INTEGER PRIMARY KEY,
    name     VARCHAR(50),
    location VARCHAR(50),
    type     VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS relay_status
(
    status_id SERIAL PRIMARY KEY,
    relay_id  INTEGER,
    status    VARCHAR(5)
);

CREATE TABLE IF NOT EXISTS schedule
(
    schedule_id   SERIAL PRIMARY KEY,
    device_id      INTEGER,
    status        VARCHAR(10),
    days          VARCHAR(50),
    time          TIME
);