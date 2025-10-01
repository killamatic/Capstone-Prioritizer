-- Drop the user and database if they already exist to allow for clean re-runs.
-- DROP USER IF EXISTS 'app_user'@'localhost';
-- DROP USER IF EXISTS 'admin'@'localhost';
DROP USER IF EXISTS 'app_user'@'localhost';
DROP DATABASE IF EXISTS event_storage_db;

-- Create a new user
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'your_strong_password';
-- CREATE USER 'admin'@'localhost' IDENTIFIED BY 'your_strong_password';
-- CREATE USER 'admin'@'localhost' IDENTIFIED BY 'root';

-- Create the database
CREATE DATABASE event_storage_db;

-- Grant the user all privileges on the new database
GRANT ALL PRIVILEGES ON event_storage_db.* TO 'app_user'@'localhost';
-- GRANT ALL PRIVILEGES ON event_storage_db.* TO 'admin'@'localhost';

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

-- test out if Date is better than datetime for event date and duration
-- TODO: make created by id NOT NULL
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

-- TODO: add & test in feedback storage: feedback boolean: true = approved, false = deny, if not null, then user has given feedback
--     Update boolean to ENUM if other indicators are added: skipped, pending 
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    predicted_priority INT,
    feedback boolean,
    event_id INT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- turn report type into enum like user v admin
CREATE TABLE IF NOT EXISTS reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_title VARCHAR(255),
    report_type VARCHAR(50),
    report_content JSON,
    report_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
