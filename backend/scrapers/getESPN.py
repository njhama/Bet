from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

nba_team_codes = [
    "atl", "bkn", "bos", "cha", "chi", "cle", "dal", "den", "det", "gsw",
    "hou", "ind", "lac", "lal", "mem", "mia", "mil", "min", "nop", "nyk",
    "okc", "orl", "phi", "phx", "por", "sac", "sas", "tor", "uta", "was"
]

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--log-level=OFF") 
driver = webdriver.Chrome(options=chrome_options)

try:
    for team_code in nba_team_codes:
        try:
            driver.get(f'https://www.espn.com/nba/team/stats/_/name/{team_code}/table/game/sort/avgPoints/dir/desc')
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Table__TR--sm')))

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tables = soup.find_all('table', class_='Table')

            player_names = []
            player_stats = []

            for table_index, table in enumerate(tables):
                rows = table.find_all('tr', class_='Table__TR--sm')
                for row in rows:
                    cols = row.find_all('td')
                    col_data = [col.text.strip() for col in cols]
                    if table_index == 0:
                        player_names.append(col_data)
                    elif table_index == 1:
                        player_stats.append(col_data)

            player_to_stats_map = {name[0]: stats for name, stats in zip(player_names, player_stats)}

            # Print team code and mapping
            print(f"\nTeam: {team_code}")
            for player, stats in player_to_stats_map.items():
                print(f"{player}: {stats}")

        except TimeoutException:
            print(f"Timeout occurred while processing team {team_code}")

    input("Press Enter to close...")

finally:
    driver.quit()
