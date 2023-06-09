# -*- coding: utf-8 -*-
from google.colab import drive
drive.mount('/content/drive')

import os
import random

# Read all the ground truth segmentation files into a list
segm_src_dir = '/content/drive/MyDrive/TCIA/UPENN-GBM/images_segm/'
segm_file_list = os.listdir(segm_src_dir)

# Shuffle the list so the order is randomized
random.shuffle(segm_file_list)

# Set up the training data ratio and split the list at that point
train_ratio = 0.8
elements = len(segm_file_list)
train_elements = int(elements * train_ratio)

# Create new list of segmentation files that will be used for training
# nnU-Net does not need the segmentation files for the test dataset, but we will need it later for running our metrics
train_segm_list = segm_file_list[:train_elements]
test_segm_list = segm_file_list[train_elements:]

# Check how many elements and if they are randomized
print (train_segm_list)
len(train_segm_list)

# Lets generate some commands to help us move the ground truth segmentation files to the right folder for nnU-Net training
# They need to be in the labelsTr folder

tr_segm_target_dir = '/content/drive/MyDrive/TCIA/nnUNet/nnUNet_raw/Dataset501_Glioblastoma/labelsTr/'

for file in train_segm_list:
  tr_segm_file = file.split('_')[0]
  patient_id = tr_segm_file.split('-')[2]
  just_id = int(patient_id.split('.')[0]) # Get the patient ID # and remove leading zeroes, and discard the .nii.gz extension
  print ('!mv ' + segm_src_dir + file + ' ' + tr_segm_target_dir + str(just_id) + '.nii.gz')

# This is not required by nnU-Net, but I am setting it up to use later for our metrics
ts_segm_target_dir = '/content/drive/MyDrive/TCIA/nnUNet_raw_data_base/nnUNet_raw_data/Task501_Glioblastoma/labelsTs/'

for file in test_segm_list:
  ts_segm_file = file.split('_')[0] # Split the file name at the first underscore and discard the _11....
  patient_id = ts_segm_file.split('-')[2] # Remove the string UPENN-GBM and return just the ID #
  just_id = int(patient_id) # Get the patient ID # and remove leading zeroes
  print ('!mv ' + segm_src_dir + file + ' ' + ts_segm_target_dir + just_id + '.nii.gz')

# nnU-Net requires image files to end in a sequence that looks like - "patientID_4 digit_MRI_sequence" number
# For example, we need to replace the file name from UPENN-GBM-00001_11_T1.nii.gz to UPENN-GBM-00001_0000.nii.gz
# Our Mapping - T1:0000, T1-GD:0001, T2:0002, FLAIR:0003
# and then move the training files to the imagesTr folder
# We will only do this for patients in our training cohort (who have ground truth segmentation files)

mri_img_src_dir = '/content/drive/MyDrive/TCIA/UPENN-GBM/images_structural/'
tr_img_target_dir = '/content/drive/MyDrive/TCIA/nnUNet_raw_data_base/nnUNet_raw_data/Dataset501_Glioblastoma/imagesTr/'


for patient in train_segm_list:
  patient_id = patient.split('.')[0]
  patient_dir = patient_id + '_11' # Get the patient list from our labelsTr folder and generate the directory name
  patient_dir_path = mri_img_src_dir + patient_dir # Generate full path of the images source directory
  just_id = int(patient_id.split('-')[2]) # Get the patient ID # and remove leading zeroes

  print ('!mv ' + patient_dir_path + '/' + patient_dir + '_T1.nii.gz ' + tr_img_target_dir + str(just_id) + '_0000.nii.gz')
  print ('!mv ' + patient_dir_path + '/' + patient_dir + '_T1GD.nii.gz ' + tr_img_target_dir + str(just_id) + '_0001.nii.gz')
  print ('!mv ' + patient_dir_path + '/' + patient_dir + '_T2.nii.gz ' + tr_img_target_dir + str(just_id) + '_0002.nii.gz')
  print ('!mv ' + patient_dir_path + '/' + patient_dir + '_FLAIR.nii.gz ' + tr_img_target_dir + str(just_id) + '_0003.nii.gz')

# Now move all the test data files to the imagesTs directory

mri_img_src_dir = '/content/drive/MyDrive/TCIA/UPENN-GBM/images_structural/'
ts_img_target_dir = '/content/drive/MyDrive/TCIA/nnUNet_raw_data_base/nnUNet_raw_data/Dataset501_Glioblastoma/imagesTs/'

test_img_list = os.listdir(mri_img_src_dir)

for patient in test_img_list:
  patient_id = patient.split('.')[0]
  #patient_dir = patient_id + '_11' # Get the patient list from our labelsTr folder and generate the directory name
  patient_dir = patient_id
  patient_dir_path = mri_img_src_dir + patient_dir # Generate full path of the images source directory
  # just_id = int(patient_id.split('-')[2]) # Get the patient ID # and remove leading zeroes
  temp_id = patient_id.split('-')[2]
  just_id = int(temp_id.split('_')[0])

  print ('!mv ' + patient_dir_path + '/' + patient_dir + '_T1.nii.gz ' + ts_img_target_dir + str(just_id) + '_0000.nii.gz')
  print ('!mv ' + patient_dir_path + '/' + patient_dir + '_T1GD.nii.gz ' + ts_img_target_dir + str(just_id) + '_0001.nii.gz')
  print ('!mv ' + patient_dir_path + '/' + patient_dir + '_T2.nii.gz ' + ts_img_target_dir + str(just_id) + '_0002.nii.gz')
  print ('!mv ' + patient_dir_path + '/' + patient_dir + '_FLAIR.nii.gz ' + ts_img_target_dir + str(just_id) + '_0003.nii.gz')
