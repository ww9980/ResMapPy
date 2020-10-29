import tkinter as tk
from tkinter import filedialog
import csv
import os
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.interpolate

x = []
y = []
z = []

root = tk.Tk()
root.withdraw()
root.lift()
filename = filedialog.askopenfilename(initialdir = "C:\Downloads",title = "Select file",filetypes = (("resmap files","*.RsM"),("all files","*.*")))

with open(filename,'r') as f:
    bulk = f.readlines()[13:]
    plots = csv.reader(bulk, delimiter=' ',skipinitialspace=True)
    for row in plots:
        x.append(float(row[7]))
        y.append(float(row[8]))
        z.append(float(row[2]))

xi, yi = np.linspace(-150,150, 500), np.linspace(-150, 150, 500)
xi, yi = np.meshgrid(xi, yi)
zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')
av = np.mean(z)
unif = str(round(100*(np.max(z) - np.min(z))/(2*av),3))
tsig = str(round(300*(st.stdev(z))/av,3))

fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 10
fig_size[1] = 8
plt.rcParams["figure.figsize"] = fig_size
colmap = cm.RdYlGn
colmap.set_over('#00091a')
colmap.set_under('#480000')

# plot
cs = plt.contourf(zi, [(0.95)*av,(0.95+0.1/13)*av,(0.95+0.2/13)*av,(0.95+0.3/13)*av,(0.95+0.4/13)*av,(0.95+0.5/13)*av,(0.95+0.6/13)*av,(0.95+0.7/13)*av,(0.95+0.8/13)*av,(0.95+0.9/13)*av,(0.95+1/13)*av,(0.95+1.1/13)*av,(0.95+1.2/13)*av,1.05*av],
             origin='lower', 
             extent=[-150,150,-150,150],
             cmap=colmap,
             extend='both')
plt.colorbar()
plt.axis('equal')
plt.xlim(150,-150)
plt.ylim(150,-150)
plt.xticks([])
plt.yticks([])
Resmap = os.path.basename(f.name)
plt.gcf().canvas.set_window_title(Resmap)
txt = Resmap + '\n\n' + 'Unif: ' + unif + '%' + '\n' + '3σ: ' + tsig + '%'
plt.figtext(0.15, 0.01, txt, horizontalalignment='left', fontsize=12)
plt.show()
f.close()