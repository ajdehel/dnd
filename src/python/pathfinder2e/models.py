import collections
import fnmatch
import json
import yaml
import pathlib

from .sheets import *

####################################################################################################

class Pathfinder2eModel:

    def __init__(self, sessions=list()):
        self._sheets = dict()
        self._groups = dict()
        self._access = collections.ChainMap(self._sheets, self._groups)

    def __iter__(self):
        yield from self._access

    def load(self, path, name=None, group=None):
        if name:
            self._raise_on_exists(name)
        sheet = self.load_sheet(path)
        if group:
            self._raise_on_notgroup(group)
        self._sheets[sheet.name] = sheet
        if group:
            self._groups[group].add(sheet.name)

    def get(self, *keys):
        for key in keys:
            yield self._access[key]

    def search(self, pattern):
        for item in self._access:
            if item.startswith(pattern):
                yield item

    def wildcard_search(self, pattern):
        for item in self._access:
            if fnmatch.fnmatch(item, pattern):
                yield item

    def add_group(self, group):
        self._check_exists(group)
        self._groups[group] = set()

    def load_session(self, path):
        try:
            session_parser = SessionParser(path)
        except Exception as e:
            print(e)
            raise
        for group, sheet_path in session_parser.sheets():
            if group not in self._groups:
                self._groups[group] = set()
            self.load(sheet_path, group=group)

    def _raise_on_exist(self, name):
        if name in self._access:
            raise RuntimeError(f"{name}: Item exists")

    def _raise_on_notexists(self, name):
        if name not in self._access:
            raise RuntimeError(f"{name}: No such sheet or group")

    def _raise_on_notgroup(self, name):
        self._raise_on_notexists(name)
        if name not in self._groups:
            raise RuntimeError(f"{name}: Not a group")

    def _raise_on_notsheet(self, name):
        self._raise_on_notexists(name)
        if name not in self._sheets:
            raise RuntimeError(f"{name}: Not a sheet")

    def _is_group(self, name):
        return name in self._groups

    def _is_sheet(self, name):
        return name in self._sheets

    #===============================================================================================
    @classmethod
    def load_sheet(cls, path):
        try:
            with path.open('r') as infile:
                sheet_data = json.load(infile)
        except Exception as e:
            print(e)
            raise
        return Pathfinder2eSheet.SubclassFactory(sheet_data)


####################################################################################################
class SessionParser:

    def __init__(self, filepath):
        self.filepath = filepath
        with self.filepath.open('r') as infile:
            self.session_data = yaml.safe_load(infile)
        if 'sheet_location' in self.session_data:
            self._sheet_dir = pathlib.Path(self.session_data['sheet_location'])
            if not self._sheet_dir.is_absolute():
                self._sheet_dir = self.filepath.parent / self._sheet_dir
        else:
            self._sheet_dir = filepath.parent

    def _get_sheet_path(self, sheet_file):
        sheet_path = pathlib.Path(sheet_file)
        if sheet_path.is_absolute():
            return sheet_path
        return self._sheet_dir / sheet_path

    def sheets(self):
        for group in self.session_data['groups']:
            for sheet_file in self.session_data['groups'][group]:
                yield (group, self._get_sheet_path(sheet_file))
        if 'sheets' in self.session_data and self.session_data['sheets']:
            for sheet_file in self.session_data['sheets']:
                yield (None, self._get_sheet_path(sheet_file))

