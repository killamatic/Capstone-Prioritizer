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

-- TODO: until hashing has been implemented, the normal password can be stored in the local database 
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    event_duration INT NOT NULL,
    predicted_priority INT,
    actual_priority INT,
    participant_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    predicted_priority INT,
    feedback boolean,
    event_id INT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

CREATE TABLE IF NOT EXISTS reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_title VARCHAR(255),
    report_type VARCHAR(50),
    report_content JSON,
    report_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
