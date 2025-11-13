import numpy as np
from PIL import Image
import cv2, torch
import scipy.io as sio

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager

def min_max_normalize(arr):
    arr = np.array(arr)
    arr_min = arr.min()
    arr_max = arr.max()
    if arr_max - arr_min == 0:
        return np.zeros_like(arr)
    return (arr - arr_min) / (arr_max - arr_min)

def convert_mat_to_pt(raw_image, mat_path, pth_path, visualization_path):
    mat = sio.loadmat(mat_path)
    map = mat['output_map_norm']

    map_tensor = torch.tensor(map, dtype=torch.float32)
    torch.save(map_tensor, pth_path)

    image = np.asarray(raw_image.copy())
    color = cv2.applyColorMap((map*255).astype(np.uint8), cv2.COLORMAP_JET) # cv2 to plt
    color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
    c_ret = np.clip(image * (1 - 0.4) + color * 0.4, 0, 255).astype(np.uint8)
    heatmap = Image.fromarray(c_ret)
    heatmap.save(visualization_path)


def draw_heatmap(raw_image, pth_path):
    map = torch.load(pth_path).numpy()

    image = np.asarray(raw_image.copy())
    color = cv2.applyColorMap((map*255).astype(np.uint8), cv2.COLORMAP_JET) # cv2 to plt
    color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
    c_ret = np.clip(image * (1 - 0.4) + color * 0.4, 0, 255).astype(np.uint8)
    heatmap = Image.fromarray(c_ret)
    return heatmap

def visualize(map, raw_image, resize):
    image = np.asarray(raw_image.copy())
    map = resize(map.unsqueeze(0))[0].cpu().numpy()
    color = cv2.applyColorMap((map*255).astype(np.uint8), cv2.COLORMAP_JET) # cv2 to plt
    color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
    c_ret = np.clip(image * (1 - 0.4) + color * 0.4, 0, 255).astype(np.uint8)
    return Image.fromarray(c_ret)

def draw_highlighted_caption(caption, 
                             target_words,
                             concreteness_all, importance_all, 
                             start_pos=(60, 24*3), fontsize=14,
                             coloring=True,
                             base_color=(0, 0, 1),  # matplotlib uses 0–1 floats
                             highlight_color=(223/255, 245/255, 39/255),
                             save_path="highlighted_caption.png"):
    """
    Matplotlib version of highlighted text renderer.
    Creates its own figure/axes and saves result to file.
    """

    # Create fig/ax
    fig, ax = plt.subplots(figsize=(12.8, 1.92), dpi=129.94923858)
    ax.set_xlim(0, 1280)
    ax.set_ylim(0, 192)
    ax.axis('off')

    x, y = start_pos
    words = caption.strip('.,!?\'" ').split()

    renderer = fig.canvas.get_renderer()
    inv = ax.transData.inverted()

    for word, importance in zip(words, importance_all):
        word_clean = word.strip('.,!?\'"')
        vocab = word_clean.lower()

        # default black text
        color = (0, 0, 0, 1)

        if coloring:
            # background highlight rectangle
            highlight_alpha = importance
            bg_color = highlight_color + (highlight_alpha,)

            text = ax.text(x, y, word, fontsize=fontsize, color='black', va='top')
            bbox = text.get_window_extent(renderer=renderer)
            text.remove()

            bbox_data = bbox.transformed(inv)
            rect_width, rect_height = bbox_data.width, bbox_data.height

            rect = patches.Rectangle((x-0.05, y-rect_height*0.2),
                                     rect_width+0.1, rect_height*1.2,
                                     color=bg_color, zorder=1)
            ax.add_patch(rect)

            if vocab in target_words:
                idx = target_words.index(vocab)
                concreteness = concreteness_all[idx] / 5
                text_alpha = concreteness
                color = base_color + (text_alpha,)

        # draw text
        ax.text(x, y, word, fontsize=fontsize,
                color=color, zorder=2)

        # move x forward
        tmp = ax.text(x, y, word + " ", fontsize=fontsize, alpha=0)
        bbox = tmp.get_window_extent(renderer=renderer)
        tmp.remove()
        bbox_data = bbox.transformed(inv)
        word_width = bbox_data.width
        x += word_width

    # Save and close
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    return save_path