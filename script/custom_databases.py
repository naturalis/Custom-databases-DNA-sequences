#!usr/bin/python

# Title:         custom_databases.py
# Description:   Retrieve, filter and combine (public) sequence data

# Custom Databases
#   The Custom Databases script uses a scientific notation of
#   species, including synonyms and expected species, stored
#   in the Dutch Species Register (NSR). Its export is used to
#   harvest matching species with sequence data from the
#   Barcode of Life Data (BOLD) database.
#
#   Usage: custom_databases.py [options]
#
#   Optional arguments:
#     -h, --help		Display this message
#     -input_dir                Input file directory
#     -infile1      		NSR Taxonomy input file
#     -infile2                  NSR Synonym input file
#     -output_dir1              Public sequence data output directory
#     -output_dir2              Outfile1/2 output directory
#     -outfile1                 Matching records
#     -outfile2                 Non-matching records
#
#   Software prerequisites: (see readme for versions and details).
# ====================================================================

# Import packages
import argparse
import os
import csv
import pandas as pd
import urllib3
import zipfile
import io
from zipfile import ZipFile
from os.path import basename
http = urllib3.PoolManager()
csv.field_size_limit(100000000)
par_path = os.path.abspath(os.path.join(os.pardir))
output_header = False

# Optional user arguments
parser = argparse.ArgumentParser()
parser.add_argument('-input_dir', default=par_path+"/data/NSR_exports",
                    help="NSR export files directory")
parser.add_argument('-infile1', default="NSR_taxonomy.csv",
                    help="Input file: NSR taxonomy export")
parser.add_argument('-infile2', default="NSR_synonyms.csv",
                    help="Input file: NSR synonym export")
parser.add_argument('-output_dir1', default=par_path+"/data/BOLD_exports",
                    help="Public sequence data output directory")
parser.add_argument('-output_dir2', default=par_path+"/data/FASTA_files",
                    help="Outfile1/2 output directory")
parser.add_argument('-outfile1', default="match.fasta",
                    help="Output file: Matching records")
parser.add_argument('-outfile2', default="mismatch.fasta",
                    help="Output file: Missmatch records")
args = parser.parse_args()
zip_path = args.output_dir1+"/BOLD_export.zip"


def nsr_taxonomy():
    """
    Loads a NSR taxonomy CSV file into a Pandas Dataframe, Isolates
    its species, and converts it into a list.
    Arguments:
        df: CSV file read as Pandas Dataframe
        scientific: Dataframe containing all species level data
        species: Isolated species taxonomy
        species_list: list of all unique species
    Return:
        List containing all unique species
    """
    # Load CSV as Pandas DataFrame
    # Define header row and seperator
    df = pd.read_csv(args.input_dir+"/"+args.infile1, header=2, sep="\t")

    # Filter out non species records
    scientific = df[df['rank'] != "genus"]

    # Isolate species (cut off at subsp.)
    species = scientific['scientific_name'].apply(lambda x: ' '.join(x.split()[:2]))

    # Drop duplicates
    species.drop_duplicates(inplace=True)

    # Convert Dataframe to Dictionary
    species_list = species.values.tolist()

    return species_list


def nsr_synonyms():
    """
    Loads a NSR synonym CSV file into a Pandas Dataframe and selects
    all scientific synonyms with their synonym and accepted taxons.
    Species names are cut off at subsp. before synonym with respective
    taxon are paired in a dictionary. All unique synonyms are stored in
    a seperate list for reference.
    Arguments:
        df: CSV file read as Pandas Dataframe
        scientific: Subset containing all scientific synonyms
        df1: Subset containing specified columns
        columns: List of dataframe columns
        synonym: All synonyms, cut off at subsp.
        taxon: All accepted taxons, cut off at subsp.
        df2: Synonyms and taxons combined
    Return:
        synonyms: List of all unique synonyms
        syn_dict: Dictionary pairing synonym with respective taxon
    """
    # Load CSV as Pandas DataFrame
    # Define header row and seperator
    df = pd.read_csv(args.input_dir+"/"+args.infile2, header=2, sep="\t")

    # Extract scientific synonyms
    scientific = df[df['language'] == "Scientific"]

    # Select specific columns
    df1 = scientific[['synonym', 'taxon']]

    # Isolate species for each column (cut off at subsp.)
    columns = list(df1.columns)
    synonym, taxon = [df1[i].apply(lambda x: ' '.join(x.split()[:2])).to_frame() for i in columns]
    df2 = synonym.join(taxon)

    # Create list of all unique synonyms
    synonym.drop_duplicates(inplace=True)
    synonyms = synonym['synonym'].values.tolist()

    # Convert Dataframe to Dictionary
    syn_dict = df2.set_index('synonym')['taxon'].to_dict()

    return synonyms, syn_dict


