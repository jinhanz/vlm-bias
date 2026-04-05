# %% Imports
import os, json, re, math
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

import ast

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

    return word_list, word_spans, space_width, space_height   

from matplotlib.patches import Ellipse

def plot_two_ellipses(
    image,
    ellipse1_center,
    ellipse1_size,
    ellipse2_center,
    ellipse2_size,
    ellipse1_kwargs=None,
    ellipse2_kwargs=None,
    path=None
):
    """
    Plot two ellipses on an image.

    Parameters
    ----------
    image : np.ndarray
        Image array (H, W, C) or (H, W)
    ellipse*_center : tuple
        (cx, cy)
    ellipse*_size : tuple
        (width, height)  # full span, not semi-axes
    ellipse*_kwargs : dict, optional
        matplotlib Ellipse styling options
    show : bool
        Whether to call plt.show()
    """

    if ellipse1_kwargs is None:
        ellipse1_kwargs = dict(edgecolor="red", linewidth=2, fill=False)

    if ellipse2_kwargs is None:
        ellipse2_kwargs = dict(edgecolor="blue", linewidth=2, fill=False)

    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.axis("off")

    e1 = Ellipse(
        xy=ellipse1_center,
        width=ellipse1_size[0],
        height=ellipse1_size[1],
        **ellipse1_kwargs
    )

    e2 = Ellipse(
        xy=ellipse2_center,
        width=ellipse2_size[0],
        height=ellipse2_size[1],
        **ellipse2_kwargs
    )

    ax.add_patch(e1)
    ax.add_patch(e2)

    fig.savefig(path)
    plt.close(fig)

    return fig, ax

import math

def constrained_enclosing_ellipse(rect_width, rect_height, max_vertical_axis):
    """
    Compute ellipse size that encloses a rectangle while capping vertical axis.

    Parameters
    ----------
    rect_width : float
    rect_height : float
    max_vertical_axis : float
        Maximum allowed semi vertical axis (b)

    Returns
    -------
    ellipse_width : float
        Full horizontal span
    ellipse_height : float
        Full vertical span
    """

    W = rect_width
    H = rect_height
    b_max = max_vertical_axis

    # Feasibility check
    if b_max < H / 2:
        raise ValueError("Vertical cap too small to enclose rectangle")

    # Unconstrained smallest ellipse
    b0 = H / math.sqrt(2)

    if b0 <= b_max:
        a = W / math.sqrt(2)
        b = b0
    else:
        b = b_max
        denom = 1 - (H / 2) ** 2 / b ** 2
        a = (W / 2) / math.sqrt(denom)

    return 2 * a, 2 * b

# %%
imageinfo_path = "/opt/jinhanz/results/2509_concreteness/stimuli/250619-250723_stimuli_experiment/20250723_193742/image_info.csv"
stimuli_path = "/opt/jinhanz/results/2509_concreteness/stimuli/250619-250723_stimuli_experiment/20250723_193742"
seg_viz_path = "/opt/jinhanz/results/2509_concreteness/results/251215_cogsci_60/visualizations/word_importance_segmentation"
fixed_roi_path = "/opt/jinhanz/results/2509_concreteness/results/251215_cogsci_60/emhmm/fixed_roi_info.xlsx"
fixed_roi_viz_path = "/opt/jinhanz/results/2509_concreteness/results/251215_cogsci_60/visualizations/fixed_roi"
fixed_roi_caption_path = "/opt/jinhanz/results/2509_concreteness/results/251215_cogsci_60/emhmm/caption_fixed_roi_info.xlsx"

imageinfo = pd.read_csv(imageinfo_path.replace('image_info.csv','image_info_segmentation.csv'))

fixed_roi_df = pd.DataFrame(columns=["Stimuli","Roi_number","Roi_center","Tmp"])
fixed_roi_df["Roi_center"] = fixed_roi_df["Roi_center"].astype(object)
fixed_roi_df["Tmp"] = fixed_roi_df["Tmp"].astype(object)

caption_fixed_roi_df = pd.DataFrame(columns=["Stimuli","Roi_number","Roi_center","Tmp"])
caption_fixed_roi_df["Roi_center"] = caption_fixed_roi_df["Roi_center"].astype(object)
caption_fixed_roi_df["Tmp"] = caption_fixed_roi_df["Tmp"].astype(object)

