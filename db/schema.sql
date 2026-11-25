USE lost_and_found;

-- Creating the table of admins
CREATE TABLE IF NOT EXISTS admins (
	admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating the table of active items
CREATE TABLE IF NOT EXISTS active_items (
	item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    date_found DATE NOT NULL,
    status ENUM('Lost', 'Found', 'Claimed') NOT NULL DEFAULT 'Found',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create the table of archived items
CREATE TABLE IF NOT EXISTS archive_items (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    date_found DATE NOT NULL,
    status ENUM('Lost', 'Found', 'Claimed') NOT NULL DEFAULT 'Found',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for paper trail of items
CREATE TABLE IF NOT EXISTS item_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    admin_id INT NULL,
    action_type ENUM(
        'Added',
        'Updated',
        'Claimed',
        'Removed',
        'Archived'
    ) NOT NULL,
    changed_field VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    details TEXT,
    action_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_item_history_admin
        FOREIGN KEY (admin_id)
        REFERENCES admins(admin_id)
        ON DELETE SET NULL
);

