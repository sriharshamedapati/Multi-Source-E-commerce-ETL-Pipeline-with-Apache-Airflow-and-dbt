CREATE TABLE users (user_id INT PRIMARY KEY, created_at TIMESTAMP, email VARCHAR(100));
CREATE TABLE products (product_id INT PRIMARY KEY, name VARCHAR(100), price DECIMAL(10,2));

INSERT INTO users VALUES (1, NOW(), 'user1@test.com'), (2, NOW(), 'user2@test.com'), (3, NOW(), 'user3@test.com'), (4, NOW(), 'user4@test.com'), (5, NOW(), 'user5@test.com'), (6, NOW(), 'user6@test.com'), (7, NOW(), 'user7@test.com'), (8, NOW(), 'user8@test.com'), (9, NOW(), 'user9@test.com'), (10, NOW(), 'user10@test.com');
INSERT INTO products VALUES (1, 'Laptop', 999.99), (2, 'Mouse', 25.00), (3, 'Keyboard', 50.00), (4, 'Monitor', 200.00), (5, 'Desk', 150.00), (6, 'Chair', 120.00), (7, 'Lamp', 30.00), (8, 'Cable', 10.00), (9, 'Webcam', 60.00), (10, 'Headphones', 80.00);