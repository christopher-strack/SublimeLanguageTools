import re
import sys

from sublime_plugin import TextCommand
from sublime import Region


class ReplaceCommand(TextCommand):

    def replace(self, text):
        raise NotImplementedError

    def run(self, edit):
        if not self.replace_selection(edit):
            self.replace_all(edit)

    def replace_selection(self, edit):
        replaced = False
        for region in filter(lambda r: not r.empty(), self.view.sel()):
            self.replace_region(edit, region)
            replaced = True
        return replaced

    def replace_all(self, edit):
        self.replace_region(edit, Region(0, self.view.size()))

    def replace_region(self, edit, region):
        s = self.replace(self.view.substr(region))
        self.view.replace(edit, region, s)


class ReplaceQuotesCommand(ReplaceCommand):

    _pattern_double = re.compile(r'"(.+?)"', re.DOTALL)
    _pattern_single = re.compile(r'\'(.+?)\'', re.DOTALL)

    def run(self, edit, quote_begin, quote_end):
        self._quote_begin = quote_begin
        self._quote_end = quote_end
        super().run(edit)

    def replace(self, text):
        s = self._pattern_double.sub(
            r'%s\1%s' % (self._quote_begin, self._quote_end), text)
        return self._pattern_single.sub(r'‘\1’', s)


class ReplaceFrenchPunctuationSpacingCommand(ReplaceCommand):

    _before_pattern = re.compile(r' ([:;?!»])')
    _after_pattern = re.compile(r'(«) ')

    def replace(self, text):
        s = self._before_pattern.sub(r'&nbsp;\1', text)
        return self._after_pattern.sub(r'\1&nbsp;', s)
