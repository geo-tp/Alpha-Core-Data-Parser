class QuestComparator:
    
    def __init__(self, compare_fields):
        self.compare_fields = compare_fields
    
    def is_different(self, source_quest, foreign_quest):
        for field in self.compare_fields:
            source_attr = getattr(source_quest, field)
            foreign_attr = getattr(foreign_quest, field)

            if type(source_attr) == type("string") and \
               type(foreign_attr) == type("string"):
                source_attr = self._get_flat_text(source_attr)
                foreign_attr = self._get_flat_text(foreign_attr)
  
            if  source_attr != foreign_attr:
                return True

        return False

    def choose(self, source_quest, foreign_quest):
        if foreign_quest.parse_timestamp and\
           foreign_quest.parse_timestamp < source_quest.parse_timestamp:
            return foreign_quest
        
        return source_quest

    def get_fields_to_update(self, source_quest, foreign_quest):
        fields_to_update = []
        for field in self.compare_fields:
            q_value = getattr(source_quest, field)
            f_value = getattr(foreign_quest, field)
            if q_value != f_value:
                fields_to_update.append(field)

        return fields_to_update

    def _get_flat_text(self, text):
        return text.lower().replace(" ", "")\
                           .replace("-", "")\
                           .strip()
