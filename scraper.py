#!/usr/bin/env python3
'''
1. Downloads the list of Appropedia projects as HTML and parses it.
2. Downloads the edit page of each project,
   and parses the source out of it.
3. Extracts and parses the Infobox content out of that.
4. Maps the Appropedia Infobox project data
   to OKH v2.0 properties.
5. Writes out one OKH.toml file per project.
'''

from __future__ import print_function
import sys
import re
import os
import urllib
import urllib.request
import json
import toml
#import yaml
import click
import validators
from bs4 import BeautifulSoup

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

BASE_URL = 'https://www.appropedia.org'
PROJECTS_LIST_URL = BASE_URL + '/w/index.php?title=Special:WhatLinksHere/Template:Infobox_project&limit=500'
content_link_p = re.compile(r'/[^/:]+$', re.IGNORECASE)
infobox_p = re.compile(r'{{Infobox project(.|\n)*?}}', re.MULTILINE)
clean_name_p = re.compile(r'[^a-zA-Z0-9]')
clean_file_name_p = re.compile(r'[^a-zA-Z0-9.\)\(;,ó-]')

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def version_token():
    pass

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)





class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"

urllib._urlopener = AppURLopener()

def download(url, path):
    '''
    Downloads a URL pointing to a file into a local file,
    pointed to by path.
    '''
    print('downloading %s to %s ...' % (url, path))
    if os.path.exists(path):
        os.remove(path)
    urllib._urlopener.retrieve(url, path)

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('storage_dir', type=click.Path(), envvar='APPRO_STORAGE_DIR',
                default='tmp')
@click.option('--redownload', '-r')
@click.version_option("1.0")
def scrape(storage_dir='tmp', redownload=False):
    '''
    1. Downloads the list of Appropedia projects as HTML and parses it.
    2. Downloads the edit page of each project,
       and parses the source out of it.
    3. Extracts and parses the Infobox content out of that.
    4. Maps the Appropedia Infobox project data
       to OKH v2.0 properties.
    5. Writes out one OKH.toml file per project.
    '''
    scraper = AppropediaScraper(storage_dir, redownload)
    scraper.fetch_project_infos()

