import re

import mwparserfromhell as mw
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import xmltodict

from twewy.fandom import NoiseInfobox, PinBox

pin_name_pattern = re.compile('^Pin \d{3}')
infobox_pattern = re.compile('^{{(Template:)?Infobox (Boss|Taboo Noise|Pig Noise|Noise)')

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from twewy.models import Noise, Pin
    d = xmltodict.parse(open("twewy_pages_current.xml").read())
    pages = d['mediawiki']['page']

    pin_pages = (page['revision']['text']['#text']
                 for page in pages
                 if pin_name_pattern.match(page['title'])
                 and page['title'] != 'Pin 000')
    pin_boxes = (PinBox(mw.parse(page).filter_templates(matches='Pin box')[0])
                 for page in pin_pages)
    pins = (Pin(number=pin.number,
                name=pin.name,
                brand=pin.brand,
                bpp_yields_number=pin.bpp_yields,
                mpp_yields_number=pin.mpp_yields,
                sdpp_yields_number=pin.sdpp_yields)
            for pin in pin_boxes)

    noise_pages = (page['revision']['text']['#text']
                   for page in pages
                   if '#text' in page['revision']['text']
                   if infobox_pattern.match(page['revision']['text']['#text']))
    noise_infoboxes= (NoiseInfobox(mw.parse(page).filter_templates(matches='Infobox.*Noise')[0])
                      for page in noise_pages)
    noise = (Noise(number=noise.number,
                   name=noise.name,
                   hp=noise.hit_points,
                   attack=noise.attack,
                   pp=noise.pin_points,
                   exp=noise.experience)
             for noise in noise_infoboxes)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db_session.add_all(pins)
    # db_session.add_all(noise)
    db_session.commit()
