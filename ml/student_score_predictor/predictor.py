import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import math

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
# pandas is a library for working with tabular data (like Excel but in Python)
# read_csv() reads the CSV file and stores it as a DataFrame —
# think of a DataFrame as a table with rows and columns
df = pd.read_csv("StudentsPerformance.csv")

print("=" * 55)
print("        STUDENT SCORE PREDICTOR")
print("=" * 55)
print("\n📋 Dataset Overview")
print(f"   Rows    : {df.shape[0]}")   # shape[0] = number of rows
print(f"   Columns : {df.shape[1]}")   # shape[1] = number of columns

# ─────────────────────────────────────────────
# 2. DATA CLEANSING
# ─────────────────────────────────────────────
# Real-world data is messy. Before training a model you must:
#   - Remove rows with missing values (empty cells)
#   - Convert text/category columns into numbers
#     because ML models only understand numbers, not words like "male" or "completed"
print("\n🧹 Data Cleansing")

# isnull() marks every cell that is empty as True
# .sum().sum() counts the total number of empty cells across the whole table
missing = df.isnull().sum().sum()
print(f"   Missing values found : {missing}")

# dropna() removes any row that has at least one empty cell
# inplace=True means modify the original DataFrame directly (don't create a copy)
df.dropna(inplace=True)
print(f"   Rows after cleaning  : {len(df)}")

# We create a new column "average score" by averaging the three subject scores
# This is what our model will try to predict — the target/output
df["average score"] = (df["math score"] + df["reading score"] + df["writing score"]) / 3

# LabelEncoder converts text categories into numbers
# e.g. "female" → 0, "male" → 1
#      "completed" → 0, "none" → 1
# Models can't do math on words, but they can on numbers
encoder = LabelEncoder()
categorical_cols = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]

for col in categorical_cols:
    # fit_transform() first learns the unique values in that column,
    # then replaces each value with its assigned number
    df[col] = encoder.fit_transform(df[col])

print("   Categorical columns  : encoded to numbers")

# ─────────────────────────────────────────────
# 3. FEATURES & TARGET
# ─────────────────────────────────────────────
# In ML:
#   Features (X) = the inputs the model uses to make a prediction
#   Target   (y) = the output/answer we want the model to predict
#
# Think of it like: X is the question, y is the answer
# The model learns: "given X, what is y?"

features = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]

X = df[features]          # inputs  — 5 columns
y = df["average score"]   # target  — 1 column (what we want to predict)

# ─────────────────────────────────────────────
# 4. TRAIN / TEST SPLIT
# ─────────────────────────────────────────────
# We split the data into two parts:
#   Training set — the model learns from this (sees both X and y)
#   Testing set  — we use this to evaluate the model (model only sees X, we check its y)
#
# Why split? You wouldn't test a student with the exact questions they studied.
# Same idea — we test the model on data it has NEVER seen before.
# test_size=0.2 means 20% goes to testing, 80% to training
# random_state=42 is a fixed seed — ensures the split is the same every run
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\n📊 Train / Test Split")
print(f"   Training samples : {len(X_train)}")
print(f"   Testing samples  : {len(X_test)}")

# ─────────────────────────────────────────────
# 5. MODEL TRAINING
# ─────────────────────────────────────────────
# LinearRegression finds the best-fit line through the data
# The line is defined by: y = m1*x1 + m2*x2 + ... + b
#   where m values are the weights (slopes) and b is the intercept
#
# fit() is where the actual "learning" happens —
# it looks at X_train and y_train and finds the best values for m and b
# by minimising the error (MSE) between predictions and actual values
model = LinearRegression()
model.fit(X_train, y_train)
print(f"\n✅ Model trained (Linear Regression)")

# ─────────────────────────────────────────────
# 6. EVALUATION — MSE & RMSE
# ─────────────────────────────────────────────
# predict() uses the trained model to predict scores for the test set
# The model has never seen X_test during training — this is a fair evaluation
y_pred = model.predict(X_test)

# Mean Squared Error (MSE) — the Cost Function
# For each prediction: calculate (predicted - actual)²
# Then take the average of all those squared errors
# We square the errors so that:
#   1. Negative and positive errors don't cancel each other out
#   2. Larger errors are penalised more heavily
#
# Lower MSE = better model
mse  = mean_squared_error(y_test, y_pred)

# RMSE = square root of MSE
# This brings the error back to the same unit as the score (points)
# So RMSE of 10 means: on average, predictions are off by ±10 points
rmse = math.sqrt(mse)

print(f"\n📈 Evaluation Report")
print(f"   Mean Squared Error (MSE)  : {mse:.2f}")
print(f"   Root Mean Sq. Error (RMSE): {rmse:.2f}")
print(f"   → On average, predictions are off by ±{rmse:.1f} points")

# ─────────────────────────────────────────────
# 7. PREDICTED vs ACTUAL (first 10 samples)
# ─────────────────────────────────────────────
# This gives you a human-readable view of how well the model is doing
# Diff = predicted - actual
#   positive diff (+) means the model over-predicted
#   negative diff (-) means the model under-predicted
print(f"\n🔍 Predicted vs Actual (first 10 test samples)")
print(f"   {'Actual':>10}  {'Predicted':>10}  {'Diff':>8}")
print(f"   {'-'*35}")
for actual, predicted in zip(list(y_test[:10]), y_pred[:10]):
    diff = predicted - actual
    print(f"   {actual:>10.1f}  {predicted:>10.1f}  {diff:>+8.1f}")

# ─────────────────────────────────────────────
# 8. PREDICT FOR A NEW STUDENT (user input)
# ─────────────────────────────────────────────
# Now we use the trained model to predict a score for a brand new student
# We ask the user to provide values for all 5 features
# These must match the same encoding used during training
# e.g. if "female" was encoded as 0 during training, we pass 0 here too
print(f"\n{'=' * 55}")
print("  PREDICT SCORE FOR A NEW STUDENT")
print(f"{'=' * 55}")

print("""
Answer the following (enter the number for your choice):

Gender
  0 = Female
  1 = Male
""")
gender = int(input("   Gender: "))

print("""
Race / Ethnicity
  0 = Group A
  1 = Group B
  2 = Group C
  3 = Group D
  4 = Group E
""")
race = int(input("   Race/Ethnicity: "))

print("""
Parental Level of Education
  0 = Associate's degree
  1 = Bachelor's degree
  2 = High school
  3 = Master's degree
  4 = Some college
  5 = Some high school
""")
parental_edu = int(input("   Parental Education: "))

print("""
Lunch
  0 = Free / Reduced
  1 = Standard
""")
lunch = int(input("   Lunch: "))

print("""
Test Preparation Course
  0 = Completed
  1 = None
""")
test_prep = int(input("   Test Prep: "))

# Wrap the inputs in a 2D list [[...]] because the model expects
# a table structure even for a single student (1 row, 5 columns)
new_student = [[gender, race, parental_edu, lunch, test_prep]]
predicted_score = model.predict(new_student)[0]   # [0] extracts the single value from the result array

print(f"\n{'=' * 55}")
print(f"  Predicted Average Score : {predicted_score:.1f} / 100")
print(f"{'=' * 55}\n")
