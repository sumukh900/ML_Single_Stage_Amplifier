import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# --------------------------
# 1. Data Loading and Preparation
# --------------------------

# Load the dataset (adjust the file path as needed)
df = pd.read_excel("C:\Sumukh\ML single stage\cs_resistive_bias_final 1.xlsx")

# Define input and target columns.
input_cols = ['gain', 'speed', 'power']
target_cols = [col for col in df.columns if col not in input_cols]

# Helper function to decide if a column is mostly numeric.
def is_numeric_column(series):
    non_null = series.dropna()
    if len(non_null) == 0:
        return False
    success = 0
    for val in non_null:
        try:
            float(val)
            success += 1
        except:
            pass
    return (success / len(non_null)) >= 0.9

# Determine target type and preprocess accordingly.
# For numeric targets, convert to numbers and fill missing with -999.0.
# For categorical targets, fill missing with 'missing' and force values to string.
target_info = {}
for col in target_cols:
    if is_numeric_column(df[col]):
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(-999.0)
        target_info[col] = 'numeric'
    else:
        df[col] = df[col].fillna('missing')
        df[col] = df[col].astype(str)  # Ensure uniform string type.
        target_info[col] = 'categorical'

# Ensure input columns are numeric.
for col in input_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna(subset=input_cols)  # Drop rows with missing inputs.

# Prepare input data.
X = df[input_cols].values

# --------------------------
# 2. Train a Separate Model for Each Target Using XGBoost
# --------------------------

models = {}
label_encoders = {}

for col in target_cols:
    y = df[col].values
    # Split the data for training and testing.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    if target_info[col] == 'numeric':
        # Train an XGBoost regressor.
        model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        models[col] = model
    else:
        # For categorical targets, ensure y_train is uniformly string.
        y_train = y_train.astype(str)
        le = LabelEncoder()
        y_train_enc = le.fit_transform(y_train)
        model = xgb.XGBClassifier(eval_metric='mlogloss', n_estimators=100, random_state=42)
        model.fit(X_train, y_train_enc)
        models[col] = model
        label_encoders[col] = le

# --------------------------
# 3. Prediction Function
# --------------------------

def predict_amplifier_params(gain, speed, power):
    """
    Given input values for gain, speed, and power, predict all target parameters.
    Numeric predictions equal to -999.0 are reported as 'Not Applicable'.
    Categorical predictions are converted back to their original string labels.
    """
    input_data = np.array([[gain, speed, power]], dtype=np.float32)
    predictions = {}
    
    for col in target_cols:
        if target_info[col] == 'numeric':
            pred = models[col].predict(input_data)[0]
            predictions[col] = "Not Applicable" if pred == -999.0 else pred
        else:
            pred_class = models[col].predict(input_data)[0]
            pred_label = label_encoders[col].inverse_transform([pred_class])[0]
            predictions[col] = pred_label
    return predictions

# --------------------------
# 4. Example Usage
# --------------------------

example_prediction = predict_amplifier_params(0.463, 55330000, 0.01381)
print("Predicted Parameters:")
for key, value in example_prediction.items():
    print(f"{key}: {value}")
