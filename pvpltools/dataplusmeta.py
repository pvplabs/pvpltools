"""
This module contains classes/functions to manage small collections
of tabular data and corresponding metadata.

The main class, called DataPlusMeta, bundles the following information:

    3. tabular data as a pandas DataFrame
    2. column definitions for the data, also as a pandas DataFrame
    1. additional metadata in a (possibly nested) dictionary
    0. an optional string identifying the data source

Methods are provided for reading and writing text files.  These will
consist of three mandatory sections:

    1. metadata in yaml format
    2. column definitions as a csv table
    3. data columns as a csv table

The three sections are separated by a two consecutive blank lines.

Note on dates and times:
    Data columns which contain pandas Timestamps will be written
    to the text files in the pandas default format.  Data type (dtype)
    information is stored in the columns definitions table, and is used
    to identify date/time columns that need parsing when read back in.

DataPlusMeta will probably be extended to read/write in other formats,
such as hdf5 or native Excel.

Copyright (c) 2019-2020 Anton Driesse, PV Performance Labs.
"""

from warnings import warn
from io import StringIO
import pandas as pd

from ruamel.yaml import YAML
yaml = YAML(typ='rt')
yaml.default_flow_style = None
yaml.allow_unicode = True

# The following constants govern the formatting and parsing of text files.
# Best to leave them as they are to maintain file compatibility.

PREAMBLE = """\
# This file contains three sections separated by two blank lines.
# The first section contains meta data, which can be parsed with yaml.
# The second and third sections contain data column definitions
# and data respectively, both formatted as csv tables.
"""
# On second thought, let's not use the preamble.
PREAMBLE = ''
UTF8_BOM = u'\uFEFF'
ENCODING = 'utf-8'
SECTION_SEPARATOR = '\n\n'
COMMENT_CHAR = '#'
COMMENT_LINE = COMMENT_CHAR + '\n'
BLANK_LINE = '\n'
# TODO find a way to optionally accept fractional seconds
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

READ_CSV_OPTIONS = dict(skipinitialspace=True,
                        comment=COMMENT_CHAR,
                        float_precision='round_trip')

TO_CSV_OPTIONS = {"lineterminator": "\n"}


