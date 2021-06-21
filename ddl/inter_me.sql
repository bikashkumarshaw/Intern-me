CREATE TABLE candidate (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(128) CHARACTER SET utf8mb4 NOT NULL,
  linkedin_profile VARCHAR(128) CHARACTER SET utf8mb4,
  preferred_env INT,
  PRIMARY KEY(id),
  FOREIGN KEY (preferred_env) REFERENCES keeping.preferred_mode_enum(id)

);

CREATE TABLE candidate_email (
  candidate_id INT NOT NULL,
  email VARCHAR(128) CHARACTER SET utf8mb4,
  is_primary_email tinyint(1) NOT NULL DEFAULT 1,
  FOREIGN KEY(candidate_id) REFERENCES candidate(id),
  PRIMARY KEY (candidate_id, email)
);

CREATE TABLE candidate_phone_number (
  candidate_id INT NOT NULL,
  phone_number VARCHAR(128) CHARACTER SET utf8mb4,
  phone_type INT NOT NULL DEFAULT 1,
  FOREIGN KEY (candidate_id) REFERENCES candidate(id),
  FOREIGN KEY (phone_type) REFERENCES housekeeping.phone_number_type_enum(id),
  PRIMARY KEY (candidate_id, phone_number)
);

CREATE TABLE candidate_education (
  candidate_id INT NOT NULL,
  school_id INT NOT NULL,
  start_month INT,
  start_year INT,
  end_month INT,
  end_year INT,
  degree_id INT,
  rank INT,
  FOREIGN KEY (candidate_id) REFERENCES candidate(id),
  FOREIGN KEY (degree_id) REFERENCES keeping.degree_enum(id),
  FOREIGN KEY (school_id) REFERENCES keeping.school_enum(id)
);
