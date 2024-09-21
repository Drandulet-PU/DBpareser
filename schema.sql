DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
  id_2 INTEGER PRIMARY KEY AUTOINCREMENT,
  id_3 INTEGER,
  name TEXT,
  work_place TEXT,
  job_title TEXT,
  gak INTEGER
  
);

DROP TABLE IF EXISTS students;
CREATE TABLE students (
  id_1 INTEGER PRIMARY KEY AUTOINCREMENT,
  id_3 INTEGER,
  name TEXT,
  topic TEXT
);

DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
  id_3 INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE
);

DROP TABLE IF EXISTS marks;
CREATE TABLE marks (
  id_1 INTEGER,
  id_2 INTEGER,
  mark INTEGER CHECK("mark" > 0 AND "mark" < 6)
);