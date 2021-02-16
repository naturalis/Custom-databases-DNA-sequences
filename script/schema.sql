-- This schema connects obtained public sequence data to the backbone of its reference data set

CREATE TABLE "nsr_species" (
	"species_id" INTEGER NOT NULL,
	"species_name" TEXT NOT NULL,
	"identification_reference" TEXT,
	PRIMARY KEY("species_id")
);

CREATE TABLE "taxdata" (
	"tax_id" INTEGER NOT NULL,
	"species_id" INTEGER NOT NULL,
	"phylum" TEXT NOT NULL,
	"class" TEXT NOT NULL,
	"order" TEXT NOT NULL,
	"family" TEXT NOT NULL,
	"genus" TEXT NOT NULL,
	"species" TEXT NOT NULL,
	"node_name" TEXT NOT NULL,
	PRIMARY KEY("tax_id", "species_id"),
	FOREIGN KEY("species_id") REFERENCES "nsr_species"("species_id")
);

CREATE TABLE "species_markers" (
	"species_markers_id" INTEGER NOT NULL,
	"species_id" INTEGER NOT NULL,
	"database_id" INTEGER NOT NULL,
	"marker_id" INTEGER NOT NULL,
	"sequence_id" INTEGER NOT NULL,
	PRIMARY KEY("species_markers_id"),
	FOREIGN KEY("database_id") REFERENCES "databases"("database_id"),
	FOREIGN KEY("marker_id") REFERENCES "markers"("marker_id"),
	FOREIGN KEY("species_id") REFERENCES "nsr_species"("species_id")
);

CREATE TABLE "markers" (
	"marker_id" INTEGER NOT NULL,
	"marker_name" TEXT NOT NULL,
	PRIMARY KEY("marker_id")
);

CREATE TABLE "databases" (
	"database_id" INTEGER NOT NULL,
	"database_name" TEXT NOT NULL,
	PRIMARY KEY("database_id")
);
