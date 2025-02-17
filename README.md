# ML_Single_Stage_Amplifier

# Single-Stage Amplifier Design using Machine Learning

This repository contains implementation and resources for automating the design of single-stage MOSFET amplifiers using machine learning techniques. The project combines Cadence Virtuoso for circuit simulation with Python-based machine learning models to optimize amplifier parameters.

## Circuit Configurations

The project includes four fundamental single-stage amplifier configurations:

### 1. Common Source with Resistive Bias
- NMOS transistor (g45n1lvt process)
- Resistive drain load (R0)
- Key features:
  - Voltage gain with signal inversion
  - Simple biasing scheme
  - Moderate output impedance
  - Basic gain-bandwidth trade-off
![WhatsApp Image 2025-02-12 at 15 00 17_9fc79c80](https://github.com/user-attachments/assets/7e77d96f-2033-4eaa-af21-185c6e450519)

### 2. Common Source with Diode Load
- Dual NMOS configuration (g45n1lvt)
- Diode-connected load transistors (w:120n)
- Advantages:
  - Improved voltage headroom
  - Better linearity
  - Suitable for differential pairs
  - Self-biasing capability
![WhatsApp Image 2025-02-13 at 15 42 50_1458fe6c](https://github.com/user-attachments/assets/2a9a330a-6df8-4074-bb40-98a3b2732af5)

### 3. Common Source with Current Load
- PMOS current source load (g45p1lvt)
- NMOS input device (g45n1lvt)
- Benefits:
  - Higher voltage gain
  - Enhanced power supply rejection
  - Better output impedance
  - Improved common-mode rejection
![WhatsApp Image 2025-02-13 at 17 40 23_ba6757fe](https://github.com/user-attachments/assets/50190bf8-d831-455b-bc9d-562a51d67898)

### 4. Common Drain (Source Follower)
- NMOS in source follower configuration
- Resistive source load
- Characteristics:
  - Unity voltage gain
  - No phase inversion
  - Low output impedance
  - Excellent input-output isolation
![WhatsApp Image 2025-02-15 at 15 06 36_b9f8baa7](https://github.com/user-attachments/assets/28b2aff6-a6a9-4931-bd8e-461b37b1282f)

## Project Structure

```
project-root/
├── data/
│   └── final.xlsx    # Raw simulation data
├── src/
│   ├── convertor_final_cleaned.py        # Data preprocessing
│   └── prediction.py                     # ML model implementation
├── documentation/
│   └── circuit_diagrams/                 # Circuit configuration images
└── README.md                             # This file
```

## Implementation Details

### Data Processing
The `convertor_final_cleaned.py` script handles:
- Reading raw Cadence simulation data
- Cleaning and normalizing parameters
- Validating operating conditions (VG < VD checks)
- Feature engineering for ML input
- Export of processed datasets

### Machine Learning Pipeline
The `prediction.py` script implements:
- Data loading and preprocessing
- Model training using XGBoost
- Parameter prediction functions
- Performance validation
- Model persistence

## Usage

### Prerequisites
```bash
python -m pip install -r requirements.txt
```

### Data Processing
```bash
python src/convertor_final_cleaned.py --input data/raw --output data/processed
```

### Model Training
```bash
python src/prediction.py --data data/processed/training_data.csv --save-model models/
```

### Parameter Prediction
```python
from src.prediction import predict_amplifier_params

# Example usage
params = predict_amplifier_params(
    desired_gain=0.463,
    bandwidth=55330000,
    power_consumption=0.01381
)
print(params)
```

## Requirements
- Python 3.8+
- pandas >= 1.2.0
- numpy >= 1.19.0
- xgboost >= 1.3.0
- scikit-learn >= 0.24.0
- Cadence Virtuoso (for circuit simulation)

## Model Performance
Current model achieves:
- Mean Absolute Error (MAE): < 5% for all parameters
- R² Score: > 0.90 for critical parameters
- Prediction Time: < 100ms per configuration

## Future Improvements
- [ ] Integration with Cadence Ocean Scripts
- [ ] Support for additional amplifier topologies
- [ ] Neural network-based parameter optimization
- [ ] Automated design space exploration
- [ ] Temperature and process variation analysis

## Acknowledgments
- Prof. Sakshi Arora
- Prof. Madhav Roa
- Omkar Gavandi
- Nitheesh Kumar
- Vaishnavi Sharma

