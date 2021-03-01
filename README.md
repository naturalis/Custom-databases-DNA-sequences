# Custom-databases-DNA-sequences
Bioinformatics project [B19017-555](https://docs.google.com/spreadsheets/d/1AiUIVsS8jiUE9vmRnP7cdBWNx_Q59V0t9vxko5U51es/edit#gid=420939240)
 (Applicant: B. van der Hoorn)



<!-- ABOUT THE PROJECT -->
## Project goals

Using an export from the Dutch Species Register (NSR) with a full taxonomic breakdown, including synonyms and expected species, (see `data/NSR_exports/`) running the python script allows for its list of species to be compared against matching genera extracted using BOLD's Public Data Portal API. Filtered on geographic site, accepted names from the NSR will be adopted on matching synonyms, before writing matching/non-matching sequence data to their allocated files (see `data/FASTA_files/`). Resulting files are, subsequently, used to:

- Create a data structure capable of providing highly visual representations and at the same time maintaining integrity of each data set’s origin.
- Search out and visualize the overlap / gaps between the obtained Public Sequence Data (BOLD) and a reference provided by the Naturalis Biodiversity center, in correlation to the NSR.
- Assess the quality and reliability of public sequence data.

### Workflow
![Workflow](https://github.com/naturalis/Custom-databases-DNA-sequences/blob/master/script/Flowchart.png?raw=true)
*The general workflow for retrieving sequence data from BOLD, in which corresponding specimen data with sequence records were obtained using an export from the NSR.*


<!-- GETTING STARTED -->
## Getting Started

Instructions and requirements to get a local copy up and running. See also the [INSTALL file](INSTALL.md)

### Part 1: Downloading public sequence data of interest

#### Prerequisites
* Python version 3.8.3

The following libraries are used:

  * argparse 1.1
  * csv 1.0
  * Pandas 1.0.5
  * re 2.2.1
  * urllib3 1.25.9
  * taxonparser 0.2.3
 
#### Installation

Clone the latest version from GitHub (recommended):  
`git clone https://github.com/naturalis/Custom-databases-DNA-sequences`  

Or, download the latest [source code](script/custom_databases.py)

#### Usage

Navigate to the installation directory and run the python script. Parameters are by default  set to a file/directory within a local github clone.

```
usage: custom_databases.py [-h] [-indir INDIR] [-infile1 INFILE1] [-infile2 INFILE2] [-outdir1 OUTDIR1] [-outdir2 OUTDIR2] [-outfile1 OUTFILE1] [-outfile2 OUTFILE2]

optional arguments:
  -h, --help          show this help message and exit
  -indir INDIR        Input folder: NSR export directory
  -infile1 INFILE1    Input file 1: NSR taxonomy export
  -infile2 INFILE2    Input file 2: NSR synonyms export
  -outdir1 OUTDIR1    Output folder 1: BOLD export directory
  -outdir2 OUTDIR2    Output folder 2: Result data directory
  -outfile1 OUTFILE1  Output file 1: Matching records
  -outfile2 OUTFILE2  Output file 2: Non-matching records
```

Using any of the optional user arguments allows for the user to change the input/output destination of the files and directories. Example of argument usage:

```sh
python custom_databases.py -indir ../data/NSR_exports -outdir1 ../data/BOLD_exports -outdir2 ../data/FASTA_files -outfile1 match.tsv -outfile2 mismatch.tsv
```

### Part 2: Data classification & analyses

#### Prerequisites
* R version 4.0.3

The following packages are used:

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

