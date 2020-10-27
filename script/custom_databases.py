#!usr/bin/python

# Title:         custom_databases.py
# Description:   Retrieve, filter and combine (public) sequence data

# Custom Databases
#   The Custom Databases script uses a full taxonomic breakdown of
#   species, including synonyms and expected species, stored
#   in the Dutch Species Register (NSR). Its export is used to
#   harvest matching species with sequence data from public
#   databases like BOLD and NCBI. This data will be filtered before
#   being compared to and merged with existing internal databases.
#
#   Usage: custom_databases.py [options]
#
#   Optional arguments:
#     -h, --help                Display this message.
#     -input_dir                Input file directory
#     -infile1                  NSR Taxonomy input file
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
par_path = os.path.abspath(os.path.join(os.pardir))


# Optional user arguments
parser = argparse.ArgumentParser()
parser.add_argument('-input_dir', default=par_path+"/data/NSR_exports"
                    , help="NSR export files directory")
parser.add_argument('-infile1', default="NSR_taxonomy.csv",
                    help="Input file: NSR taxonomy export")
parser.add_argument('-infile2', default="NSR_synonyms.csv",
                    help="Input file: NSR synonym export")
parser.add_argument('-outfile1', default="match.fasta",
                    help="Output file: Matching records")
parser.add_argument('-outfile2', default="mismatch.fasta",
                    help="Output file: Missmatch records")
parser.add_argument('-output_dir1', default=par_path+"/data/BOLD_exports",
                    help="Public sequence data output directory")
parser.add_argument('-output_dir2', default=par_path+"/data/FASTA_files",
                    help="Outfile1/2 output directory")
args = parser.parse_args()


def nsr_taxonomy():
    """
    Loads a CSV file into a Pandas Dataframe. Isolates
    species and genera consecutively, and converts them
    into their respective list.
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

    # Filter out genus only records
    scientific = df[df['rank'] != "genus"]

    # Isolate species (cut off at subsp.)
    species = scientific['scientific_name'].apply(lambda x: ' '.join(x.split()[:2]))

    # Add genus only records to copy of species
    genus_only = df[df['rank'] == "genus"]
    data = pd.concat([genus_only['scientific_name'], species])

    # Isolate all genera
    genera = data.str.split(" ", 1).str.get(0)

    # Define DataFrames, drop duplicates, and covert to List
    dataframes = [species, genera]
    [i.drop_duplicates(inplace=True) for i in dataframes]
    species_list, genera_list = [i.values.tolist() for i in dataframes]

    return species_list, genera_list


def nsr_synonyms():
    """
    Loads a CSV file into a Pandas Dataframe. Selects all
    scientific synonyms, and selects the synonym and
    accepted taxons. Species names are cut off at subsp.
    before synonym with respective taxon are paired
    in a dictionary. All unique synonyms are stored in
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


def bold_nsr(species, synonyms, syn_dict):
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
    # Ensure record contains sequence data
    if bool(line.get('nucleotides')) == True:
        # Define record fields to use
        header = ['processid', 'species_name', 'markercode']
        # Open respective outputfile from parameter
        with open(args.output_dir2+"/"+file, "a") as f:
            # Combine record fields in fasta format and append to file
            f.write(">"+'|'.join([line.get(field) for field in header]))
            f.write('|'+str(line.get('genbank_accession')) if line.get('genbank_accession') else '|none')
            f.write('|'+str(line.get('catalognum'))+'\n' if line.get('catalognum') else '|none\n')
            f.write(str(line.get('nucleotides'))+'\n')
    else:
        pass
    
    # TSV
    #with open(args.output_dir2+"/"+file, "a") as f:
    #    for key, value in line.items():
    #        f.write('%s\t' % (value))
    #    f.write("\n")
    

def main():
    """
    Main logic. Powers each function with their respective input.
    """
    # Create clean output files
    open(args.output_dir2+"/"+args.outfile1, 'w').close()
    open(args.output_dir2+"/"+args.outfile2, 'w').close()

    # Run functions
    species, genera = nsr_taxonomy()
    synonyms, syn_dict = nsr_synonyms()
    bold_extract(genera)
    bold_nsr(species, synonyms, syn_dict)
    print("Done")
main()
