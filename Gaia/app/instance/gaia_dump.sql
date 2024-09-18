PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('2783c52d2519');
CREATE TABLE IF NOT EXISTS "user" (
	userid INTEGER NOT NULL, 
	username VARCHAR(40) NOT NULL, 
	email VARCHAR(40) NOT NULL, 
	phone VARCHAR(15), 
	password VARCHAR(40) NOT NULL, 
	"fullName" VARCHAR(40) NOT NULL, 
	ismod BOOLEAN, 
	PRIMARY KEY (userid), 
	UNIQUE (username), 
	UNIQUE (email)
);
INSERT INTO user VALUES(1,'dsoul','denissoulima@gmail.com','2032032003','123123','Denis Soulima',0);
COMMIT;
