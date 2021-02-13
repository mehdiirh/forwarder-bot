import json
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(this_dir, 'jsons/data.json')


class Data:

    @staticmethod
    def open_file():
        with open(data_file) as f:
            data = f.read()
            data = json.loads(data)
            f.close()
        return data

    @staticmethod
    def replace_file_data(new_data: dict):

        if not isinstance(new_data, dict):
            return

        with open(data_file, 'w') as f:
            data = json.dumps(new_data, indent=4)
            f.write(data)

    def add_to_file(self, key: str, value: str):
        data = self.open_file()
        data_of_key = data[key]

        if isinstance(data_of_key, list):
            if value not in data_of_key:
                value = [value]
                value += data_of_key
            else:
                raise ValueError('مقدار `{value}` از قبل وجود دارد'.format(value=value))

        data[key] = value
        self.replace_file_data(data)

    def remove_from_file(self, key: str, value: str):
        data = self.open_file()
        data_of_key = data[key]

        if isinstance(data_of_key, list):
            if value in data_of_key:
                data_of_key = list(filter(lambda el: el != value, data_of_key))
                data[key] = data_of_key
                self.replace_file_data(data)
            else:
                raise ValueError('مقدار `{value}` وجود ندارد'.format(value=value))

    @property
    def channels(self) -> list:
        data = self.open_file()
        return data['channels']

    @property
    def words(self) -> list:
        data = self.open_file()
        return data['words']

    @property
    def group_id(self) -> [str, int]:
        data = self.open_file()
        group = data['group_id']

        if str(group).isdigit():
            group = int(group)

        return group
