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
from taxon_parser import TaxonParser, UnparsableNameException
from zipfile import ZipFile
from os.path import basename
import urllib3
import csv
import os
import argparse
import pandas as pd
import unicodedata
import re
import zipfile
import io

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
    """ Captures and writes all binomial taxonomy to a CSV file.

    Loads a NSR Taxonomy export CSV file into a Pandas Dataframe, utf-8
    encoded. All taxonomic names for species-level records are sent to
    taxonParser() to parse them into their elementary components.
    Indexes and writes returned species to a CSV file.

    Arguments:
        taxonomyFile: NSR Taxonomy export read as Pandas Dataframe
        taxonomy: Dataframe with capture group on species-level records
        taxonList: List item containing parsed taxonomic components
        parser: Object containing the name parts and original taxon
        index: Numerical counter
        binomial: Binomial nomenclature of taxon
        authorship: Authorship of taxon
    Return:
        taxonList: List of all extracted taxonomy (Species + Authority)
    """
    # Input file
    taxonomyFile = pd.read_csv(args.indir+"/"+args.infile1, header=2,
                               sep="\t", encoding="utf8")

    # Parse taxonomic names into their elementary components
    taxonomy = taxonomyFile.loc[taxonomyFile['rank'] == 'soort']
    taxonList = []
    for taxon in taxonomy['scientific_name']:
        parser = taxonParser(taxon)
        if not parser or parser is False:
            pass
        else:
            taxonList.append(parser)

    # Write taxonomy to file
    index = 0
    with io.open(par_path+"/results/nsr_species.csv", "w", encoding="utf-8") as outfile:
        outfile.write('"species_id","species_name","identification_reference"\n')
        for i in taxonList:
            binomial = ' '.join(str(i).split()[:2])
            authorship = ' '.join(str(i).split()[2:])
            outfile.write('%s,%s,"%s"\n' % (index, binomial, authorship))
            index += 1

    return taxonList


def nsrSynonyms():
    """ Captures and writes all binomial synonyms to a CSV file.

    Loads a NSR Synonyms export CSV file into a Pandas Dataframe, utf-8
    encoded. All synonyms with respective taxons of scientific notation
    are sent to taxonParser() to parse them into their elementary
    components. Returned synonyms and taxons are paired in a dictionary,
    and written to a CSV file.

    Arguments:
        synonymsFile: NSR Synonyms export read as Pandas Dataframe
        synonyms: Dataframe with capture group on scientific notations
        synonymDict: Dictionary containing parsed taxonomic components
        synonym: Object containing the name parts and original synonym
        taxon: Object containing the name parts and original taxon
    Return:
        synonymList: List of all synonyms (binomial name + authority)
        synonymDict: Dictionary pairing synonym with respective taxon
    """
    # Input file
    synonymsFile = pd.read_csv(args.indir+"/"+args.infile2, header=2,
                               sep="\t", encoding="utf8")

    # Parse taxonomic names into their elementary components
    synonyms = synonymsFile.loc[synonymsFile['language'] == 'Scientific']
    synonymDict = {}
    for synonym, taxon in zip(synonyms['synonym'], synonyms['taxon']):
        synonym = taxonParser(synonym)
        taxon = taxonParser(taxon)
        if not taxon or synonym is False or taxon is False:
            pass
        else:
            synonymDict[synonym] = taxon

    # Write dictionary to file
    with io.open(par_path+"/results/nsr_synonyms.csv", "w", encoding="utf-8") as outfile:
        outfile.write("synonym_name,taxon\n")
        for key, value in synonymDict.items():
            outfile.write('"%s","%s"' % (key, value))
            outfile.write("\n")

    return [*synonymDict], synonymDict


def nsrGenera(taxonList, synonymList):
    """ Extracts the unique genera from both taxonomy and synonym lists.

    Combines the scientific names of obtained taxonomy and synonyms to
    one list, filtering out empty lines. Selects all unique genera.

    Arguments:
        species: Scientific notation of all species and known synonyms
    Return:
        generaList: List of all unique genera
    """
    species = list(filter(None, sorted(taxonList + synonymList)))
    generaList = [i.split()[0] for i in species]
    generaList = list(dict.fromkeys(generaList))
    return generaList


def taxonParser(taxon):
    """ Parse any taxonomic name into its elementary components.

    Used library is a pure Python adaptation of the GBIF Java
    name-parser library. Taxonomic names are parsed into their
    elementary components. Genus, specific epithet, and authors are
    concatenated for all binomial names and returned. For any name
    that can not be parsed, an UnparsableNameException is thrown.

    Arguments:
        parser: Object to parse
        parsed_name: Object containing the name parts and original taxon
    Return:
        scientific_name: Concatenation of binomial name and authorship
    """
    parser = TaxonParser(taxon)
    scientific_name = ""

    try:
        parsed_name = parser.parse()
        if parsed_name.isBinomial() is True:
            scientific_name = str(parsed_name.genus) + " " + str(parsed_name.specificEpithet)
            if str(parsed_name.combinationAuthorship) != "<unknown>":
                scientific_name += " " + str(parsed_name.combinationAuthorship)
            elif str(parsed_name.basionymAuthorship) != "<unknown>":
                scientific_name += " " + str(parsed_name.basionymAuthorship)
            else:
                scientific_name = False
        else:
            pass
    except UnparsableNameException:
        pass

    return scientific_name


def bold_extract(genera):
    """ Obtains public sequence data for a list of genera.

    Downloads records using BOLD's Public Data Portal API. Base URL for
    data retrieval is appended to each genus from the NSR genera list.
    Genera are retrieved one genus at a time and saved as TSV file.

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
    """ Compresses all BOLD output files into a zip file format. """
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
    """ Match obtained sequence records to the reference species names.

    Iterates over every output file from BOLD and compares sequence data
    to the list of species from the NSR. Subgenera will be filtered out
    creating a file with as many accepeted names as possible. Mismatches
    against the NSR are copied to a seperate list.

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
                                bold_identification = re.sub('[()]', '', str(line['identification_reference']))
                                bold_name = line['species_name'] + " " + bold_identification
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
    """ Writes matching/non-matching records to respesctive file.

    Opens respective output file and appends the record. Ensures each
    file contains a header row.

    Arguments:
        output_header: List of record fields to be emitted
        f: Outputfile, either match or mismatch depending on parameter
    """
    # Write header to output files (executes only one time per run)
    global output_header
    if output_header is False:
        for temp in (args.outfile1, args.outfile2):
            with io.open(args.outdir2+"/"+temp, mode="a", encoding="utf-8") as f:
                for key, value in line.items():
                    f.write('%s\t' % (key))
                f.write("\n")
        output_header = True

    # Write sequence data, for each record
    with io.open(args.outdir2+"/"+file, mode="a", encoding="utf-8") as f:
        for key, value in line.items():
            f.write('%s\t' % (value))
        f.write("\n")


def main():
    """ Main logic. Powers each function with their respective input. """
    # Create clean output files
    open(args.outdir2+"/"+args.outfile1, 'w').close()
    open(args.outdir2+"/"+args.outfile2, 'w').close()

    # Run functions
    taxonList = nsrTaxonomy()
    synonymList, synonymDict = nsrSynonyms()
    generaList = nsrGenera(taxonList, synonymList)
    bold_extract(generaList)
    zip_directory(args.outdir1, zip_path)
    bold_nsr(taxonList, synonymList, synonymDict, zip_path)
    print("Done")
main()
