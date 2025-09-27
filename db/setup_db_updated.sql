-- Drop the user and database if they already exist to allow for clean re-runs.
DROP USER IF EXISTS 'app_user'@'localhost';
DROP DATABASE IF EXISTS event_storage_db;

-- Create a new user
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'your_strong_password';

-- Create the database
CREATE DATABASE event_storage_db;

-- Grant the user all privileges on the new database
GRANT ALL PRIVILEGES ON event_storage_db.* TO 'app_user'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

-- Use the new database
USE event_storage_db;


CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_date DATETIME NOT NULL,
    expected_priority INT,
    resources_required VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);
