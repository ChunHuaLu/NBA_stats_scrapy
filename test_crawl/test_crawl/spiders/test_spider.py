import scrapy
import logging
import csv
import itertools

from selenium import webdriver
import xml.etree.ElementTree as ET
class TestScrapy(scrapy.Spider):
    name = "test"
    driver = webdriver.Chrome('/usr/local/bin/__pycache__/chromedriver')
    start_urls = [
        'https://stats.nba.com/game/0041900165/',
    ]


    def parse(self, response):
        self.driver.get(response.url)
        page = response.url.split('/')[-2]
        filename = 'scrape_data-%s.html' % page

        attributes_name = ["MIN", "FGM", "FGA",	"FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "PF", "PTS", "+/-"]
        team_stat_dict = dict()
        with open(filename, 'wb') as f:
            tmp = self.driver.find_elements_by_xpath("//div[@class='nba-stat-table__overflow']//tr[@data-ng-repeat]")

            x = []
            for item in tmp:
                content = "<div>"
                content = content + item.get_attribute('innerHTML')
                content2 = item.get_attribute('innerHTML')
                content = content + "</div>"
                root = ET.fromstring(content)
                i = 0
                for child in root.iter():
                    tmp_dict = {}
                    if child.tag == "a":
                        tmp_attrib = child.attrib
                        if child.text is not None:
                            tmp_name = child.text
                            tmp_name = tmp_name.replace("\n", "")
                            #tmp_name = tmp_name.replace(" ", "")
                            if tmp_name is not None:
                                if "target" not in tmp_attrib:
                                    player_name = tmp_name
                                    logging.info(" name ")
                                    logging.info(player_name)
                                    logging.info(" attrib ")
                                    logging.info(tmp_attrib)
                                    team_stat_dict[player_name] = dict()
                                else:
                                    player_score = child.text
                                    player_score = player_score.replace("\n", "")
                                    player_score = player_score.replace(" ", "")
                                    player_score = player_score.replace("\t", "")
                                    team_stat_dict[player_name][attributes_name[i]] = player_score
                                    i += 1
                    if child.tag == "td":
                        tmp_attrib = child.attrib
                        if child.text is not None:
                            player_score = child.text
                            player_score = player_score.replace("\n", "")
                            player_score = player_score.replace(" ", "")
                            player_score = player_score.replace("\t", "")
                            if "class" not in tmp_attrib:
                                if player_score is not None:
                                    logging.info(" score ")
                                    logging.info(player_score)
                                    #tmp_dict[attributes_name[i]] = player_score
                                    team_stat_dict[player_name][attributes_name[i]] = player_score
                                    i = i + 1


                logging.info(team_stat_dict)
                #
                # #logging.info("content")
                # #logging.info(content)

                #logging.info(type(content2))
                content2 = bytes(content2, encoding='UTF-8')
                #logging.info("content to byte")
                #logging.info(type(content2))
                x.append(content2)
                f.write(content2)
        csv_attrib = ["Player name","MIN", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "PF", "PTS", "+/-"]

        with open("player_stat.csv", "w") as f:
            w = csv.DictWriter(f, csv_attrib)
            w.writeheader()

            for k in team_stat_dict:
                csv_row = dict()
                for field in csv_attrib:
                    if team_stat_dict[k].get(field) is not None:
                        csv_row[field] = team_stat_dict[k].get(field)
                    else:
                        if field == "Player name":
                            csv_row[field] = k
                        else:
                            csv_row[field] = None
                w.writerow(csv_row)
                #w.writerow({field: team_stat_dict[k].get(field) or k for field in csv_attrib})
