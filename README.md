# A Semi-Supervised Approach to Citation Matching in the Humanities
EPFL Spring 2018 Semester Project

Supervised by Matteo Romanello, Digital Humanities Laboratory, EPFL

## Description
Citation matching in the humanities publication is not an easy task. This project adopts a step-by-step approach to match references in the [Linked Books](https://dhlab.epfl.ch/page-127959-en.html) dataset. Due to the large scale of data available, the search space is required to be reduced to efferently find the match. 

* The approach starts with matching partial references with full references in one document based on some general rules. 

* Secondly, with the help of hash functions, the full references are grouped together into a global candidate group. 

* Finally, semi-supervised learning method is applied to address the problem of lacking ground truth and classify within the candidate group whether two citations point to the same document. 

* Manually annotating the global candidate group is needed for the evaluation of this approach.


## Reposotory Structure
The reposotory is organized as following:

* **material**: presentation sildes and report

* **code**: main code and notebook
	* Local Clustering:
		* Local Clustering.ipynb
	* Hash Matching:
		* getfullref.py: get "full" references
		* hashfunction.py: definition of hash function
		* hashgenerate.py: generate hashes for all full references
		* hashsplit.py: change the structure of reference and its hashes
		* hashmatch.py: match references based on hashes
		* Hash Stat.ipynb: show some statistics of returned references of each hash
		* Hash Sample.ipynb: apply hash black list and select samples for annotating
	* Global Matching:
		* Global Matching.ipynb
	* Support Modules:
		* dbmodel.py: modules for database
		* readref.py: read and store reference into desired structure	


## Reference
* Colavizza, Giovanni, Matteo Romanello, and Frédéric Kaplan. 
  "[The references of references: a method to enrich humanities library catalogs with citation data](https://link.springer.com/article/10.1007/s00799-017-0210-1)." 
  *International Journal on Digital Libraries* (2017): 1-11.
* Fedoryszak, Mateusz, et al. "[Methodology for evaluating citation parsing and matching](https://www.researchgate.net/profile/ukasz_Bolikowski/publication/235984473_Methodology_for_Evaluating_Citation_Parsing_and_Matching/links/0c960528f569f125cd000000.pdf)." Intelligent Tools for Building a Scientific Information Platform. Springer, Berlin, Heidelberg, 2013. 145-154.
* Fedoryszak, Mateusz, and Łukasz Bolikowski. 
  "[Efficient Blocking Method for a Large Scale Citation Matching](http://www.dlib.org/dlib/november14/fedoryszak/11fedoryszak.html)." 
  *D-Lib Magazine 20*, no. 11/12 (2014).
* Fedoryszak, Mateusz, Dominika Tkaczyk, and Łukasz Bolikowski. "[Large scale citation matching using Apache Hadoop](https://arxiv.org/pdf/1303.6906v1.pdf)." arXiv preprint arXiv:1303.6906 (2013).