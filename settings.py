from src.views import CliView
from src.comparators import QuestComparator
from src.formatters import SQLFormatter
from src.models import QuestTemplate
from src.adapters import WarcraftStrategyQuestAdapter
from src.parsers import FileParser

class Settings:

    db_user = "root"
    db_pass = "pwd"
    db_host = "localhost"
    db_name = "alpha_world"

    filepath_to_parse = "/home/user/Documents/CODE/Git/alpha_wow/DataParser/quest_details_june_2004.html"
    filepath_to_save_results = "/home/user/Documents/CODE/Git/alpha_wow/DataParser/output.sql"

    model = QuestTemplate
    adapter = WarcraftStrategyQuestAdapter
    parser = FileParser
    comparator = QuestComparator
    formatter = SQLFormatter
    view = CliView

    max_id = 1339

    compare_fields = [
        "entry",
        "QuestLevel",
        "PrevQuestId",
        "NextQuestId",
        "SrcItemId",
        "SrcItemCount",
        "Title",
        "Details",
        "Objectives",
        "ReqItemId1",
        "ReqItemId2",
        "ReqItemId3",
        "ReqItemId4",
        "ReqItemCount1",
        "ReqItemCount2",
        "ReqItemCount3",
        "ReqItemCount4",
        "ReqItemCount1",
        "ReqCreatureOrGOId1",
        "ReqCreatureOrGOId2",	
        "ReqCreatureOrGOId3",	
        "ReqCreatureOrGOId4",	
        "ReqCreatureOrGOCount1", 
        "ReqCreatureOrGOCount2",
        "ReqCreatureOrGOCount3",
        "ReqCreatureOrGOCount4",
        "RewChoiceItemId1",
        "RewChoiceItemId2",
        "RewChoiceItemId3",
        "RewChoiceItemId4",
        "RewChoiceItemId5",	
        "RewChoiceItemId6",	
        "RewChoiceItemCount1",
        "RewChoiceItemCount2",	
        "RewChoiceItemCount3",	
        "RewChoiceItemCount4",	
        "RewChoiceItemCount5",	
        "RewChoiceItemCount6",	
        "RewItemId1",
        "RewItemId2",
        "RewItemId3",
        "RewItemId4",	
        "RewItemCount1",
        "RewItemCount2",
        "RewItemCount3",
        "RewItemCount4",
        "RewXP",
    ]
    
