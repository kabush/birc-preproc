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

    # Handle command line args
    parser = argparse.ArgumentParser(description='Preprocess study in BIDS format')
    parser.add_argument('-i','--input',help='Path to BIDS formatted study data')
    parser.add_argument('-y','--study',help='Study identifier')
    parser.add_argument('-s','--single',help='Single participant flag',action='store_true')
    parser.add_argument('-b','--subset',help='Subset of participants starting at --participant <id>',action='store_true')
    parser.add_argument('-p','--participant',help='Single participant identifier')

    args = parser.parse_args()
    path_in = args.input
    study = args.study
    single = args.single
    subset = args.subset
    participant = args.participant

    # Define output location
    path_out = '../outputs/' + study + '/' 
    path_drv = path_out + 'derivatives/'
    path_work = path_drv + 'work/'

    # Construct output locations
    if(not os.path.exists(path_out)):
        cmd = '! mkdir ' + path_out
        print(cmd)
        os.system(cmd)
    if(not os.path.exists(path_drv)):
        cmd = '! mkdir ' + path_drv
        print(cmd)
        os.system(cmd)
    if(not os.path.exists(path_work)):
        cmd = '! mkdir ' + path_work
        print(cmd)
        os.system(cmd)

    # Operate for single subject or full bids
    use_list = []
    if(single):

        use_list = [participant]

    else:

        # Load the participant's list
        df_subjs = pd.read_csv(path_in + 'participants.tsv', delimiter='\t')

        # Run a subset starting from <participant_id>
        if(subset):
            
            use_list = df_subjs['participant_id'].to_list()
            print(use_list)
            idx = df_subjs.index[df_subjs['participant_id']==participant][0]
            use_list = use_list[idx:]
            print(use_list)

        # Run all participants
        else:

            use_list = df_subjs['participant_id'].to_list()

    # For each subject (run fmriprep)
    for subj in use_list:
        
        # Build command
        cmd = 'singularity run --cleanenv -B ' + path_in + ' ' + path_fmriprep + ' ' + path_in + ' ' + path_drv + ' participant --participant_label ' + str(subj) + ' --fs-license-file ' + path_fsl_license + ' --fs-no-reconall --nthreads 16 -w ' + path_work + ' --output-spaces MNI152NLin2009cAsym:res-native'
        print(cmd)
        
        # Execute command
        os.system(cmd)
                
if __name__ == '__main__':
    main()
