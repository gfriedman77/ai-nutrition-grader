# Note: Run preprocess_nutrition5k.py prior to this script to create rgb file.

# This script will create macronutrient ratios and then grade images accordingly.
# Points and associated grades are based on health recommendations for the "average person."
# This is solely for proof of concept and would be individualized according to user needs.

# --- Libraries ---
import os
import pandas as pd

# --- Step 1: Define repo root and data directories ---
ROOT = os.path.dirname(os.path.abspath(__file__))  # folder where this script lives (classification)
INPUT_CSV = os.path.join(ROOT, "..", "preprocessing", "dishes_with_available_pics.csv")
RATIOS_CSV = os.path.join(ROOT, "dish_ratios.csv")
GRADE_CSV = os.path.join(ROOT, "dishes_with_grade.csv")

# --- Step 2: Create macronutrient ratios ---
df = pd.read_csv(INPUT_CSV)  # Access preprocessed data
df['Fat to Protein'] = pd.to_numeric((df['fat'] / df['protein']).round(9), errors='coerce')
df['Carb to Protein'] = pd.to_numeric((df['carb'] / df['protein']).round(9), errors='coerce')

# Keep only necessary columns
df = df[['dish_ID', 'Fat to Protein', 'Carb to Protein']]
df = df.reset_index(drop=True)

# Save ratios
df.to_csv(RATIOS_CSV, index=False)
print(f"Saved macronutrient ratios → {RATIOS_CSV}")


# --- Step 3: Calculate points and grades ---

def calculate_points(row):  # define function to score by ratio for points
    points = 0
    # Fat-to-Protein ratio
    if 0.5 <= row['Fat to Protein'] <= 2:
        points += 10
    elif row['Fat to Protein'] > 5:
        points -= 10

    # Carb-to-Protein ratio
    if 0.5 <= row['Carb to Protein'] <= 2:
        points += 10
    elif row['Carb to Protein'] > 3:
        points -= 5

    return points


df['Points'] = df.apply(calculate_points, axis=1)  # apply to each row, create points column


def assign_grade(score):  # define function to grade using points from prior result
    if -15 <= score <= -11:
        return 'F'
    elif -10 <= score <= -6:
        return 'D'
    elif -5 <= score <= -1:
        return 'C'
    elif 0 <= score <= 4:
        return 'B'
    elif 5 <= score <= 9:
        return 'B+'
    elif 10 <= score <= 14:
        return 'A'
    elif 15 <= score <= 20:
        return 'A+'
    else:
        return None  # no grade for scores outside the expected range


df['Grade'] = df['Points'].apply(assign_grade)  # apply to each row, create grade column

df['Points'].value_counts()  # check balance of score (points)
df['Grade'].value_counts()  # check balance of grades (letters)

df[['dish_ID', 'Grade']].to_csv(GRADE_CSV, index=False)  # keep only dish_ID and grade for final CSV
print(f"Saved grades → {GRADE_CSV}")
