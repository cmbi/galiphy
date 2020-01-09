## Run Galiphy script in terminal
# From this python script, the tool can be run in the terminal
import os,errno
import argparse
import sys
import pandas as pd
from argparse import RawDescriptionHelpFormatter
from tool11 import tool11

def openfile(file):
    file_list = open(file).read().splitlines()
    return file_list

def run_tool(listgenes, HPOfilename, output_path):
    phen_df, genescores_df, numbers, outfile_phen, outfile_genes, outfile_phenpergenes, accepted_df, dropped_df, Q, missing, dupli = tool11(listgenes, HPOfilename, output_path)
    #print "missing:", missing, len(missing), "dupli:", len(dupli), "dropped:", len(dropped_df), "accepted:", len(accepted_df)
    # information about the variables are also send to the html pages, as the result page has different sections shown dependent on the clients input.
    number_dropped = len(dropped_df)
    number_accepted = len(accepted_df)
	

if __name__ == "__main__":

    ## Parse arguments
    parser = argparse.ArgumentParser(description="Galiphy:\n"
                                                 "======================================================================\n\n"
                                                 "- Short explanation of the tool.\n"
                                                 "Goal: \t\t Find new candidate genes associated with your cellular function of interest.\n"
                                                 "Input:\t\t List of genes that share a cellular function and a phenotype database called HPO.\n"
                                                 "Algorithm:\t Based on the enrichment of phenotypes among the input genes. Steps:\n"
                                                 "\t1: All phenotypes in the HPO database are scored.\n"
                                                 "\t2: All genes in the HPO database are scored based on the phenotype frequency.\n"
                                                 "Conclusion: Genes with high scores probably have a similar cellular function as \nyour input genes and are phenotypically linked to your genes of interest.\n\n"
                                                 "- How to get the latest phenotype database.\n"
                                                 "Get the HPO database, two methods:\n"
                                                 " a) Run the getHPOdb.sh script. It requires wget to be installed.\n"
                                                 " b) Manually download the file from the url in the getHPOdb.sh script. Delete the first line of the text file.\n"
                                                 "\n"
                                                 "- Needed:\n"
                                                 "\t\t- Input file (.txt) with a list of genes in a single column.\n"
                                                 "\t\t- The latest HPO database (.txt). \n"
                                                 "\t\t- A existing directory for the output files (ending with /).\n\n"
                                                 "- Python (v2.7) non-standard libraries:\n"
                                                 "\t\tmygene\n"                                               
                                                 "- Example command:\n"
                                                 "python terminal_galiphy.py -l /Users/Ilja/projects/terminal_galiphy/input.txt \\\n-o /Users/Ilja/projects/terminal_galiphy/output/ \\\n-d /Users/Ilja/projects/terminal_galiphy/HPO_08-01-2020.txt\n\n"
                                                 "For more information, tutorial and example, visit online version of the tool:\n\t https://www3.cmbi.umcn.nl/galiphy",

                                     formatter_class=RawDescriptionHelpFormatter)


    parser.add_argument("-l", "--list_genes", required=True, help="List of input genes file")
    parser.add_argument("-d", "--database", required=True, help="HPO database file")
    parser.add_argument("-o", "--output", required=True, help="Directory for output files")
    #parser.add_argument("-v", "--verbose", required=False, help="Verbose mode")
    
    args = parser.parse_args()

    listgenes = openfile(args.list_genes)

    print("Input file: {}".format(args.list_genes))

    print args.database
    print args.output

    run_tool(listgenes, args.database, args.output)