def nsr_combined(species, synonyms):
    """
    Combines the scientific names of obtained taxonomy and synonyms
    to one list. Subselects all genera.
    Arguments:
        genera: List of all unique genera
    Return:
        List containing all unique species and/or their genera
    """
    # Combine taxa
    species.extend(synonyms)
    species = sorted(set(species))

    # Subselect genera
    genera = [i.split()[0] for i in species]
    return species, genera


def bold_extract(genera):
    """
    Downloads all collected genera using BOLD's Public Data Portal API.
    Base URL for data retrieval is appended to each genus from the NSR list.
    Genera are retrieved one genus at a time and saved to the allocated folder.
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


def zip_directory(folder_path, zip_path):
    """
    Crompesses all BOLD Sequence Data output into a zip file format.
    """
    # create a ZipFile object
    with ZipFile(zip_path, mode='w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                # Filter on TSV files
                if filename.endswith(".tsv"):
                    # Create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath, basename(filePath))


def bold_nsr(species, synonyms, syn_dict, zip_path):
    """
    Iterating over every downloaded file from BOLD, sequence data is compared
    against species from the NSR. Subgenera will be filtered out creating a
    file with as many accepeted names as possible. Mismatches against the NSR
    are copied to a seperate list.
    Arguments:
        file: String, current filename (genus) from the BOLD downloads
        filename: String, decoding the filename from the filesystem encoding
        tsvreader: File (genus) read in a tab delimited matter
        line: Rows of the current file (genus)
    """
    # Loop over each genus(file) downloaded from BOLD
    print('Comparing sequence data to list of species...')
    # Open file from zip
    with zipfile.ZipFile(zip_path) as z:
        for file in z.namelist():
            if not os.path.isdir(file):
                # Read the file
                filename = os.fsdecode(file)
                if filename.endswith(".tsv"):
                    with z.open(filename, 'r') as zfile:
                        zfile = io.TextIOWrapper(io.BytesIO(zfile.read()), errors='ignore')
                        tsvreader = csv.DictReader(zfile, delimiter="\t")
                        # Filter for Dutch records only
                        for line in tsvreader:
                            if line['country'] == "Netherlands":
                                # Skip subgenus
                                if "." in str(line['species_name']):
                                    pass
                                # Compare genus to known species from NSR
                                elif line['species_name'] in species:
                                    bold_output(args.outfile1, line)
                                # Check for synonyms, apply accepted name
                                elif line['species_name'] in synonyms:
                                    for synonym, taxon in syn_dict.items():
                                        if synonym == line['species_name']:
                                            line['species_name'] = taxon
                                            bold_output(args.outfile1, line)
                                # Write missmatches to seperate file
                                else:
                                    bold_output(args.outfile2, line)
                    continue
                else:
                    continue


def bold_output(file, line):
    """
    Opens respective output file and appends the record. Ensures all
    emitted records contain sequence data. Specific fields to emit
    are stored in a list and will be combined, along with filtered
    fields, into a fasta header format corresponding with the data.
    Arguments:
        header: List of record fields to be emitted
        f: Outputfile, either match or mismatch depending on parameter
    """
##    # Fasta format
##    # Ensure record contains sequence data
##    if bool(line.get('nucleotides')) == True:
##        # Define record fields to use
##        header = ['processid', 'species_name', 'markercode']
##        # Open respective outputfile from parameter
##        with open(args.output_dir2+"/"+file, "a") as f:
##            # Combine record fields in fasta format and append to file
##            f.write(">"+'|'.join([line.get(field) for field in header]))
##            f.write('|'+str(line.get('genbank_accession')) if line.get('genbank_accession') else '|none')
##            f.write('|'+str(line.get('catalognum'))+'\n' if line.get('catalognum') else '|none\n')
##            f.write(str(line.get('nucleotides'))+'\n')
##    else:
##        pass

    # Tab Seperated
    global output_header

    # Write header to output files (executes only one time per run)
    if output_header is False:
        for temp in (args.outfile1, args.outfile2):
            with open(args.output_dir2+"/"+temp, "a") as f:
                for key, value in line.items():
                    f.write('%s\t' % (key))
                f.write("\n")
        output_header = True

    # Write sequence data, for each record
    with open(args.output_dir2+"/"+file, "a") as f:
        for key, value in line.items():
            f.write('%s\t' % (value))
        f.write("\n")


def main():
    """
    Main logic. Powers each function with their respective input.
    """
    # Create clean output files
    open(args.output_dir2+"/"+args.outfile1, 'w').close()
    open(args.output_dir2+"/"+args.outfile2, 'w').close()

    # Run functions
    species = nsr_taxonomy()
    synonyms, syn_dict = nsr_synonyms()
    nsr_species, nsr_genera = nsr_combined(species, synonyms)
    bold_extract(nsr_genera)
    zip_directory(args.output_dir1, zip_path)
    bold_nsr(nsr_species, synonyms, syn_dict, zip_path)
    print("Done")
main()
