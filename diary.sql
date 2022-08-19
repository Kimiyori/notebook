CREATE TABLE "main_table" (
	"id"	INTEGER NOT NULL,
	"date_of_the_day"	DATE NOT NULL UNIQUE,
	"about_the_day"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE UNIQUE INDEX "date_index" ON "main_table" (
	"date_of_the_day"	ASC
);
CREATE TABLE "tags" (
	"id"	INTEGER NOT NULL,
	"tag"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE UNIQUE INDEX "tag_index" ON "tags" (
	"tag"   ASC
);
CREATE TABLE "tagmap" (
	"id"	INTEGER NOT NULL,
	"main_id"	INTEGER NOT NULL,
	"tag_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT) ,
	FOREIGN KEY("tag_id") REFERENCES "tags"("id"),
	FOREIGN KEY("main_id") REFERENCES "main_table"("id")
);
CREATE INDEX "tagmax_index" ON "tagmap" (
	"main_id",
	"tag_id"
);