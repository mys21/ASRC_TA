import numpy as np
import h5py
import os
import matplotlib.pyplot as plt

f = h5py.File('default_datafile_2.hdf5','r')

avg_data = np.array(f['Average'])

bg = np.mean(avg_data,axis=0)

for i in range(len(avg_data[:,0])):
	avg_data = avg_data - bg

fig1,ax = plt.subplots()
ax.plot(avg_data)
fig1.show()

f.close()
