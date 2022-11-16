import FlowCal
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os

# function to make FACS graphs
# files: [list] of fcs file paths (str)
# labels: [list] of Labels for each sample (str)
# colour: [list] of colours to be assigned for the respective sample
# y axis: [Boolean] referring to the presence of the y-axis

def facs_graph(files, labels, colour, y_axis):
    # reads first file
    data = FlowCal.io.FCSData(files[0])
    data = FlowCal.transform.to_rfi(data) # transforms arbitrary fluorescence units to Relative Fluoresence Units
    mean = FlowCal.stats.mean(data, channels=['FITC-A']) # calculates the population mean
    mean = [mean]
    data_1 = data[:, ['FITC-A']] # Extracts the channel with green fluorescence
    
    # if you have more fcs files to plot in the same graph
    if len(files) != 1:   
        for file in files[1:]:
            label_f = os.path.splitext(file)
            data_f = FlowCal.io.FCSData(file)
            data_f = FlowCal.transform.to_rfi(data_f)
            mean_f = FlowCal.stats.mean(data_f, channels=['FITC-A'])
            data_f = data_f[:, ['FITC-A']]
            data_1 = np.append(data_1, data_f) # have all the samples in a single column (long data)
            mean.append(mean_f)
    
    df = pd.DataFrame(data_1, columns=["FITC-A"]) # convert numpy array to a Pandas dataframe to use in seaborn
    
    # create a label for each of the samples in the concatentated df.
    label = []
    for i in labels:
        for x in range(10000):
            label.append(i)
    
    df["Label"]=label
    
    # set figure size
    fig, ax = plt.subplots(figsize=(5, 15))
    # set graph styles
    sns.set_style("white")
    sns.set_style("ticks")
    sns.set_context("talk")

    # plot each species
    graph = sns.histplot(df, y="FITC-A", 
                        log_scale=True, 
                        element='poly',
                        palette=colour,
                        hue = "Label",
                        alpha=0.3)
    
    # set graph configurations
    graph.set_ylim(1.4, 5000)
    graph.set_xlim(0, 1000)
    plt.xticks([0, 500, 1000])
    
    # plot the population means on the graph
    for i in range(len(labels)):
        plt.axhline(mean[i][0], color=colour[i], linestyle=":")
        
    # to label the y axis
    if y_axis == True:
        plt.ylabel("Relative Fluoresence Units (RFU)")
    else:
        plt.tick_params(labelleft=False, left=False)
        graph.set(ylabel=None)
    
    return graph
