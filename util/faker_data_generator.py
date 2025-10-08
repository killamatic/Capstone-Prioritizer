from faker import Faker
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set a fixed seed for the built-in random module
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# Set a fixed seed for the Faker instance for reproducibility
Faker.seed(SEED)
fake = Faker()

# Define a fixed reference date (Today) for consistent calculations.
# Fixed date (2025, 10, 8) ensures reproducible.
# The date needs to be the current date to allow for linear timing reltionship
TODAY = datetime(2025, 10, 8) 

# The user defined Coefficients for each attribute for the Linear Relationship based on attribute
# Y = Intercept + (C1*X1) + (C2*X2) + (C3*X3) + (C4*X4) + Noise
COEFFICIENTS = {
    "event_duration": 0.15,          # Coefficient for event duration (minutes)
    "participant_count": 0.8,       # Coefficient for participant count
    "resources_required": 2.5,       # Coefficient for resources required
    "time_until_event": -1.2,        # Coefficient for date time (closer event) -> higher priority
    "base_intercept": 50.0,          # Increased baseline score
    "noise_scale": 2.0               # Standard deviation of the noise
}

def generate_synthetic_events(n=100):
    """
    Generates synthetic event data where the target variable (calculated_priority_score) is a linear function of the input features.
    """
    events = []
    # store local coefficients
    C = COEFFICIENTS

    for _ in range(n):
        # Generate input features (X)
        duration = random.choice([30, 60, 90, 120])  # minutes
        participants = random.randint(5, 150)
        resources = random.randint(1, 10)            # rooms/equipment
        
        # Generate the event date 0<date<60 days from TODAY
        event_date_raw = fake.date_between(start_date="-1d", end_date="+60d")

        
        # Calculate Time Until Event in Days
        # Convert the date object to a datetime object for comparison with TODAY
        event_datetime = datetime(event_date_raw.year, event_date_raw.month, event_date_raw.day)
        # time_until_event_days is positive for future events, negative for past events
        time_until_event_days = (event_datetime - TODAY).days

        # Calculate the base target score (Y_base) based on the linear model
        base_score = (
            C["base_intercept"] + 
            (C["event_duration"] * duration) +
            (C["participant_count"] * participants) + 
            (C["resources_required"] * resources) + 
            (C["time_until_event"] * time_until_event_days)
        )
        
        # Add normally distributed noise to simulate realworld imperfect data
        noise = np.random.normal(0, C["noise_scale"])
        
        # Final priority score (Y)
        final_score = base_score + noise
        
        # Ensure the score is positive and not too insignificant
        final_score = max(1.0, final_score) 

        final_score = scale_to_priority(final_score)

        event = {
            "event_name": fake.catch_phrase(),
            "event_duration": duration,
            "participant_count": participants,
            "resources_required": resources,
            "event_date": event_date_raw.isoformat(),
            "time_until_event_days": time_until_event_days,
            # Target variable (Y) 
            "actual_priority": final_score
        }
        events.append(event)
    return pd.DataFrame(events)

def scale_to_priority(input_number: int) -> int:
    """
    Scales an input number from the range [1, 400] to an integer output 
    in the range [1, 10].

    Args:
        input_number: The number to scale (expected to be between 1 and 400).

    Returns:
        int: The scaled priority score (between 1 and 10).
    """
    print("the value inputed: ")
    print(input_number)
    # --- 1. Define the ranges ---
    MIN_IN = 1
    MAX_IN = 400
    MIN_OUT = 1
    MAX_OUT = 10

    if (input_number < MIN_IN):
        input_number = 1
    if(input_number > MAX_IN):
        input_number = 400

    print("after input capture: ")
    print(input_number)

    # Formula: V_out = ((V_in - Min_in) * (Max_out - Min_out) / (Max_in - Min_in)) + Min_out
    input_normalized = (input_number - MIN_IN) / (MAX_IN - MIN_IN)
    scaled_value = (input_normalized * (MAX_OUT - MIN_OUT)) + MIN_OUT
    
    # Clamp and Round the floating-point result to the nearest integer
    priority = round(scaled_value)

    # Ensure the result is strictly clamped between 1 and 10 for safety
    final_priority = max(MIN_OUT, min(MAX_OUT, priority))

    print("final priority: ")
    print(final_priority)

    return final_priority

if __name__ == "__main__":
    df = generate_synthetic_events(200)
    # output_filepath = "../data/synthetic_training_data.csv"
    output_filepath = "../data/synthetic_training_data_updated.csv"
    # df.to_csv("../data/fake_events.csv", index=False)
    df.to_csv(output_filepath, index=False)
    
    print(f"Generated {len(df)} synthetic training records => {output_filepath}")
    print("\n--- Hidden from ML Linear Relationship (Model's Goal) ---")
    for key, value in COEFFICIENTS.items():
        if key not in ["base_intercept", "noise_scale"]:
            print(f"  Feature '{key}': Coefficient = {value}")
    print(f"  Intercept (Baseline): {COEFFICIENTS['base_intercept']}")
    print(f"  Noise (Standard Deviation): {COEFFICIENTS['noise_scale']}")