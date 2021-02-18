import os
import sys

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from potion import Tind, TindItem, TindRecord

if __debug__:
    from sidetrack import log, set_debug


MARC_XML = r'''<?xml version="1.0" encoding="UTF-8"?>
<collection xmlns="http://www.loc.gov/MARC21/slim">
<record>
  <controlfield tag="000">01059cam\a2200361Ia\4500</controlfield>
  <controlfield tag="001">735973</controlfield>
  <controlfield tag="005">20201028221548.0</controlfield>
  <controlfield tag="008">120118s2012\\\\nyua\\\\\b\\\\001\0\eng\d</controlfield>
  <datafield tag="010" ind1=" " ind2=" ">
    <subfield code="a">2011931725</subfield>
  </datafield>
  <datafield tag="015" ind1=" " ind2=" ">
    <subfield code="a">GBB1D1820</subfield>
    <subfield code="2">bnb</subfield>
  </datafield>
  <datafield tag="016" ind1="7" ind2=" ">
    <subfield code="a">015969759</subfield>
    <subfield code="2">Uk</subfield>
  </datafield>
  <datafield tag="019" ind1=" " ind2=" ">
    <subfield code="a">761380918</subfield>
  </datafield>
  <datafield tag="020" ind1=" " ind2=" ">
    <subfield code="a">1429215089</subfield>
  </datafield>
  <datafield tag="020" ind1=" " ind2=" ">
    <subfield code="a">1429224045 (hbk.)</subfield>
  </datafield>
  <datafield tag="020" ind1=" " ind2=" ">
    <subfield code="a">9781429215084</subfield>
  </datafield>
  <datafield tag="020" ind1=" " ind2=" ">
    <subfield code="a">9781429224048 (hbk.)</subfield>
  </datafield>
  <datafield tag="035" ind1=" " ind2=" ">
    <subfield code="a">(OCoLC)773193687</subfield>
    <subfield code="z">(OCoLC)761380918</subfield>
  </datafield>
  <datafield tag="040" ind1=" " ind2=" ">
    <subfield code="a">IPL</subfield>
    <subfield code="c">IPL</subfield>
    <subfield code="d">YDXCP</subfield>
    <subfield code="d">UKMGB</subfield>
    <subfield code="d">BWX</subfield>
    <subfield code="d">CIT</subfield>
  </datafield>
  <datafield tag="049" ind1=" " ind2=" ">
    <subfield code="a">CIT5</subfield>
  </datafield>
  <datafield tag="050" ind1=" " ind2="4">
    <subfield code="a">QA303</subfield>
    <subfield code="b">.M338 2012</subfield>
  </datafield>
  <datafield tag="100" ind1="1" ind2=" ">
    <subfield code="a">Marsden, Jerrold E</subfield>
  </datafield>
  <datafield tag="245" ind1="1" ind2="0">
    <subfield code="a">Vector calculus /</subfield>
    <subfield code="c">Jerrold E. Marsden, Anthony Tromba</subfield>
  </datafield>
  <datafield tag="250" ind1=" " ind2=" ">
    <subfield code="a">6th ed</subfield>
  </datafield>
  <datafield tag="260" ind1=" " ind2=" ">
    <subfield code="a">New York :</subfield>
    <subfield code="b">W.H. Freeman,</subfield>
    <subfield code="c">c2012</subfield>
  </datafield>
  <datafield tag="300" ind1=" " ind2=" ">
    <subfield code="a">xxv, 545 p. :</subfield>
    <subfield code="b">ill. (some col.) ;</subfield>
    <subfield code="c">26 cm</subfield>
  </datafield>
  <datafield tag="504" ind1=" " ind2=" ">
    <subfield code="a">Includes bibliographical references and index</subfield>
  </datafield>
  <datafield tag="650" ind1=" " ind2="0">
    <subfield code="a">Calculus</subfield>
  </datafield>
  <datafield tag="650" ind1=" " ind2="0">
    <subfield code="a">Vector analysis</subfield>
  </datafield>
  <datafield tag="690" ind1=" " ind2=" ">
    <subfield code="a">Caltech authors</subfield>
  </datafield>
  <datafield tag="700" ind1="1" ind2=" ">
    <subfield code="a">Tromba, Anthony</subfield>
  </datafield>
  <datafield tag="907" ind1=" " ind2=" ">
    <subfield code="a">.b14946786</subfield>
    <subfield code="b">150825</subfield>
    <subfield code="c">120214</subfield>
  </datafield>
  <datafield tag="909" ind1="C" ind2="O">
    <subfield code="o">oai:caltech.tind.io:735973</subfield>
    <subfield code="p">caltech:bibliographic</subfield>
  </datafield>
  <datafield tag="948" ind1=" " ind2=" ">
    <subfield code="a">PP</subfield>
  </datafield>
  <datafield tag="980" ind1=" " ind2=" ">
    <subfield code="a">BIB</subfield>
  </datafield>
  <datafield tag="998" ind1=" " ind2=" ">
    <subfield code="a">sfl</subfield>
    <subfield code="b">120313</subfield>
    <subfield code="c">a</subfield>
    <subfield code="d">m</subfield>
    <subfield code="e">-</subfield>
    <subfield code="f">eng</subfield>
    <subfield code="g">nyu</subfield>
    <subfield code="h">0</subfield>
    <subfield code="i">1</subfield>
  </datafield>
</record>
</collection>'''.encode()


