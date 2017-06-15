PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE 	LE modError(
   ip           text NOT NULL,
   mod         text PRIMARY KEY      NOT NULL
);
CREATE 	LE countData(
mod text PRIMARY KEY     NOT NULL,
ip           TEXT    NOT NULL,
count            INT     NOT NULL
);
INSERT INTO "countData" VALUES('Current Load','99.12.90.100',4);
COMMIT;

