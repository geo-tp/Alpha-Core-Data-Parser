import re
from datetime import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm
from src.models import QuestTemplate, ItemTemplate, CreatureTemplate
import numpy as np

class WarcraftStrategyQuestAdapter:

    """
    For Warcraft Strategy Quest details 2004
    https://crawler.thealphaproject.eu/mnt/crawler/media/Database/WarcraftStrategy/quest_details_june_2004.html
    """

    def __init__(self, general_timestamp, database):
        self.general_timestamp = general_timestamp
        self.database = database

    def parse(self, file_content) -> list:
        """
        Parse HTML quests content to a list of QuestTemplate
        """

        self.database.connect()

        # We split html to be able to extract data quest by quest
        splitted_html = self._split_html(file_content) 

        parsed_quests = []
        for content in tqdm(splitted_html):
            try:
                quest_template = QuestTemplate()
                html_soup = BeautifulSoup(content, features="lxml")
                tables = html_soup.find_all("table")
                
                quest_template.parse_timestamp = self._extract_date(content)
                quest_template.entry = self._extract_entry(html_soup)

                # HEADER TABLE
                header_table = tables[0]
                self._set_header_table_values(header_table, quest_template)

                # MAIN TABLE    
                main_table = tables[1]
                self._set_main_table_values(main_table, quest_template)

                parsed_quests.append(quest_template)

            except AttributeError:
                # an entry was not found in database (too high, incorrect name...)
                # Better to not update anything in this case
                continue

        self.database.close()

        return parsed_quests

    def _set_header_table_values(self, header_table, quest_template) -> None:
        tds = header_table.find_all("td")
        quest_template.Title = self._replace_special_chars(tds[4].get_text(), extended=True)

        for td in tds:
            text = td.get_text()
            if "Level" in text:
                # the next td is the value
                quest_template.QuestLevel = int(td.find_next_sibling("td").get_text())
            if "Previous Quest" in text:
                p_quest_td = td.find_next_sibling("td")
                p_quest_a = p_quest_td.find("a", href=True)
                quest_template.PrevQuestId = self._extract_entry_from_link(p_quest_a["href"])
            if "Next Quest" in text:
                # We cant parse Next Quest because there is no way
                # to make a difference between NextQuestId and NextQuestInChain
                pass
            
    def _set_main_table_values(self, main_table, quest_template) -> None:
        tds = main_table.find_all("td")

        for td in tds:
            text = td.get_text()
            if "Objectives" in text:
                obj = td.find_next_sibling("td")
                for br in obj.find_all("br"):
                    br.replace_with("\n")
                quest_template.Objectives = self._replace_special_chars(obj.get_text())
            if "Description" in text:
                desc = td.find_next_sibling("td")
                for br in desc.find_all("br"):
                    br.replace_with("\n")
                quest_template.Details = self._replace_special_chars(desc.get_text())
            if "You are given" in text:
                src_item_name = td.find_next_sibling("td").get_text().strip()
                quest_template.SrcItemId = self.database.get_by_name(ItemTemplate, src_item_name).entry
                quest_template.SrcItemCount = 1
            if "Collect" in text:
                items = td.find_next_sibling("td").get_text()
                req_items, req_item_counts = self._extract_objects(ItemTemplate, items)
                self._set_group_values(
                    quest_template, "ReqItemId", "ReqItemCount", req_items, req_item_counts
                )
            if "Slay" in text:
                mobs = td.find_next_sibling("td").get_text()
                req_mobs, req_mob_counts = self._extract_objects(CreatureTemplate, mobs)
                self._set_group_values(
                    quest_template, "ReqCreatureOrGOId", "ReqCreatureOrGOCount", req_mobs, req_mob_counts
                )
            if "Choose one of" in text:
                items = td.find_next_sibling("td").get_text()
                choose_items, choose_item_counts = self._extract_objects(ItemTemplate, items)
                self._set_group_values(
                    quest_template, "RewChoiceId", "RewChoiceCount", choose_items, choose_item_counts
                )
            if "You will receive" in text:
                items = td.find_next_sibling("td").get_text()
                rew_items, rew_item_counts = self._extract_objects(ItemTemplate, items)
                self._set_group_values(
                    quest_template, "RewItemId", "RewItemCount", rew_items, rew_item_counts
                )
            if "Coins:" in text:
                money = td.find_next_sibling("td").get_text().strip()
                money_split = money.split("\xa0\xa0")
                mul = 100 if int(money_split[0]) < 49 else 1
                quest_template.RewOrReqMoney = int(money_split[0]) * mul 

                if (len(money_split) == 2):
                    quest_template.ReqOrRewMoney += int(money_split[1])


    def _set_group_values(self, quest_template, field_value, field_count, values, counts):
        while len(values) < 4:
            values.append(0)
            counts.append(0)

        for i in range(4):
            setattr(quest_template, f"{field_value}{i+1}", values[i])
            setattr(quest_template, f"{field_count}{i+1}", counts[i])


    def _format_date(self, date) -> str:
        return date.split(" ")[0]

    def _split_html(self, html) -> list[str]:
        return html.split("<br><br><br>")[1:-1]

    def _extract_entry(self, html) -> int:
        div = html.find("div") # there is always only one div
        return int(str(html).split("QuestId=")[1].split("</div")[0])

    def _extract_entry_from_link(self, link) -> str:
        end_link = link.split("php?").pop()
        return int(end_link.split("=").pop())

    def _extract_date(self, text) -> datetime.date:
        """
        The newest date avalaible in the text
        correspond to Last Updated date if any, or Submitted date
        """
        regex = r"\d{4}-\d{2}-\d{2}" # date like 2004-10-10
        dates = re.findall(regex, text)
        newest_date = self.general_timestamp

        if dates:
            newest_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
            for date in dates:
                date = datetime.strptime(date, "%Y-%m-%d").date()
                if date > newest_date:
                    newest_date = date

        return newest_date

    def _extract_objects(self, model, text) -> dict:
        """
        Extract from string "Wolf Claw (9), Wolf Meat (2)..."
        to dict {"Wolf Claw" : 9, "Wolf Meat", 2...}
        """
        regex = r'\(.+?\)' # to find the count number in str like (10)
        text_split = text.split(",")

        names_and_count = {}
        for t in text_split:
             # sometime (need effect) is present in name
            t_mod = t.replace("(needs effect)", "")
            match = re.search(regex, t_mod)
            count = match.group()
            name = t.replace(count, "").strip()
            names_and_count[name] = int(count[1:-1]) # remove parentheses

        req_entries = []
        req_counts = []
        for name, count in names_and_count.items():
            req_entries.append( self.database.get_by_name(model, name).entry)
            req_counts.append(int(count))

        return req_entries, req_counts

    def _replace_special_chars(self, text, extended=False) -> str:
        if extended:
            text = text.replace("(Elite)", "")\
                       .replace("(elite)", "")\
                       .replace("( Elite )", "")\
                       .replace("( elite )", "")

        return text.strip()\
                   .replace("\n", "$B")\
                   .replace("<br>", "$B")\
                   .replace("<name>", "$n")\
                   .replace("[name]", "$n")\
                   .replace("[ name ]", "$n")\
                   .replace("< name >", "$n")\
                   .replace("<race>", "$r")\
                   .replace("[race]", "$r")\
                   .replace("[ race ]", "$r")\
                   .replace("< race >", "$r")\
                   .replace("<class>", "$c")\
                   .replace("[class]", "$c")\
                   .replace("[ class ]", "$c")\
                   .replace("< class >", "$c")