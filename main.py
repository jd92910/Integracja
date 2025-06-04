'''''
import csv
import json
import xml.etree.ElementTree as ET
'''
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import mysql.connector
import pandas as pd
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_CONFIG = {
    'host': 'localhost',
    'user': 'nigga',
    'password': 'pass',
    'database': 'gdp_data'
}

def save_csv_to_mysql(file: UploadFile, table_name: str):
    df = pd.read_csv(file.file)
    df = df[df['Variable observation date'].astype(str).str[:4].astype(int) >= 1990]
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Tworzenie tabeli
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            observation_date VARCHAR(50),
            value DOUBLE
        )
    ''')
    cursor.execute(f"DELETE FROM {table_name}")

    for _, row in df.iterrows():
        cursor.execute(
            f"INSERT INTO {table_name} (observation_date, value) VALUES (%s, %s)",
            (row['Variable observation date'], row['Variable observation value'])
        )
    conn.commit()
    cursor.close()
    conn.close()

def fetch_data_from_table(table_name):
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(f"SELECT observation_date, value FROM {table_name}", conn)
    conn.close()
    return df

@app.post("/upload")
async def upload(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    save_csv_to_mysql(file1, "table1")
    save_csv_to_mysql(file2, "table2")
    return {"message": "Pliki załadowano i zapisano do bazy danych."}

@app.get("/chart", response_class=HTMLResponse)
async def chart(request: Request):
    df1 = fetch_data_from_table("table1")
    df2 = fetch_data_from_table("table2")
    df1.sort_values('observation_date', inplace=True)
    df2.sort_values('observation_date', inplace=True)
    return templates.TemplateResponse("chart.html", {
        "request": request,
        "df1_dates": df1['observation_date'].tolist(),
        "df1_values": df1['value'].tolist(),
        "df2_dates": df2['observation_date'].tolist(),
        "df2_values": df2['value'].tolist()
    })