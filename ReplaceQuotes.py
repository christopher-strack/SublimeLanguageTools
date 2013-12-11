import re
import sys

from sublime_plugin import TextCommand
from sublime import Region


_pattern_double = re.compile(r'"(.+?)"', re.DOTALL)
_pattern_single = re.compile(r'\'(.+?)\'', re.DOTALL)

def replace_quotes(text, quote_begin, quote_end):
    s = _pattern_double.sub(r'%s\1%s' % (quote_begin, quote_end), text)
    return _pattern_single.sub(r'‘\1’', s)


class ReplaceQuotesCommand(TextCommand):

    def run(self, edit, quote_begin, quote_end):
        if not self.replace_selection(edit, quote_begin, quote_end):
            self.replace_all(edit, quote_begin, quote_end)

    def replace_selection(self, edit, quote_begin, quote_end):
        replaced = False
        for region in filter(lambda r: not r.empty(), self.view.sel()):
            self.replace_region(
                edit, region,
                quote_begin, quote_end)
            replaced = True
        return replaced

    def replace_all(self, edit, quote_begin, quote_end):
        self.replace_region(
            edit, Region(0, self.view.size()),
            quote_begin, quote_end)

    def replace_region(self, edit, region, *a, **k):
        s = replace_quotes(self.view.substr(region), *a, **k)
        self.view.replace(edit, region, s)
