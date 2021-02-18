        args = locals().copy()
        del args['self']
        given_keywords = list(keyword for keyword in args if args[keyword])
        record = None
        if len(given_keywords) == 1:
            given = given_keywords[0]
            record = self._record_from_argument[given](self, args[given])
        elif len(given_keywords) == 0:
            raise ValueError(f"At least one argument required, but none given")
        else:                           # More than one keyword arg given.
            given = ', '.join(given)
            raise ValueError(f"Conflicting arguments given: {given}")



    # Initialize the dispatcher after defining the methods themselves.
    _record_from_argument = {'barcode' : staticmethod(_record_from_barcode).__func__,
                             'tind_id' : staticmethod(_record_from_tind_id).__func__,
                             'marc_xml': staticmethod(_record_from_xml).__func__}

