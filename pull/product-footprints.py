import requests, json, csv, logging, multiprocessing, yaml, time, os
from functools import partial
from myconfig import email, password

# ✅ Pull only for Maine (US-ME) and India (IN)
states = ['US-ME', 'IN']

epds_url = "https://buildingtransparency.org/api/epds"
page_size = 250

logging.basicConfig(
    level=logging.DEBUG,
    filename="output.log",
    datefmt="%Y/%m/%d %H:%M:%S",
    format="%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s",
)
logger = logging.getLogger(__name__)

def log_error(status_code: int, response_body: str):
    logging.error(f"Request failed with status code: {status_code}")
    logging.debug("Response body:" + response_body)

def get_auth():
    url_auth = "https://buildingtransparency.org/api/rest-auth/login"
    headers_auth = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload_auth = {
        "username": email,
        "password": password
    }
    response_auth = requests.post(url_auth, headers=headers_auth, json=payload_auth)
    if response_auth.status_code == 200:
        authorization = 'Bearer ' + response_auth.json()['key']
        print("Fetched the new token successfully")
        return authorization
    else:
        print(f"Failed to login. Status code: {response_auth.status_code}")
        print("Response body:" + str(response_auth.json()))
        return None

def fetch_a_page(page: int, headers, state: str) -> list:
    logging.info(f'Fetching state: {state}, page: {page}')
    params = {"plant_geography": state, "page_size": page_size, "page_number": page}
    for attempt in range(5):
        response = requests.get(epds_url, headers=headers, params=params)
        if response.status_code == 200:
            return json.loads(response.text)
        elif response.status_code == 429:
            log_error(response.status_code, "Rate limit exceeded. Retrying...")
            time.sleep(2 ** attempt + 5)
        else:
            log_error(response.status_code, str(response.json()))
            return []
    return []

def fetch_epds(state: str, authorization) -> list:
    params = {"plant_geography": state, "page_size": page_size}
    headers = {"accept": "application/json", "Authorization": authorization}
    response = requests.get(epds_url, headers=headers, params=params)
    if response.status_code != 200:
        log_error(response.status_code, str(response.json()))
        return []
    total_pages = int(response.headers['X-Total-Pages'])
    full_response = []
    for page in range(1, total_pages + 1):
        page_data = fetch_a_page(page, headers, state)
        full_response.extend(page_data)
        time.sleep(1)
    time.sleep(10)
    return full_response

def remove_null_values(data):
    if isinstance(data, list):
        return [remove_null_values(item) for item in data if item is not None]
    elif isinstance(data, dict):
        return {k: remove_null_values(v) for k, v in data.items() if v is not None}
    return data

def get_zipcode_from_epd(epd):
    zipcode = epd.get('manufacturer', {}).get('postal_code')
    if not zipcode:
        zipcode = epd.get('plant_or_group', {}).get('postal_code')
    return zipcode

# ✅ Output to products-data folder
def create_folder_path(state, zipcode, display_name):
    base_path = os.path.join("../../products-data", state)
    if zipcode and len(zipcode) >= 5:
        return os.path.join(base_path, zipcode[:2], zipcode[2:], display_name)
    else:
        return os.path.join(base_path, "unknown", display_name)

def save_json_to_yaml(state: str, json_data: list):
    filtered_data = remove_null_values(json_data)
    for epd in filtered_data:
        display_name = epd['category']['display_name'].replace(" ", "_")
        material_id = epd['material_id']
        zipcode = get_zipcode_from_epd(epd) or "unknown"
        folder_path = create_folder_path(state, zipcode, display_name)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{material_id}.yaml")
        with open(file_path, "w") as yaml_file:
            yaml.dump(epd, yaml_file, default_flow_style=False)

def map_response(epd: dict) -> dict:
    return {
        'Category_epd_name': epd['category']['openepd_name'],
        'Name': epd['name'],
        'ID': epd['open_xpd_uuid'],
        'Zip': epd['plant_or_group'].get('postal_code', None),
        'County': epd['plant_or_group'].get('admin_district2', None),
        'Address': epd['plant_or_group'].get('address', None),
        'Latitude': epd['plant_or_group'].get('latitude', None),
        'Longitude': epd['plant_or_group'].get('longitude', None)
    }

def write_csv_others(title: str, epds: list):
    os.makedirs("../../products-data", exist_ok=True)
    with open(f"../../products-data/{title}.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "ID", "Zip", "County", "Address", "Latitude", "Longitude"])
        for epd in epds:
            writer.writerow([epd['Name'], epd['ID'], epd['Zip'], epd['County'], epd['Address'], epd['Latitude'], epd['Longitude']])

def write_csv_cement(epds: list):
    os.makedirs("../../products-data", exist_ok=True)
    with open("../../products-data/Cement.csv", "a") as csv_file:
        writer = csv.writer(csv_file)
        for epd in epds:
            writer.writerow([epd['Name'], epd['ID'], epd['Zip'], epd['County'], epd['Address'], epd['Latitude'], epd['Longitude']])

def write_epd_to_csv(epds: list, state: str):
    cement_list = []
    others_list = []
    for epd in epds:
        if epd is None:
            continue
        category_name = epd['Category_epd_name'].lower()
        if 'cement' in category_name:
            cement_list.append(epd)
        else:
            others_list.append(epd)
    write_csv_cement(cement_list)
    write_csv_others(state, others_list)

# ✅ MAIN SCRIPT
if __name__ == "__main__":
    authorization = get_auth()
    if authorization:
        for state in states:
            print(f"Fetching and processing: {state}")
            results = fetch_epds(state, authorization)
            save_json_to_yaml(state, results)
            mapped_results = [map_response(epd) for epd in results]
            write_epd_to_csv(mapped_results, state)