class AppropediaScraper:

    def __init__(self, storage_dir='tmp', force_redownload=False):
        self.storage_dir = storage_dir
        self.force_redownload = force_redownload

    def resolve_appro_wiki_user(self, user_name: str) -> str:
        # NOTE We just return what is supplied, because the only (additional)
        # info we'd be interested in, is the EMail, which is not available
        # there.
        return user_name
        user_file = self.storage_dir + '/user__' + clean_name_p.sub('_', user_name)
        download(BASE_URL + '/User:' + urllib.parse.quote_plus(user_name), user_file)
        user_file_h = open(user_file, mode='r')
        user_page_content = user_file_h.read()
        user_file_h.close()
        soup = BeautifulSoup(user_page_content, features="lxml")
        # TODO 'Download such a user page and analyze it, to be able to parse it'
        '''
        {{Infobox user
        |image=foto_de_emilio.jpg
        |caption=Executive Director of Appropedia Foundation
        |name=Emilio Velis
        |affiliations=[[Appropedia Foundation]], Brandeis University, [[Escuela Superior de Economía y Negocios]]
        |location=San Salvador, El Salvador
        |nationality=El Salvador
        |languages=Spanish, English, Portuguese
        |skills=digital fabrication, programming, design, volunteer management, research
        |interests=open source, design, sustainability, maker culture, digital media
        |site=https://www.emiliovelis.com/
        |twitter=https://twitter.com/emilio
        |github=https://github.com/dubsnipe/
        |wikipedia=https://en.wikipedia.org/wiki/User:Dbsnp
        }}
        ...
        '''

    def image_name2url(self, title, image):
        clean_name = clean_file_name_p.sub('_', image)
        wiki_url = BASE_URL + '/File:' + urllib.parse.quote_plus(clean_name)
        #https://www.appropedia.org/w/images/8/85/2005_zaragoza_system.jpg
        image_page_file = os.path.join(self.storage_dir, 'image__' + title +
                                       '__' + clean_name + '.html')
        if not os.path.exists(image_page_file) or self.force_redownload:
            download(wiki_url, image_page_file)
        image_page_h = open(image_page_file, mode='r')
        image_page = image_page_h.read()
        image_page_h.close()
        soup = BeautifulSoup(image_page, features="lxml")

        # Look for appropedia-hosted file
        for lnk in soup.findAll('a'):
            lnk_url = lnk.get('href')
            if lnk_url.startswith('/w/images/'):
                return BASE_URL + lnk_url

        # if not on appropedia, look for a wikimedia link
        for lnk in soup.findAll('a'):
            lnk_url = lnk.get('href')
            if lnk_url.startswith('https://upload.wikimedia.org/wikipedia/commons/') and lnk_url.endswith(clean_name):
                return lnk_url
        # example https://upload.wikimedia.org/wikipedia/commons/b/bc/Wind_generator_system.jpg
        raise RuntimeError('Failed to find original image URL')

    def apppropedia2okh(self, props_appro: dict):
        '''
        | title          = name
        | url            = repo
        | "CC-BY-SA 4.0" = license
        | "2.0"          = okhv
        | image          = image
        | caption        = function
        | language-code  = documentation-language
        | keywords       = function++
        | uses           = technology-readiness-level, documentation-readiness-level
        | authors        = licensor
        | status         = technology-readiness-level, documentation-readiness-level
        | made           = technology-readiness-level, documentation-readiness-level
        | replicated     = technology-readiness-level, documentation-readiness-level
        | date-completed = 
        | date-published = 
        | date-updated   = 
        | location       = 
        | designed-in    = 
        | replicated-in  = 
        | affiliations   = 
        | materials      = 
        | cost-currency  = 
        | cost           = 
        | sdg            = 
        | ported-from    = 
        | translation-of = 
        | translators    = 

        okhv = "2.0"
        name = "crKbd, Corne, Helidox"
        repo = "https://github.com/foostan/crkbd/commit/894984e"
        version = "894984e"
        license = "MIT"
        licensor = "Kosuke Adachi <foostan@github.com>"
        readme = "README.md"
        image = ["https://user-images.githubusercontent.com/736191/49698496-0c3c0c80-fc08-11e8-87bc-4fd2aa7f3f78.jpg", "corne-cherry/doc/v3/assets/build_diode_overview.jpg"]
        documentation-language = ["en_US", "jp_JP"]
        technology-readiness-level = "OTRL-6"
        documentation-readiness-level = "ODRL-5"
        function = "The Corne is a 40% split mechanical USB general purpose keyboard."
        cpc-patent-class = "G06C 7/02"
        tsdc = "PCB"
        bom = "https://github.com/foostan/crkbd/blob/master/corne-classic/doc/buildguide_en.md"
        manufacturing-instructions = "/corne-*/doc/**/*.md"
        #user-manual = "/manual/"
        '''
        if 'authors' in props_appro:
            authors_raw = props_appro['authors']
        elif 'author' in props_appro:
            authors_raw = props_appro['author']
        else:
            authors_raw = None
        authors = []
        if not authors_raw is None:
            for author_raw in authors_raw.split(','):
                author = author_raw.strip()
                if author.startswith('User:'):
                    author = self.resolve_appro_wiki_user(author[5:])
                authors.append(author)
        if len(authors) == 1:
            authors = authors[0]

        if 'image' in props_appro:
            image = props_appro['image']
            if not validators.url(image):
                image = self.image_name2url(props_appro['title'], image)
        else:
            image = None

        description = None
        if 'keywords' in props_appro and 'caption' in props_appro:
            description = props_appro['keywords'] + ' - ' + props_appro['caption']
        elif 'keywords' in props_appro:
            description = props_appro['keywords']
        elif 'caption' in props_appro:
            description = props_appro['caption']

        technology_readiness = None
        if props_appro.get('replicated', 'No') == 'Yes' \
                or not props_appro.get('replicated-in', None) is None: # 'made-independently'
            technology_readiness = 'OTLR-5'
        elif props_appro.get('made', 'No') == 'Yes':
            technology_readiness = 'OTLR-4'
        elif 'status' in props_appro: # 'development-stage'
            stati = props_appro['status'].split(',')
            if 'Commercialized' in stati \
                    or 'Deployed' in stati \
                    or 'Implemented' in stati \
                    or 'Verified' in stati:
                technology_readiness = 'OTLR-5'
            elif 'Prototype' in stati:
                technology_readiness = 'OTLR-4'
        '''
        Values found for 'status':
        Commercialized
        Deployed
        Design, Prototype
        Idea
        Implemented
        Open design
        Prototype
        Verified
        '''

        props_okh = {
            'name': props_appro['title'],
            'repo': props_appro['url'],
            'license': 'CC-BY-SA 4.0',
            'okhv': '2.0',
        }
        if len(authors) > 0:
            props_okh['licensor'] = authors
        if not image is None:
            props_okh['image'] = image
        if not description is None:
            props_okh['function'] = description
        if 'language-code' in props_appro:
            props_okh['documentation-language'] = props_appro['language-code']
        if not image is None:
            props_okh['technology-readiness-level'] = technology_readiness
        return props_okh

    def store_properties(self, props_appro):
        props_okh = self.apppropedia2okh(props_appro)
        toml_okh = toml.dumps(props_okh)
        '''
        print('')
        print('')
        print('')
        print('appropedia:')
        print(json.dumps(props_appro, indent=1, sort_keys=True))
        print('')
        print('OKH (JSON):')
        print(json.dumps(props_okh, indent=1, sort_keys=True))
        print('')
        print('OKH (TOML):')
        print(toml_okh)
        '''
        okh_file = os.path.join(self.storage_dir, 'okh-appropedia_org-' +
                clean_name_p.sub('_', props_appro['title']) + '.toml')
        okh_file_h = open(okh_file, mode='w')
        okh_file_h.write(toml_okh)
        okh_file_h.close()
        print('Written to "%s"' % okh_file)

    def scrape_project(self, title):
        edit_url = BASE_URL + '/w/index.php?title=' + title + '&action=edit'
        edit_content_file = os.path.join(self.storage_dir, 'project_edit__' + title + '.html')
        if not os.path.exists(edit_content_file) or self.force_redownload:
            download(edit_url, edit_content_file)
        edit_content_fh = open(edit_content_file, mode = 'r')
        edit_content = edit_content_fh.read()
        edit_content_fh.close()
        proj_soup = BeautifulSoup(edit_content, features="lxml")
        for text_area in proj_soup.findAll('textarea'):
            if text_area.get('id') == 'wpTextbox1':
                page_src = str(text_area.contents[0])
                infobox_match = infobox_p.search(page_src)
                if infobox_match:
                    props_appro = {
                        "title": title,
                        "url": BASE_URL + '/' + title,
                    }
                    infobox_content = infobox_match.group(0)
                    for ib_line in infobox_content.split('\n'):
                        ib_line = ib_line.strip()
                        if ib_line[:1] == '|':
                            key_value = ib_line[1:].split('=')
                            props_appro[key_value[0]] = key_value[1]
                    self.store_properties(props_appro)

    def fetch_project_infos(self):
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        html_list_file = os.path.join(self.storage_dir, 'list.html')
        if not os.path.exists(html_list_file) or self.force_redownload:
            download(PROJECTS_LIST_URL, html_list_file)
        list_file = open(html_list_file, mode='r')
        soup = BeautifulSoup(list_file.read(), features="lxml")
        list_file.close()
        passed_permies = False
        i = 0
        for link in soup.findAll('a'):
            lnk = link.get('href')
            if content_link_p.match(lnk):
                title = lnk[1:]
                if not passed_permies:
                    if title == 'Permies':
                        passed_permies = True
                    continue
                print('Scraping project %d ...' % i)
                self.scrape_project(title)
                i = i + 1

if __name__ == '__main__':
    scrape()
