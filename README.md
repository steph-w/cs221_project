# CS 221: Latent Dirichlet Allocation for Detecting Topics in AI Research
## Max Drach (mdrach) Stephanie Wang (steph17)
### /data

### /kmeans

### /lda

#### /lda.py 
This python program runs latent Dirichlet allocation on a collection of text documents in the specified folder. Change the path at **line 193** to the path at which the text documents are located. The code we provide already points to the data path:
<code> data = read_data("../data/trivial/") </code>
To adjust the number of topics *k*, the number of *iterations*, and the initial alpha and beta, adjust the parameters on **line 196**:
<code> assignments = lda.run(num_topics=4, iterations=20, alpha_init=0.01, beta_init=0.01) </code>

#### /lda_with_visual.py
This python program 
### /utils