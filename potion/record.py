'''
record.py: the Record object class for Potion

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

class Record():
    '''Object class for representing a record from TIND.'''

    def __init__(self):
        self.tind_id     = ''
        self.tind_server = ''
        self.barcode     = ''
        self.title       = ''
        self.author      = ''
        self.year        = ''
        self.edition     = ''
        self.imprint     = ''
        self.language    = ''
        self.description = ''
        self.note        = ''
        self.call_no     = ''
        self.thumbnail   = ''
        self.isbn_list = []


    def __str__(self):
        part1 = f' {self.tind_id}' if self.tind_id else ''
        part2 = f' at {self.tind_server}' if self.tind_server else ''
        return f'Record{part1}{part2}'


    def __repr__(self):
        return f'<Record {self.tind_id}>'


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented


    def __ne__(self, other):
        # Based on lengthy Stack Overflow answer by user "Maggyero" posted on
        # 2018-06-02 at https://stackoverflow.com/a/50661674/743730
        eq = self.__eq__(other)
        if eq is not NotImplemented:
            return not eq
        return NotImplemented


    def __lt__(self, other):
        return self.tind_id < other.tind_id


    def __gt__(self, other):
        if isinstance(other, type(self)):
            return other.tind_id < self.tind_id
        return NotImplemented


    def __le__(self, other):
        if isinstance(other, type(self)):
            return not other.tind_id < self.tind_id
        return NotImplemented


    def __ge__(self, other):
        if isinstance(other, type(self)):
            return not self.tind_id < other.tind_id
        return NotImplemented
