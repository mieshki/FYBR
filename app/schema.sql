CREATE TABLE users(
    id BIGINT UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    PRIMARY KEY(id)
);
CREATE TABLE ride(
    id BIGINT UNIQUE NOT NULL,
    date DATE NOT NULL,
    gpx_file VARCHAR(100000) NOT NULL,
    user_id BIGINT NOT NULL,
    bike_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (bike_id) REFERENCES bike(id),
    PRIMARY KEY (id)
);
CREATE TABLE photo(
    id BIGINT UNIQUE NOT NULL,
    photo VARCHAR(100) NOT NULL,
    ride_id BIGINT NOT NULL,
    FOREIGN KEY (ride_id) REFERENCES ride(id),
    PRIMARY KEY (id)
);
CREATE TABLE bike(
    id BIGINT UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    user_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (id)
)