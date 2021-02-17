'''
record.py: the TindRecord object class for Potion

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

class TindRecord():
    '''Object class for representing a record from TIND.'''

    # The reason for an explicit list of fields here is so that we can use it
    # in the definition of __repr__().
    __fields = {
        'tind_id'     : str,            # Tind id == MARC control field 001.
        'url'         : str,            # Page for the record in TIND.
        'title'       : str,            # MARC data field 245
        'subtitle'    : str,            # MARC data field 245
        'author'      : str,            # MARC data field 245 or 100
        'edition'     : str,            # MARC data field 250
        'year'        : str,            # extracted from control field 008
        'isbn_issn'   : list,           # MARC data field 020
        'description' : str,            # MARC data field 300 concatenated
        'bib_note'    : str,            # MARC data field 504a
        'thumbnail'   : str,
        'items'       : list,
    }


    def __init__(self, **kwargs):
        # Always first initialize every field.
        for field, field_type in self.__fields.items():
            setattr(self, field, ([] if field_type == list else ''))
        # Set values if given arguments.
        for field, value in kwargs.items():
            setattr(self, field, value)


    def __str__(self):
        details = f' {self.url}' if self.url else ''
        return f'TindRecord{details}'


    def __repr__(self):
        field_values = []
        for field in self.__fields.keys():
            value = getattr(self, field, None)
            if value:
                if isinstance(value, list):
                    field_values.append(f'{field}={value}')
                else:
                    field_values.append(f'{field}="{value}"')
        if field_values:
            return 'TindRecord(' + ', '.join(field_values) + ')'
        else:
            return 'TindRecord()'


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
