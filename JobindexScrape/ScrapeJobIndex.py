import requests
from bs4 import BeautifulSoup
import re
import html
import csv

jobs = []

for side in range(1, 4):
    URL = f"https://www.jobindex.dk/jobsoegning?address=Lucernevej+7%2C+8200+Aarhus+N&page={side}&radius=100&q=plc-programmering+plc+hmi+scada+automationsteknolog+%27automation+engineer%27"

    page = requests.get(URL)

    matches = re.findall(r'"html":"(.*?)","', page.text)

    for job_html in matches:

        job_html = job_html.replace('\\"', '"').replace('\\/', '/')
        job_html = html.unescape(job_html)

        soup = BeautifulSoup(job_html, "html.parser")

        #-------------------------------------------------------------

        job_card = soup.select_one("div.jobsearch-result")

        title_card = soup.find("h4")

        if title_card:
            title_card = title_card.text.replace("\\", "")

        location_card = soup.find("span", class_="jix_robotjob--area")

        distance_card = soup.find("span", class_="job-distance")

        if distance_card:
            distance_card = distance_card.text.replace("\\", "").replace("n", "").replace("km", "")

        
        #-------------------------------------------------------------------------

        if job_card:

            company_element = job_card.select_one(".jix-toolbar-top__company a")

            if company_element:
                company_card = company_element.get_text(strip=True)
            else:
                company_card = "Ukendt"

            link = job_card.select_one("a.seejobmobil")

            if link:

                if location_card:
                    location = location_card.get_text(strip=True)
                else:
                    location = "Ukendt"

                if distance_card:
                    distance = distance_card
                else:
                    distance = "Ukendt"

                jobs.append({
                    "Virksomhed": company_card,
                    "Jobtitel": title_card,
                    "Lokation": location,
                    "Afstand": distance,
                    "Enhed": "km",
                    "Link": link.get("href")
                })


with open("jobindex_jobs.csv", "w", newline="", encoding="utf-8-sig") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=["Virksomhed", "Jobtitel", "Lokation", "Afstand","Enhed", "Link"],
        delimiter=";"
    )

    writer.writeheader()
    writer.writerows(jobs)

print(f"{len(jobs)} jobs gemt i jobindex_jobs.csv")