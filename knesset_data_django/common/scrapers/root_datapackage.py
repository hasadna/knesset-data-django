import zipfile
import os
from datapackage import DataPackage
import json
from jsontableschema import Schema
import csv
from collections import OrderedDict


class RootDatapackage(object):

    def __init__(self, datapackage_dir, with_dependencies):
        self.datapackage_dir = datapackage_dir
        self.with_dependencies = with_dependencies
        datapackage_descriptor_file = os.path.join(datapackage_dir, "datapackage.json")
        with open(datapackage_descriptor_file) as f:
            descriptor = json.load(f)
        self.fix_descriptor(descriptor)
        self.datapackage = DataPackage(descriptor, default_base_path=self.datapackage_dir)

    def fix_descriptor(self, descriptor):
        for resource in descriptor["resources"]:
            if isinstance(resource["path"], list):
                resource["data"] = resource["path"]
                del resource["path"]

    def get_resource(self, name):
        return Resource(self, name)

    @classmethod
    def load_from_zip(cls, datapackage_zip_file, data_root):
        with zipfile.ZipFile(datapackage_zip_file, 'r') as zipf:
            zipf.extractall(data_root)
        return os.path.join(data_root, "datapackage")


class Resource(object):

    def __init__(self, datapackage, name):
        self.datapackage = datapackage
        self.name = name
        self.resource = [r for r in datapackage.datapackage.resources if r.descriptor["name"] == name][0]

    def get_path(self, relpath=None):
        if not relpath:
            return os.path.join(self.datapackage.datapackage_dir, self.name)
        else:
            return os.path.join(self.get_path(), relpath)

    def fetch(self, **kwargs):
        raise Exception("Direct fetching is not supported, you must scrape from a prepared datapackage")

    def fetch_from_datapackage(self, **kwargs):
        schema = Schema(self.resource.descriptor["schema"])
        path = self.get_path("{}.csv".format(self.get_path()))
        if os.path.exists(path):
            with open(path) as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # skip header line
                for row in csv.reader(f):
                    cast_row = OrderedDict()
                    for i, val in enumerate(row):
                        field = schema.fields[i]
                        if field.type == "string":
                            val = val.decode("utf-8")
                        elif field.type == "datetime" and val != "":
                            val = "{}Z".format(val)
                        try:
                            val = field.cast_value(val)
                        except Exception as e:
                            raise Exception("Failed to cast value for field '{}' ({}) with value '{}': {}".format(field.name, field.type, val, e.message))
                        cast_row[field.name] = val
                    yield cast_row
