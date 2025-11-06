# %% Imports
import os, json, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

import matplotlib.pyplot as plt
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
import re

# %%
def word_segmentation(image_path, caption, save_path):

    dpi = 129.94923858
    text_y_start = 24 * 4
    x0 = 60
    font_size = 14

    # ---- Load the image ----
    img = mpimg.imread(image_path)
    height, width = img.shape[:2]

    fig, ax = plt.subplots(figsize=(12.8, 10.24), dpi=dpi)
    # ax.set_xlim(0, 1280)
    # ax.set_ylim(0, 1024)
    ax.imshow(img, extent=[0, width, 0, height])
    ax.axis('off')

    # ---- Tokenize with whitespace preserved ----
    tokens = re.findall(r'\S+|\s+', caption)

    # ---- Font setup ----
    fp = FontProperties(size=font_size)

    # Get renderer for measurements
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    # ---- Helper to measure text width in pixels ----
    def get_text_width_px(text, fontprop, renderer):
        # create a dummy Text object
        t = ax.text(0, 0, text, fontproperties=fontprop)
        bbox = t.get_window_extent(renderer=renderer)
        t.remove()  # cleanup
        return bbox.width, bbox.height

    word_list = []
    word_spans = []
    current_x = x0

    # approximate space width using single space
    space_width, space_height = get_text_width_px(" ", fp, renderer)

    for tok in tokens:
        if tok.isspace():
            width_px = space_width * len(tok)
            height_px = space_height
        else:
            width_px, height_px = get_text_width_px(tok, fp, renderer)

        # Draw rectangle only for visible text
        if not tok.isspace():
            rect = Rectangle(
                (current_x-space_width/2, text_y_start-3*height_px),
                width_px+space_width, height_px*5,
                linewidth=0.8, edgecolor='red', facecolor='none', alpha=0.5
            )
            ax.add_patch(rect)

            # Record span
            word_list.append(re.sub(r'[^\w\s]', '', tok))
            word_spans.append([int(current_x-space_width/2), int(current_x+width_px+space_width/2), int(text_y_start-3*height_px), int(text_y_start+2*height_px)])

        current_x += width_px

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=103.05)
    plt.close()

    return word_list, word_spans   

# %%
imageinfo_path = "./stimuli/250619-250723_stimuli_experiment/20250723_193742/image_info.csv"
imageinfo = pd.read_csv(imageinfo_path)
stimuli_path = "./stimuli/250619-250723_stimuli_experiment/20250723_193742"
seg_viz_path = "./results/251021_acl_preliminary/251021_word_importance_segmentation"

imageinfo['word_list'] = None
imageinfo['word_spans'] = None

for b in range(1,5):

    b = str(b)
        
    for img_path in os.listdir(os.path.join(stimuli_path, b)):

        # if 'mismatched' in img_path:
        #     continue

        condition = 'abstract' if 'abs' in img_path else 'concrete'

        imageinfo_row = imageinfo[imageinfo['trial_id'] == img_path].iloc[0]
        caption = imageinfo_row["caption_text"]

        word_list, word_spans = word_segmentation(os.path.join(stimuli_path, b, img_path), caption, os.path.join(seg_viz_path, img_path))

        # Update the "word_spans" column in imageinfo DataFrame
        imageinfo.at[imageinfo[imageinfo['trial_id'] == img_path].index[0], 'word_list'] = word_list
        imageinfo.at[imageinfo[imageinfo['trial_id'] == img_path].index[0], 'word_spans'] = word_spans

imageinfo.to_csv(imageinfo_path.replace('image_info.csv','image_info_segmentation.csv'), encoding="utf_8_sig", index=False)