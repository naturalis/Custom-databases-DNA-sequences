<!-- ABOUT THE DIRECTORY -->
# Data

The data folder contains exported taxonomic data sets from the NSR (input), obtained specimen and sequence data records from BOLD (output), and filtered occurrence data based on matching criteria (output).

- [Taxonomic input data](NSR_exports)
- [Obtained specimen data and sequence records](BOLD_exports)
- [Filtered occurrence data](TSV_files)


<!-- Subdirectory 1: NSR exports -->
## Taxonomic input data (NSR exports)
An export from the Dutch Species Register ([NSR](https://www.nederlandsesoorten.nl/node/374)) provided all species of interest for the project. Exported with their scientific taxonomy, including expected species and including all registered synonyms, resulted in two [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values); one with the current taxonomy (`NSR_exports/NSR_taxonomy.csv`) and one for their synonyms (`NSR exports/NSR_synonyms.csv`).

The taxonomy file contains all taxa stored with their scientific name and authority. Each record’s additional metadata consists of a common (Dutch) name, rank, and NSR identification number. The synonyms file contains all known synonyms for names stored in the taxonomy file, referenced by the “taxon” column. Each record holds the synonymous name, synonymy type, language, and NSR identification number for a known synonym.


<!-- Subdirectory 2: BOLD exports -->
## Obtained specimen data and sequence records (BOLD exports)
Following the verification and acceptance of NSR taxa, specimen data and sequence records were obtained for all species' genera using BOLD’s Public Data Portal [API](http://boldsystems.org/index.php/resources/api?type=webservices). Exported in [TSV format](https://en.wikipedia.org/wiki/Tab-separated_values), each file contains the available records for its respective genera. Formatted files consist of 80 fields, covering the vouchered specimen, taxonomic hierarchy, collection data, and sequence for each record (example file at `BOLD_exports/genera.tsv`). Reducing storage requirements, all files are archived in a single zip file.


<!-- Subdirectory 3: TSV files -->
## Filtered occurrence data (TSV files)
Obtained specimen data is filtered and compared against the NSR taxonomy, along with verification of subsequent criteria. In case of mismatches between species names and a synonym existed, adoption of the accepted name took place using the synonyms file - covering misalignments in identification between the two databases (`TSV_files/match.tsv`). Mismatches against the NSR, provided they hold no known synonym, are copied to a seperate list (`TSV_files/mismatch.tsv`).
