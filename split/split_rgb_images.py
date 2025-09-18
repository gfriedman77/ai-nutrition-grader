# Note: Run preprocess_nutrition5k.py and grade_mapping.py prior to running this script.

# This script places images in folders for a 70% train, 15% test, and 15% unseen split.

# --- Libraries ---
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import shutil

# --- Step 1: Define repo root and data directories ---

# --- Base paths ---
ROOT = os.path.dirname(os.path.abspath(__file__))  # folder where this script lives (split)
RGB_DIR = os.path.join(ROOT, "..", "preprocessing", "rgb_images")  # folder with rgb images
GRADE_CSV = os.path.join(ROOT, "..", "classification", "dishes_with_grade.csv")  # CSV with grades

# --- Output folders inside 'split' folder ---
TRAIN_DIR = os.path.join(ROOT, "train")
TEST_DIR = os.path.join(ROOT, "test")
UNSEEN_DIR = os.path.join(ROOT, "unseen")

# --- Parameters ---
IMG_HEIGHT = 128
IMG_WIDTH = 128
batch_size = 70

# Load CSV
df = pd.read_csv(GRADE_CSV)

# --- Split into train/test/unseen ---
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df["Grade"]) #70:30
test_df, unseen_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df["Grade"]) # 15:15

# --- Clear & recreate output folders ---
for d in [TRAIN_DIR, TEST_DIR, UNSEEN_DIR]:
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)

# Copy images by grade
def copy_images(subset_df, subset_dir):
    for _, row in subset_df.iterrows():
        dish_id = str(row["dish_ID"])
        grade = row["Grade"]
        src = os.path.join(RGB_DIR, f"{dish_id}.jpg")
        class_dir = os.path.join(subset_dir, grade)
        os.makedirs(class_dir, exist_ok=True)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(class_dir, f"{dish_id}.jpg"))

copy_images(train_df, TRAIN_DIR)
copy_images(test_df, TEST_DIR)
copy_images(unseen_df, UNSEEN_DIR)

print("Train/Test/Unseen folders ready in:", ROOT)
