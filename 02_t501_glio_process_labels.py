# -*- coding: utf-8 -*-


from google.colab import drive
drive.mount('/content/drive')

import nibabel as nib
import numpy as np
import os
import pathlib
import matplotlib.pyplot as plt

base_img_path = '/content/drive/MyDrive/TCIA/nnUNet/nnUNet_raw/Dataset501_Glioblastoma/labelsTr/'
tr_label_files = os.listdir(base_img_path)
tr_label_files.sort()
# print(tr_label_files)
print(len(tr_label_files))

for file in tr_label_files:

  file_name = base_img_path + file
  # Load image
  img = nib.load(file_name)
  print("-"*100)
  print ("Patient label file: ", file)

  # Store image as a numpy array
  img_data = img.get_fdata()

  # Check array min, max and unique values for image label values
  print("Before label check")
  print(np.amin(img_data),np.amax(img_data))
  print(np.unique(img_data))

for file in tr_label_files:

  file_name = base_img_path + file
  # Load image
  img = nib.load(file_name)
  print("-"*100)
  print ("Patient label file: ", file)

  # Store image as a numpy array
  img_data = img.get_fdata()

  # Check array min, max and unique values for image
  print("Before label check")
  print(np.amin(img_data),np.amax(img_data))
  print(np.unique(img_data))

  # Where label is 4, reset it to 3 so nnUnet doesnt complain about non-consecutive labels
  img_data[(img_data == 4.0)] = 3

  # Check min, max and unique values again
  print("After label conversion")
  print(np.amin(img_data),np.amax(img_data))
  print(np.unique(img_data))

  # Convert array back to Nii image
  new_img = nib.Nifti1Image(img_data, img.affine, img.header)

  # Set up new image path
  new_img_path = base_img_path + file
  print ('Saved to: ' + new_img_path)
  # Save image to out_dir_path
  nib.save(new_img, new_img_path)