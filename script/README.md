<!-- ABOUT THE DIRECTORY -->
# Scripts

The script folder contains scripts in Python (extension: .py), SQL (extension: .sql), and R Markdown (extension: .Rmd). Scripts are used to obtain public reference specimen data and sequence records from BOLD (Python), search out and visualize the overlap / gaps between BOLD and specimen records readily available at Naturalis Biodiversity Center (R Markdown), and the creation of a relational database (SQL)

- [BOLD export script](custom_databases.py)
- [Visualization script](custom_databases.Rmd)
- [Database schema](schema.sql)


<!-- Description of script files -->
## Description of script files
This README.md gives a brief description of each script file. Documentation of code within the scripts is available for both Python and R Markdown.

### custom_databases.py
-----------------------
The python script is used to obtain public reference data from the BOLD database. It harvests the scientific notation of accepeted taxa, including synonyms and expected species, from the NSR input files. Extracted taxonomy is used, by means of genera, to retrieve matching specimen data and sequence records from BOLD. Filtered on a geographic site, accepted names from the NSR are adopted on matching synonyms. The script is divided into multiple functions (blocks of code), each devoted to a specific area of the process. A description of each functions' use and the classification of arguments is provided with the first statements of each function, supported by in-line documentation. The functions include:

- nsrTaxonomy() - Captures and writes all binomial taxonomy to a CSV file
- nsrSynonyms() - Captures and writes all binomial synonyms to a CSV file.
- nsrGenera() - Extracts the unique genera from both taxonomy and synonym files.
- taxonParser() - Parses any taxonomic name into its elementary components.
- boldExtract() - Obtains public specimen data and sequence records for the list of genera.
- zipDirectory() - Compresses all BOLD output files into a zip file format.
- boldNSR() - Matches obtained specimen data to the reference species names.
- boldOutput() - Writes matching/non-matching records to their respesctive files.
- main() - Powers each function with their respective input.

### custom_databases.Rmd
------------------------
The R markdown file performs the steps needed to:
1. Obtain taxonomic information and Naturalis specimen records for selected taxa,
2. Create a data structure capable of providing highly visual representations
and at the same time maintaining integrity of each data set’s origin,
3. Search out and visualize the overlap / discrepancies between obtained public
reference data and records readily available at Naturalis Biodiversity Center.

It retrieves the higher taxa of species from the NSR, as well as classification of all taxa present in the NCBI taxonomy database. Occurence records of available Naturalis specimen data are retrieved for all NSR taxa. Molecular data from all sources are linked through NSR’s accepted names and synonyms to create a more streamlined data structure. At last, a visualisation of collected taxanomic information is performed which computes and draws reactive shiny filters through a collapsible d3js tree. The R Markdown file is divided into multiple segments, each able to be run independently (providing the necessary data sets have previously been loaded into the environment). A description for each segement is provided with the first statements before its code block, supported by in-line documentation. The segments of code include:

- libraries - Loads external libraries (download of packages not included).
- globals - Defines global variables that are used throughout the file.
- datasets - Loads the respective input data sets (NSR taxa, BOLD records).
- nsrSynonyms - Matches NSR synonyms to respective indexed species, and updates its output file.
- nsrBackbone - Retrieves higher classification of NSR taxa from the NSR.
- natCoverage - Obtains matching species occurrence records from Naturalis specimen data.
- tree_ncbi - Obtains classification of species as present in the NCBI taxonomy database.
- species_markers - Consolidates the BOLD and Naturalis specimen records into one data set.
- tree - Creates the taxonomic backbone of NSR taxa, accompanied by information on their presence in either of the collected specimen data sets.
- tree-visualisation - Visualizes the taxonomic data (tree) through a collapsible Reingold-Tilford tree diagram, aided by various charts for analysis of its selected taxa.

### schema.sql
--------------
Represents the logical configurations (blueprint) for the creation of the SQLite database. Able to be populated with the project's output files (see `results/`).
