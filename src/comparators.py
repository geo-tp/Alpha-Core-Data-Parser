class QuestComparator:

    def __init__(self, compare_fields):
        self.compare_fields = compare_fields
        self._set_group_fields()
    
    def is_different(self, source_quest, foreign_quest):
        """
        Compare if a foreign quest is different from the source entry
        """
        for field in self.compare_fields:
            source_attr = getattr(source_quest, field)
            foreign_attr = getattr(foreign_quest, field)

            if type(source_attr) == type("string") and \
               type(foreign_attr) == type("string"):
                source_attr = self._get_flat_text(source_attr)
                foreign_attr = self._get_flat_text(foreign_attr)

            elif field[:-1] in self.group_fields:
                # we need to compare all values at once in case there are not sorted
                group_is_different = self._is_different_fields_group(source_quest, foreign_quest, field[:-1])
                
                if group_is_different:
                    return True
  
            if  source_attr != foreign_attr:
                return True

        return False

    def choose(self, source_quest, foreign_quest):
        """
        Select which quest should be saved based on timestamp
        """
        if foreign_quest.parse_timestamp and\
           foreign_quest.parse_timestamp < source_quest.parse_timestamp:
            return foreign_quest
        
        return source_quest

    def get_fields_to_update(self, source_quest, foreign_quest):
        fields_to_update = []
        for field in self.compare_fields:
            q_value = getattr(source_quest, field)
            f_value = getattr(foreign_quest, field)

            # to compare all grouped fields at once
            if field[:-1] in self.group_fields:
                group_is_different = self._is_different_fields_group(
                    source_quest, 
                    foreign_quest, 
                    field[:-1]
                )

                if not group_is_different:
                    continue
            
            if q_value != f_value:
                fields_to_update.append(field)

        return fields_to_update

    def _get_flat_text(self, text):
        return text.lower().replace(" ", "")\
                           .replace("-", "")\
                           .strip()

    def _is_different_fields_group(self, source_quest, foreign_quest, field_group):
        """
        Compare group fields at once to avoid sorting differences
        """
        source_group = [getattr(source_quest, f"{field_group}{i}") for i in range(1, 5)]
        foreign_group = [getattr(source_quest,f"{field_group}{i}") for i in range(1, 5)]

        if source_group.sort() != foreign_group.sort():
            return True

        return False

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
        