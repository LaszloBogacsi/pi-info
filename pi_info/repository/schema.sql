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

CREATE TABLE IF NOT EXISTS device
(
    device_id INTEGER PRIMARY KEY,
    name      VARCHAR(50),
    location  VARCHAR(50),
    type      VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS device_status
(
    device_id INTEGER PRIMARY KEY,
    status    VARCHAR(5)
);

CREATE TABLE IF NOT EXISTS schedule
(
    schedule_id SERIAL PRIMARY KEY,
    group_id    VARCHAR(50),
    device_id   VARCHAR(500),
    status      VARCHAR(10),
    days        VARCHAR(50),
    time        TIME
);

CREATE TABLE IF NOT EXISTS device_group
(
    group_id VARCHAR(50) PRIMARY KEY,
    name     VARCHAR(50),
    delay    INTEGER,
    ids      VARCHAR(500),
    status   VARCHAR(10)
);