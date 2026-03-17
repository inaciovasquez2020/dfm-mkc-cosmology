import matplotlib.pyplot as plt

def plot_chain(chain,labels=None):

    n = chain.shape[1]

    for i in range(n):
        plt.figure()
        plt.plot(chain[:,i])
        if labels:
            plt.title(labels[i])
        plt.xlabel("step")
        plt.ylabel("value")

    plt.show()
