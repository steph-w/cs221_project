# Plots categories from lda and k-means

import matplotlib.pyplot as plt
import tkinter
#import seaborn

def plot_trends_over_time(assignments, timelist):
    print assignments
    print timelist
    plt.yticks(range(max(assignments.values())+1))
    x = range(len(assignments))
    plt.plot(x, assignments.values(), marker='o')
    plt.xticks(x, timelist, rotation=30)
    plt.margins(0.1, 0.1)
    plt.xlabel("Source")
    plt.ylabel("Topic Category")
    plt.title("Topic Categories Over Time")
    plt.grid(True)
    plt.show() #block=False)
    #raw_input("<Enter to close>")

def plot_topic_top_terms(topic_top_terms):
    for k in range(len(topic_top_terms)):
        terms = sorted(topic_top_terms[k], key=topic_top_terms[k].get)[::-1]
        values = [topic_top_terms[k][t] for t in terms]
        plt.bar(range(len(values)), values)
        plt.xticks(range(len(terms)), terms, rotation=30)
        plt.xlabel("Word")
        plt.ylabel("Probability")
        plt.title("Top %d words for Topic %d" % (len(terms),k))
        plt.grid(True)
        plt.show()
