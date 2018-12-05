## Galiphy version 1.1
# This script imports HPO, and has the clients gene list as input.
# It calculates phenotype scores based on enrichment.
# Phenotypes are mapped back to their genes and gene scores are generated.
# Outputs are 3 tsv files which are written in the output folder. 

import os,errno
import pandas as pd
import mygene
import math
import numpy as np
from datetime import datetime


def handlinginput(infile):
    """
    Step 1: handling input
    Input:
    Raw input from the client
    - list of Entrez gene IDs, Entrez gene symbols or Ensembl ID

    Output:
    Dataframe with valid genes found in the clients input
    - [query] 

    This function prepares a dataframe of the input from the client.
    The imported tool 'mygene' generates a dataframe out of the raw gene list. 
    The duplicate genes and not found genes in the query list are stripped from the generated dataframe.
    They are put into lists. 
    """
    mg = mygene.MyGeneInfo()
    try: # if none of the query genes are recognized, return three empty lists so that tool does not run other functions.
        mygene_dict = mg.querymany(infile, df_index = True, returnall = True, as_dataframe=True,species='human', scopes="ensemblgene,symbol,entrezgene")
    except:
        return [], [], []
    try:
        idname_df = mygene_dict['out'][['_id', 'name', 'symbol']].drop_duplicates().dropna()
    except:
        idname_df = []
    dupli = mygene_dict['dup'] # genes that mygene noticed as duplicates in the query list
    missing = mygene_dict['missing'] # genes that mygene could not recognize in its database
    print "length mygeneinfo df:",len(idname_df)
    return idname_df, dupli, missing

def add10toHPOfile(query_df,HPOfile):
    """
    Step 2: checking with HPO

    In this function, a dataframe is made with HPO data.
    First, a False or True is added to the query genes based on  
    their occurence in HPO. The list of 'True-genes' is the query 
    with which will be continued in this script.
    Then, the other way around, it is checked whether the genes in the 
    HPO data are among the query list, an 1 
    is put into the last column of the HPO dataframe of that gene. 
    Otherwise, a 0 is added.
    
    input:
    The geneID list (coming from the only input in the tool)
    - [geneID]
    The HPO file
    - [geneID] [genename] [phen description] [phenID]
    
    output:
    DataFrame of HPO
    - [geneID] [genename] [phen description] [phenID] [query (1/0)]
    Length of the query
    - Q, integer
    
    """

    """example of one row in HPO file: 
    8192	CLPP	Aplasia/Hypoplasia of the cerebellum	HP:0007360"""

    HPO_df = pd.read_table(HPOfile, 
                                    header=0,
                                    names=['geneID', 'genename', 'description', 'phenID'],
                                    dtype = {'geneID' : str})
    
    """the input-list comes from a geneID converter, should convert to only 1 column with geneIDs"""
    print "query_df:\n",query_df
    queryinHPO_df = query_df['_id'].isin(HPO_df['geneID']) # generates a dataframe (True False) on index of query dataframe, whether query gene is in HPO
    query10 = pd.concat([query_df, queryinHPO_df.rename('isinHPO')], axis=1) # adds this new dataframe to the query dataframe (as last column)
    accepted_df = query10[query10['isinHPO']==True].iloc[:,:3] # split dataframe into a True df, i.e. algorithm continues with the accepted genes 
    dropped_df = query10[query10['isinHPO']==False].iloc[:,:3] # and a False df, these are shown to the client
    print '\n\naccepted:\n',accepted_df,'\ndropped:\n',dropped_df
    HPOinquery_df = HPO_df['geneID'].isin(accepted_df['_id']).map({True: 1, False: 0}) # make df with 1's and 0's of HPO genes that are (1) or arent (0) in clients query
    HPO10_df = pd.concat([HPO_df,HPOinquery_df.rename('query10')], axis=1) # add this 1/0 column to the HPO df
    return HPO10_df, len(accepted_df), accepted_df, dropped_df


def formula_lin_zerocorr(q, Q, nq, nQ):
    """
    This function is added in the 1.1 version of Galiphy. 
    When phenotypes had no occurences among the query genes, but because
    the zero is changed to 0.1, the phenotype score ends up to be positive.
    Since a positive score is not wanted for any phenotype that does not
    occur among the query genes, the score are lowered in this function.
    The zero correction is the score for q=0 and nq=1.
    Every time the q (frequency among query genes) is zero (and thus 0.1),
    the zero correction is substracted from the resulting score. This way,
    every PS of q=0 ends up to be negative (or zero, in case of q=0 nq=1).
    """
    
    if q == 0.1:
        zero_corr = math.log((0.1 / float(Q)) / float((1 / float(nQ))), 2)
    else:
        zero_corr = 0
    return math.log((q / float(Q)) / float((nq / float(nQ))), 2) - zero_corr


