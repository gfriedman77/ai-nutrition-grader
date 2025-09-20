# Note about data:
#   From the original dataset, we only used the "cafe 1" metadata csv due to missing data in "cafe 2". 
#   In order to create our metadata csv, we copied the first 5 columns of data for the macronutrient information.

# Note about preprocessing:
    # The code below proceeds to identifs all dish IDs from the "dishes and nutrition.csv" metadata with pictures available.
        # It then takes from the folders with those dish IDs the RGB image files and names them accordingly.
        # The new CSV and folder created by these steps go into the preprocessing folder where this script lives.
    # Finally, the script checks the dimensions of the RGB image files so we can manipulate real world examples to share the same dimensions.

# --- Libraries ---
import os
import pandas as pd
import shutil
from PIL import Image

# --- Step 1: Define repo root and data directories ---
ROOT = os.path.dirname(os.path.abspath(__file__)) # folder where this script lives (preprocessing)
DATA_DIR = os.path.join(ROOT,"..","data") # data directory (folder) one level up, in the repo
REALSENSE_DIR = os.path.join(DATA_DIR, "realsense_overhead") # 'realsense_overhead' directory containing folders for each dish
METADATA_CSV = os.path.join(DATA_DIR, "dishes_and_nutrition.csv")

# --- Step 2: Load metadata and filter dish_IDs with images ---
df = pd.read_csv(METADATA_CSV, sep=',',header=None)
df.columns = ["dish_ID", "weight_grams", "cal", "fat", "carb","protein"]  # rename columns properly

existing_dish_ids = set(os.listdir(REALSENSE_DIR)) # list of all folders in 'realsense_overhead' directory
df_filtered = df[df['dish_ID'].astype(str).isin(existing_dish_ids)] # only keep rows where dish_ID' exists in the list of folders
df_filtered.shape # (3262, 5) check data

# Save csv with filtered dish IDs in preprocessing directory
FILTERED_CSV = os.path.join(ROOT, "dishes_with_available_pics.csv")# Create path for new csv
df_filtered_to_csv = df_filtered.to_csv(FILTERED_CSV, index = False)

# --- Step 3: Copy one RGB image per dish to preprocessing directory ---
RGB_DIR = os.path.join(ROOT, "rgb_images") # Create path for new image folder
os.makedirs(RGB_DIR, exist_ok=True) # Creates folder on disk if it doesn't already exist (so it's possible to re-run script if needed)

for dish_id in df_filtered["dish_ID"].astype(str): # loop through each dish_ID folder in filtered list
    dish_folder = os.path.join(REALSENSE_DIR, dish_id) # construct path to specific dish folder
    if os.path.isdir(dish_folder): # check if dish folder exists
        for file_name in os.listdir(dish_folder):
            if "rgb" in file_name.lower(): # isolate RGB image files
                src = os.path.join(dish_folder, file_name) # define source file path to RGB image file
                dst = os.path.join(RGB_DIR, f"{dish_id}.jpg") # define new path with dish_ID as file name in destination folder
                shutil.copy2(src, dst)
                break  # move to the next dish_ID after finding the one RGB file

print(f"Filtered CSV saved at: {FILTERED_CSV}")
print(f"RGB images saved in: {RGB_DIR}")

# --- Step 4: Check one sample image pixel dimensions --- 
sample_img = os.path.join(RGB_DIR, f"{df_filtered['dish_ID'].iloc[0]}.jpg") # Specify the path to one of the RGB images

with Image.open(sample_img) as img:  # Open the image and get its dimensions
    width, height = img.size
    print(f"Sample image dimensions: {width} x {height}") # 640 x 480
