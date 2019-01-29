#  -*- coding: utf-8 -*-
import contextlib
import datetime
import locale
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger()

COMMON_XPATH = './/bf-tournament-card/div/'
COMMON_INFORMATIONS_XPATH = f'{COMMON_XPATH}div[3]'
ORG_XPATH = f'{COMMON_XPATH}/div[4]/span'
NAME_XPATH = f'{COMMON_INFORMATIONS_XPATH}/div[1]/h4'
DATE_XPATH = f'{COMMON_INFORMATIONS_XPATH}/div[2]/table[1]/tbody/tr[1]/td[2]'
TIME_XPATH = f'{COMMON_INFORMATIONS_XPATH}/div[2]/table[1]/tbody/tr[2]/td[2]'
REGION_XPATH = f'{COMMON_INFORMATIONS_XPATH}/div[2]/table[2]/tbody/tr[1]/td[2]'
TN_NAME_ON_TN_PAGE_XPATH = '//*[@id="tournament"]/div/bf-tournament/div[2]/div[1]/div[3]/div/div/div[2]/div/ul/li[1]/a/span'
PRIZE_BUTTON_XPATH = '//*[@id="tournament"]/div/bf-tournament/div[2]/div/div[4]/div/div/bf-tournament-info/bf-tab-bar/div/div[3]/a'
PRIZE_XPATH = '//*[@id="tournament"]/div/bf-tournament/div[2]/div[1]/div[4]/div/div/bf-tournament-info/div[3]/div'


@contextlib.contextmanager
def setlocale(*args, **kw):
    """ Sets the locale.

    :param args:
    :param kw:
    """
    saved = locale.setlocale(locale.LC_ALL)
    yield locale.setlocale(*args, **kw)
    locale.setlocale(locale.LC_ALL, saved)


def get_tournaments(game, region='Global', platform='Any Platform', type='Any Format'):
    """Use Selenium to open the selected tournaments browsing page, and returns a list with each tournament as a dict.

    :param game: select between lol, fortnite, cod_bo4, hs, ow, pubg, fifa, c-ops, ssbu, shadowverse, qc
    :param region: Check below for each game. Default = Global
    :param platform: Check below for each game. Default = Any Platform
    :param type: solo, team, team&draft. Default = Any Format. All games have this critera available.
    :return

    LoL:
        Regions: North America, EU West, EU Nordic & East, Oceania, Russia, Turkey, Brazil, Republic of Korea, Latin America North, Latin America South, Japan
    Fortnite:
        Regions: Asia, South-east Asia, Europe, Latin America, North America, Oceania, Middle East, Africa
    Fortnite:
        Regions: Asia, South-east Asia, Europe, Latin America, North America, Oceania, Middle East, Africa
        Platforms: PC, Xbox One, PS4, Cross Platform, Mobile, Switch
    CoD BO4:
        Regions: Asia, South-east Asia, Europe, Latin America, North America, Oceania, Middle East, Africa
        Platforms: PC, Xbox One, PS4
    Hearthstone:
        Regions: Americas, Europe, Asia, China
        Platforms: PC
    Overwatch:
        Regions: Americas, Europe, Asia
        Platforms: PC, Xbox One, PS4
    PUBG:
        Regions: North America, Europe, Korea/Japan, Asia, Oceania, South and Central America, South East Asia
        Platforms: PC, Xbox One, PS4
    FIFA 19:
        Regions: Asia, South-east Asia, Europe, Latin America, North America, Oceania, Middle East, Africa
        Platforms: PC, Xbox One, PS4
    Critical Ops:
        Regions: North America, South America, Europe, Asia
        Platforms: PC, Xbox One, PS4
    """
    game_correspondance = {
        'lol': 'league-of-legends',
        'cod_bo4': 'call-of-duty-black-ops-4',
        'hs': 'hearthstone',
        'ow': 'overwatch',
        'pubg': 'playerunknowns-battlegrounds',
        'fifa': 'fifa-19',
        'c-ops': 'critical-ops',
        'ssbu': 'super-smash-bros-ultimate',
        'qc': 'quake-champions',
    }

    try:
        if game_correspondance[game]:
            game = game_correspondance[game]
    except KeyError:
        pass

    browser = webdriver.Chrome()  # replace with .Firefox(), or with the browser of your choice
    browser.implicitly_wait(10)
    initial_url = f"https://battlefy.com/browse/{game}?region={region}&platform={platform}&type={type}"
    browser.get(initial_url)  # navigate to the page

    tournaments = browser.find_elements_by_class_name('tournament-card-container')

    tournaments_count = len(tournaments)

    tournaments_list = []

    for tn_id in range(0, tournaments_count):

        tournaments = browser.find_elements_by_class_name('tournament-card-container')

        tournament = tournaments[tn_id]

        # Wait for the name of the tournament to be located by Selenium
        wait = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, NAME_XPATH))
        )

        element_to_click = tournament.find_element_by_xpath(NAME_XPATH)
        name_t = tournament.find_element_by_xpath(NAME_XPATH).text
        litteral_date = tournament.find_element_by_xpath(DATE_XPATH).text
        litteral_time = tournament.find_element_by_xpath(TIME_XPATH).text
        region = tournament.find_element_by_xpath(REGION_XPATH).text
        org_name = tournament.find_element_by_xpath(ORG_XPATH).text

        litteral_datetime = f'{str(datetime.datetime.now().year)} {litteral_date} {litteral_time}'

        actual_date = None
        with setlocale(locale.LC_ALL, "C"):
            # 2019 Tue, Jan 29th 1:45 AM GMT
            try:
                actual_date = time.strptime(litteral_datetime, "%Y %a, %b %dth %I:%M %p %Z")
            except ValueError:
                try:
                    actual_date = time.strptime(litteral_datetime, "%Y %a, %b %dst %I:%M %p %Z")
                except ValueError:
                    try:
                        actual_date = time.strptime(litteral_datetime, "%Y %a, %b %dnd %I:%M %p %Z")
                    except ValueError:
                        try:
                            actual_date = time.strptime(litteral_datetime, "%Y %a, %b %drd %I:%M %p %Z")
                        except:
                            logging.exception('')

        # Click on the tournament card
        element_to_click.click()

        # Wait for the tournament name to appear
        wait = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, TN_NAME_ON_TN_PAGE_XPATH))
        )
        # Then wait for the "Prize" tab to appear
        wait = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, PRIZE_BUTTON_XPATH))
        )

        # Scroll to the bottom of the page otherwise the Prize tab can be hidden by the "Join" button
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Click on Prize tab
        element_to_click = browser.find_element_by_xpath(PRIZE_BUTTON_XPATH)
        element_to_click.click()

        # Wait for the Prize text to be located
        wait = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, PRIZE_XPATH))
        )

        prize = browser.find_element_by_xpath(PRIZE_XPATH).text

        url = browser.current_url

        tn_dict = {
            'name': name_t,
            'url': url,
            'prize': prize,
            'date': actual_date,
            'region': region,
            'org': org_name
        }

        tournaments_list.append(tn_dict)

        browser.get(initial_url)

    browser.close()

