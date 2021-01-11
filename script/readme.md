# Scripts

Brief description of each script.


## custom_databases.py
Using an export from the Dutch Species Register (NSR) with a full taxonomic breakdown, including synonyms and expected species, running the script allows for its list of species to be compared against matching genera extracted using BOLD's Public Data Portal API. Filterting to Dutch records only, it writes matching/non-matching sequence data to their allocated files.


## custom_databases.Rmd
The  R markdown file performs the steps needed to search out and visualize the coverage between the obtained public sequence data (using the custom_databases.py script) and its reference from the Dutch Species Register (NSR).
