# Galiphy online tool

## Summary
### Finding new candidate genes associated with molecular systems by computational screening for typical phenotypes.
This tool gives a prediction of candidate genes by scoring of phenotypes. This scoring is dependent on how typical each
phenotype is for the query of the client. Subsequently, genes are scored using the phenotype scores. The input is a 
list of genes of the client's interest, output are three tsv files which shows all scoring results. On the basis of these
files, the client can find information about candidate genes.

## Technical

### Prerequisites

See [requirements.txt](requirements.txt).

### Dependencies

Phenotype database downloaded monthly from [HPO](http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt)

### Built With

* Flask
* Python 2.7
* Html
* CSS

## Reference

See [reference page](https://www3.cmbi.umcn.nl/galiphy/reference).

### Online access

Running on [cmbi.umcn.nl/galiphy](https://www3.cmbi.umcn.nl/galiphy)

### Versioning

Version 1.1 on 07-11-2018 > [tool11.py](tool11.py)

Version 1.0 on 10-10-2018 > [tool10.py](tool10.py)

### Authors

* **Ilja van Hoek** - *Building and maintenance* - [contact](https://www3.cmbi.umcn.nl/galiphy/contact)
* **Martijn Huijnen** - *Supervision* - [contact](https://www.radboudumc.nl/en/people/martijn-huijnen/comparative-genomics)

