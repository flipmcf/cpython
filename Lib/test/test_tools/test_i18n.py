"""Tests to cover the Tools/i18n package"""

import os
import unittest

from test.script_helper import assert_python_ok
from test.test_tools import toolsdir
from test.support import temp_cwd

class Test_pygettext(unittest.TestCase):
    """Tests for the pygettext.py tool"""
    
    script = os.path.join(toolsdir,'i18n', 'pygettext.py')

    def getHeader(self, data):
        """ utility: return the header of a .po file as a dictionary """
        header = {}
        for line in data.split('\n'):
        
            if not line: 
                continue
            if line.startswith(('#', 'msgid','msgstr')): 
                continue
                    
            line = line.strip('"')

            key, val = line.split(':',1)
            header[key] = val.strip()

        return header
    
    def test_header(self):
        """Make sure the required fields are in the header
           spec: http://www.gnu.org/software/gettext/manual/gettext.html#Header-Entry
        """
        with temp_cwd(None) as cwd:
            assert_python_ok(self.script)
            with open('messages.pot') as fp:
                data = fp.read()
            header = self.getHeader(data)
            
            self.assertIn("Project-Id-Version", header)
            self.assertIn("POT-Creation-Date", header)
            self.assertIn("PO-Revision-Date", header)
            self.assertIn("Last-Translator", header)
            self.assertIn("Language-Team", header)
            self.assertIn("MIME-Version", header)
            self.assertIn("Content-Type", header)   
            self.assertIn("Content-Transfer-Encoding", header)                                    
            self.assertIn("Generated-By", header)
            
            #not sure if these should be required in POT (template) files
            #self.assertIn("Report-Msgid-Bugs-To", header)
            #self.assertIn("Language", header)
            
            #"Plural-Forms" is optional
                                    
                                    
    def test_POT_Creation_Date(self):
        """ Match the date format from xgettext for POT-Creation-Date """
        from datetime import datetime
        with temp_cwd(None) as cwd:
            assert_python_ok(self.script)
            
            with open('messages.pot') as fp:
                data = fp.read()
            header = self.getHeader(data)
            creationDate = header['POT-Creation-Date']
            
            #peel off the escaped newline at the end of string
            if creationDate.endswith('\\n'):
                creationDate = creationDate[:-len('\\n')]
            
            #if this throws an exception: you fail.
            asDatetime = datetime.strptime(creationDate, '%Y-%m-%d %H:%M%z')  