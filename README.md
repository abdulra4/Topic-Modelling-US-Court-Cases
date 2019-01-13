# Topic-Modelling-US-Supreme-Court-Cases

Latent Dirichlet Allocation
---------------------------

Latent Dirichlet Allocation (LDA) is an example of a topic model used to
classify text in a document to a particular topic. It builds a topic per
document model and words per topic model, modelled as Dirichlet distributions.
The unsupervised probabilistic model is then used to discover underlying themes
in a document. LDA assumes that: (i) documents are produced from a mixture of
topics and each document belongs to each of the topics to a certain degree; and
(ii) each topic is a generative model which generates words of the vocabulary
with certain probabilities.

Implementation
--------------

The code I prepare to implement the LDA model requires the following data
wrangling and pre-processing steps:
* Wrangling: Extracting and parsing through court documents to prepare a clean
text of opinions released by the court for a case.
* Tokenising: Splitting the text into sentences and the sentences into words,
then lowercasing the words and removing punctuations.
* Standardising: All words that have fewer than two characters are removed;
stopwords are removed; words in the third person are changed to first person and
verbs; and future tenses are changed into present and words are reduced to
their root form.

Following the steps above, the prepared data is fed into a modelling module from
 the gensim library.

Optimisation Methods
--------------------

To optimise the preparation and modelling of the topics, I use a variety of
single processing, multiprocessing and distributed computing approaches at
different stages of the topic modelling process. This is compared and contrasted
with alternative approaches that could be used, evaluating the type of
computational bottlenecks, the difficulty of implementation, and memory
considerations, as well as other limitations encountered.

Caselaw Access Project (CAP)
----------------------------

CAP is a Harvard Law School Library Innovation Lab Project that has collated all
official, book-published United States case law --- every volume designated as
an official report of decisions by a court within the United States. It includes
all state courts, federal courts, and territorial courts for American Samoa,
Dakota Territory, Guam, Native American Courts, Navajo Nation, and the Northern
Mariana Islands and dates back to 1658. Each volume has been converted into
structured, case-level data broken out by the majority and dissenting opinion,
with human-checked metadata for party names, docket number, citation, and date.
It, however, does not include new cases as they are published but is up to date
as of June 2018.

As the data is categorised by state, we can access 52 XML dumps which provide
data for each state. The implementation below uses the cases for the states
Arizona, District of Columbia, Illinois and Massachusetts as a sample set.

Results
-------

Overall, running the complete processes for one state, we can reduce the total
run-time by approximately 40 per cent. These results are particularly helpful
when used at scale.

Useful Links
------------
[Case Law Access Project] (https://case.law/)
[Gensim Library] (https://radimrehurek.com/gensim/index.html)
[Abhijeet Kumar] (https://github.com/abhijeet3922/Topic-Modelling-on-Wiki-corpus)
[Susan Li] (https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21)