def scorephenotypes(HPO10_df, Q, output_phen, output_phenpergenes):
    """
    Step 3: Scoring the phenotypes

    Scoring of phenotypes according to Bayesian integration :
    (2)log((q/Q)/(nq/nQ))
    in which q = freq of phenotype among query genes, Q = no. of query genes
    nq =  freq of phenotype among non-query genes, nQ = no. of non-query genes
    n = freq of phenotype among HPO file, N = no. of genes in HPO file
    4 dictionaries are made, of which 3 are returned (see:output).
    phen10_dict = {phenID : [1, 1, 0 , 1, ...], ...} 
    Every number represents a gene with which the phenotype is associated.
    1: query gene, 0: non-query gene. (as is depicted in this whole script) 
    
    input:
    1) DataFrame of HPO 
    - [geneID] [genename] [phen description] [phenID] [query (1/0)]
    2) Length of the query
    - Q, integer
    3) Output filename of phenotype scores
    
    output:
    1) scoring_dict = phenID : [phen description, q, nq, n, phenscore]
    2) genestophen_dict = geneID : [phenID, phenID, phenID, ...]
    3) gene_dict = geneID : [genename, 1/0]
    CSV of scored phenotypes
    
    """
    

    gene_dict = { row[1] : [ row[2], row[-1] ] for row in HPO10_df.itertuples()} # {geneID : [genename, 1/0]}
    HPO_dict = { row[4] : row[3] for row in HPO10_df.itertuples()} # {phenID : phendescr}
    genestophen_dict = {k: g['phenID'].tolist() for k,g in HPO10_df.groupby("geneID")} # {geneID : [phenID, phenID, phenID, ...]}
    phen10_dict = {k: g['query10'].tolist() for k,g in HPO10_df.groupby("phenID")} # {phenID : [1, 1, 0 , 1, ...]}
    nQ = len(gene_dict) - Q # nQ & Q: parameters dependent of input query, len(gene_dict) = total genes; differs as HPO expands
    
    phenscores_dict = {}
    for phenID in phen10_dict:
        n = len(phen10_dict[phenID]) # total freq of phenotype
        q = sum(phen10_dict[phenID]) # freq of 1's (query genes) of phenotype
        nq = n - q # freq of non-query genes among phenotypes
        # zeroes in the formula give a mathematical error. Therefore,
        # frequencies of zero are changed to 0.1's
        if q == 0:
            q = 0.1
        if nq == 0:
            nq = 0.1
        # generating phenotype score for the phenotype
        phenscore = formula_lin_zerocorr(q,Q,nq,nQ)
        phenscores_dict[phenID] = [HPO_dict[phenID], q, nq, n, phenscore]
        
    phenscores_list = [[k]+v for k, v in phenscores_dict.items()] # change dictionary to list so that it can be turned into df
    phen_df = pd.DataFrame.from_records(phenscores_list, columns = ['Phenotype_ID','Description','q','nq','tot','Phenotype_score'])
    phen_df.sort_values(by="Phenotype_score", ascending=False, inplace=True)
    phen_df.reset_index(drop=True, inplace=True)
    phen_df.index += 1
    # Make df with all genes and all phenotypes associated with them with the phenotype scores and frequencies. For insight and generating gene scores later.
    phenpergenes_df = HPO10_df.merge(phen_df, left_on='phenID', right_on='Phenotype_ID', how='left').drop(['description', 'phenID'], axis=1).sort_values(by=['query10','genename', 'Phenotype_score'], ascending=[0, 1, 0])
    phenpergenes_df.reset_index(drop=True, inplace=True)
    phenpergenes_df.index += 1
    
    numbers = "\n Q(query genes) = \t%i \n nQ(non-query genes) =\t%i \n N(genes in HPO) = \t%i"%(Q,nQ,(Q+nQ))
    print numbers
    phen_df.to_csv(output_phen,sep='\t')
    phenpergenes_df.to_csv(output_phenpergenes,sep='\t')
    return phenscores_dict, genestophen_dict, gene_dict, phen_df, phenpergenes_df, numbers


