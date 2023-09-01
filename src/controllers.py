from tqdm import tqdm

class DataParseController:

    """
    Compare entries from Source data with Foreign Data
    Save the results on the given output with the given formatter
    """

    def __init__(
        self, 
        source_data, 
        foreign_data,
        comparator,
        formatter,
        model, 
        view,
        output,
        limit=None
        ):

        self.comparator = comparator
        self.formatter = formatter
        self.model = model
        self.view = view
        self.output = output
        self.limit = limit

        self.source_repo = {model.entry : model for model in source_data}
        self.foreign_repo = {model.entry : model for model in foreign_data}
    
    def run(self):

        self.view.start()

        for entry, foreign_entry_obj in tqdm(self.foreign_repo.items()):
            source_entry_obj = self.source_repo.get(entry, None)

            if self.limit and entry > self.limit:
                continue

            if not source_entry_obj:
                continue

            if self.comparator.is_different(source_entry_obj, foreign_entry_obj):
                chosen_entry = self.comparator.choose(source_entry_obj, foreign_entry_obj)
                if chosen_entry != source_entry_obj:
                    fields_to_update = self.comparator.get_fields_to_update(source_entry_obj, chosen_entry)
                    self._save_results(chosen_entry, fields_to_update)

        self.view.end()

    def _save_results(self, data_model, fields_to_update):
        if not (fields_to_update):
            return

        table_name = data_model.get_table_name()
        entry = data_model.entry
        values = data_model.get_values(fields_to_update)
        timestamp = data_model.parse_timestamp
        formatted_values = self.formatter.get(table_name, entry, values, timestamp)

        self.output.save(formatted_values, 'a')