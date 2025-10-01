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
# Fixed date (2025-01-01) ensures reproducible.
# The date needs to be the current date to allow for linear timing reltionship
TODAY = datetime(2025, 9, 27) 

# The user defined Coefficients for each attribute for the Linear Relationship based on attribute
# Y = Intercept + (C1*X1) + (C2*X2) + (C3*X3) + (C4*X4) + Noise
COEFFICIENTS = {
    "event_duration": 0.15,          # Coefficient for event duration (minutes)
    "participants_count": 0.8,       # Coefficient for participant count
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
        
        # Generate the event date +/- 60 days from TODAY
        # below 3 lines may be implemented in the event of consistent date needed, otherwise the TODAY needs todays date
        # start_date = TODAY - timedelta(days=60)
        # end_date = TODAY + timedelta(days=60)
        # event_date_raw = fake.date_between_dates(date_start=start_date.date(), date_end=end_date.date())
        event_date_raw = fake.date_between(start_date="-60d", end_date="+60d")

        
        # Calculate Time Until Event in Days
        # Convert the date object to a datetime object for comparison with TODAY
        event_datetime = datetime(event_date_raw.year, event_date_raw.month, event_date_raw.day)
        # time_until_event_days is positive for future events, negative for past events
        time_until_event_days = (event_datetime - TODAY).days

        # Calculate the base target score (Y_base) based on the linear model
        base_score = (
            C["base_intercept"] + 
            (C["event_duration"] * duration) +
            (C["participants_count"] * participants) + 
            (C["resources_required"] * resources) + 
            (C["time_until_event"] * time_until_event_days)
        )
        
        # Add normally distributed noise to simulate realworld imperfect data
        noise = np.random.normal(0, C["noise_scale"])
        
        # Final priority score (Y)
        final_score = base_score + noise
        
        # Ensure the score is positive and not too insignificant
        final_score = max(1.0, final_score) 

        event = {
            "event_name": fake.catch_phrase(),
            "event_duration": duration,
            "participants_count": participants,
            # TODO: modify resources_required to be any other attributes needed
            "resources_required": resources,
            "event_date": event_date_raw.isoformat(),
            "time_until_event_days": time_until_event_days,
            # Target variable (Y) 
            # "calculated_priority_score": final_score
            # "predicted_priority": final_score # is generating priority from linear relations
            "generated_priority": final_score
        }
        events.append(event)
    return pd.DataFrame(events)

if __name__ == "__main__":
    df = generate_synthetic_events(200)
    # output_filepath = "../data/synthetic_training_data.csv"
    output_filepath = "../data/synthetic_training_data_updated.csv"
    # df.to_csv("../data/fake_events.csv", index=False)
    df.to_csv(output_filepath, index=False)
    # print("Generated 200 fake events => data/fake_events.csv")
    
    print(f"Generated {len(df)} synthetic training records => {output_filepath}")
    print("\n--- Hidden from ML Linear Relationship (Model's Goal) ---")
    for key, value in COEFFICIENTS.items():
        if key not in ["base_intercept", "noise_scale"]:
            print(f"  Feature '{key}': Coefficient = {value}")
    print(f"  Intercept (Baseline): {COEFFICIENTS['base_intercept']}")
    print(f"  Noise (Standard Deviation): {COEFFICIENTS['noise_scale']}")