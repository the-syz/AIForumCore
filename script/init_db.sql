CREATE DATABASE IF NOT EXISTS aiforum CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'aiforum'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON aiforum.* TO 'aiforum'@'localhost';
FLUSH PRIVILEGES;