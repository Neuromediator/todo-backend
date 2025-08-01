import os
import json
from typing import List


def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    @classmethod
    def from_json(cls, value):
        entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            entry.add_entry(cls.from_json(sub_entry))
        return entry

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            content = json.load(f)
            return cls.from_json(content)

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        filename = os.path.join(path, self.title)
        content = self.json()
        with open(f'{filename}.json', 'w') as f:
            json.dump(content, f)

    def __str__(self):
        return self.title


class EntryManager:
    def __init__(self, data_path):
        self.data_path: str = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for item in os.listdir(self.data_path):
            filepath = os.path.join(self.data_path, item)
            if item.endswith('.json'):
                entry = Entry.load(filepath)
                self.entries.append(entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)
        return entry
