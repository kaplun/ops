# -*- coding: utf-8 -*-
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""BibDocFile Regression Test Suite."""

__revision__ = "$Id$"

import unittest
from invenio.testutils import make_test_suite, run_test_suite
from invenio.bibdocfile import BibRecDocs#, BibDoc, BibDocFile
from invenio.config import \
        CFG_SITE_URL, \
	CFG_PREFIX, \
	CFG_WEBSUBMIT_FILEDIR



class BibRecDocsTest(unittest.TestCase):
    """regression tests about BibRecDocs"""

    def test_BibRecDocs(self):
        """bibdocfile - BibRecDocs functions"""
        my_bibrecdoc = BibRecDocs(2)
        #add bibdoc
        my_bibrecdoc.add_new_file(CFG_PREFIX + '/lib/webtest/invenio/test.jpg', 'Main', 'img_test', False, 'test add new file', 'test', '.jpg')
        my_bibrecdoc.add_bibdoc(doctype='Main', docname='file', never_fail=False)
        self.assertEqual(len(my_bibrecdoc.list_bibdocs()), 3)
        my_added_bibdoc = my_bibrecdoc.get_bibdoc('file')
        #add bibdocfile in empty bibdoc
        my_added_bibdoc.add_file_new_version(CFG_PREFIX + '/lib/webtest/invenio/test.gif', \
        description= 'added in empty bibdoc', comment=None, format=None, hide_previous_versions=False)
        #propose unique docname
        self.assertEqual(my_bibrecdoc.propose_unique_docname('file'), 'file_2')
        #has docname
        self.assertEqual(my_bibrecdoc.has_docname_p('file'), True)
        #merge 2 bibdocs
        my_bibrecdoc.merge_bibdocs('img_test', 'file')
        self.assertEqual(len(my_bibrecdoc.get_bibdoc("img_test").list_all_files()), 2)
        #check file exists
        self.assertEqual(my_bibrecdoc.check_file_exists(CFG_PREFIX + '/lib/webtest/invenio/test.jpg'), True)
        #get bibdoc names
        self.assertEqual(my_bibrecdoc.get_bibdoc_names('Main')[0], '0104007_02')
        self.assertEqual(my_bibrecdoc.get_bibdoc_names('Main')[1],'img_test')
        #get total size
        self.assertEqual(my_bibrecdoc.get_total_size(), 1628647)
        #get total size latest version
        self.assertEqual(my_bibrecdoc.get_total_size_latest_version(), 1628647)
        #display
        value = my_bibrecdoc.display(docname='img_test', version='', doctype='', ln='en', verbose=0, display_hidden=True)
        self.assert_("<small><b>Main</b>" in value)
        #get xml 8564
        value = my_bibrecdoc.get_xml_8564()
        self.assert_('/record/2/files/img_test.jpg</subfield>' in value)
        #check duplicate docnames
        self.assertEqual(my_bibrecdoc.check_duplicate_docnames(), True)
        #delete
        my_bibrecdoc.delete_bibdoc('img_test')


class BibDocsTest(unittest.TestCase):
    """regression tests about BibDocs"""

    def test_BibDocs(self):
        """bibdocfile - Bibdocs functions"""
        #add file
        my_bibrecdoc = BibRecDocs(2)
        my_bibrecdoc.add_new_file(CFG_PREFIX + '/lib/webtest/invenio/test.jpg', 'Main', 'img_test', False, 'test add new file', 'test', '.jpg')
        my_new_bibdoc = my_bibrecdoc.get_bibdoc("img_test")
        value = my_bibrecdoc.list_bibdocs()
        self.assertEqual(len(value), 2)
        #get total file (bibdoc)
        self.assertEqual(my_new_bibdoc.get_total_size(), 91750)
        #get recid
        self.assertEqual(my_new_bibdoc.get_recid(), 2)
        #change name
        my_new_bibdoc.change_name('new_name')
        #get docname
        self.assertEqual(my_new_bibdoc.get_docname(), 'new_name')
        #get type
        self.assertEqual(my_new_bibdoc.get_type(), 'Main')
        #get id
        self.assert_(my_new_bibdoc.get_id() > 80)
        #set status
        my_new_bibdoc.set_status('new status')
        #get status
        self.assertEqual(my_new_bibdoc.get_status(), 'new status')
        #get base directory
        self.assert_(my_new_bibdoc.get_base_dir().startswith(CFG_WEBSUBMIT_FILEDIR))
        #get file number
        self.assertEqual(my_new_bibdoc.get_file_number(), 1)
        #add file new version
        my_new_bibdoc.add_file_new_version(CFG_PREFIX + '/lib/webtest/invenio/test.jpg', description= 'the new version', comment=None, format=None, hide_previous_versions=False)
        self.assertEqual(my_new_bibdoc.list_versions(), [1, 2])
        #revert
        my_new_bibdoc.revert(1)
        self.assertEqual(my_new_bibdoc.list_versions(), [1, 2, 3])
        self.assertEqual(my_new_bibdoc.get_description('.jpg', version=3), 'test add new file')
        #get total size latest version
        self.assertEqual(my_new_bibdoc.get_total_size_latest_version(), 91750)
        #get latest version
        self.assertEqual(my_new_bibdoc.get_latest_version(), 3)
        #list latest files
        self.assertEqual(len(my_new_bibdoc.list_latest_files()), 1)
        self.assertEqual(my_new_bibdoc.list_latest_files()[0].get_version(), 3)
        #list version files
        self.assertEqual(len(my_new_bibdoc.list_version_files(1, list_hidden=True)), 1)
        #display
        value = my_new_bibdoc.display(version='', ln='en', display_hidden=True)
        self.assert_('>test add new file<' in value)
        #format already exist
        self.assertEqual(my_new_bibdoc.format_already_exists_p('.jpg'), True)
        #get file
        self.assertEqual(my_new_bibdoc.get_file('.jpg', version='1').get_version(), 1)
        #set description
        my_new_bibdoc.set_description('new description', '.jpg', version=1)
        #get description
        self.assertEqual(my_new_bibdoc.get_description('.jpg', version=1), 'new description')
        #set comment
        my_new_bibdoc.set_description('new comment', '.jpg', version=1)
        #get comment
        self.assertEqual(my_new_bibdoc.get_description('.jpg', version=1), 'new comment')
        #get history
        assert len(my_new_bibdoc.get_history()) > 0
        #delete file
        my_new_bibdoc.delete_file('.jpg', 2)
        #list all files
        self.assertEqual(len(my_new_bibdoc.list_all_files()), 2)
        #delete file
        my_new_bibdoc.delete_file('.jpg', 3)
        #add new format
        my_new_bibdoc.add_file_new_format(CFG_PREFIX + '/lib/webtest/invenio/test.gif', version=None, description=None, comment=None, format=None)
        self.assertEqual(len(my_new_bibdoc.list_all_files()), 2)
        #delete file
        my_new_bibdoc.delete_file('.jpg', 1)
        #delete file
        my_new_bibdoc.delete_file('.gif', 1)
        #empty bibdoc
        self.assertEqual(my_new_bibdoc.empty_p(), True)
        #hidden?
        self.assertEqual(my_new_bibdoc.hidden_p('.jpg', version=1), False)
        #hide
        my_new_bibdoc.set_hidden(True, '.jpg', version=1)
        #hidden?
        self.assertEqual(my_new_bibdoc.hidden_p('.jpg', version=1), True)
        #add and get icon
        my_new_bibdoc.add_icon( CFG_PREFIX + '/lib/webtest/invenio/icon-test.gif', basename=None, format=None)
        value =  my_bibrecdoc.list_bibdocs()[1]
        self.assertEqual(value.get_icon(), my_new_bibdoc.get_icon())
        #delete icon
        my_new_bibdoc.delete_icon()
        #get icon
        self.assertEqual(my_new_bibdoc.get_icon(), None)
        #icon_p
        self.assertEqual(my_new_bibdoc.icon_p(), False)
        #delete
        my_new_bibdoc.delete()
        self.assertEqual(my_new_bibdoc.deleted_p(), True)
        #undelete
        my_new_bibdoc.undelete(previous_status='')
        #delete
        my_bibrecdoc.delete_bibdoc('new-name')


class BibDocFilesTest(unittest.TestCase):
    """regression tests about BibDocFiles"""

    def test_BibDocFiles(self):
        """bibdocfile - BibdocFiles functions """
        #add bibdoc
        my_bibrecdoc = BibRecDocs(2)
        my_bibrecdoc.add_new_file(CFG_PREFIX + '/lib/webtest/invenio/test.jpg', 'Main', 'img_test', False, 'test add new file', 'test', '.jpg')
        my_new_bibdoc = my_bibrecdoc.get_bibdoc("img_test")
        my_new_bibdocfile = my_new_bibdoc.list_all_files()[0]
        #get url
        self.assertEqual(my_new_bibdocfile.get_url(), CFG_SITE_URL + '/record/2/files/img_test.jpg')
        #get type
        self.assertEqual(my_new_bibdocfile.get_type(), 'Main')
        #get path
        self.assert_(my_new_bibdocfile.get_path().startswith(CFG_WEBSUBMIT_FILEDIR))
        self.assert_(my_new_bibdocfile.get_path().endswith('/img_test.jpg;1'))
        #get bibdocid
        self.assertEqual(my_new_bibdocfile.get_bibdocid(), my_new_bibdoc.get_id())
        #get name
        self.assertEqual(my_new_bibdocfile.get_name() , 'img_test')
        #get full name
        self.assertEqual(my_new_bibdocfile.get_full_name() , 'img_test.jpg')
        #get full path
        self.assert_(my_new_bibdocfile.get_full_path().startswith(CFG_WEBSUBMIT_FILEDIR))
        self.assert_(my_new_bibdocfile.get_full_path().endswith('/img_test.jpg;1'))
        #get format
        self.assertEqual(my_new_bibdocfile.get_format(), '.jpg')
        #get version
        self.assertEqual(my_new_bibdocfile.get_version(), 1)
        #get description
        self.assertEqual(my_new_bibdocfile.get_description(), my_new_bibdoc.get_description('.jpg', version=1))
        #get comment
        self.assertEqual(my_new_bibdocfile.get_comment(), my_new_bibdoc.get_comment('.jpg', version=1))
        #get recid
        self.assertEqual(my_new_bibdocfile.get_recid(), 2)
        #get status
        self.assertEqual(my_new_bibdocfile.get_status(), '')
        #get size
        self.assertEqual(my_new_bibdocfile.get_size(), 91750)
        #get checksum
        self.assertEqual(my_new_bibdocfile.get_checksum(), '28ec893f9da735ad65de544f71d4ad76')
        #check
        self.assertEqual(my_new_bibdocfile.check(), True)
        #display
        value = my_new_bibdocfile.display(ln='en')
        assert 'files/img_test.jpg?version=1">' in value
        #hidden?
        self.assertEqual(my_new_bibdocfile.hidden_p(), False)
        #delete
        my_new_bibdoc.delete()
        self.assertEqual(my_new_bibdoc.deleted_p(), True)


TEST_SUITE = make_test_suite(BibRecDocsTest, \
                             BibDocsTest, \
                             BibDocFilesTest)
if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)