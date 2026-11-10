CREATE TABLE UserRoles (
    id SERIAL PRIMARY KEY,
    role VARCHAR(255)
);

CREATE TABLE Status (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50) CHECK (status IN ('free', 'in_progress', 'cancelled', 'completed'))
);

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(255),
    hashed_password VARCHAR(255),
    userRole INTEGER REFERENCES UserRoles(id),
    money FLOAT
);

CREATE TABLE Orders (
    id SERIAL PRIMARY KEY,
    userID INTEGER REFERENCES Users(id),
    price FLOAT,
    driverID INTEGER REFERENCES Users(id),
    address VARCHAR(255),
    orderStatus INTEGER DEFAULT 1 REFERENCES Status(id)
);

CREATE TABLE Reviews (
    id SERIAL PRIMARY KEY,
    userID INTEGER REFERENCES Users(id),
    orderID INTEGER REFERENCES Orders(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5)
);