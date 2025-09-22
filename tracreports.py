import re, time
import sys
from decimal import Decimal

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
uc.Chrome.__del__ = lambda self: None

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get('https://tracreports.org/phptools/immigration/ntanew/')
    return driver


def choice_parameter(driver, wait):
    try:
        all_cases = driver.find_element(By.ID, 'stat_count')
        all_cases.click()
        console_print('*******************************\n')
        console_print('All cases choices')
    except:
        print('All cases not choices')

    time.sleep(1)

    try:
        by_fiscal_year = driver.find_element(By.ID, 'timescale_fy')
        by_fiscal_year.click()
        console_print('Fiscal year choices\n\n*******************************\n')
    except:
        print('Fiscal year not choices')

    time.sleep(1)

    try:
        driver.find_element(By.ID, 'headlessui-listbox-button-1').click()
        time.sleep(1)
        nationality = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[.//span[text()='Nationality']]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nationality)
        time.sleep(1)
        nationality.click()
        console_print('Nationality selected')
    except:
        pass

    time.sleep(1)

    try:
        driver.find_element(By.ID,'headlessui-listbox-button-3').click()
        time.sleep(1)
        immigrant_count = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[.//span[text()='Immigrant County']]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", immigrant_count)
        time.sleep(1)
        immigrant_count.click()
        console_print('Immigrant County selected')
    except:
        pass
    time.sleep(1)

    try:
        driver.find_element(By.ID,'headlessui-listbox-button-5').click()
        time.sleep(1)
        how_long_in_us = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[.//span[text()='How Long in U.S.']]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", how_long_in_us)
        time.sleep(1)
        how_long_in_us.click()
        console_print('How Long in U.S. selected\n\n*******************************\n')
    except:
        pass

    time.sleep(5)


def select_nationality_by_text(driver, nationality):
    try:
        select_nationality = driver.find_element(By.XPATH,f'//*[@id="app"]/div/div/div[3]/div/div[1]/div[2]/div/div/div/table/tbody/tr[.//td[text()="{nationality}"]]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_nationality)
        time.sleep(1)
        select_nationality.click()
        time.sleep(1)
    except:
        pass


def select_immigrant_country_by_text(driver, immigrant_country):
    try:
        select_immigrant_country = driver.find_element(By.XPATH,
                                                 f'//*[@id="app"]/div/div/div[3]/div/div[2]/div[2]/div/div/div/table/tbody/tr[.//td[text()="{immigrant_country}"]]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_immigrant_country)
        time.sleep(1)
        select_immigrant_country.click()
        time.sleep(1)
    except:
        pass


def select_how_long_in_us_by_text(driver, how_long_in_us):
    try:
        select_how_long = driver.find_element(By.XPATH,
                                                       f'//*[@id="app"]/div/div/div[3]/div/div[3]/div[2]/div/div/div/table/tbody/tr[.//td[text()="{how_long_in_us}"]]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_how_long)
        time.sleep(1)
        select_how_long.click()
        time.sleep(1)
    except:
        pass


def apply_client_filters(driver, nationality=None, immigrant_country=None, how_long_in_us=None):

    if nationality:
        select_nationality_by_text(driver, nationality)
        print(f'Nationality selected {nationality}')

    if immigrant_country:
        select_immigrant_country_by_text(driver, immigrant_country)
        print(f'Immigrant country selected {immigrant_country}')
    if how_long_in_us:
        select_how_long_in_us_by_text(driver, how_long_in_us)
        print(f'Hwo long in US selected {how_long_in_us}\n\n*******************************\n')
    time.sleep(10)


def _parse_number(s: str) -> int:
    s = s.strip().replace("\xa0", " ")
    s = s.replace(" ", "").replace(",", "")
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([kKmM]?)", s)
    if not m:
        s = re.sub(r"[^\d.]", "", s)
        return int(float(s)) if s else 0
    val, suf = m.groups()
    factor = 1_000 if suf.lower() == "k" else 1_000_000 if suf.lower() == "m" else 1
    return int(Decimal(val) * factor)

def extract_by_hover(driver, timeout=3):
    wait = WebDriverWait(driver, timeout)
    svg = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="barchart"]')))
    bars = svg.find_elements(By.CSS_SELECTOR, "#barchart > g > rect.bar") or \
           svg.find_elements(By.XPATH, ".//*[name()='rect' and contains(@class,'bar')]")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", svg)

    ac = ActionChains(driver)
    results, seen = [], set()

    for bar in bars:
        try:
            ac.move_to_element(bar).pause(0.30).perform()
        except Exception:
            ac.move_to_element_with_offset(bar, 1, -1).pause(0.20).perform()

        try:
            tip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tooltip")))
        except TimeoutException:
            continue

        text = (tip.text or tip.get_attribute("innerText") or "").replace("\xa0", " ").strip()
        m_fy = re.search(r"FY:\s*(\d+)", text)
        m_v  = re.search(r"Value:\s*([0-9][\d,.\s]*[kKmM]?)", text)
        if m_fy and m_v:
            fy = m_fy.group(1).zfill(2)
            val = _parse_number(m_v.group(1))
            if fy not in seen:
                results.append((fy, val))
                seen.add(fy)

    return sorted(results, key=lambda x: int(x[0]))

def prompt(msg: str) -> str:
    print(msg, end="", file=sys.stderr, flush=True)
    return input().strip()

def tee_print(msg: str, end: str = "\n"):
    """Печатает и в лог-файл (stdout), и в консоль (stderr)."""
    print(msg, end=end)
    print(msg, end=end, file=sys.stderr, flush=True)

def console_print(msg: str, end: str = "\n"):
    """Печатает ТОЛЬКО в консоль (stderr). Полезно для инструкций/подсказок."""
    print(msg, end=end, file=sys.stderr, flush=True)

def main():
    tee_print("=== Script starting ===\n")
    driver = None
    try:
        driver = create_driver()
        wait = WebDriverWait(driver, 10)
        choice_parameter(driver, wait)

        console_print(
            "Please enter the filters EXACTLY as they appear on TRAC Reports — "
            "New Proceedings Filed in Immigration Court.\n"
            "• Nationality — use the same country name as in the dropdown (e.g., All, Mexico, Cuba).\n"
            "• Immigrant destination — use the same county/city + state format (e.g., Dallas County, TX).\n"
            "• How long in the U.S. — use one of the site’s options (e.g., All-Mexico, Not Known, Between 3 and 4 years).\n"
            "Tip: Copy & paste from the site to avoid typos.\n\n*******************************\n"
        )

        nationality = prompt("Enter your nationality (e.g. Mexico, Cuba, US): ")
        immigrant_country = prompt("Enter immigrant country (e.g. Dallas County, TX): ")
        how_long_in_us = prompt("Enter how long you have lived in the US (e.g. All-Mexico, Not Known, Between 3 and 4 years): ")
        console_print('\nPlease wait ...\n')
        apply_client_filters(
            driver,
            nationality=nationality,
            immigrant_country=immigrant_country,
            how_long_in_us=how_long_in_us
        )

        time.sleep(5)
        rows = extract_by_hover(driver)
        for fy, val in rows:
            tee_print(f"FY {fy}: {val}")

        console_print("Completion of work ")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    Path("../logs").mkdir(exist_ok=True)
    with open("../logs/run.txt", "w", encoding="utf-8") as f, redirect_stdout(f):
        main()