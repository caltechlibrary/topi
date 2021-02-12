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

    # The reason for an explicit list of fields here is so that we can use it
    # in the definition of __repr__().
    __fields = {
        'tind_id'     : str,
        'tind_server' : str,
        'barcode'     : str,
        'title'       : str,
        'author'      : str,
        'year'        : str,
        'edition'     : str,
        'imprint'     : str,
        'language'    : str,
        'description' : str,
        'note'        : str,
        'call_no'     : str,
        'thumbnail'   : str,
        'isbn_list'   : list
    }


    def __init__(self, **kwargs):
        # Always first initialize every field.
        for field, field_type in self.__fields.items():
            setattr(self, field, ([] if field_type == list else ''))
        # Set values if given arguments.
        for field, value in kwargs.items():
            setattr(self, field, value)


    def __str__(self):
        part1 = f' {self.tind_id}' if self.tind_id else ''
        part2 = f' at {self.tind_server}' if self.tind_server else ''
        return f'Record{part1}{part2}'


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
            return 'Record(' + ', '.join(field_values) + ')'
        else:
            return 'Record()'


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
