

CREATE TABLE UserRoles (
    id INT PRIMARY KEY,
    role VARCHAR(255) NOT NULL
);

CREATE TABLE Status (
    id INT PRIMARY KEY,
    status VARCHAR(255) NOT NULL
);



CREATE TABLE Users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL, 
    name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    userRole INT NOT NULL,
    money DECIMAL(15, 2) DEFAULT 0.00, 
    CONSTRAINT fk_users_role FOREIGN KEY (userRole) 
        REFERENCES UserRoles(id)
);



CREATE TABLE Orders (
    id BIGINT PRIMARY KEY,
    userID BIGINT NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    driverID BIGINT,
    orderStatus INT NOT NULL,
    
   
    CONSTRAINT fk_orders_customer FOREIGN KEY (userID) 
        REFERENCES Users(id),
        
   
    CONSTRAINT fk_orders_driver FOREIGN KEY (driverID) 
        REFERENCES Users(id),
        
   
    CONSTRAINT fk_orders_status FOREIGN KEY (orderStatus) 
        REFERENCES Status(id)
);


CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_orders_userID ON Orders(userID);
CREATE INDEX idx_orders_driverID ON Orders(driverID);
CREATE INDEX idx_orders_status ON Orders(orderStatus);