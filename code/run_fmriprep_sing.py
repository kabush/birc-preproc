## ========================================
## ========================================
## 
##  Keith Bush, PhD (2022)
##  Univ. of Arkansas for Medical Sciences
##  Brain Imaging Research Center (BIRC)
## 
## ========================================
## ========================================

import os
import argparse
import pandas as pd

def main():

    # Define project paths
    path_fsl_license = '../envs/fsl_license/license.txt'
    path_fmriprep = '../envs/singularity_images/fmriprep-20.2.1.simg'
    path_work = '../outputs/work'

    # Handle command line args
    parser = argparse.ArgumentParser(description='Preprocess study in BIDS format')
    parser.add_argument('-i','--input',help='Path to BIDS formatted study data')
    parser.add_argument('-s','--study',help='Data Map study identifier')
    args = parser.parse_args()
    path_in = args.input
    study = args.study

    # Load the participant's list
    df_subjs = pd.read_csv(path_in + 'participants.tsv', delimiter='\t')
    print(df_subjs)
    use_list = df_subjs['participant_id'].to_list()
    
    # Define output location
    path_out = '../outputs/' + study + '/' 
    path_drv = path_out + 'derivatives/'
    
    # Construct output location
    if(os.path.exists(path_out)):
    
        cmd = '! rm -rf ' + path_out
        print(cmd)
        os.system(cmd)
    
    cmd = '! mkdir ' + path_out
    print(cmd)
    os.system(cmd)
    
    cmd = '! mkdir ' + path_drv
    print(cmd)
    os.system(cmd)
    
    # For each subject (run fmriprep)
    for subj in use_list:
    
        # Build command
        cmd = 'singularity run --cleanenv -B ' + path_in + ' ' + path_fmriprep + ' ' + path_in + ' ' + path_drv + ' participant --participant_label ' + str(subj) + ' --fs-license-file ' + path_fsl_license + ' --fs-no-reconall --nthreads 16 -w ' + path_work + ' --output-spaces MNI152NLin2009cAsym:res-native'
        print(cmd)
        
        # Execute command
        os.system(cmd)
                
if __name__ == '__main__':
    main()