for b in range(1,5):

    b = str(b)
        
    for img_path in os.listdir(os.path.join(stimuli_path, b)):

        if 'mismatched' in img_path:
            continue

        condition = 'abstract' if 'abs' in img_path else 'concrete'

        imageinfo_row = imageinfo[imageinfo['trial_id'] == img_path].iloc[0]
        space_height = 24
        
        word_list = ast.literal_eval(imageinfo_row['word_list'])
        word_spans = ast.literal_eval(imageinfo_row['word_spans'])
        ## Fixed ROI info

        # enclosing ellipse size (just about to cover the entire image/caption area)
        scale = math.sqrt(2)

        image_coordinates = ast.literal_eval(imageinfo_row['image_coordinates'])
        image_size = ast.literal_eval(imageinfo_row['image_size'])

        image_x_start = image_coordinates[0]
        image_x_end = image_coordinates[1]
        image_y_start = 1024 - image_coordinates[3]
        image_y_end = 1024 - image_coordinates[2]

        image_width = image_size[0]
        image_height = image_size[1]

        all_caption_roi_center = []
        all_caption_tmp = []

        for span in word_spans:
            c_x_start = span[0]
            c_x_end = span[1]
            c_y_start = 1024 - span[3]
            c_y_end = 1024 - span[2]

            c_width = c_x_end - c_x_start
            c_height = c_y_end - c_y_start

            constrained_caption_height = space_height * 3

            caption_x_center, caption_y_center = int(c_x_start + c_width//2), int(c_y_start + c_height//2)

            all_caption_roi_center.extend([caption_x_center, caption_y_center-832])
            all_caption_tmp.extend([int(c_width/1.2), int(constrained_caption_height)])

        caption_fixed_roi_df = pd.concat([caption_fixed_roi_df, pd.DataFrame({
            "Stimuli": img_path,
            "Roi_number": len(word_spans),
            "Roi_center": [all_caption_roi_center],
            "Tmp": [all_caption_tmp]
        })], ignore_index=True)

        caption_x_start = word_spans[0][0]
        caption_x_end = word_spans[-1][1]
        caption_y_start = 1024 - word_spans[0][3]
        caption_y_end = 1024 - word_spans[0][2]

        caption_width = caption_x_end - caption_x_start
        caption_height = caption_y_end - caption_y_start
        constrained_caption_height = space_height * 3

        image_x_center, image_y_center = int(image_x_start + image_width//2), int(image_y_start + image_height//2)
        caption_x_center, caption_y_center = int(caption_x_start + caption_width//2), int(caption_y_start + caption_height//2)

        max_image_roi_y_height = 2 * (880 - image_y_center)
        image_roi_width, image_roi_height = constrained_enclosing_ellipse(image_width, image_height, max_image_roi_y_height//2)

        fixed_roi_df = pd.concat([fixed_roi_df, pd.DataFrame({
            "Stimuli": img_path,
            "Roi_number": 2,
            "Roi_center": [[image_x_center, image_y_center, caption_x_center, caption_y_center]],
            "Tmp": [[int(image_roi_width/1.2), int(image_roi_height/1.2),
                    int(caption_width*scale), int(constrained_caption_height*scale)]]
        })], ignore_index=True)

        # plot_two_ellipses(image=mpimg.imread(os.path.join(stimuli_path, b, img_path)),
        #                   ellipse1_center=(image_x_center, image_y_center),
        #                   ellipse1_size=(int(image_roi_width), int(image_roi_height)),
        #                   ellipse2_center=(caption_x_center, caption_y_center),
        #                   ellipse2_size=(int(caption_width*scale), int(constrained_caption_height*scale)),
        #                   path=os.path.join(fixed_roi_viz_path, img_path))

for col in ["Roi_center","Tmp"]:
    fixed_roi_df[col] = fixed_roi_df[col].apply(json.dumps)
    caption_fixed_roi_df[col] = caption_fixed_roi_df[col].apply(json.dumps)
fixed_roi_df.to_excel(fixed_roi_path, index=False)
caption_fixed_roi_df.to_excel(fixed_roi_caption_path, index=False)
# # %%
# import pandas as pd, json, ast, math

# df = pd.read_excel("/opt/jinhanz/results/2509_concreteness/results/251215_cogsci_60/emhmm/fixed_roi_info_orig.xlsx")
# df['Tmp'] = df['Tmp'].apply(lambda x: [int(v/1.2) for v in ast.literal_eval(x)])
# df = df[df['Stimuli'].str.contains('mismatched') == False]
# df.to_excel("/opt/jinhanz/results/2509_concreteness/results/251215_cogsci_60/emhmm/fixed_roi_info.xlsx", index=False)

# %%
