#!/bin/bash
data_directory='/Users/Ilja/projects/galiphy/data'
# Get latest HPO database. genes to phenotypes format.
wget -P $data_directory -N http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt

# Remove first line of the downloaded file
echo "$(tail -n +2 $data_directory/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt)" > $data_directory/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt