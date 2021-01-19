'''
Copyright 2021, Kaletise

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Contact me via Telegram, VK, Reddit or Twitter: @kaletise
'''

import json
import os


class Config:
    def __init__(self, file, default={}, auto_init=True,
                 indent=4, sort_keys=True):
        self.file = file
        self.default = default
        self.data = {}
        self.indent = indent
        self.sort_keys = sort_keys
        if auto_init:
            self.init()

    def init(self):
        if os.path.isfile(self.file):
            self.load()
        else:
            self.data = self.default
            self.save()

    def get(self, key):
        if key in self.data.keys():
            return self.data[key]
        if key in self.default.keys():
            return self.default[key]

    def set(self, key, value):
        self.data[key] = value

    def save(self):
        open(self.file, 'w').write(json.dumps(
            self.data, indent=self.indent, sort_keys=self.sort_keys
        ))

    def load(self):
        if not os.path.isfile(self.file):
            return False
        try:
            self.data = json.load(open(self.file))
        except json.decoder.JSONDecodeError:
            return False
