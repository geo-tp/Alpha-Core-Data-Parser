class DataParseController:

    def __init__(
        self, 
        source_data, 
        foreign_data,
        comparator,
        formatter,
        model, 
        view,
        output,
        limit=0
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

        for entry, foreign_entry_obj in self.foreign_repo.items():
            source_entry_obj = self.source_repo.get(entry, None)

            if entry > self.limit:
                continue

            if source_entry_obj and source_entry_obj:
                if self.comparator.is_different(source_entry_obj, foreign_entry_obj):
                    chosen_entry = self.comparator.choose(source_entry_obj, foreign_entry_obj)
                    fields_to_update = self.comparator.get_fields_to_update(source_entry_obj, chosen_entry)
                    self._save_results(chosen_entry, fields_to_update)

        self.view.end()

    def _save_results(self, data_model, fields_to_update):
        if not (fields_to_update):
            return

        table_name = data_model.get_table_name()
        entry = data_model.entry
        values = data_model.get_values(fields_to_update)
        formatted_values = self.formatter.get(table_name, entry, values)

        self.output.save(formatted_values, 'a')