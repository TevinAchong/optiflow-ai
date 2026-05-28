from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
print(f"ROOT folder: {ROOT}")

OUT = ROOT / "data" / "sample"
OUT.mkdir(parents=True, exist_ok=True) # actually creates the out folder

random_number_generator = np.random.default_rng(seed=42)

START_DATE = "2027-01-01"
DAYS = 180
DATES = pd.date_range(START_DATE, periods=DAYS, freq="D")

CONTRACTS = [
    {
        "contract_id": "C1",
        "contract_name:" : "Contract 1",
        "min_inventory" : -100_000,
        "max_inventory" : 250_000
    },
    {
        "contract_id": "C2",
        "contract_name:" : "Contract 2",
        "min_inventory" : -100_000,
        "max_inventory" : 250_000
    },
    {
        "contract_id": "C3",
        "contract_name:" : "Contract 3",
        "min_inventory" : -225_000,
        "max_inventory" : 300_000
    },
    {
        "contract_id": "C4",
        "contract_name:" : "Contract 4",
        "min_inventory" : -225_000,
        "max_inventory" : 300_000
    }
]

ASSETS = [
    {
        "asset_id": "A1",
        "asset_name": "Plant 1",
        "asset_type": "plant"
    },
    {
        "asset_id": "A2",
        "asset_name": "Plant 2",
        "asset_type": "plant"
    },
    {
        "asset_id": "A3",
        "asset_name": "Plant 3",
        "asset_type": "plant"
    },
    {
        "asset_id": "A4",
        "asset_name": "Tank 1",
        "asset_type": "tank"
    },
    {
        "asset_id": "A5",
        "asset_name": "Jetty 1",
        "asset_type": "jetty"
    }
]

def make_contracts() -> pd.DataFrame:
    '''
    Create a DataFrame of contracts with columns: contract_id, contract_name, min_inventory, max_inventory
    '''
    return pd.DataFrame(CONTRACTS)

def make_assets() -> pd.DataFrame:
    '''
    Create a DataFrame of assets with columns: asset_id, asset_name, asset_type
    '''
    return pd.DataFrame(ASSETS)

def make_inventory_baseline(simulation_low_inventory: int, simulation_high_inventory: int) -> pd.DataFrame:
    '''
    Creates a DataFrame containing the inventory of each contract
    on the first day of the contract year
    '''
    rows = []
    for contract in CONTRACTS:
        rows.append({
            "date" : START_DATE,
            "contract_id" : contract["contract_id"],
            "opening_inventory_mmbtu" : int(random_number_generator.integers(simulation_low_inventory, simulation_high_inventory))
        })
    return pd.DataFrame(rows)

def make_production_forecast() -> pd.DataFrame:
    '''
    For each day in the contract year, 
    for each contract, create a production forecast by
    sampling from a normal distribution with mean 0 and std 10,000
    '''
    rows = []
    for d in DATES:
        for c in CONTRACTS:
            # Generates one random number from a normal distribution
            # Average value = 24,000 
            # Typical variation = 4,000
            base_volume = random_number_generator.normal(24_000, 4_000)

            # Determines if the loss in production for a given day is an integer between 
            # 8000 and 17,999 or 0 based on the number produced by .random()
            # .random() outputs from 0.00 to 1.00
            maintenance_hit = 0 if random_number_generator.random() > 0.04 else random_number_generator.integers(8_000, 18_000)

            # Max is used in case the maintenance hit ends up being higher than 
            # the base production volume
            production = max(0, base_volume - maintenance_hit)

            rows.append({
                "date" : d.date().isoformat(),
                "contract_id" : c["contract_id"],
                "production_mmbtu" : round(production, 2)
            })
    return pd.DataFrame(rows)


