#!/bin/env python3

import csv
import datetime
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--seed", action="store_true", dest="seed", default=False,
                  help="create seed configuration (default: create layers configuration)")

(options, args) = parser.parse_args()


caches = []
sources = []
layers = []
seeds = []

seeds_tpl = """
  {identifier}_seed:
    caches: [{identifier}_cache]
    coverages: [citta_metropolitana_roma]
    grids: [localgrid]
    levels:
      to: 6
"""


caches_tpl = """
  {identifier}_cache:
    sources: [{identifier}_wms]
    grids: [localgrid]
    concurrent_tile_creators: 2
    cache:
      type: file
"""


sources_tpl = """
  {identifier}_wms:
    type: wms
    wms_opts:
      version: 1.3.0
      featureinfo: True
    req:
      url: {url}
      layers: {nome}
      transparent: true
    supported_formats: [png,jpeg,tiff]
    coverage:
      bbox: [11.492503, 41.374824, 13.51084, 42.340712]
      srs: 'EPSG:4326'
"""

layers_tpl = """
  - name: {nome}
    title: {desc}
    sources: [{identifier}_cache]
"""


with open('layers.csv') as csvfile:

    layer_reader = csv.DictReader(csvfile)
    for row in layer_reader:
        identifier = row['nome layer'].replace(' ', '_')
        nome = row['nome layer']
        desc = row['Descrizione']
        url = row['url wms'].replace('siticatasto', 'g3w-suite')
        caches.append(caches_tpl.format(nome=nome, desc=desc, url=url, identifier=identifier))
        layers.append(layers_tpl.format(nome=nome, desc=desc, url=url, identifier=identifier))
        sources.append(sources_tpl.format(nome=nome, desc=desc, url=url, identifier=identifier))
        seeds.append(seeds_tpl.format(nome=nome, desc=desc, url=url, identifier=identifier))

    caches_yaml = '\n'.join(caches)
    layers_yaml = '\n'.join(layers)
    sources_yaml = '\n'.join(sources)
    seeds_yaml = '\n'.join(seeds)
    timestamp = datetime.datetime.now().isoformat()

    yaml = f"""

###################################################################################
# Layers and caches, generated by createconfig.py {timestamp}


layers:
    {layers_yaml}

caches:
    {caches_yaml}

sources:
    {sources_yaml}

        """

    seed_yaml = f"""

###################################################################################
# Seeds, generated by createconfig.py {timestamp}


seeds:
    {seeds_yaml}

        """

    print(yaml if not options.seed else seed_yaml)