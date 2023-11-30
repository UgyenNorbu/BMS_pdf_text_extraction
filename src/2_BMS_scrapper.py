import requests
import pandas
from bs4 import BeautifulSoup

# login_url = 'http://202.144.157.83/bms/public/p'
LOGIN_URL = "http://192.168.20.83/bms/public/p"

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
    # print("ORIGINAL")
    # print(df.head())

    df = df.drop([0, 2, 4])
    df = df.drop(df.columns[4], axis=1)
    # print("AFTER ROW DROPPING")
    # print(df.head())

    df.iat[1, 0] = df.iat[0, 2]
    df.iat[1, 1] = df.iat[0, 3]
    df = df.drop(df.columns[[2, 3]], axis=1)

    text = df.iloc[38, 0]
    text_spl = text.split(':')
    df.iloc[38, 0]  = text_spl[0].strip()
    df.iloc[38, 1] = text_spl[1].strip()

    # print("AFTER UPDATING CELL 0th COL")
    # print(df.tail(10))
    return df


# target_url = 'http://202.144.157.83/bms/public/brinv/bridgedata/112'
# target_url = "http://202.144.157.83/bms/public/brinv/bridgedata/120"
TARGET_URL = "http://192.168.20.83/bms/public/brinv/bridgedata/112"

output_df = scrap_table(session, TARGET_URL)
excel_filename = 'output/2.xlsx'
output_df.to_excel(excel_filename, index=False, header=None)


