# import_data.py – FINAL CLEAN VERSION
import pandas as pd
from app import app, db, Company
import os

if os.path.exists("companies.db"):
    os.remove("companies.db")
    print("Deleted old database")

df = pd.read_excel(r"finalcleaned_NF'26_Varun_Chandar.xlsx", sheet_name="Sheet1")

with app.app_context():
    db.create_all()
    added = 0
    for _, row in df.iterrows():
        company = str(row['Company Name']).strip()
        if not company or company.lower() in ['company name', 'nan']:
            continue

        new = Company(
            name=company,
            poc_name=str(row['Name of POC']) if pd.notna(row['Name of POC']) else 'Unknown',
            designation=str(row['Designation']) if pd.notna(row['Designation']) else 'Unknown',
            mobile=str(row['Phone number']) if pd.notna(row['Phone number']) else '',
            email=str(row['Email']) if pd.notna(row['Email']) else ''
        )
        db.session.add(new)
        added += 1

    db.session.commit()
    print(f"Successfully imported {added} contacts!")