class DataPlusMeta():
    """
    Class to bundle tabular data with metadata, with methods to read
    and write files.

    Author: Anton Driesse, PV Performance Labs

    data : pandas.DataFrame, default=None
        Two-dimensional tabular data.

    cdef : pandas.DataFrame, default=None
        Column definitions for the tabular data. Should logically have one
        row for each column in data. (This may be enforced in file
        operations.)

    meta : dict, default=None
        Dictionary containing any useful (or not) metadata. May contain
        lists and other nested dictionaries.

    source : str, default=None
        Identifies the source of the data, if needed.  Typically a file
        name.
    """
    def __init__(self, data=None, cdef=None, meta=None, source=None):
        self.data = data
        self.cdef = cdef
        self.meta = meta or {}
        self.source = source or ''

        # Check and warn if cdef does not match data
        self.check_cdef(raise_on_mismatch=False)

        return

    def __repr__(self):
        '''
        Produce a simple string describing self.
        '''
        if self.data is None:
            ndata = 0
        else:
            ndata = self.data.shape[1] + 1

        classname = self.__class__.__name__
        source = self.source or 'unknown source'

        return ('%s object with %d data columns from %s.' %
                (classname, ndata, source))

    def check_cdef(self, raise_on_mismatch=False):
        '''
        Check whether cdef is consistent with data.  This means matching
        labels and matching dtype values.

        A mismatch generates a warning by default, or can raise a RuntimeError.
        '''

        if (self.cdef is None) & (self.data is None):
            mismatch = False

        elif (self.cdef is None) ^ (self.data is None):
            mismatch = True
            message = 'Either cdef or data is missing.'

        else:
            dtypes = self.data.reset_index().dtypes.astype(str)

            if not all(self.cdef.index == dtypes.index):
                mismatch = True
                message = 'Labels in cdef do not match labels in data.'

            elif 'dtype' not in self.cdef.columns:
                mismatch = True
                message = 'No dtypes in cdef.'

            elif not all(self.cdef.dtype == dtypes):
                mismatch = True
                message = 'dtypes in cdef do not match dtypes in data'

            else:
                mismatch = False

        if mismatch:
            if raise_on_mismatch:
                raise RuntimeError(message)
            else:
                warn(message)
                return False
        return True

    def update_cdef(self, raise_on_fail=True):
        '''
        Update the dtype column in cdef with dtype values found in data,
        or create a new cdef table and/or dtype column.

        Optionally raises a RuntimeError if cdef labels do not match
        data labels.
        '''
        if self.data is None:
            self.cdef = None
        else:
            dtypes = self.data.reset_index().dtypes.astype(str)

            if self.cdef is None:
                self.cdef = pd.DataFrame(dtypes, columns=['dtype'])
                self.cdef.index.name = 'column'

            elif all(self.cdef.index == dtypes.index):
                self.cdef['dtype'] = dtypes

            else:
                message = 'Labels in cdef do not match labels in data.'
                if raise_on_fail:
                    raise RuntimeError(message)
                else:
                    warn(message)
                    return False
        return True

    @classmethod
    def from_txt(cls, file, use_dtypes=True):
        """
        Read the contents of a text file to create a DataPlusMeta object.

        file : str
            Name or path of a text file
        """

        # read the entire file so that it can be split easily
        with open(file, encoding=ENCODING) as f:
            buffer = f.read()

        sections = buffer.split('\n' + SECTION_SEPARATOR)

        # having 3 sections is a basic requirement
        if len(sections) != 3:
            raise RuntimeError('%s does not have three sections.' % file)

        # parse meta
        meta = yaml.load(sections[0])

        # parse column definitions
        cdef = pd.read_csv(StringIO(sections[1]), index_col=0,
                           dtype=dict(dtype=str),
                           **READ_CSV_OPTIONS)

        if use_dtypes and ('dtype' in cdef.columns):
            dtypes = cdef['dtype'].dropna()

            # identify timestamps
            timestamps = dtypes.str.startswith('datetime')

            # pass others to read_csv
            dtype_dict = dtypes[~timestamps].to_dict()

            data = pd.read_csv(StringIO(sections[2]), index_col=None,
                               dtype=dtype_dict, **READ_CSV_OPTIONS)

            # post-parse date columns with standard format
            for col in dtypes[timestamps].index:
                data[col] = pd.to_datetime(data[col], format=DATE_FORMAT)

        else:
            # tolerate missing dtype in cdef for files created by other means
            data = pd.read_csv(StringIO(sections[2]), index_col=None,
                               **READ_CSV_OPTIONS)

        # set index column for normal use
        data = data.set_index(data.columns[0])

        return cls(data, cdef, meta, source=file)

    def to_txt(self, file, update_cdef=True, preamble=None):
        """
        Write the contents of a DataPlusMeta object to a text file.

        file : str
            Name or path of a text file

        Specified file is overwritten without warning if it exists.
        """
        if self.data is None:
            raise RuntimeError('There is no data to store.')

        with open(file, 'w'):
            pass

        if update_cdef:
            self.update_cdef(raise_on_fail=True)
        else:
            self.check_cdef(raise_on_mismatch=True)

        # fill in missing names, if needed
        if self.cdef.index.name is None:
            self.cdef.index.name = 'column'

        if self.data.index.name is None:
            self.data.index.name = self.cdef.index[0]

        with open(file, 'w', encoding=ENCODING) as f:
            f.write(UTF8_BOM)

            if preamble:
                lines = preamble.splitlines()
                for line in lines:
                    f.write(COMMENT_CHAR + ' ' + line + '\n')
                f.write(BLANK_LINE)

            yaml.dump(self.meta, stream=f)

            f.write(SECTION_SEPARATOR)

            # Note: line_terminator is set to '\n' to avoid double conversion
            # to \n\r on Windows when the buffer is written to the file

            self.cdef[:0].to_csv(f, index=True, **TO_CSV_OPTIONS)
            f.write(BLANK_LINE)
            self.cdef.to_csv(f, header=False, index=True, **TO_CSV_OPTIONS)

            f.write(SECTION_SEPARATOR)

            self.data.iloc[:0].to_csv(f, index=True, **TO_CSV_OPTIONS)
            f.write(BLANK_LINE)
            self.data.to_csv(f, header=False, index=True, **TO_CSV_OPTIONS)
        return
