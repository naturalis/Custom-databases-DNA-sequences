# Data

Brief explanation of the use and source of each dataset.


## NSR export
To supplement the internal databases at Naturalis, the Dutch Species Register ([NSR](https://www.nederlandsesoorten.nl/node/374)) export contains all species of interest for this project.
Exported with their complete taxonomy, including expected species, and including all registered synonyms, two files are used; one with the current taxonomy (`NSR_exports/NSR_taxonomy.csv`) and one for their synonyms (`NSR exports/NSR_synonyms.csv`).

Stored as a [CSV file](https://en.wikipedia.org/wiki/Comma-separated_values), the taxonomy file contains all taxa stored with their scientific name and authority. Each record’s additional metadata consists of a common (Dutch) name, rank, and NSR identification number. The synonyms file in turn stores all known synonyms for names stored in the taxonomy file, referenced by the ‘taxon’ column. Each record holds the synonymous name, synonymy type, language, and NSR identification number for a known synonym.

Using the taxonomy file, all species’ genera are aggregated and used to download their subtended species with their sequences present in the Barcode of Life Datatabase ([BOLD](http://www.barcodinglife.org/)).
Sequence data is compared against species from the NSR. In case of mismatches between species names and a synonym exists, adoption of the accepted name takes place using the synonyms file - covering misalignments in identification between the two databases.


## BOLD exports
Using BOLD’s Public Data Portal [API](http://boldsystems.org/index.php/resources/api?type=webservices) genera are retrieved one genus at a time and saved to the allocated folder (example file at `BOLD_exports/genera.tsv`).
Obtaining as many records available, the [TSV files](https://en.wikipedia.org/wiki/Tab-separated_values) consists of the vouchered specimen, taxonomic hierarchy, collection data, and sequence for each record.
Reducing storage requirements, all files are archived in a single zip file.


## TSV files
Iterating over every downloaded file from BOLD, sequence data is compared against species from the NSR. Subgenera will be filtered out creating a file with as many accepeted names as possible (`FASTA_files/match.tsv`). Mismatches against the NSR, provided they hold no known synonym, are copied to a seperate list (`FASTA_files/mismatch.tsv`).
