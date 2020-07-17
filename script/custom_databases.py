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
#   Software prerequisites: (see readme for versions and details).
# ====================================================================

# Import packages
import os
import csv
import pandas as pd
import urllib3
http = urllib3.PoolManager()


def dutch_species_register():
    """
    Load csv file and extract genera.
    Arguments:
        df: csv file read as Pandas Dataframe
        genera: subset of Dataframe containing all genera
    Return:
        List containing all unique genera
    """
    # Making data frame
    # Header line: 2nd row; Seperator: tab; Loaded colums: 1st column
    df = pd.read_csv("testfile.csv", header=1, sep="\t", usecols=[0])

    # Remove species from binomial nomenclature
    genera = df.apply(lambda x: x.str.split().str[0])

    # Drop duplicates
    genera.drop_duplicates(keep=False, inplace=True)

    # Convert Pandas DataFrame into List
    genera_list = genera["wetenschappelijke naam"].values.tolist()
    return genera_list


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
    # Create BOLD subdirectory if it doesn't already exists
    if not os.path.exists('BOLD'):
        os.makedirs('BOLD')

    # Download sequence data from BOLD using list of url's
    print('Beginning sequence data retrieval...')
    counter = 0
    for url in source_urls:
        r = http.request('GET', url)
        name = genera[counter]
        counter += 1
        with open("BOLD/"+name+".tsv", "wb") as fcont:
            fcont.write(r.data)


def bold_nsr():
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
    # Load NSR species in list as reference
    taxonomy = open("taxonomy.txt", "r")
    species = taxonomy.read().split('\n')

    # Open output files for writing
    f1 = open("bold.tsv", "w")
    f2 = open("mismatch.tsv", "w")

    # Loop over each genus(file) downloaded from BOLD
    for file in os.listdir("BOLD/"):
        filename = os.fsdecode(file)
        if filename.endswith(".tsv"):
            with open("BOLD/"+os.path.join(filename), errors='ignore') as tsvfile:
                tsvreader = csv.reader(tsvfile, delimiter="\t")
                # Filter for Dutch records only
                for line in tsvreader:
                    if line[54] == "Netherlands":
                        # Skip subgenus
                        if "sp." in str(line[21]) or "var." in str(line[21]):
                            pass
                        # Compare genus to known species from NSR
                        elif line[21] in species:
                            f1.write(str(line)+"\n")
                        # Write missmatches to seperate file
                        else:
                            f2.write(str(line)+"\n")
            continue
        else:
            continue

    # Close output files
    f1.close()
    f2.close()


def main():
    genera = dutch_species_register()
    bold_extract(genera)
    bold_nsr()
    print("Done")
main()
