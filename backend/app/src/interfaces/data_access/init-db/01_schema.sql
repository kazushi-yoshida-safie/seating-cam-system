
CREATE TABLE roles (
    role_id INT PRIMARY KEY,
    role_name VARCHAR(256),
    admin_password VARCHAR(256),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(256),
    email VARCHAR(256) UNIQUE NOT NULL,
    password_hasj VARCHAR(256),
    slack_id VARCHAR(256) UNIQUE NOT NULL,
    role_id INT,
    face_encoding TEXT,
    profile_image_url VARCHAR(256),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE departments (
    department_id INT NOT NULL PRIMARY KEY,
    department_name VARCHAR(256),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seats (
    seat_id BIGINT NOT NULL PRIMARY KEY,
    seat_name VARCHAR(256),
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    department_id INT NOT NULL,
    seating_user VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE devices (
    device_id BIGINT NOT NULL PRIMARY KEY,
    device_name VARCHAR(256),
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    seat_id BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seat_id) REFERENCES seats(seat_id)   
);

CREATE TABLE recognition_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id BIGINT NOT NULL,
    user_id UUID NOT NULL,
    event_type BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