def test_xml():
    tind = Tind('https://caltech.tind.io')
    r = tind.record(marc_xml = MARC_XML)
    assert r.tind_id == '735973'
    assert r.title   == 'Vector calculus'
    assert r.author  == 'Jerrold E. Marsden, Anthony Tromba'
    assert r.year    == '2012'
    assert r.edition == '6th ed'
    assert len(r.items) == 3
    barcodes = [item.barcode for item in r.items]
    assert "35047018228114" in barcodes
    assert "35047019492099" in barcodes
    assert "35047019292101" in barcodes


def test_item1():
    tind = Tind('https://caltech.tind.io')
    item = tind.item(barcode = "35047018228114")
    assert item.barcode == "35047018228114"
    assert item.type == 'Book'
    assert item.call_number == 'QA303 .M338 2012'
    assert item.location == 'SFL basement books'
    assert item.parent.tind_id == '735973'


def test_barcode1():
    tind = Tind('https://caltech.tind.io')
    item = tind.item(barcode = 35047019626837)
    assert item.barcode == '35047019626837'
    assert item.parent.tind_id == '990468'
    assert item.parent.title   == 'Fundamentals of geophysics'
    assert item.parent.author  == 'William Lowrie, Andreas Fichtner'
    assert item.parent.edition == 'Third edition'
    assert item.parent.year    == '2020'
    assert item.call_number == 'QC806.L67 2020'


def test_barcode2():
    tind = Tind('https://caltech.tind.io')
    item = tind.item(barcode = 350470000611207)
    assert item.barcode == '350470000611207'
    assert item.call_number == 'PR6013.R416 Z465'
    assert item.parent.tind_id  == '466498'
    assert item.parent.title    == 'Pack my bag'
    assert item.parent.subtitle == 'a self-portrait'
    assert item.parent.author   == 'Henry Green'
    assert item.parent.edition  == ''
    assert item.parent.year     == '1940'


def test_barcode3():
    tind = Tind('https://caltech.tind.io')
    item = tind.item(barcode = 35047019626829)
    assert item.barcode == '35047019626829'
    assert item.call_number == 'Q175 .G5427'
    assert item.parent.tind_id  == '990456'
    assert item.parent.title    == 'GIS for science'
    assert item.parent.subtitle == 'applying mapping and spatial analytics'
    assert item.parent.author   == 'Dawn J. Wright and Christian Harder, editors'
    assert item.parent.year     == '2019'
    assert item.parent.edition  == ''


def test_tind_id1():
    tind = Tind('https://caltech.tind.io')
    r = tind.record(tind_id = 673541)
    assert r.tind_id  == '673541'
    assert r.title    == 'Subtitles'
    assert r.subtitle == 'on the foreignness of film'
    assert r.author   == 'Atom Egoyan and Ian Balfour'
    assert r.year     == '2004'
    assert r.edition  == ''


