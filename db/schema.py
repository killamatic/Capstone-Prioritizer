# Creates table definitions as SQL strings


# Table definitions as SQL strings
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_EVENTS_TABLE = """
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
"""

# Need to link prediction to its event
CREATE_PREDICTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_name VARCHAR(255) NOT NULL,
    prediction_date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_REPORTS_TABLE = """
CREATE TABLE IF NOT EXISTS reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(100),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSON
);
"""

# Collect tables into a list for easy iteration
TABLES = [
    CREATE_USERS_TABLE,
    CREATE_EVENTS_TABLE,
    CREATE_PREDICTIONS_TABLE,
    CREATE_REPORTS_TABLE
]