"""
Extract rating scores from individual result files from deployed folder and compile them into a single CSV file.
"""
import os
from datetime import datetime
import pandas as pd

formal_dir = "/opt/jinhanz/results/2509_concreteness/deployed/deploy_0818/formal/" # TODO: setup config info file
df_combined = pd.DataFrame()

analysis = "251215_cogsci_60"
output_dir = f"/opt/jinhanz/results/2509_concreteness/results/{analysis}/human/ratings"

excluded_participants = [ "004", "015", "011", "007", "018", "031", "025", "036", "053", "046", "026", "051", "039", "074","057"]

os.makedirs(output_dir, exist_ok=True)

for b in range(1,5):
    block_dir = os.path.join(formal_dir, f"Block{b}_deploy", "results")
    
    for subject_dir in os.listdir(block_dir):
        subject_path = os.path.join(block_dir, subject_dir)
        if not os.path.isdir(subject_path):
            continue

        if subject_dir[:3] in excluded_participants:
            continue
        
        subject_res_path = os.path.join(subject_path, "RESULTS_FILE.txt")

        if os.path.exists(subject_res_path):
            df = pd.read_csv(subject_res_path, delim_whitespace=True)
            # TODO: assert subject number matches, assert block number matches
            # TODO: readin block order information
            df_combined = pd.concat([df_combined, df], ignore_index=True)
df_combined['answer'] = df_combined['answer'] / 100
df_combined['image_id'] = df_combined['imagename'].apply(lambda x: f"val2014/{'_'.join(x.split('_')[2:])}")
df_combined['match'] = df_combined['imagename'].apply(lambda x: x.split('_')[0])
df_combined['condition'] = df_combined['imagename'].apply(lambda x: x.split('_')[1])
df_combined.to_csv(os.path.join(output_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_rating_scores.csv"), index=False)