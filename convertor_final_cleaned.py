import pandas as pd

# Specify the file path of your CSV file.
file_path = r"C:\Sumukh\ML single stage\cs_current_source.csv"  # Use a raw string or double backslashes

# Read the CSV file.
df = pd.read_csv(file_path)

# List to store all processed rows
processed_data = []

# Identify blocks of parameter sets
num_inputs = 37044  # Define total number of input sets
rows_per_input = len(df) // num_inputs  # Approximate rows per input set

# Iterate over all 162 input blocks
for i in range(num_inputs):
    start_idx = i * rows_per_input
    end_idx = start_idx + rows_per_input
    
    subset = df.iloc[start_idx:end_idx]
    
    # --- 1. Extract header parameters ---
    param_str = subset.iloc[0, 0]  # First row contains parameters
    if param_str.startswith("Parameters:"):
        param_str = param_str.replace("Parameters:", "").strip()
    
    params = {}
    for item in param_str.split(","):
        item = item.strip()
        if "=" in item:
            key, val = item.split("=", 1)
            params[key.strip()] = val.strip()

    # --- 2. Extract measured outputs ---
    measured = {}
    for idx in range(1, len(subset)):
        output_name = subset.iloc[idx]["Output"]
        nominal_val = subset.iloc[idx]["Nominal"]
        if pd.notnull(output_name):
            measured[output_name] = nominal_val

    # --- 3. Build final data dictionary ---
    final_data = {
        "resistance": measured.get("resistance", params.get("R", "")),
        "width1": measured.get("width", params.get("w1", "")),
        "length1": params.get("l1", ""),
        "width2": measured.get("width", params.get("w2", "")),
        "length2": params.get("l2", ""),
        "gate_voltage": params.get("VG", ""),
        "drain_voltage": params.get("VD", ""),
        "source_voltage": params.get("VS", ""),
        "current_source_voltage": params.get("VB", ""),
        "power": -float(measured.get("Power", 0)) if measured.get("Power", "") else "",
        "speed": measured.get("Speed", ""),
        "gain": measured.get("Gain", ""),
        "topology": "CS_Current_source_load"  # Fixed topology
    }

    processed_data.append(final_data)

# Convert list of dictionaries to DataFrame
final_df = pd.DataFrame(processed_data)

# Save the new CSV file.
output_path = r"C:\Sumukh\ML single stage\cs_current_source_converted_output.csv"
final_df.to_csv(output_path, index=False)

print(f"Processed {num_inputs} inputs. CSV file saved to:", output_path)

# Remove rows where VG < VD
final_df = final_df[~(final_df['gate_voltage'] < final_df['drain_voltage'])]

# Save the cleaned dataset
output_path = r"C:\Sumukh\ML single stage\cs_current_source_cleaned_output.csv"
final_df.to_csv(output_path, index=False)

print("Rows with VG < VD removed. Cleaned CSV file saved to:", output_path)

# Convert voltage values to float for accurate comparison
def convert_to_float(value):
    try:
        if isinstance(value, str):
            if value.endswith('m'):
                return float(value.replace('m', '')) * 1e-3
            elif value.endswith('u'):
                return float(value.replace('u', '')) * 1e-6
            elif value.endswith('n'):
                return float(value.replace('n', '')) * 1e-9
            else:
                return float(value)
        return float(value)
    except:
        return None

final_df['gate_voltage_num'] = final_df['gate_voltage'].apply(convert_to_float)
final_df['drain_voltage_num'] = final_df['drain_voltage'].apply(convert_to_float)

# Remove rows where VG < VD after numeric conversion
final_df = final_df[~(final_df['gate_voltage_num'] < final_df['drain_voltage_num'])]

# Save the newly cleaned dataset
output_path = r"C:\Sumukh\ML single stage\cs_current_source_final_cleaned_output.csv"
final_df.to_csv(output_path, index=False)

print("Rows with VG < VD removed after numeric conversion. Final cleaned CSV file saved to:", output_path)
