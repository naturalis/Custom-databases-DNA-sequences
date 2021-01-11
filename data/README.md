# Data types

Brief explanation of the use and source of each dataset.


## NSR export
To enchance the internal databases at Naturalis, the Dutch Species Register ([NSR](https://www.nederlandsesoorten.nl/node/374)) export contains all species of interest for this project.
Exported with their complete taxonomy, including expected species, and including all registered synonyms, two files are used; one with the current taxonomy (`NSR_exports/NSR_taxonomy.csv`) and one for their synonyms (`NSR exports/NSR_synonyms.csv`).

Stored as a [CSV file](https://en.wikipedia.org/wiki/Comma-separated_values), the taxonomy file holds the Scientific Names, Common Names, Rank, and NSR ID of each species. The synonyms file in turn stores the Synonym name, Synonym Type, Classification, Taxon, and NSR ID for each known synonym.

Using the taxonomy file, their genera are isolated and used to download the corresponding species with sequences present in the Barcode of Life Datatabase ([BOLD](http://www.barcodinglife.org/)).
All sequence data is compared against species from the NSR. In case of any mismatches and providing a synonym exists their accepted name will be adopted using the synonyms file - covering misalignments in identification between the two databases.


## BOLD exports
Using BOLD’s Public Data Portal [API](http://boldsystems.org/index.php/resources/api?type=webservices) genera are retrieved one genus at a time and saved to the allocated folder (`BOLD_exports/genera.tsv`).
To acquire as much information as possible, the [FASTA files](https://en.wikipedia.org/wiki/FASTA_format) consisting of sequences holds all possible fields, including but not limited to Process ID, Species Name, Markercode, Genbank Accession, Catalognumber, Researchers, Geographic site, and Nucleotides of each species.
Reducing storage requirements, all files are archived in a single zip file.


## Fasta files
Iterating over every downloaded file from BOLD, sequence data is compared against species from the NSR. Subgenera will be filtered out creating a file with as many accepeted names as possible (`FASTA_files/match.fasta`). Mismatches against the NSR, provided they hold no known synonym, are copied to a seperate list (`FASTA_files/mismatch.fasta`).
Depending on user settings, a subset of fields can be made to covert the tab seperated data to FASTA format.



