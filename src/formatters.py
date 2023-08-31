class SQLFormatter:

    @staticmethod
    def get(table_name, entry, values):
        string_values = ""
        for field, value in values.items():
            try:
                value = int(value)
                string_values += f'`{field}` = {value}, '
            except ValueError: # it's a str
                string_values += f"`{field}` = `{value}`, "

        # remove last ", "
        string_values = string_values[:-2]

        return f"UPDATE `{table_name}` SET {string_values} WHERE `entry` = {entry};\n"
