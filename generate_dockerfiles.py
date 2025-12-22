import csv
import os
from jinja2 import Environment, FileSystemLoader

os.makedirs('dockerfiles', exist_ok=True)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('Dockerfile.j2')

with open('serverlist.csv', 'r') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        context = {
            'shortname': row['shortname'],
            'servername': row['gameservername'],
            'gamename': row['gamename'],
            'distro': row['os']
        }
        output = template.render(context)
        with open(f'dockerfiles/Dockerfile.{row["shortname"]}', 'w') as out:
            out.write(output)
        count += 1
    print(f'Generated {count} Dockerfiles')
