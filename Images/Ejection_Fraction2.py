#!/usr/bin/env python
import os
import visvis as vv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio as img
import scipy.ndimage as ndi


path = 'C:\\Users\\Public\\Pictures\\Sample Pictures\\video1.mp4'
reader = img.get_reader(path)
timing = []


for i, im in enumerate(reader):
    im = im[:,:,1]
    imgfilter = ndi.gaussian_filter(im, sigma=1)
    maskselect = np.where(imgfilter > 150, 1, 0)
    mask = ndi.binary_closing(maskselect)

    labels, nlabels = ndi.label(mask)
    lv = labels[500, 700]

    # lvMask = np.where(labels == lv, im, 0)
    # lmean = ndi.mean(im, labels, index=lv)

    nvoxels = ndi.sum(1, labels=labels, index=lv)
    timing.append(nvoxels)

    # print(lmean, nvoxels)
    # cent = ndi.center_of_mass(im, labels, index=lv)
    # plt.imshow(lvMask, cmap='rainbow')
    # plt.imshow(im, cmap='gray')
    # plt.scatter(cent[1], cent[0])
    # plt.show()


plt.plot(timing)
plt.ylabel('Volume (mm^3)')
plt.xlabel('Time in cardiac Cycle')
plt.title('Plot of Left Ventricular Volume over Time')
plt.show()


# Return index timing with max and min values
tmin = np.argmin(timing)
tmax = np.argmax(timing)

print(tmin, tmax)

# Calculate ejection fraction
vol = max(timing) - min(timing)
frac = vol / max(timing)
print(f'Est. ejection volume (mm^3): {vol}')
print(f'Est. ejection fraction: {frac*100:.02f}%')
