import time

class ModelComparator:

    def __init__(self, compare_fields):
        self.compare_fields = compare_fields
        self._set_group_fields()
    
    def is_different(self, source_model, foreign_model):
        """
        Compare if a foreign ressource is different from the source
        """
        return True if self.get_fields_to_update(source_model, foreign_model) else False

    def choose(self, source_model, foreign_model):
        """
        Select which model should be saved based on timestamp
        """
        if foreign_model.parse_timestamp and\
           foreign_model.parse_timestamp < source_model.parse_timestamp:
            return foreign_model
        
        return source_model

    def get_fields_to_update(self, source_model, foreign_model):
        fields_to_update = []
        for field in self.compare_fields:

            s_value = getattr(source_model, field)
            f_value = getattr(foreign_model, field)

            if f_value == None:
                continue

            if isinstance(s_value, str) and isinstance(f_value, str):
                s_value = self._get_flat_text(s_value)
                f_value = self._get_flat_text(f_value)

            # to compare all grouped fields at once
            if field[:-1] in self.group_fields:
                s_group, f_group = self._get_group_values(
                    source_model, foreign_model, field[:-1] 
                )
                if s_group == f_group:
                    continue

            if s_value != f_value:
                fields_to_update.append(field)

        return fields_to_update

    def _get_flat_text(self, text):
        return text.replace(" ", "")\
                   .replace("-", "")\
                   .replace(".", "")\
                   .replace(",", "")\
                   .strip()\
                   .lower()\

    def _get_group_values(self, source_model, foreign_model, field_group):
        """
        get lists of group fields values
        """
        source_group = [getattr(source_model, f"{field_group}{i}") for i in range(1, 5)]
        foreign_group = [getattr(foreign_model,f"{field_group}{i}") for i in range(1, 5)]
        foreign_group = [v if v != None else 0 for v in foreign_group]
        source_group.sort()
        foreign_group.sort()

        return source_group, foreign_group

    def _set_group_fields(self):
        """
        Determine fields group like RewItemId, RewItemIdCount...
        """
        fields = [field[:-1] for field in self.compare_fields]
        group_fields = []

        for _ in range(len(fields)):
            a = fields.pop()
            if a in fields and a not in group_fields:
                group_fields.append(a)

        self.group_fields = group_fields
        