def scoregenes(phenscores_dict, genestophen_dict, gene_dict, output_genes):
    """
    Step 4: Scoring the genes

    In this function, the scores of the phenotype belonging to a gene are 
    summed, resulting in a genescore. It loops through every key in genestophen_dict
    and loops through the list of its values, the phenotypes. During the looping,
    the score of the gene is adjusted according to each phenotype-score 
    (found in phenscores_dict). 
    
    input:
    1) phenscores_dict = phenID : [phen description, q, nq, n, score]
    2) genestophen_dict = geneID : [phenID, phenID, phenID, ...]
    3) gene_dict = geneID : [genename, 1/0]
    4) output filename of scoring genes
    5) 'y'/'n' make files out of resulting scoring DataFrame 
    
    output:
    1) DataFrame genescores_df
    - [geneID] [genename] [query 1/0] [gene_score]
    CSV of scored genes
    """
    genescores_dict = {}
    for geneID in genestophen_dict: 
        genescore = 0
        for phenID in genestophen_dict[geneID]:
            genescore += phenscores_dict[phenID][-1]
        genescores_dict[geneID] = round(genescore, 4)

    # List are made from each element in the gene dictionary so that
    # a genescore dataframe can be made from all the lists in which 
    # each list is a column.
    geneID_list = []
    genename_list = []
    query_list = []
    score_list = []
    for geneID in gene_dict:
        geneID_list.append(geneID)
        genename_list.append(gene_dict[geneID][0]) 
        query_list.append(gene_dict[geneID][-1])
        score_list.append(genescores_dict[geneID])

    genescores_df = pd.DataFrame.from_items([('Gene_ID',geneID_list),('Gene_name',genename_list),('Query',query_list),('Gene_score',score_list)])
    genescores_df.sort_values(by="Gene_score", ascending=False, inplace=True)
    genescores_df.reset_index(drop=True, inplace=True)
    genescores_df.index += 1
    genescores_df.to_csv(output_genes,sep='\t')
    return genescores_df

def openfile(file):
    with open(file, 'r') as readfile:
        for line in readfile:
            line = line.replace('\n','')
            print type(line)
            return line

def tool11(filehandle):
    """
    Requesthandler


    In this function all other function are called. Step 1 to 4.
    Also some output file names are generated.

    """

    
    HPOfilename = openfile('db_directory.txt')+"ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt"

    # Step 1: Query checking
    ## if none of the genes are valid human genes, the tool cannot be run 
    ## empty lists are returned and only the missing values are return to client
    query, dupli, missing = handlinginput(filehandle)
    if len(query) == 0: 
        return [], [], [],[], [], [],[], [], [], missing, []
    else:
        print "query not empty"
    print "query is:",query

    # Step 2: checking with HPO
    ## if none of the query genes are in the HPO database, the tool cannot be run
    ## empty lists are returned and only the empty accepted dataframe, 

    HPO_10, Q, accepted_df, dropped_df = add10toHPOfile(query,HPOfilename)
    if len(accepted_df) == 0:
        return [], [], [],[], [], [], accepted_df, dropped_df, [], missing, dupli
    else:
        print "accepted_df not empty"


    # preparing file names with dates so that they all have a unique name
    date = str(datetime.now())[:-7].replace(" ","_").replace(":","-")
    output_phen = 'output/Galiphy_v1_0_PhenotypeScores_'+date+'.tsv'
    output_genes = 'output/Galiphy_v1_0_GeneScores_'+date+'.tsv'
    output_phenpergenes = 'output/Galiphy_v1_0_PhenotypeScores_To_Genes_'+date+'.tsv'

    # Step 3: Score phenotypes
    phenscores_dict, genestophen_dict, gene_dict, phen_df, phenpergenes_df, numbers = scorephenotypes(HPO_10, Q, output_phen, output_phenpergenes)
    
    # Step 4: Score genes
    genescores_df = scoregenes(phenscores_dict, genestophen_dict, gene_dict, output_genes)


    print '\nPhenotype scoring results: (saved as "%s")\n'%output_phen[7:] 
    print '\n\nGene scoring results: (saved as "%s")\n'%output_genes[7:]
    return phen_df, genescores_df, numbers, output_phen, output_genes, output_phenpergenes, accepted_df, dropped_df, Q, missing, dupli

