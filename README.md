## Introduction

### Inspiration
The "AI nutrition grader" builds upon "Presenting Nutritrack," a project that won my team an AI app design 
pitch competition when we presented a custom CNN proof-of-concept and discussed our business plan.

### Design
The model built for this project, unlike the original, is a transfer learning design. The data remained the same; it comes from the Nutrition5K dataset (RGB images of food on plates).

### Workflow

The workflow follows the standard transfer learning pipeline in deep learning:

1) Load pretrained MobileNetV2 weights → transfer learning base.
2) Train only the top layers first → feature extraction.
3) Unfreeze some pretrained layers to adapt to the food data → fine-tuning.

The MobileNetV2 backbone is pretrained on ImageNet, a large dataset. The AI nutrition grader model
builds a custom classification head for feature extraction and then fine-tunes the deeper layers 
to adapt to its own food image dataset (drawn from the Nutrition5K dataset).

## Repo 

There are 3 main ways to navigate the repo:

1) **Overview:** Check out the Jupyter notebook in the Testing folder and the output in the Results folder.

2) **Context:** Check out the slides and business plan for Presenting Nutritrack, the project that inspired this one.

3) **Exploration:** Try this order:
   
- **Data:** See information below about LFS to access thousands of images.
- **Preprocessing:** Run preprocess_nutrition5k.py 
- **Classification:** Run grade_mapping.py
- **Split:** Run split_rgb_images.py
- **Testing:** Run "CNN Transfer Learning" Jupyter notebook.

## Access

This repository uses [Git LFS](https://git-lfs.github.com/) to store large files such as the images 
in `data/realsense_overhead`.  Bear in mind that the full set of images will take up over 3 MB initially. 
I've included all image files offered by Nutrition5K for any one dish in case others want to explore more.

To clone the repository and download the full dataset, run:

```bash
# 1. Clone the repository
git clone https://github.com/gfriedman77/ai-nutrition-grader.git
cd ai-nutrition-grader

# 2. Install Git LFS (only needed once per computer)
git lfs install

# 3. Download all large files tracked by Git LFS
git lfs pull
