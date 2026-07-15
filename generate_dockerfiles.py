import csv
import os
from jinja2 import Environment, FileSystemLoader

# Custom (non-LinuxGSM) games use the "atr-" shortname prefix and ship
# HAND-AUTHORED Dockerfiles (dockerfiles/Dockerfile-atr-*) built FROM a custom
# base -- the Proton base (lgsm-atr-custom-base) for windows-via-proton games,
# or the LinuxGSM base directly for linux-native games. They are NOT rendered
# from Dockerfile.j2 and must never be overwritten by this generator.
# See CONTRIBUTING-custom-games.md.
CUSTOM_PREFIX = 'atr-'

os.makedirs('dockerfiles', exist_ok=True)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('Dockerfile.j2')

with open('serverlist.csv', 'r') as f:
    reader = csv.DictReader(f)
    generated = 0
    skipped = 0
    for row in reader:
        shortname = row['shortname']
        if shortname.startswith(CUSTOM_PREFIX):
            # Hand-authored custom game; leave its Dockerfile untouched.
            skipped += 1
            continue
        context = {
            'shortname': shortname,
            'servername': row['gameservername'],
            'gamename': row['gamename'],
            'distro': row['os'],
        }
        output = template.render(context)
        with open(f'dockerfiles/Dockerfile-{shortname}', 'w') as out:
            out.write(output)
        generated += 1
    print(f'Generated {generated} Dockerfiles ({skipped} custom atr-* skipped)')
