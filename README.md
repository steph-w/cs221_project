# CS 221: Latent Dirichlet Allocation for Detecting Topics in AI Research
#### Max Drach (mdrach) Stephanie Wang (steph17)
## Commands we Ran
1. To obtain the pdf files from [JAIR.ORG](https://www.jair.org/contents.html), run <code>extract_pdfs.py</code> in utils
2. To clean the pdf files, run <code>clean_raw_pdf_files.py</code> and <code>remove_non_letters.py</code> and in utils
3. Run <code>obtain_and_remove_stopwords.py</code> to remove the stopwords and most frequent and unfrequent terms in the text documents
4. At this point we have a folder of documents that we want to perform LDA on. We run <code> lda_with_visual.py </code> on the path containing the documents to obtain the assignments for the documents to a topic. 
## Code Documentation
### /data
##### /cs229_papers
This folder contains the dataset of all cs229 papers.
##### /journal_ai_research_abstracts
This folder contains the dataset of all AI research paper abstracts.
##### /journal_ai_research_papers
This folder contains the dataset of all AI research papers. 
***
### /kmeans

***
### /lda

##### /lda.py 
This python program runs latent Dirichlet allocation on a collection of text documents in the specified folder. Change the path at **line 193** to the path at which the text documents are located. The code we provide already points to the data path:  

<code> data = read_data("../data/trivial/") </code>  

To adjust the number of topics *k*, the number of *iterations*, and the initial alpha and beta, adjust the parameters on **line 196**:  

<code> assignments = lda.run(num_topics=4, iterations=20, alpha_init=0.01, beta_init=0.01) </code>  

The output of running lda.py is a printed list of topic assignments for each text document.

##### /lda_with_visual.py
This python program also runs latent Dirichlet allocation on a collections of text documents in the specified folder.  
  
 Change the path at **line 213** to the path at which the text documents are located. The code we provide already points to the data path:  

 <code>data = read_data("../data/journal_ai_research_papers/split_by_article_clean")</code>  

 Unlike lda.py, lda_with_visual.py supplements the printed list of document to topic assignments with a visual of topic trends over time, graphs of the highest probability words that occur in a specific topic, and finally an interactive visual that shows the similarity distribution of the topics, as well as the most relevant words in each topic (for this visual to work launch in your browser, you must download the package found at [https://github.com/bmabey/pyLDAvis](https://github.com/bmabey/pyLDAvis)).

***
### /utils

***