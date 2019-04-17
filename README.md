# Galiphy online tool
<img src="/static/galiphy_logo.png" width=56px>

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

This montly download is done with *wget* and removing the first line from the downloaded text file. In addition, the number of genes are counted in the text file and saved in a file "*GENES_IN_HPO.txt*" in the same folder as "*app.py*". 
The database textfile directory should be in a textfile named "*db_directory.txt*",
the "*tool11.py*"" script retrieves the HPO database "*ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt*" from this directory. 
The docker container needs to be restarted every time the database is updated. See Docker paragraph.

*Current local file: /home/galiphy/updateHPOdb.sh 
Current database folder: /home/galiphy/data/*


### Built With

* Flask
* Python 2.7
* Html
* CSS

### Docker environment

The tool is built in the Docker environment. 

**Build docker image**

A) 
```
docker build -t galiphy .
```

**Restart docker container**

B)
```
docker stop cont_ID_galiphy
```
C)
```
docker rm cont_ID_galiphy
```
D)
```
docker run -d --name "cont_ID_galiphy" -p 5001:5001 -v "/home/galiphy:/home/galiphy" -v "/var/www/galiphy/output:/usr/src/app/output" galiphy
```
*The first -v indicates the directory of the files that are outside the container, in this case, the HPO database and the number of genes in it.
the second -v indicates the files that are written in the output folder within the container, are placed outside the container. A directory that is cleaned periodically.*

**Rebuilding the docker image**

Step A, B and C, then remove the image:
```
docker rmi -f galiphy
```
Finally, step A and D




## Reference

See [reference page](https://www3.cmbi.umcn.nl/galiphy/reference).

### Online access

Running on [cmbi.umcn.nl/galiphy](https://www3.cmbi.umcn.nl/galiphy)

### Versioning

Version 1.1 on 07-11-2018 > [tool11.py](tool11.py)

Version 1.0 on 10-10-2018 > [tool10.py](tool10.py)

### Authors

* **Ilja van Hoek :octocat:** - *Building and maintenance* - [contact](https://www3.cmbi.umcn.nl/galiphy/contact)
* **Martijn Huijnen** - *Supervision* - [contact](https://www.radboudumc.nl/en/people/martijn-huijnen/comparative-genomics)

