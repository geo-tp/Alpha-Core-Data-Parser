from src.controllers import DataParseController
from src.databases import MysqlDatabase
from src.files import File
from settings import Settings

if __name__ == "__main__":
    
    # SOURCE DATA 
    database = MysqlDatabase(
        Settings.db_user,
        Settings.db_pass, 
        Settings.db_host, 
        Settings.db_name
    )
    database.connect()
    Settings.view.load("source data")
    source_data : list[Settings.model] = database.get_all(Settings.model)
    database.close()

    # FOREIGN DATA
    file_to_parse = File(Settings.filepath_to_parse).load()
    Settings.view.load("foreign data")
    parser = Settings.parser(Settings.adapter, database)
    foreign_data : list[Settings.model] = parser.parse(file_to_parse)

    # RESULTS FILE
    output_file = File(Settings.filepath_to_save_results)

    ctrl = DataParseController(
        source_data, 
        foreign_data,
        Settings.comparator(Settings.compare_fields),
        Settings.formatter,
        Settings.model,
        Settings.view,
        output_file,
        limit=Settings.max_id
    )

    ctrl.run()