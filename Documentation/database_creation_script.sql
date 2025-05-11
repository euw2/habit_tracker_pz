CREATE TABLE User (
  id INTEGER PRIMARY KEY,
  password VARCHAR(255),
  email VARCHAR(255),
  recovery_code VARCHAR(255),
  username VARCHAR(255)
);
 
CREATE TABLE Habit (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255),
  description TEXT
);
 
CREATE TABLE Activity (
  id INTEGER PRIMARY KEY,
  date DATE,
  habit_id INTEGER,
  user_id INTEGER,
  FOREIGN KEY (habit_id) REFERENCES Habit(id),
  FOREIGN KEY (user_id) REFERENCES User(id)
);
 
CREATE TABLE Habit_Statistics (
  habit_id INTEGER,
  user_id INTEGER,
  days_in_row INTEGER,
  total_completed INTEGER,
  last_updated DATE,
  FOREIGN KEY (habit_id) REFERENCES Habit(id),
  FOREIGN KEY (user_id) REFERENCES User(id)
);