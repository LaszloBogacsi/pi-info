CREATE TABLE IF NOT EXISTS sensor_data (
        sensor_data_id SERIAL PRIMARY KEY,
        type1 varchar(20),
        value1 decimal,
        type2 varchar(20),
        value2 decimal,
        status varchar(20),
        sensor_id INTEGER,
        published_time TIMESTAMP)