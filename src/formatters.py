class SQLFormatter:

    @staticmethod
    def get(table_name, entry, values, timestamp):
        string_values = ""
        for field, value in values.items():
            if isinstance(value, int):
                string_values += f'`{field}` = {value}, '
            else: # it's a str or a date
                value = str(value).replace("'","\\'") # replace ' by \'
                string_values += f"`{field}` = '{value}', "

        return f"UPDATE `{table_name}` SET `parse_timestamp`='{timestamp}', {string_values}WHERE `entry` = {entry};\n"
