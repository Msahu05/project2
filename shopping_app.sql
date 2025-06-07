CREATE TABLE users (
    id SERIAL PRIMARY KEY, -- Changed INT AUTO_INCREMENT to SERIAL for auto-incrementing primary key
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);