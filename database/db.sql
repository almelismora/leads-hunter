USE leads_hunter;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS c_favorites;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);





CREATE TABLE clients (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    post_link VARCHAR(100), 
    user_link VARCHAR(100),
    name VARCHAR(200),
    account VARCHAR(150),
    description TEXT,
    website_link VARCHAR(400),
    website_name VARCHAR(300),
    email VARCHAR(250),
    phone VARCHAR(150)
);


CREATE TABLE c_favorites (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200),
    account VARCHAR(150),
    description VARCHAR(500),
    website_link VARCHAR(400),
    website_name VARCHAR(300),
    email VARCHAR(250),
    phone VARCHAR(150),
    note TEXT,
    user_id INT UNSIGNED,
    CONSTRAINT `fkufav`
    FOREIGN KEY (user_id) REFERENCES clients (id)
);