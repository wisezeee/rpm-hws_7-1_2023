CREATE TABLE IF NOT EXISTS token (username text primary key, token uuid);

CREATE TABLE country (id integer generated always as identity not null primary key, 
    name text not null, 
    continent text not null,  
    population int);

INSERT INTO token VALUES ('admin', 'f9f668fc-e868-4c09-947b-6a07b3850d5c');