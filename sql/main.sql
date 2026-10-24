
CREATE TABLE UserRoles (
    id INTEGER PRIMARY KEY,
    role VARCHAR(255)
);


CREATE TABLE Status (
    id INTEGER PRIMARY KEY,
    status VARCHAR(255)
);


CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(255),
    hashed_password VARCHAR(255),
    userRole INTEGER REFERENCES UserRoles(id),
    money FLOAT
);


CREATE TABLE Orders (
    id INTEGER PRIMARY KEY,
    userID INTEGER REFERENCES Users(id),
    price FLOAT,
    driverID INTEGER REFERENCES Users(id),
    orderStatus INTEGER REFERENCES Status(id)
);