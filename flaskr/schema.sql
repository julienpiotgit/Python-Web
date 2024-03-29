DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS groupe;
DROP TABLE IF EXISTS commentaire;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE groupe (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  groupe_id INTEGER NOT NULL,
  titre TEXT NOT NULL,
  description TEXT NOT NULL,
  FOREIGN KEY (groupe_id) REFERENCES user (id)
);

CREATE TABLE commentaire (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  commentaire TEXT NOT NULL,
  groupe_id INTEGER NOT NULL,
  FOREIGN KEY (groupe_id) REFERENCES groupe (id)
);