def test_tind_id2():
    tind = Tind('https://caltech.tind.io')
    r = tind.record(tind_id = 670639)
    assert r.tind_id == '670639'
    assert r.title   == 'French fest'
    assert r.author  == 'played by Mark Laubach'
    assert r.year    == '1997'
    assert r.edition == ''


def test_tind_id3():
    tind = Tind('https://caltech.tind.io')
    r = tind.record(tind_id = 748838)
    assert r.tind_id == '748838'
    assert r.title   == 'Lasers and electro-optics'
    assert r.author  == 'Christopher C. Davis, University of Maryland'
    assert r.year    == '2014'
    assert r.edition == 'Second edition'


def test_tind_id4():
    tind = Tind('https://caltech.tind.io')
    r = tind.record(tind_id = 676897)
    assert r.tind_id == '676897'
    assert r.title   == 'The diamond age'
    assert r.author  == 'Neal Stephenson'
    assert r.year    == '2003'
    assert r.edition == 'Bantam trade pbk. reissue'


def test_tind_id5():
    tind = Tind('https://caltech.tind.io')
    r = tind.record(tind_id = 705063)
    assert r.tind_id    == '705063'
    assert r.url        == 'https://caltech.tind.io/record/705063'
    assert r.title      == 'Python essential reference'
    assert r.author     == 'David M. Beazley'
    assert r.edition    == '4th ed'
    assert r.year       == '2009'
    assert r.isbn_issn  == ['0672329786', '9780672329784']
    assert len(r.items) == 1
    assert r.items[0].parent      == r
    assert r.items[0].barcode     == '35047018886929'
    assert r.items[0].type        == 'Book'
    assert r.items[0].call_number == 'QA76.73.P98 B43 2009'


def test_tind_id6():
    tind = Tind('https://caltech.tind.io')
    r = tind.record(tind_id = 574858)
    assert r.tind_id    == '574858'
    assert r.url        == 'https://caltech.tind.io/record/574858'
    assert r.title      == 'Feedback control theory'
    assert r.author     == 'John C. Doyle, Bruce A. Francis, Allen R. Tannenbaum'
    assert r.year       == '1992'
    assert r.isbn_issn  == ['0023300116']
    assert len(r.items) == 2
    assert r.items[0].parent      == r
    assert r.items[0].barcode     == '35047011140233'
    assert r.items[0].type        == 'Book'
    assert r.items[0].call_number == 'TJ216 .D69 1992'
    assert r.items[0].description == 'c.1'
    assert r.items[0].library     == 'Sherman Fairchild Library'
    assert r.items[0].location    == 'SFL 2 books'
    assert r.items[1].parent      == r
    assert r.items[1].barcode     == '35047019061456'
    assert r.items[1].type        == 'Book'
    assert r.items[1].call_number == 'TJ216 .D69 1992'


def test_repr1():
    tind = Tind('https://caltech.tind.io')
    r = tind.item(barcode = 35047019626837)
    assert str(r) == 'TindItem 35047019626837'
    assert repr(r) == ('TindItem(parent="TindRecord '
                       'https://caltech.tind.io/record/990468", '
                       'barcode="35047019626837", type="Book", '
                       'call_number="QC806.L67 2020", '
                       'description="c.1", library="Sherman Fairchild Library", '
                       'location="SFL1 Closed Reserve (24-hr)", status="on shelf")')



def test_repr2():
    tind = Tind('https://caltech.tind.io')
    r = tind.record(676897)
    assert str(r) == 'TindRecord https://caltech.tind.io/record/676897'
    assert repr(r) == ('TindRecord(tind_id="676897", title="The diamond age", '
                       'author="Neal Stephenson", edition="Bantam trade pbk. reissue", '
                       'year="2003", isbn_issn=[\'0553380966\'], '
                       'description="499 p. ; 21 cm", '
                       'thumbnail_url="https://bookcover.tind.io//bookcover/thumbnails/0553380966_large", '
                       'items=[TindItem(parent="TindRecord https://caltech.tind.io/record/676897", '
                       'barcode="35047018297788", type="Book", '
                       'call_number="PS3569.T3868 D53 2003", description="c.1", '
                       'library="Millikan Library", '
                       'location="Millikan 9 leisure collection", status="on shelf")])')
