# Script folder

Brief description of each script.


## custom_databases.py
Using an export from the Dutch Species Register (NSR) with a full taxonomic breakdown, including synonyms and expected species, running the script allows for its list of species to be compared against matching genera extracted using BOLD's Public Data Portal API. Filterting to Dutch records only, it writes matching/non-matching sequence data to their allocated files. Subsequently, it saves the original list of species for future reference.


## custom_databases.Rmd
The R markdown file performs the steps needed to:
1. Create a more streamlined data structure which allows us to track all information of the species of interest between the various datasets.
2. Search out and visualize the coverage between the obtained public sequence data and its reference from the Dutch Species Register (NSR).


## schema.sql
Contains the elements and relations needed to create a SQLite database. Able to be populated with the projects output files (see `results/`).
