from bs4 import BeautifulSoup
import pandas
import requests
import time

LOGIN_URL = 'http://202.144.157.83/bms/public/p'
# LOGIN_URL = "http://192.168.20.83/bms/public/p"

username = 'unorbu@moit.gov.bt'
password = 'abcd1234'

session = requests.Session()
login_payload = {
    'username': username,
    'password': password,
}
login_response = session.post(LOGIN_URL, data=login_payload)

def scrap_table(session_input, url):
    target_page_response = session_input.get(url)
    soup = BeautifulSoup(target_page_response.text, 'html.parser')

    table = soup.find('table', class_='table table-bordered table-striped table-hover')

    rows = []
    for row in table.find_all('tr'):
        row_data = [cell.text for cell in row.find_all(['td', 'th'])]
        rows.append(row_data)

    df = pandas.DataFrame(rows)

    df = df.drop([0, 2, 4])
    df = df.drop(df.columns[4], axis=1)

    df.iat[1, 0] = df.iat[0, 2]
    df.iat[1, 1] = df.iat[0, 3]
    df = df.drop(df.columns[[2, 3]], axis=1)

    text = df.iloc[38, 0]
    text_spl = text.split(':')
    df.iloc[38, 0]  = text_spl[0].strip()
    df.iloc[38, 1] = text_spl[1].strip()
    df.iloc[7,0] = df.iloc[7,0].strip()

    return df

# Read URL from CSV file and export excel with unique names
data = pandas.read_csv("data/url_list.csv", header=None)

def export_data(n, input_df):
    data_select = input_df.iloc[n][0]
    TARGET_URL = "http://202.144.157.83" + data_select
    file_name = "output/BMS_" + str(data_select.split("bridgedata/")[1]).strip() + ".xlsx"
    output_df = scrap_table(session, TARGET_URL)
    time.sleep(5)
    output_df.to_excel(file_name, index=False, header=None)
    print(n)
    print("DONE...")

for i in range(105, 116):
    export_data(i, data)
    time.sleep(1)
