#!/usr/bin/env python

import re, yaml
from flask import Flask, request, redirect

class Engines:
    def __init__(self):
        self.load()

    def load(self):
        self.engines = yaml.load(open("engines.yaml"))

    def get(self,key):
        for item in self.engines:
            if item["key"]==key:
                return Engine(item)
        raise KeyError

    def get_default(self):
        for item in self.engines:
            if item.has_key("default"):
                return Engine(item)
        raise KeyError

class Engine:
    def __init__(self,dic):
        self.__dict__=dic

app = Flask(__name__)
app.debug = True

@app.route('/about')
def about():
    engines = Engines()
    rows = "".join(['<tr><td>%s</td><td>%s</td></tr>' % (i["key"], i["name"]) for i in engines.engines])
    html = '''
<html>
<body>
<h3>Engines installed</h3>
<table border="1">''' + rows + '''
</table>
</body>
</html>'''
    return html

@app.route('/search')
def search():
    default = "g"

    engines = Engines()

    q = request.args["q"]

    m = re.match(r'(\w+)\s+(.+)',q)

    if m:
        key, to = m.groups()
        try:
            url = engines.get(key).url
        except KeyError:
            to = q
            url = engines.get_default().url
    else:
        url = engines.get_default().url
        to = q

    url = url % (to,)
    return redirect(url)

if __name__ == '__main__':
    app.run()
