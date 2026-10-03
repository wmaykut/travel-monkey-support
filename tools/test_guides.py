"""Focused checks for update handling and the content-loss guard."""
import unittest
from check_guides import verify_text, source_units
from pdf_guides import slug, link_target

SOURCE = '''# Travel Monkey quick start

Last updated: November 7, 2027

An opening paragraph.

## 1. Start here

Keep **allergies** separate from dislikes.

| Control | What it does |
|---|---|
| **Lock it in** | Records your choice |
'''


class GuideBuildTests(unittest.TestCase):
    def test_updated_dates_and_markdown_emphasis_are_preserved(self):
        verify_text(SOURCE, 'November 7, 2027 An opening paragraph. Start here Keep allergies separate from dislikes. Control What it does Lock it in Records your choice', 'test')

    def test_missing_paragraph_fails_validation(self):
        with self.assertRaisesRegex(ValueError,'source content missing'):
            verify_text(SOURCE,'November 7, 2027 An opening paragraph. Start here Control What it does Lock it in Records your choice','test')

    def test_stale_date_fails_validation(self):
        with self.assertRaisesRegex(ValueError,'outdated document date'):
            verify_text(SOURCE,'October 2, 2026 An opening paragraph. Start here Keep allergies separate from dislikes. Control What it does Lock it in Records your choice','test')

    def test_tables_are_checked_cell_by_cell(self):
        self.assertIn('**Lock it in**',source_units(SOURCE))
        self.assertNotIn('---',source_units(SOURCE))

    def test_internal_links_stay_local(self):
        self.assertEqual(link_target('#try-a-sample-trip'),'#try-a-sample-trip')
        self.assertEqual(slug('Data, iCloud, and offline use'),'data-icloud-and-offline-use')


if __name__=='__main__': unittest.main()
