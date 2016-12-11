# Plots categories from lda and k-means

import matplotlib.pyplot as plt
import tkinter
#  import seaborn

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
    plt.show(block=False)
    raw_input("<Enter to close>")
