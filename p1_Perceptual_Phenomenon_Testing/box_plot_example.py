# First, the required packages are imported.
# * The `pyplot` submodule from the **matplotlib** library, a python 2D
# plotting library which produces publication quality figures.  
# * The **numpy** library for efficient numeric-array manipulation.
import matplotlib.pyplot as plt
import numpy as np

# The data is read from a csv (comma-separated values) file, it's organized in
# nine columns. The data represent 100 measures surveyed from 3 different
# cities on 3 different days.
cities = np.genfromtxt('MyData.csv',
                       delimiter=',',
                       dtype=np.float32)

# Single Horizontal Whisker Plot
# ------------------------------

# For this we will use the seventh column and save it as `data`. The plot is
# created by `boxplot()`, this generic plot is latter customized, adjusting the
# appearance of every element.
plt.figure()
data = cities[:,6]
plot1 = plt.boxplot(data,               
                    vert=False,         # creates horizontal box
                    widths = 0.2,       # width of the box
                    patch_artist=True)  # enable further customizatons

plt.setp(plot1['boxes'],            # customise box appearance
         color='DarkMagenta',       # outline colour
         linewidth=1.5,             # outline line width
         facecolor='SkyBlue')       # fill box with colour

plt.setp(plot1['whiskers'],         # customise whisker appearence
         color='DarkMagenta',       # whisker colour
         linewidth=1.5)             # whisker thickness

plt.setp(plot1['caps'],             # customize lines at the end of whiskers 
         color='DarkMagenta',       # cap colour
         linewidth=1.5)             # cap thickness

plt.setp(plot1['fliers'],           # customize marks for extreme values
         color='Tomato',            # set mark colour
         marker='o',                # maker shape
         markersize=10)             # marker size

plt.setp(plot1['medians'],          # customize median lines
         color='Tomato',            # line colour
         linewidth=1.5)             # line thickness

# ---

# Plotting Vertical Box Plots
# ---------------------------

# Now we are going to plot the 9 boxes for the columns next to each other
# using customized colours and tick labels. The array `box_colours` is a list
# of colours to fill the boxes. Again, the `boxplot()` routine creates the
# plot. The positions of each box are determined by the `locations` array.
box_colours = ['SkyBlue', 'LightGreen', 'Plum',
              'SkyBlue', 'LightGreen', 'Plum',
              'SkyBlue', 'LightGreen', 'Plum']

locations = [1, 2, 3, 5, 6, 7, 9, 10, 11]

plt.figure()
plot2 = plt.boxplot(cities, 
                    widths=0.7,
                    notch=True,             # adds median notch
                    positions=locations,    # boxes locations
                    patch_artist=True,
                    )

# The next code draws horizontal grid lines, to make it easier to read the data
plt.grid(axis='y',          # set y-axis grid lines
        linestyle='--',     # use dashed lines
        which='major',      # only major ticks
        color='lightgrey',  # line colour
        alpha=0.7)          # make lines semi-translucent

# Now we will fill each box in a different colour
for box, colour in zip(plot2['boxes'], box_colours):
    plt.setp(box, color='DarkMagenta', 
             linewidth=1.5, 
             facecolor=colour)

# Customize the `whiskers`, `caps`, `fliers` and `medians` just as in the
# previous example
plt.setp(plot2['whiskers'], color='DarkMagenta', linewidth=1.5)
plt.setp(plot2['caps'], color='DarkMagenta', linewidth=1.5)
plt.setp(plot2['fliers'], color='OrangeRed', marker='o', markersize=10)
plt.setp(plot2['medians'], color='OrangeRed', linewidth=1.5)

# Now we set the tick labels and rotate them, add the y-axis label, the title
# and display the plot.
names = ['City A', 'City B', 'City C',
         'City A', 'City B', 'City C',
         'City A', 'City B', 'City C']

plt.xticks(locations,               # tick marks
           names,                   # labels
           rotation='vertical')     # rotate the labels

plt.ylabel('Data')                  # y-axis label
plt.title('Box and Whisker Plots')  # plot title
                    
plt.show()                          # render the plot
