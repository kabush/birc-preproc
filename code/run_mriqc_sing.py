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
    path_mriqc_img = '../envs/singularity_images/mriqc-0.15.1.simg'
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
    path_mriqc = path_drv + 'mriqc/'

    # Construct output locations
    if(not os.path.exists(path_out)):
        cmd = '! mkdir ' + path_out
        print(cmd)
        os.system(cmd)

    if(not os.path.exists(path_drv)):
        cmd = '! mkdir ' + path_drv
        print(cmd)
        os.system(cmd)

    # Clear out previous run
    cmd = '! rm -rf ' + path_mriqc
    os.system(cmd)

    cmd = '! mkdir ' + path_mriqc
    os.system(cmd)

    # For each subject (run mriqc)
    for subj in use_list:

        subj_pcs = subj.split('-')

        cmd = 'singularity run --cleanenv -B ' + path_in + ' ' + path_mriqc_img + ' ' + path_in + ' ' + path_mriqc + ' participant --participant_label ' + str(subj_pcs[1]) + ' -w ' + path_work 
        print(cmd)
        
        # Execute command
        os.system(cmd)
                
if __name__ == '__main__':
    main()
