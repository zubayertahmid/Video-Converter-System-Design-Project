CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';
CREATE DATABASE auth;
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
USE auth;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (email, password) VALUES ('zubayer@email.com', 'Admin123');
