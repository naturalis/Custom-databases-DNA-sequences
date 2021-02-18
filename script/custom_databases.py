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
#   Software prerequisites: (see readme for versions and details).
# ====================================================================

# Import packages
import urllib3
import csv
import os
import argparse
import pandas as pd
import unicodedata
import re
import zipfile
import io
from zipfile import ZipFile
from os.path import basename

# Set global variables
http = urllib3.PoolManager()
csv.field_size_limit(100000000)
par_path = os.path.abspath(os.path.join(os.pardir))
pd.options.mode.chained_assignment = None
output_header = False

# User arguments
parser = argparse.ArgumentParser()
parser.add_argument('-indir', default=par_path+"/data/NSR_exports",
                    help="Input folder: NSR export directory")
parser.add_argument('-infile1', default="NSR_taxonomy.csv",
                    help="Input file 1: NSR taxonomy export")
parser.add_argument('-infile2', default="NSR_synonyms.csv",
                    help="Input file 2: NSR synonyms export")
parser.add_argument('-outdir1', default=par_path+"/data/BOLD_exports",
                    help="Output folder 1: BOLD export directory")
parser.add_argument('-outdir2', default=par_path+"/data/FASTA_files",
                    help="Output folder 2: Result data directory")
parser.add_argument('-outfile1', default="match.tsv",
                    help="Output file 1: Matching records")
parser.add_argument('-outfile2', default="mismatch.tsv",
                    help="Output file 2: Non-matching records")
args = parser.parse_args()
zip_path = args.outdir1+"/BOLD_export.zip"


def nsrTaxonomy():
    """
    Loads a NSR Taxonomy CSV file into a Pandas Dataframe. Non-ascii
    characters for each column (primairly identification references)
    will be decoded. Binomial Nomenclature and Authority for each
    species-level record is extracted via regex and saved to a list.
    Brackets are removed from the references for the sake of consistency.
    Arguments:
        taxonomyFile: CSV file read as Pandas Dataframe
        df_Taxonomy: Dataframe with capture group, on species-level records
    Return:
        taxonomyList: List of all extracted taxonomy (Species + Authority)
    """
    # Input file
    taxonomyFile = pd.read_csv(args.indir+"/"+args.infile1, header=2, sep="\t")

    # Decode non-ascii characters
    for column in taxonomyFile:
        taxonomyFile[column] = taxonomyFile[column].astype(str).apply(
            lambda x: unicodedata.normalize('NFKD', x).encode(
                'ascii', 'ignore').decode("utf-8"))

    # Extract Binomial Nomenclature and Authority for species-level records
    df_Taxonomy = taxonomyFile.loc[taxonomyFile['rank'] == 'soort']
    df_Taxonomy['scientific'] = df_Taxonomy['scientific_name'].str.extract(
        r'(\b[A-Z][a-z]*\b\s\b[a-z]*\b\s\(?\b[A-Z][a-z]*\b.*,\s\d{4}\)?)')
    df_Taxonomy = df_Taxonomy.dropna()
    taxonomyList = list(dict.fromkeys(df_Taxonomy['scientific']))
    taxonomyList = [re.sub(r"[()]", "", taxon) for taxon in taxonomyList]

    return taxonomyList


def nsrSynonyms(species):
    """
    Loads a NSR Synonyms CSV file into a Pandas Dataframe. Non-ascii
    characters for each column (primairly identification references)
    will be decoded. Synonyms of scientific notation are extracted
    via regex for each known taxonomy, and saved to a list. Brackets
    are removed from the references for the sake of consistency. Taxon
    and respective synonym are subsequently paired in a dictionary.
    Arguments:
        synonymsFile: CSV file read as Pandas Dataframe
        df_Synonyms: Dataframe containing only scientific synonyms
        synonymsMatch: Dataframe with capture group, on known taxonomy
        synonymsIndex: List of indexes of each extracted synonym
        synonymsRows: Dataframe reuniting synonym with respective taxon
    Return:
        synonymsList: List of all extracted synonyms (Species + Authority)
        synonymsDict: Dictionary pairing synonym with taxon notation
    """

    # Input file
    synonymsFile = pd.read_csv(args.indir+"/"+args.infile2, header=2, sep="\t")

    # Decode special characters
    for column in synonymsFile:
        synonymsFile[column] = synonymsFile[column].astype(str).apply(
            lambda x: unicodedata.normalize('NFKD', x).encode(
                'ascii', 'ignore').decode("utf-8"))

    # Extract synonyms
    df_Synonyms = synonymsFile.loc[synonymsFile['language'] == 'Scientific']
    #synonymsMatch = df_Synonyms[df_Synonyms['taxon'].isin(species)]
    df_Synonyms['species'] = df_Synonyms['synonym'].str.extract(
        r'(\b[A-Z][a-z]*\b\s\b[a-z]*\b\s\(?\b[A-Z][a-z]*\b.*,\s\d{4}\)?)')
    synonymsMatch = df_Synonyms.dropna()
    synonymsList = list(dict.fromkeys(synonymsMatch['species']))
    synonymsList = [re.sub(r"[()]", "", synonym) for synonym in synonymsList]

    # Pair synonyms with respective taxon
    synonymsIndex = synonymsMatch['species'].index.values.tolist()
    synonymsRows = df_Synonyms.loc[synonymsIndex, :]
    synonymsRows['taxonFiltered'] = synonymsRows['taxon'].str.extract(
        r'(\b[A-Z][a-z]*\b\s\b[a-z]*\b\s\(?\b[A-Z][a-z]*\b.*,\s\d{4}\)?)')
    synonymsRows = synonymsRows.dropna()
    synonymsDict = synonymsRows.set_index('synonym')['taxonFiltered'].to_dict()
   
    # Write dictionary to file
    with open(args.indir+"/synonyms_extract.csv", "w") as f:
        f.write("Synonym,Taxon\n")
        for key, value in synonymsDict.items():
            f.write('"%s","%s"' % (key, value))
            f.write("\n")

    return synonymsList, synonymsDict


