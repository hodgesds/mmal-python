CREATE TABLE IF NOT EXISTS temp(timestamp INTEGER PRIMARY KEY, temp INTEGER);
INSERT INTO temp VALUES(1470600282123000000, 10);
INSERT INTO temp VALUES(1470600282218000000, 11);
INSERT INTO temp VALUES(1470600282377000000, 12);
INSERT INTO temp VALUES(1470600282450000000, 11);
CREATE TABLE IF NOT EXISTS wind(timestamp TEXT PRIMARY KEY, speed INTEGER, direction REAL);
INSERT INTO wind VALUES('2016-08-07T16:00:20-04:00', 10, 162.3);
INSERT INTO wind VALUES('2016-08-07T16:00:20-05:00', 11, 183.8);
INSERT INTO wind VALUES('2016-08-07T16:00:20-06:00', 12, 190.1);
INSERT INTO wind VALUES('2016-08-07T16:00:20-07:00', 15, 220.4);
INSERT INTO wind VALUES('2016-08-07T16:00:20-08:00', 13, 180.2);
INSERT INTO wind VALUES('2016-08-07T16:00:20-09:00', 10, 215.0);
INSERT INTO wind VALUES('2016-08-07T16:00:20-10:00', 7, 236.3);
INSERT INTO wind VALUES('2016-08-07T16:00:20-11:00', 9, 220.9);
INSERT INTO wind VALUES('2016-08-07T16:00:20-12:00', 8, 263.7);
INSERT INTO wind VALUES('2016-08-07T16:00:20-13:00', 10, 233.4);
INSERT INTO wind VALUES('2016-08-07T16:00:20-14:00', 11, 212.2);
INSERT INTO wind VALUES('2016-08-07T16:00:20-15:00', 13, 193.9);
INSERT INTO wind VALUES('2016-08-07T16:00:20-16:00', 12, 178.7);
INSERT INTO wind VALUES('2016-08-07T16:00:20-17:00', 11, 154.3);
INSERT INTO wind VALUES('2016-08-07T16:00:20-18:00', 100000, 220.1);
