# Results

Brief description of each output file categorized segment:

#### Part 1: Downloading public sequence data of interest ([script](/script/custom_databases.py))

1. [**Species**](species.csv) - Indexed, list of all original species names extracted from the Dutch Species Register (NSR) exports.

#### Part 2: Data classification & analyses ([script](/script/custom_databases.Rmd))

2. [**Markers**](markers.csv) - Indexed, list of genetic markers including the main 4 DNA barcoding markers: COI-5P, ITS, matK, and rbcL.
3. [**Databases**](databases.csv) - Indexed, list of databases reflecting our obtained public sequence data.
4. [**Taxonomic data**](taxdata.csv) - Taxonomic hierarchies, synonym, and IDs from the ncbi_tree corresponding to recognized NSR species names.
5. [**Species markers**](species_markers.csv) - Construct which links the [matching sequence data](/data/FASTA_files/match.fasta) back to the indexed list of species names, their corresponding marker, and a sequence ID provided by their respective database.

#### Part 3: Database ([script](/script/schema.sql))
6. [**Database**](custom_datases.sqlite) - SQLite database, populated with the 5 aforementioned datasets.

### Dataset Relationships
![ERD](https://github.com/naturalis/Custom-databases-DNA-sequences/blob/master/results/ERD.png?raw=true)
