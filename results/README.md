# Results

Brief description of each output file categorized by segment:

#### Part 1: Downloading public sequence data of interest ([script](/script/custom_databases.py))

1. [**Species**](nsr_species.csv) - Indexed, list of all original species names extracted from the Dutch Species Register (NSR) exports.

#### Part 2: Data classification & analyses ([script](/script/custom_databases.Rmd))

2. [**Synonyms**](nsr_synonyms.csv) - Indexed, list of all known synonyms for NSR species names.
3. [**Markers**](markers.csv) - Indexed, list of genetic markers including the main 4 DNA barcoding markers: COI-5P, ITS, matK, and rbcL.
4. [**Databases**](databases.csv) - Indexed, list of databases reflecting obtained public sequence data.
5. [**Tree_nsr**](tree_nsr.csv) - NSR's higher taxa of respective species names, accompanied by their Tax ID.
6. [**Tree_ncbi**](tree_ncbi.csv) - Taxonomic classification of recognized NSR species names provided by GenBank, accompanied by their Tax ID.
7. [**Species markers**](species_markers.csv) - Construct which links the [matching sequence data](/data/FASTA_files/match.tsv) back to the indexed list of species names, their corresponding marker, and a sequence ID provided by their respective database.

#### Part 3: Database ([script](/script/schema.sql))
8. [**Custom Database**](custom_databases.sqlite) - SQLite database, populated with the 7 aforementioned datasets.

### Dataset Relationships
![ERD](https://github.com/naturalis/Custom-databases-DNA-sequences/blob/master/results/ERD.png?raw=true)
