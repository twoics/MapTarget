"""
The module contains a class that provides access to json files
"""
# Standard library import
import json

# Local application imports
from .base import BASE_CONTEXT


class JsonConnector:
    """
    Class provides data transfer from a json file
    """

    def get_icons(self) -> dict:
        """
        :return: Icon dictionary
        """
        return self.get_data("icons.json", "icons")

    def get_standard_queries(self) -> dict:
        """
        :return: Standard requests (coffee, cinema...)
        """
        return self.get_data("queries.json", "standard_queries")

    @staticmethod
    def get_data(file: str, field: str = None):
        """
        Method for accessing the json file
        :param file: Name and type of file to be accessed
        :param field: The field to get
        :return: Dict
        """
        try:
            with open(BASE_CONTEXT.get_resource(file)) as json_file:
                if field is None:
                    return json_file
                json_dict = json.load(json_file)
                if field in json_dict:
                    return json_dict[field]
                raise ValueError("Field doesn't find")
        except FileNotFoundError:
            raise ValueError("File doesn't exists")
