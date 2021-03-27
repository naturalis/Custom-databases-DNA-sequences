# Custom-databases-DNA-sequences
Bioinformatics project [B19017-555](https://docs.google.com/spreadsheets/d/1AiUIVsS8jiUE9vmRnP7cdBWNx_Q59V0t9vxko5U51es/edit#gid=420939240)
 (Applicant: B. van der Hoorn)


<!-- ABOUT THE PROJECT -->
## Project goals

To help assess the biodiversity of Dutch freshwater and saltwater areas, this project aims to develop a system to (periodically) obtain missing reference data from public databases, and perform an initial assessment of both its quality and reliability. An export from the Dutch Species Register (NSR) contains the scientific notation of species of interest, including synonyms and expected species, (see `data/NSR_exports/`). Obtaining curated reference material from the Naturalis Biodiversity Center and a snapshot of public sequence data, resulting data is used to:

- Search out and visualize the overlap / gaps between the obtained Public Sequence Data (BOLD) and a reference provided by the Naturalis Biodiversity center, in correlation to the NSR.
- Create a data structure capable of providing highly visual representations and at the same time maintaining integrity of each data set’s origin.
- Assess the quality and reliability of public sequence data.

### Workflow
![Workflow](https://github.com/naturalis/Custom-databases-DNA-sequences/blob/master/script/Flowchart.png?raw=true)


<!-- GETTING STARTED -->
## Getting Started

Instructions and requirements to get a local copy up and running, see [INSTALL file](INSTALL.md)

### Part 1: Downloading public specimen data and sequence records

Navigate to the installation directory and run the python script. Parameters are by default set to a file/directory within a local github clone.

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

Classification and analyses of the data set can be achieved by following the execution of code laid out in the Rmarkdown file using ie. R Studio, see [script](script).

1. Open RStudio and install the necessary packages:
```
install.packages(c("rmarkdown","data.table","taxizedb","myTAI","tidyr","shiny","DT","plyr","dplyr","stringr","d3Tree","billboarder","nbaR"))
```

2. Go to "File" on the top left corner, click "Open file" / "Open script" and navigate to the `script/custom_databases.Rmd` file.

3. Set the working directory to the script source (in RStudio: Session > Set working directory > To source file location).

4. In the top right corner of the opened script file, click "run app" if you're on RStudio. Alternatively, run the script line by line using ctrl+SHIFT+ENTER for each chunk of code. Note: chunks of code can be run independently as long as the necessary data is loaded into the environment.

5. After running the script, or the tree-vizualition segment, a window will pop up, and you can click "open in browser" to run the shiny app in your default browser.


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
