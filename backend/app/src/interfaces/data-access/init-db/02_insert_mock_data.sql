
INSERT INTO roles (role_id, role_name, admin_password) VALUES
(1, 'Admin', 'admin_password_hash_placeholder'),
(2, 'General User', NULL);

-- 2. departmentsテーブルへのデータ挿入
INSERT INTO departments (department_id, department_name) VALUES
(10, 'Sales Department'),
(20, 'Engineering Department');

-- 3. usersテーブルへのデータ挿入 (UUIDを明示的に指定)
INSERT INTO users (user_id, name, email, password_hasj, slack_id, role_id, face_encoding, profile_image_url) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', '山田 太郎', 'taro.yamada@example.com', 'hashed_password_123', 'U012ABCDEF', 1, 'face_encoding_data_string_1', 'https://example.com/images/taro.jpg'),
('0c7b2a6d-4f1c-4b8a-8c1b-2b3b4a5a6b7c', '鈴木 花子', 'hanako.suzuki@example.com', 'hashed_password_456', 'U345GHIJKL', 2, 'face_encoding_data_string_2', 'https://example.com/images/hanako.jpg');

-- 4. seatsテーブルへのデータ挿入 (department_idのタイポに注意)
INSERT INTO seats (seat_id, seat_name, is_active, deoartment_id) VALUES
(101, 'A-1', TRUE, 10),
(102, 'A-2', FALSE, 10),
(201, 'B-1', TRUE, 20),
(202, 'B-2', TRUE, 20);

-- 5. devicesテーブルへのデータ挿入
INSERT INTO devices (device_id, device_name, is_active, seat_id) VALUES
(1001, 'Entrance Camera', TRUE, 101),
(2001, 'Dev Floor Tablet', TRUE, 201);

-- 6. recognition_logsテーブルへのデータ挿入
-- event_type: FALSE(入室), TRUE(退室)を想定
INSERT INTO recognition_logs (device_id, user_id, event_type, created_at) VALUES
(1001, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', FALSE, '2025-09-24 09:00:00+09'),
(2001, '0c7b2a6d-4f1c-4b8a-8c1b-2b3b4a5a6b7c', FALSE, '2025-09-24 09:05:10+09'),
(1001, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', TRUE,  '2025-09-24 18:02:30+09'),
(2001, '0c7b2a6d-4f1c-4b8a-8c1b-2b3b4a5a6b7c', TRUE,  '2025-09-24 18:30:00+09');