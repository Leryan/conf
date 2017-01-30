#!/usr/bin/env python2

# -*- coding: utf-8 -*-

import sys

try:
    import pyparsing as pp
except ImportError:
    sys.stderr.write("Install pyparsing python library.\n")
    sys.exit(1)

from StringIO import StringIO

spaces = pp.OneOrMore(pp.White(' '))
opspaces = pp.Optional(spaces)
comment = pp.oneOf('; #') + pp.restOfLine()
block_define = pp.Keyword('define') + pp.Word(pp.alphas) + pp.Literal('{')
key_value = pp.Word(pp.alphanums + '_' + '-') + spaces + pp.restOfLine()
block_end = pp.Word("}") + pp.restOfLine()

text = """; outside comment
#another outsite comment
define broker {
    key value
    #comment blah
    ;comment2 blah
    key value ;comment
}

;# outsite comment 2

define module {
    module_name canopsis
      module_type canopsis
    host localhost
} ;# end block comment
; comment 3
"""


class ParseMustStop(Exception):
    pass


class ParseCompleteStop(Exception):
    pass


class BaseParse(object):

    def __init__(self):
        self.setHooks()
        self.textLines = []

    def setHooks(self):
        all_names = dir(self)

        names = [getattr(self, method)
                 for method in all_names if method.startswith('parseHook')]

        methods = [method for method in names if callable(method)]

        self.parse_hooks = sorted(methods)

    def setText(self, text):
        self.textLines = text.replace("\r", "").split("\n")

    def parse(self):
        for line in self.textLines:
            for parseHook in self.parse_hooks:
                try:
                    parseHook(line)

                except ParseMustStop, e:
                    break

                except ParseCompleteStop, e:
                    return e, line


class ConfState(object):

    def __init__(self):
        super(ConfState, self).__init__()
        self.in_block = False
        self.current_block_type = ''
        self.current_block_buffer = []
        self.modify_current_block = False
        self.modify_informations = {}

    def addLineKeyValue(self, key, value, rawline):
        self.current_block_buffer.append(
            {'type': 'keyval', 'key': key, 'value': value, 'rawline': rawline})

    def addLineComment(self, comment, rawline):
        self.current_block_buffer.append(
            {'type': 'comment', 'comment': comment, 'rawline': rawline})

    def resetBlockBuffer(self):
        self.current_block_buffer = []

    def setModifyInformation(self, key, value):
        self.modify_informations[key] = value

    def rewriteBlock(self):
        lines = []

        if not self.modify_current_block:
            lines = [line['rawline'] for line in self.current_block_buffer]

        else:
            for line in self.current_block_buffer:
                if line['type'] == 'keyval':
                    lines.append(
                        '    {0}    {1}'.format(line['key'], line['value']))

                elif line['type'] == 'comment':
                    lines.append('    {0}'.format(line['comment']))

        return "\n".join(lines)

    def rewriteCanopsisModuleConfig(self):
        pass



class ConfParse(BaseParse):

    def __init__(self):
        super(ConfParse, self).__init__()
        self.finalConf = StringIO()
        self.resetNextNewConfLine()
        self.confstate = ConfState()

    def writeNextNewConfLine(self):
        if self.nextNewConfLine != None:
            self.finalConf.write(self.nextNewConfLine + "\n")

    def setNextNewConfLine(self, text):
        self.nextNewConfLine = text

    def resetNextNewConfLine(self):
        self.nextNewConfLine = None

    def tryPyParsing(func):
        def wrapper(self, *args, **kwargs):
            self.setNextNewConfLine(args[0])
            try:
                func(self, *args, **kwargs)

            except pp.ParseException, e:
                self.resetNextNewConfLine()

            except ParseMustStop, e:
                self.writeNextNewConfLine()
                raise ParseMustStop(e)

            self.writeNextNewConfLine()
        return wrapper

    @tryPyParsing
    def parseHook001Comment(self, line):
        r = comment.parseString(line)
        if self.confstate.in_block:
            self.confstate.addLineComment(r[0] + r[1], line)
            self.resetNextNewConfLine()
        raise ParseMustStop()

    @tryPyParsing
    def parseHook002DefineBlock(self, line):
        r = block_define.parseString(line)
        self.confstate.current_block_type = r[1]
        self.confstate.in_block = True
        raise ParseMustStop()

    @tryPyParsing
    def parseHook003KeyValue(self, line):
        if not self.confstate.in_block:
            return

        self.resetNextNewConfLine()

        r = key_value.parseString(line)
        key = r[0]
        spaces = r[1]
        value = r[2]

        if key == 'module_type' and value == 'canopsis':
            self.confstate.modify_current_block = True
            self.confstate.setModifyInformation('type', 'canopsis')
            self.confstate.setModifyInformation('key', ['host', 'blabla'])

        self.confstate.addLineKeyValue(key, value, line)
        raise ParseMustStop()

    @tryPyParsing
    def parseHook004BlockEnd(self, line):
        r = block_end.parseString(line)
        self.confstate.in_block = False
        text = self.confstate.rewriteBlock()
        self.setNextNewConfLine(text + "\n" + r[0] + r[1])
        self.confstate.resetBlockBuffer()
        raise ParseMustStop()


if __name__ == '__main__':
    confparser = ConfParse()
    confparser.setText(text)
    confparser.parse()
    print('>>> Original text:')
    sys.stdout.write(text)
    print('<<< New text:')
    sys.stdout.write(confparser.finalConf.getvalue())
