import json
from base import BASE_CONTEXT


class JsonConnector:
    def get_icons(self) -> dict:
        return self.get_data("icons.json", "icons")

    def get_standard_queries(self) -> dict:
        return self.get_data("queries.json", "standard_queries")

    def get_html(self) -> dict:
        return self.get_data("web.json", "HTML")

    def get_js(self) -> dict:
        return self.get_data("web.json", "JS")

    @staticmethod
    def get_data(file: str, field: str):
        try:
            with open(BASE_CONTEXT.get_resource(file)) as json_file:
                json_dict = json.load(json_file)
                if field in json_dict:
                    return json_dict[field]
                raise ValueError("Field doesn't find")
        except FileNotFoundError:
            raise ValueError("File doesn't exists")
