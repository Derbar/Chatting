CREATE DATABASE sp;
CREATE TABLE sp.tb_member (
	id int(11) unsigned NOT NULL AUTO_INCREMENT,
	username varchar(255) NOT NULL,
	password varchar(255) NOT NULL,
	PRIMARY KEY(id)
);
INSERT INTO sp.tb_member (username, password) values ('admin', password('admin')); 
INSERT INTO sp.tb_member (username, password) values ('test', password('1234'));
