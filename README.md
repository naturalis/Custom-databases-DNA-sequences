# Custom-databases-DNA-sequences
Bioinformatics project [B19017-555](https://docs.google.com/spreadsheets/d/1AiUIVsS8jiUE9vmRnP7cdBWNx_Q59V0t9vxko5U51es/edit#gid=420939240)
 (Applicant: B. van der Hoorn)



<!-- ABOUT THE PROJECT -->
## Project goals

Using an export from the Dutch Species Register (NSR) with a full taxonomic breakdown, including synonyms and expected species, (see `data/NSR_exports/`) running the python script allows for its list of species to be compared against matching genera extracted using BOLD's Public Data Portal API. Filterting to Dutch records only and writing matching/non-matching sequence data to their allocated files (see `data/FASTA_files/`). These are then, subsequently, used for the following:

- To create a more streamlined data structure which allows us to track all information of the species of interest between the various datasets. Making it possible to execute more elaborate querries due to its linked structure.
- To search out and visualize the overlap / gaps between the obtained Public Sequence Data (BOLD) and its reference provided by the Dutch Species Register (NSR).

### Workflow
![Workflow](https://github.com/naturalis/Custom-databases-DNA-sequences/blob/master/script/Flowchart.png?raw=true)



<!-- GETTING STARTED -->
## Getting Started

Instructions and requirements to get a local copy up and running. See also the [INSTALL file](INSTALL.md)

### Part 1: Downloading public sequence data of interest

#### Prerequisites
* Python version 3.8.3

The following libraries are used:

  * Argparse 1.1
  * csv 1.0
  * Pandas 1.0.5
  * urllib3 1.25.9
 
#### Installation

Clone the latest version from GitHub (recommended):  
`git clone https://github.com/naturalis/Custom-databases-DNA-sequences`  

Or, download the latest [source code](script/custom_databases.py)

#### Usage

Navigate to the installation directory and run the python script.

```
Usage: custom_databases.py [OPTIONS]

Optional arguments:
  -h, --help                Display this message
  -input_dir                Input file directory
  -infile1                  NSR Taxonomy input file
  -infile2                  NSR Synonym input file
  -output_dir1              Public sequence data output directory
  -output_dir2              Outfile1/2 output directory
  -outfile1                 Matching records
  -outfile2                 Non-matching records
```

Using any of the optional user arguments allows for the user to change the input/output destination of the files and folders. Example:

```sh
python custom_databases.py -input_dir ../data/NSR_exports -outfile1 match.fasta -outfile2 mismatch.fasta -output_dir1 ../data/BOLD_exports -output_dir2 ../data/FASTA_files
```

### Part 2: Data classification & analyses

#### Prerequisites
* R version 4.0.3

The following libraries are used:

  * rmarkdown 2.6
  * taxizedb 0.3.0
  * myTAI 0.9.2
  * tidyr 1.1.2
  * shiny 1.5.0
  * DT 0.17
  * plyr 1.1.2
  * dplyr 1.0.3
  * d3tree 0.2.2
  * billboarder 0.2.8

#### Usage

Classification and analyses of the dataset can be achieved by following the execution of code laid out in the Rmarkdown file using ie. R Studio.
Download the latest [source code](script/custom_databases.Rmd) if no copy of the respository has been made.



<!-- CHANGELOG -->
## Changelog

See the [changelog](CHANGES.md) for a list of all notable changes made to the project.



<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.



<!-- Additional remarks -->
## Additional remarks
### Related projects:
- [B19009-560](https://docs.google.com/spreadsheets/d/1ZPdazHaaNi29q7tpruxqp_EYCcA-hNZnx6c2bqjQaq8/edit#gid=420939240) - Barcoding database status reporting tool (Applicant: A. Speksnijder)
- [B19011-560](https://docs.google.com/spreadsheets/d/16KGTSKY5OtizeFCqsoc0rCyX7rQfVMGZabcmB-D2rkA/edit#gid=420939240) - Local custom database creator in the galaxy (Applicant: A. Speksnijder)

