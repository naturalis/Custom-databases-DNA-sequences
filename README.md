# Custom-databases-DNA-sequences
Bioinformatics project [B19017-555](https://docs.google.com/spreadsheets/d/1AiUIVsS8jiUE9vmRnP7cdBWNx_Q59V0t9vxko5U51es/edit#gid=420939240)
 (Applicant: B. van der Hoorn)



<!-- ABOUT THE PROJECT -->
## Project goals

Using an export from the Dutch Species Register (NSR)  with a full taxonomic breakdown, including synonyms and expected species, (see `data/NSR exports/`) running the script allows for its list of species to be compared against matching genera extracted using BOLD's Public Data Portal API. Filterting to Dutch records only and writing matching/non-matching sequence data to their allocated files. Periodically performed, a custom database can be created and kept up to date regarding new or changes to the public sequence data of interest.

### Workflow
![Workflow](https://github.com/naturalis/Custom-databases-DNA-sequences/blob/master/script/Flowchart.png?raw=true)



<!-- GETTING STARTED -->
## Getting Started

Instructions and requirements to get a local copy up and running. See also the [INSTALL file](INSTALL.md)

### Prerequisites

* Python version 3.8.3

The following libraries are used:

  * Argparse 1.1
  * csv 1.0
  * Pandas 1.0.5
  * urllib3 1.25.9

### Installation

Clone the latest version from GitHub (recommended):  
`git clone https://github.com/naturalis/Custom-databases-DNA-sequences`  

Or, download the latest [source code](script/custom_databases.py)

### Usage

Navigate to the installation directory and run the python script.

```sh
python custom_databases.py
```

Using any of the optional user arguments allows for the user to change the input/output destination of the files and folders. Example:

```sh
python custom_databases.py -input_dir ../data/NSR_exports -outfile1 match.fasta -outfile2 mismatch.fasta -output_dir1 ../data/BOLD_exports -output_dir2 ../data/FASTA_files
```



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

