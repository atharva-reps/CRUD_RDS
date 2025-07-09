create database dev;
use dev;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT
);

INSERT INTO students (name, age) VALUES
('Rahul Verma', 20),
('Priya Sharma', 22),
('Amit Kumar', 19),
('Sneha Reddy', 21),
('John Mathew', 23);
