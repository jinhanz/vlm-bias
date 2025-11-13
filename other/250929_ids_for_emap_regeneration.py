import os, json
import pandas as pd
from collections import defaultdict

with open("/home/jinhanz/cs/concreteness/stimuli/coco_caption_concereteness_with_lemmatization.json") as f:
    data = json.load(f)

stimuli_df = pd.read_csv("/home/jinhanz/cs/concreteness/processing/stimuli_experiment/20250723_193742/image_info.csv")

matched_ids = defaultdict(dict)

for i, item in stimuli_df.iterrows():
    image_id = item['image_id']
    image_size = eval(item['image_size'])
    caption = item['caption_text']
    match = True if item['match'] == "matched" else False

    record = None

    for img in data:
        if img['image'] == image_id:
            record = img
            break
    
    captions_list = record['caption_concreteness']

    caption_id = None

    for c in captions_list:
        if c['caption'].strip() == caption.strip():
            caption_id = c['id']
            break

    if match and caption_id is None: 
        print(image_id, caption)

    if match:
        if image_id not in matched_ids:
            matched_ids[image_id]['resized_w'] = image_size[0]
            matched_ids[image_id]['resized_h'] = image_size[1]
            matched_ids[image_id]['caption_ids'] = []
        matched_ids[image_id]['caption_ids'].append(caption_id)
    # else:
    #     mismatched_ids[image_id].append(caption_id)

json.dump(matched_ids, open("250929_matched_ids_for_resized_images.json", "w"))
# json.dump(mismatched_ids, open("250929_mismatched_ids_for_emap_regeneration.json", "w"))