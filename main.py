import csv
import json
import xml.etree.ElementTree as ET
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'nigga',
    'password': 'pass',
    'database': 'gdp_data'
}

TABLE_NAME = 'gdp_poland'

def create_table_if_not_exists(cursor):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            observation_date VARCHAR(20),
            value VARCHAR(100)
        )
    ''')

def import_csv_to_mysql(csv_file):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    create_table_if_not_exists(cursor)

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(row['Variable observation date'][:4])
            if year >= 1990:
                cursor.execute(
                    f"INSERT INTO {TABLE_NAME} (observation_date, value) VALUES (%s, %s)",
                    (row['Variable observation date'], row['Value'])
                )
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Dane zaimportowano do bazy danych MySQL (od 1990 roku).")

def filter_data_from_1990(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        filtered_data = [row for row in reader if int(row['Variable observation date'][:4]) >= 1990]
    return filtered_data

def csv_to_json(csv_file, json_file):
    with open(json_file, mode='w', encoding='utf-8') as f:
        json.dump(csv_file, f, indent=4, ensure_ascii=False)


def csv_to_xml(csv_file, xml_file):
        root = ET.Element("root")

        for row in csv_file:
            item = ET.SubElement(root, "record")
            for key, val in row.items():
                child = ET.SubElement(item, key.strip())
                child.text = val.strip()

        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)


def main():
    csv_file = 'Assets/GDP.csv'
    csv_file = filter_data_from_1990(csv_file)
    csv_file2 = 'Assets/Fertility.csv'
    csv_file2 = filter_data_from_1990(csv_file2)
    format_choice = input("Wybierz format wyjściowy (json/xml): ").strip().lower()
    file_choice = input("Wybierz plik do sformatowania (1-GDP/2-Fertility): ")
    if file_choice == '1':
        if format_choice == 'json':
            csv_to_json(csv_file, 'Assets/output.json')
            print("Dane zapisano do pliku output.json")
        elif format_choice == 'xml':
            csv_to_xml(csv_file, 'Assets/output.xml')
            print("Dane zapisano do pliku output.xml")
        else:
            print("Nieznany format. Wybierz 'json' lub 'xml'.")
    elif file_choice == '2':
        if format_choice == 'json':
            csv_to_json(csv_file2, 'Assets/output2.json')
            print("Dane zapisano do pliku output2.json")
        elif format_choice == 'xml':
            csv_to_xml(csv_file2, 'Assets/output2.xml')
            print("Dane zapisano do pliku output2.xml")
        else:
            print("Nieznany format. Wybierz 'json' lub 'xml'.")

if __name__ == "__main__":
    main()