-- Connect to the RDS instance
mysql --host=eventdatabase.cxa6gecsas3w.us-east-1.rds.amazonaws.com --user=admin --password

-- After entering the password, create the table
CREATE TABLE registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(225) NOT NULL,
    email VARCHAR(225) NOT NULL,
    event VARCHAR(225) NOT NULL
);
