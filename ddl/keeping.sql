CREATE TABLE school_enum
(
  id INT NOT NULL AUTO_INCREMENT,
  name NVARCHAR(512) NOT NULL,
  PRIMARY KEY (id) 
);

CREATE TABLE degree_enum
(
  id INT NOT NULL AUTO_INCREMENT,
  name NVARCHAR(512) NOT NULL,
  PRIMARY KEY (id) 
);

CREATE TABLE preferred_mode_enum
(
  id INT NOT NULL AUTO_INCREMENT,
  name NVARCHAR(64) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE preferred_time_enum
(
  id INT NOT NULL AUTO_INCREMENT,
  name NVARCHAR(64) NOT NULL,
  PRIMARY KEY (id)
);

insert into keeping.preferred_mode_enum (name) values("wfh");
insert into keeping.preferred_mode_enum (name) values("part-time");
insert into keeping.preferred_mode_enum (name) values("contract");
insert into keeping.preferred_mode_enum (name) values("internship");
insert into keeping.preferred_mode_enum (name) values("freelance");

insert into keeping.preferred_time_enum (name) values("12am-4am");
insert into keeping.preferred_time_enum (name) values("4am-8am");
insert into keeping.preferred_time_enum (name) values("8am-12pm");
insert into keeping.preferred_time_enum (name) values("12pm-4pm");
insert into keeping.preferred_time_enum (name) values("4pm-8pm");
insert into keeping.preferred_time_enum (name) values("8pm-12am");
