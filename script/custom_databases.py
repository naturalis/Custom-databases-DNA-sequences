#!usr/bin/python

# Title:         custom_databases.py
# Description:   Retrieve, filter and combine (public) sequence data

# Custom Databases
#   The Custom Databases script uses a full taxonomic breakdown
#   of species stored in the Dutch Species Register (NSR) and
#   harvests matching sequence data from public databases like
#   BOLD and NCBI. Public sequence data will be filtered before
#   compared and merged with existing internal databases.
#
#   Usage: custom_databases.py [options]
#
#   Optional arguments:
#     -h, --help		Display this message.
#     -input_dir                Input file directory
#     -infile1      		    NSR Taxonomy input file
#     -infile2                  NSR Synonym input file
#     -outfile1                 Matching records
#     -outfile2                 Non-matching records
#     -output_dir1              Public sequence data output directory
#     -output_dir2              Outfile1/2 output directory
#
#   Software prerequisites: (see readme for versions and details).
# ====================================================================

# Import packages
import argparse
import os
import csv
import pandas as pd
import urllib3
http = urllib3.PoolManager()
csv.field_size_limit(100000000)
dir_path = os.path.dirname(os.path.realpath(__file__))


# Optional user arguments
parser = argparse.ArgumentParser()
parser.add_argument('-input_dir', default=dir_path, help="Input directory")
parser.add_argument('-infile1', default="NSR_taxonomy.csv",
                    help="Input file: NSR taxonomy export")
parser.add_argument('-infile2', default="NSR_synonyms.csv",
                    help="Input file: NSR synonym export")
parser.add_argument('-outfile1', default="match.tsv",
                    help="Output file: Matching records")
parser.add_argument('-outfile2', default="mismatch.tsv",
                    help="Output file: Missmatch records")
parser.add_argument('-output_dir1', default="BOLD",
                    help="Public sequence data output directory")
parser.add_argument('-output_dir2', default=dir_path,
                    help="Compare output directory")
args = parser.parse_args()


def dutch_species_register():
    """
    Loads a CSV file into a Pandas Dataframe. Isolates
    species and genera consecutively, and converts
    them into their respective list.
    Arguments:
        df: CSV file read as Pandas Dataframe
        scientific: Dataframe containing all species level data
        species: Isolated species taxonomy
        genus_only: Dataframe containing all genus level data
        data: Species and genus level dataframes combined
        genera: Isolated genus taxonomy
        dataframes: list of all dataframes
        species_list: list of all unique species
        genera_list: list of all unique genera
    Return:
        Lists containing all unique species and genera
    """
    # Load CSV as Pandas DataFrame
    # Define header row and seperator
    df = pd.read_csv(args.input_dir+"/"+args.infile1, header=2, sep="\t")

    # Filter out genera only records
    scientific = df[df['rank'] != "genus"]

    # Isolate species (cut off at subsp.)
    species = scientific['scientific_name'].apply(lambda x: ' '.join(x.split()[:2]))

    # Add genera only records to copy of species
    genus_only = df[df['rank'] == "genus"]
    data = pd.concat([genus_only['scientific_name'], species])

    # Isolate all genera
    genera = data.str.split(" ", 1).str.get(0)

    # Define DataFrames, drop duplicates, and covert to List
    dataframes = [species, genera]
    [i.drop_duplicates(inplace=True) for i in dataframes]
    species_list, genera_list = [i.values.tolist() for i in dataframes]

    return species_list, genera_list


def bold_extract(genera):
    """
    Downloads all collected genera using BOLD's Public Data Portal API.
    Base URL for data retrieval is appended to each genus from the NSR list.
    A seperate BOLD folder for storage is created if non-existent. Genera
    are retrieved one genus at a time and saved to the allocated folder.
    Arguments:
        base_url: String, default URL for data retrieval using BOLD's API
        source_urls: List of all URL's to be retrieved
        counter: Integer to keep track of genus in source list
        url: String, url correlating to the selected genus
        r: HTTPResponse, variable for retrieving web-url's
        name: String containing name of current genus
    """
    # Prepare Web Service Endpoint for BOLD's Public Data Portal API
    # Appending BOLD's base URL to each genera from the NSR list.
    base_url = 'http://v4.boldsystems.org/index.php/API_Public/combined?taxon='
    source_urls = list(map(lambda x: "{}{}{}".
                           format(base_url, x, '&format=tsv'), genera))

    # Download sequence data from BOLD using list of url's
    print('Beginning sequence data retrieval...')
    counter = 0
    for url in source_urls:
        r = http.request('GET', url)
        name = genera[counter]
        counter += 1
        with open(args.output_dir1+"/"+name+".tsv", "wb") as fcont:
            fcont.write(r.data)


def bold_nsr(species):
    """
    Iterating over every downloaded file from BOLD, sequence data is compared
    against species from the NSR. Subgenera will be filtered out creating a
    file with as many accepeted names as possible. Mismatches against the NSR
    are copied to a seperate list.
    Arguments:
        taxonomy: File containing all species from the NSR
        species: Species file saved as list
        f1: Outputfile to contain matching species sequence data
        f2: Outputfile to contain missmatches between NSR and BOLD
        file: String, current filename (genus) from the BOLD downloads
        filename: String, decoding the filename from the filesystem encoding
        tsvreader: File (genus) read in a tab delimited matter
        line: Rows of the current file (genus)
    """

    # Open output files for writing
    f1 = open(args.output_dir2+"/"+args.outfile1, "w")
    f2 = open(args.output_dir2+"/"+args.outfile2, "w")

    # Loop over each genus(file) downloaded from BOLD
    print('Comparing sequence data to list of species...')
    for file in os.listdir(args.output_dir1):
        filename = os.fsdecode(file)
        if filename.endswith(".tsv"):
            with open(args.output_dir1+"/"+os.path.join(filename), errors='ignore') as tsvfile:
                tsvreader = csv.DictReader(tsvfile, delimiter="\t")
                # Filter for Dutch records only
                for line in tsvreader:
                    if line['country'] == "Netherlands":
                        # Skip subgenus
                        if "." in str(line['species_name']):
                            pass
                        # Compare genus to known species from NSR
                        elif line['species_name'] in species:
                            for key, value in line.items():
                                f1.write('%s\t' % (value))
                            f1.write("\n")
                        # Write missmatches to seperate file
                        else:
                            for key, value in line.items():
                                f2.write('%s\t' % (value))
                            f2.write("\n")
            continue
        else:
            continue

    # Close output files
    f1.close()
    f2.close()


def main():
    species, genera = dutch_species_register()
    bold_extract(genera)
    bold_nsr(species)
    print("Done")
main()
