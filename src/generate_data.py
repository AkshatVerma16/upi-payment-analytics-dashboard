import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# 1. Get the current folder where this script is saved (src folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Define the path for the data folder (One level up, then into 'data')
data_dir = os.path.join(current_dir, '..', 'data')

# 3. Create 'data' folder if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created directory: {data_dir}")

def create_upi_dataset(rows=5000):
    users = [f'User_{i}' for i in range(1, 101)]
    merchants = ['Amazon', 'Zomato', 'Swiggy', 'Local_Kirana', 'Petrol_Pump', 'Airtel', 'Netflix']
    locations = ['Delhi', 'Mumbai', 'Bangalore', 'Kanpur', 'Pune']
    types = ['P2P', 'P2M']

    data = []
    start_date = datetime(2026, 1, 1)

    for i in range(rows):
        txn_id = f'TXN_{10000 + i}'
        user = random.choice(users)
        
        if random.random() > 0.15:
            amount = round(random.uniform(10, 500), 2)
        else:
            amount = round(random.uniform(2000, 50000), 2)

        dt = start_date + timedelta(days=random.randint(0, 90), 
                                    hours=random.randint(0, 23), 
                                    minutes=random.randint(0, 59))
        
        data.append([txn_id, user, amount, dt, random.choice(merchants), 
                     random.choice(locations), random.choice(types)])

    df = pd.DataFrame(data, columns=['transaction_id', 'user_id', 'amount', 
                                     'date_time', 'merchant', 'location', 'payment_type'])
    
    # 4. Save using the absolute path
    file_path = os.path.join(data_dir, 'upi_data.csv')
    df.to_csv(file_path, index=False)
    
    print(f"SUCCESS: File saved at: {file_path}")

if __name__ == "__main__":
    create_upi_dataset()