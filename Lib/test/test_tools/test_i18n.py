"""Tests to cover the Tools/i18n package"""

import os
import unittest

from test.script_helper import assert_python_ok
from test.test_tools import toolsdir
from test.support import temp_cwd

class TestPygettext(unittest.TestCase):
    
    script = os.path.join(toolsdir,'i18n', 'pygettext.py')

    def getHeader(self, data):
        """ return the header of a .po file """
        header = {}
        for line in data.split('\n'):
        
            if not line: 
                continue
            if line.startswith(('#', 'msgid','msgstr')): 
                continue
                    
            line = line.strip('"\n')

            key, val = line.split(':',1)
            header[key] = val

        return header
    
    def test_header(self):
        with temp_cwd(None) as cwd:
            assert_python_ok(self.script)
            with open('messages.pot') as fp:
                data = fp.read()
            header = self.getHeader(data)
            
            self.assertIn("POT-Creation-Date", header)
            self.assertIn("PO-Revision-Date", header)
            self.assertIn("Last-Translator", header)
            self.assertIn("Language-Team", header)
            self.assertIn("MIME-Version", header)
            self.assertIn("Content-Type", header)       
            self.assertIn("Content-Transfer-Encoding", header)                                    
            self.assertIn("Generated-By", header)
                                    
                                    
    def test_POT_Creation_Date_tz(self):
        from datetime import datetime
        with temp_cwd(None) as cwd:
            assert_python_ok(self.script)
            
            with open('messages.pot') as fp:
                data = fp.read()
            header = self.getHeader(data)
            creationDate = header['POT-Creation-Date']
            
            #peel off some extra string junk
            if creationDate.endswith('\\n '):
                creationDate = creationDate[:-len('\\n ')]
            
            #if this throws an exception: you fail.
            asDatetime = datetime.strptime(creationDate, '%Y-%m-%d %H:%M%z')  