# Results

Brief description of each output file categorized segment:

#### Part 1: Downloading public sequence data of interest ([script](/script/custom_databases.py))

1. [**Species**](species.csv) - Indexed, list of all original species names extracted from the Dutch Species Register (NSR) exports.

#### Part 2: Data classification & analyses ([script](/script/custom_databases.Rmd))

2. [**Markers**](markers.csv) - Indexed, list of genetic markers including the main 4 DNA barcoding markers: COI-5P, ITS, matK, and rbcL.
3. [**Taxonomic Backbone**](taxdata-full.csv) - Taxonomic hierarchies for each species matching the original NSR species names.
4. [**Summary table**](species_markers.csv) - Construct which links the [matching sequence data](/data/FASTA_files/match.fasta) back to the indexed list of species names, their corresponding marker, and a count for the amount of records it holds.
