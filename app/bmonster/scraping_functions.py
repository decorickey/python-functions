import logging
import urllib.parse
from collections import namedtuple
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

from .schemas import PerformerSchema
from .schemas import ScheduleSchema

BASE_URL = "https://www.b-monster.jp"
SCHEDULE_PATH = "reserve/"
PERFORMER_LIST_PATH = "instructors/"
PERFORMER_SEARCH_PATH = "_inc_/instructors/detail"


def _get_html_soup(url: str, params: dict = None):
    if params is None:
        params = {}
    r = requests.get(url, params=params, timeout=3)
    try:
        r.raise_for_status()
    except requests.exceptions.RequestException:
        logging.exception("Request Error")
        raise
    return BeautifulSoup(r.text, "html.parser")


def scraping_performer():
    url = urllib.parse.urljoin(BASE_URL, PERFORMER_LIST_PATH)
    soup = _get_html_soup(url)

    panels = soup.select("body section#instructors-panels div.panel")
    for panel in panels:
        performer_name = panel.find("h3").text

        url = urllib.parse.urljoin(BASE_URL, PERFORMER_SEARCH_PATH)
        soup = _get_html_soup(url, params={"nick_name": performer_name.lower()})
        href = soup.select_one("div.instructor-info a").get("href")
        query = urllib.parse.urlparse(href).query
        performer_id = urllib.parse.parse_qs(query).get("instructor_id")[0]
        yield PerformerSchema(id=performer_id, name=performer_name)


def _scraping_schedule(soup: BeautifulSoup):
    Item = namedtuple("Item", ["start_at", "instructor", "program"])
    week = soup.select("body div#scroll-box div.grid div.flex-no-wrap")
    for i, day in enumerate(week):
        panels = day.select("li.panel")
        for panel in panels:
            if (t := panel.select_one("p.tt-time")) and (text := t.text):
                start_time = text.split(" - ")[0]
                start_time = start_time.split(":")
                hour = int(start_time[0])
                minute = int(start_time[1])
                start_at = datetime.now(tz=ZoneInfo("Asia/Tokyo")).replace(
                    hour=hour, minute=minute, second=0, microsecond=0
                ) + timedelta(days=i)
            else:
                continue

            if p := panel.select_one("p.tt-instructor"):
                instructor = p.text
            else:
                continue

            if program := panel.select("p.tt-mode"):
                program = program[0]["data-program"]
                program = program if "(l)" not in program else program[:-3]
                if not program or program == "無料体験会":
                    continue
            else:
                continue

            if start_at and instructor and program:
                yield Item(start_at=start_at, instructor=instructor, program=program)


def scraping_schedule_by_performer(performer_id: int, performer_name: str):
    url = urllib.parse.urljoin(BASE_URL, SCHEDULE_PATH)
    params = {"instructor_id": performer_id, "date": date.today().isoformat()}
    soup = _get_html_soup(url, params)
    for item in _scraping_schedule(soup):
        yield ScheduleSchema(
            studio=item.instructor,
            start_at=item.start_at,
            performer_name=performer_name,
            program=item.program,
        )


def scraping_schedule_by_studio(studio_name: str, studio_code: str):
    url = urllib.parse.urljoin(BASE_URL, SCHEDULE_PATH)
    params = {"studio_code": studio_code}
    soup = _get_html_soup(url, params)
    for item in _scraping_schedule(soup):
        yield ScheduleSchema(
            studio=studio_name,
            start_at=item.start_at,
            performer_name=item.instructor,
            program=item.program,
        )