def nsrOutput(species, synonyms):
    """
    Stores all unique species, index, as a csv file. Combines the
    scientific names of obtained taxonomy and synonyms to one list.
    Selects all unique genera to be used in the BOLD pipeline.
    Arguments:
        name: Binomial nomenclature of species
        identification: Identification reference of species
        combined: Scientific notation of all species and known synonyms
    Return:
        genera: List containing all unique genera
    """
    # Write species to file
    index = 0
    with open(par_path+"/results/nsr_species.csv", "w") as f:
        f.write('"species_id","species_name","identification_reference"\n')
        for i in species:
            name = ' '.join(str(i).split()[:2])
            identification = ' '.join(str(i).split()[2:])
            f.write('%s,%s,"%s"\n' % (index, name, identification))
            index += 1  

    # Combine species with their known synonyms
    combined = sorted(species + synonyms)

    # Select genera of each species and known synonym
    genera = [i.split()[0] for i in combined]

    # Drop duplicates from list
    genera = list(dict.fromkeys(genera))

    return genera


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
    # Appending BOLD's base URL to each genera from the NSR list
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
        with open(args.outdir1+"/"+name+".tsv", "wb") as fcont:
            fcont.write(r.data)


def zip_directory(folder_path, zip_path):
    """
    Compresses all BOLD Sequence Data output files into a zip file format.
    """
    # Create a ZipFile object
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
    # Open genera file from zip
    with zipfile.ZipFile(zip_path) as z:
        for file in z.namelist():
            if not os.path.isdir(file):
                # Read genera file
                filename = os.fsdecode(file)
                if filename.endswith(".tsv"):
                    with z.open(filename, 'r') as zfile:
                        zfile = io.TextIOWrapper(io.BytesIO(zfile.read()), errors='ignore')
                        tsvreader = csv.DictReader(zfile, delimiter="\t")
                        # Read each record
                        for line in tsvreader:
                            # Filter on Geographical site
                            if (line['country'] == "Netherlands"):
                                # Decode special characters
                                bold_identification = re.sub('[()]', '', line['identification_reference'])
                                bold_name = line['species_name'] + " " + bold_identification
                                bold_name = bold_name.encode('raw_unicode_escape').decode("utf-8")
                                bold_name = unicodedata.normalize('NFKD', bold_name).encode('ascii', 'ignore').decode("utf-8")
                                # Compare BOLD with NSR species names
                                if (bold_name in species):
                                    bold_output(args.outfile1, line)
                                # Check for synonyms, apply accepted name
                                elif (bold_name in synonyms):
                                    for synonym, taxon in syn_dict.items():
                                        synonym = ' '.join(synonym.split()[:2])
                                        if synonym == line['species_name']:
                                            taxon = ' '.join(taxon.split()[:2])
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
    emitted records contain sequence data.
    Arguments:
        output_header: List of record fields to be emitted
        f: Outputfile, either match or mismatch depending on parameter
    """
    # Write header to output files (executes only one time per run)
    global output_header
    if output_header is False:
        for temp in (args.outfile1, args.outfile2):
            with open(args.outdir2+"/"+temp, "a") as f:
                for key, value in line.items():
                    f.write('%s\t' % (key))
                f.write("\n")
        output_header = True

    # Write sequence data, for each record
    with open(args.outdir2+"/"+file, "a") as f:
        for key, value in line.items():
            f.write('%s\t' % (value))
        f.write("\n")


def main():
    """
    Main logic. Powers each function with their respective input.
    """
    # Create clean output files
    open(args.outdir2+"/"+args.outfile1, 'w').close()
    open(args.outdir2+"/"+args.outfile2, 'w').close()

    # Run functions
    taxonomyList = nsrTaxonomy()
    synonymsList, synonymsDict = nsrSynonyms(taxonomyList)
    generaList = nsrOutput(taxonomyList, synonymsList)
    bold_extract(generaList)
    zip_directory(args.outdir1, zip_path)
    bold_nsr(taxonomyList, synonymsList, synonymsDict, zip_path)
    print("Done")
main()
