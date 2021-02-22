# Script folder

Brief description of each script.


## custom_databases.py
Using an export from the Dutch Species Register (NSR), the script harvests the scientific notation of species, including synonyms and expected species. Extracted taxonomy is used, by means of genera, to obtain matching specimens and sequence data from the Barcode of Life Data System (BOLD) database. Filtered on geographic site. Accepted names from the NSR will be adopted on matching synonyms.


## custom_databases.Rmd
The R markdown file performs the steps needed to:
1. Create a data structure capable of providing highly visual representations and at the
same time maintaining integrity of each data set’s origin.
2. Search out and visualize the overlap / gaps between the obtained Public Sequence Data
(BOLD) and a reference provided by the Naturalis Biodiversity center, in correlation to
the NSR.
3. Assess the quality and reliability of obtained public sequence data.


## schema.sql
Represents the logical configurations for the creation of the SQLite database. Able to be populated with the project's output files (see `results/`).
