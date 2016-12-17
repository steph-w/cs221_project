# CS 221: Latent Dirichlet Allocation for Detecting Topics in AI Research
#### by Max Drach (mdrach), Stephanie Wang (steph17)
## Commands we Ran
Start here if you want to simply run LDA on a preprocessed dataset:  

1. Run <code> lda_with_visual.py </code>, modifying **line 213** to point to a pre-existing preprocessed dataset from the <code>/data</code> folder

Alternatively to run data preprocessing before LDA:  

1. To obtain the pdf files from [JAIR.ORG](https://www.jair.org/contents.html), run <code>extract_pdfs.py</code> in utils
2. To clean the pdf files, run <code>clean_raw_pdf_files.py</code> and <code>remove_non_letters.py</code> and in utils
3. Run <code>obtain_and_remove_stopwords.py</code> to remove the stopwords and most frequent and unfrequent terms in the text documents
4. At this point we have a folder of documents that we want to perform LDA on. We run <code> lda_with_visual.py </code>, modifying **line 213** to point to the path containing the documents to obtain the assignments for the documents to a topic as well as result visuals.  

## Code Documentation
### /data
##### /cs229_papers
This folder contains the dataset of all cs229 papers.
##### /journal_ai_research_abstracts
This folder contains the dataset of all AI research paper abstracts.
##### /journal_ai_research_papers
This folder contains the dataset of all AI research papers. 
***
### /kmeans.py
This python program runs our K-means baseline on a collection of text documents in the specified folder. Change the path at **line 8** to point to the path containing the documents. 
To change the number of clusters, *k*, change <code>n_clusters</code> at **line 21**.
The output of this program is the top words associated with each cluster topic. 
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
#### /data_processing
##### /clean_abstracts.py
This program cleans the AI journal abstracts, removing improperly formed text and residual html code.

##### /clean_raw_pdf_files.py
This program cleans the AI pdf abstracts, removing improperly formed text.

##### /extract_abstracts.py
This program extracts the abstracts from JAIR.ORG
##### /extract_pdfs.py
This program extracts the PDFs from JAIR.ORG

##### /lowercase_and_remove_punct.py
This program turns all characters to lowercase and removes punctuation


##### /obtain_and_remove_stopwords.py
This program removes all stopwords, and the most frequent and infrequent terms

##### /pdf_to_text.py
This program converts the raw PDF files to text

##### /remove_non_letters.py
This program removes all non-letter characters in the text

#### /plotter.py
This program contains two functions. The first plots the topic assignment for each document, and the second plots the probabilities of the top ten words that have the highest probability of being associated with the topic.