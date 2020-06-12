DROP TABLE IF EXISTS compiled_agency;
CREATE TABLE compiled_agency(
"state" TEXT,
"station_name" TEXT,
"nsn" TEXT,
"item_name" TEXT,
"quantity" INTEGER,
"ui" TEXT,
"acquisition_value" DECIMAL,
"demil_code" TEXT,
"demil_ic" TEXT,
"ship_date" DATE,
"org_ship_date" DATETIME,
"station_type" TEXT,
"file_date" DATE,
"book_name" TEXT,
"sheet_name" TEXT
);
