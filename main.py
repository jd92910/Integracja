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
TABLE_NAME2 = 'fertility_poland'
def create_table_if_not_exists(cursor, var):
    if var == '1':
        cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    observation_date VARCHAR(20),
                    value VARCHAR(100)
                )
            ''')
    elif var == '2':
        cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME2} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    observation_date VARCHAR(20),
                    value VARCHAR(100)
                )
            ''')

def import_csv_to_mysql(csv_file, var):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    create_table_if_not_exists(cursor, var)

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(row['Variable observation date'][:4])
            if year >= 1990:
                if var == '1':
                    cursor.execute(
                        f"INSERT INTO {TABLE_NAME} (observation_date, value) VALUES (%s, %s)",
                        (row['Variable observation date'], row['Variable observation value'])
                    )
                elif var == '2':
                    cursor.execute(
                        f"INSERT INTO {TABLE_NAME2} (observation_date, value) VALUES (%s, %s)",
                        (row['Variable observation date'], row['Variable observation value'])
                    )
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Dane zaimportowano do bazy danych MySQL (od 1990 roku).")

def export_from_mysql_to_json(json_file, var):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    if var == '1':
        cursor.execute(f"SELECT observation_date, value FROM {TABLE_NAME} WHERE LEFT(observation_date, 4) >= '1990'")
        rows = cursor.fetchall()
    elif var == '2':
        cursor.execute(f"SELECT observation_date, value FROM {TABLE_NAME2} WHERE LEFT(observation_date, 4) >= '1990'")
        rows = cursor.fetchall()

    with open(json_file, mode='w', encoding='utf-8') as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)

    cursor.close()
    conn.close()
    print(f"✅ Dane zapisano do pliku {json_file}")

def export_from_mysql_to_xml(xml_file, var):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    if var == '1':
        cursor.execute(f"SELECT observation_date, value FROM {TABLE_NAME} WHERE LEFT(observation_date, 4) >= '1990'")
        rows = cursor.fetchall()
    elif var == '2':
        cursor.execute(f"SELECT observation_date, value FROM {TABLE_NAME2} WHERE LEFT(observation_date, 4) >= '1990'")
        rows = cursor.fetchall()

    root = ET.Element("root")

    for row in rows:
        item = ET.SubElement(root, "record")
        for key, val in row.items():
            child = ET.SubElement(item, key)
            child.text = str(val)

    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

    cursor.close()
    conn.close()
    print(f"✅ Dane zapisano do pliku {xml_file}")
'''
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
'''

def main():
    csv_file = 'Assets/GDP.csv'
    #csv_file = filter_data_from_1990(csv_file)
    csv_file2 = 'Assets/Fertility.csv'
    #csv_file2 = filter_data_from_1990(csv_file2)
    format_choice = input("Wybierz format wyjściowy (json/xml): ").strip().lower()
    file_choice = input("Wybierz plik do sformatowania (1-GDP/2-Fertility): ")
    '''''
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
    '''
    if file_choice == '1':
        import_csv_to_mysql(csv_file, file_choice)
        if format_choice == 'json':
            export_from_mysql_to_json('Assets/output.json', file_choice)
        elif format_choice == 'xml':
            export_from_mysql_to_xml('Assets/output.xml', file_choice)
        else:
            print("❌ Nieznany format. Wybierz 'json' lub 'xml'.")
    elif file_choice == '2':
        import_csv_to_mysql(csv_file2, file_choice)
        if format_choice == 'json':
            export_from_mysql_to_json('Assets/output2.json', file_choice)
        elif format_choice == 'xml':
            export_from_mysql_to_xml('Assets/output2.xml', file_choice)
        else:
            print("❌ Nieznany format. Wybierz 'json' lub 'xml'.")

if __name__ == "__main__":
    main()
