<!-- ABOUT THE DIRECTORY -->
# Results (creation of custom databases)

The results folder contains all relevant [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values) to create a custom database.

1. [**Species**](nsr_species.csv) - List of species from the Dutch Species Register (NSR).
2. [**Synonyms**](nsr_synonyms.csv) - List of known synonyms for NSR species names.
3. [**Species markers**](species_markers.csv) - Construct which links the [matching sequence data](/data/TSV_files/match.tsv) to their corresponding NSR species names, and holds information on its marker, database of origin, and a sequence ID provided by their respective database.
4. [**Markers**](markers.csv) - List of genetic markers, including the main 4 DNA barcoding markers: COI-5P, ITS, matK, and rbcL.
5. [**Databases**](databases.csv) - List of databases reflecting sources of collected data.
6. [**Tree_nsr**](tree_nsr.csv) - Classification of higher taxa for species names, as provided by the NSR.
7. [**Tree_ncbi**](tree_ncbi.csv) - Classification of species names as present in the NCBI taxonomy database.
8. [**Custom Database**](custom_databases.sqlite) - SQLite database, populated with the 7 aforementioned datasets.

<!-- Content of result files -->
## The content of result files
This README.md gives a brief description of each *.csv file. These files contain taxonomic information of obtained public reference data and internal reference data from Naturlis Biodiversity Center. The entity-relationship model below represents the flow of information between each of the data sets, as stored in the accompanying SQLite database file (`custom_databases.sqlite`). 

![ERD](https://github.com/naturalis/Custom-databases-DNA-sequences/blob/master/results/ERD.png?raw=true)

### nsr_species.csv
-------------------
This file represents the NSR taxonomy input file, filtered to accepeted taxa. The description for each taxa includes the following fields:

- species_id -- Identifier corresponding to unique NSR species name
- species_name -- Scientific name; identifying genus and species
- identification_reference -- Authority when first mentioned, and year of publication

### nsr_synonyms.csv
--------------------
This file represent the NSR synonyms input file, filtered to accepted synonyms. The description for each synonym includes the following fields:

- synonym_id -- Identifier corresponding to unique NSR synonym name
- species_id -- Identifier corresponding to matching NSR species name
- synonym_name -- Scientific name; identifying genus and species
- identification_reference -- Authority when first mentioned, and year of publication

### species_markers.csv
-----------------------
This file represents the obtained curated reference material from the Naturalis Biodiversity Center and a snapshot of public specimen data and sequence records from BOLD, matching the NSR taxonomy (or a known synonym). The description for each occurrence of a species includes the following fields:

- species_marker_id -- Unique identifier linking species to their associated records
- species_id -- Identifier corresponding to unique NSR species name
- database_id -- Identifier corresponding to database storing the record
- marker_id -- Identifier corresponding to marker of the record
- sequence_id -- Unique identifier corresponding to external record metadata

### markers.csv
---------------
Markers file has these fields:

- marker_id -- Identifier corresponding to unique marker name
- marker_name -- Name of associated marker

### databases.csv
-----------------
Databases file has these fields:

- database_id -- Identifier corresponding to unique database name
- database_name -- Name of associated database

### tree_nsr.csv
-----------------
This file contains the higher taxa of NSR species as obtained from the NSR. The description for each taxa includes the following fields:

- tax_id -- Taxon ID in NSR taxonomy database
- species_id -- Identifier corresponding to unique NSR species name
- parent_tax_id -- Parent taxa id in NSR taxonomy database
- rank -- Rank of associated taxa (kingdom, phylum, class, etc.)
- name -- Name of associated taxa itself

### tree_ncbi.csv
-----------------
This file contains the classification of NSR taxa as obtained from the NCBI taxonomy database. The description for each taxonomy node includes the following fields:

- tax_id -- Node id in GenBank taxonomy database
- species_id -- Identifier corresponding to unique NSR species name
- parent_tax_id -- Parent node id in GenBank taxonomy database
- rank -- Rank of associated node (kingdom, phylum, class, etc.)
- name -- Name of associated node itself
