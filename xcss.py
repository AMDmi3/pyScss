#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
xCSS Framework for Python

@author    German M. Bravo (Kronuz)
           Based on some code from the original xCSS project by Anton Pawlik
@version   0.5
@see       http://xcss.antpaw.org/docs/
           http://sass-lang.com/
           http://oocss.org/spec/css-object-model.html
@copyright (c) 2011 German M. Bravo (Kronuz)
           (c) 2010 Anton Pawlik
@license   MIT License
           http://www.opensource.org/licenses/mit-license.php

xCSS for Python is a superset of CSS that is more powerful, elegant and easier
to maintain than plain-vanilla CSS. The library works as a CSS source code
preprocesor which allows you to use variables, nested rules, mixins, and have
inheritance of rules, all with a CSS-compatible syntax which the preprocessor
then compiles to standard CSS.

xCSS, as an extension of CSS, helps keep large stylesheets well-organized. It
borrows concepts and functionality from projects such as OOCSS and other similar
frameworks like as Sass. It's build on top of the original PHP xCSS codebase
structure but it's been completely rewritten and many bugs have been fixed.

"""
import re
import sys
import string

MEDIA_ROOT = '/usr/local/www/mdubalu/media/'
ASSETS_ROOT = MEDIA_ROOT + 'assets/'
MEDIA_URL = '/media/'
ASSETS_URL = MEDIA_URL + 'assets/'
SAAS_ROOT = '/usr/local/www/mdubalu/myapp/templates/frameworks'

# units and conversions
_units = ['em', 'ex', 'px', 'cm', 'mm', 'in', 'pt', 'pc', 'deg', 'rad'
          'grad', 'ms', 's', 'hz', 'khz', '%']
_conv = {
    'size': {
        'em': 13.0,
        'px': 1.0
    },
    'length': {
        'mm':  1.0,
        'cm':  10.0,
        'in':  25.4,
        'pt':  25.4 / 72,
        'pc':  25.4 / 6
    },
    'time': {
        'ms':  1.0,
        's':   1000.0
    },
    'freq': {
        'hz':  1.0,
        'khz': 1000.0
    },
    'any': {
        '%': 1.0 / 100
    }
}
_conv_type = {}
_conv_factor = {}
for t, m in _conv.items():
    for k, f in m.items():
        _conv_type[k] = t
        _conv_factor[k] = f
del t, m, k, f

# color literals
_colors = {
    'aliceblue': '#f0f8ff',
    'antiquewhite': '#faebd7',
    'aqua': '#00ffff',
    'aquamarine': '#7fffd4',
    'azure': '#f0ffff',
    'beige': '#f5f5dc',
    'bisque': '#ffe4c4',
    'black': '#000000',
    'blanchedalmond': '#ffebcd',
    'blue': '#0000ff',
    'blueviolet': '#8a2be2',
    'brown': '#a52a2a',
    'burlywood': '#deb887',
    'cadetblue': '#5f9ea0',
    'chartreuse': '#7fff00',
    'chocolate': '#d2691e',
    'coral': '#ff7f50',
    'cornflowerblue': '#6495ed',
    'cornsilk': '#fff8dc',
    'crimson': '#dc143c',
    'cyan': '#00ffff',
    'darkblue': '#00008b',
    'darkcyan': '#008b8b',
    'darkgoldenrod': '#b8860b',
    'darkgray': '#a9a9a9',
    'darkgreen': '#006400',
    'darkkhaki': '#bdb76b',
    'darkmagenta': '#8b008b',
    'darkolivegreen': '#556b2f',
    'darkorange': '#ff8c00',
    'darkorchid': '#9932cc',
    'darkred': '#8b0000',
    'darksalmon': '#e9967a',
    'darkseagreen': '#8fbc8f',
    'darkslateblue': '#483d8b',
    'darkslategray': '#2f4f4f',
    'darkturquoise': '#00ced1',
    'darkviolet': '#9400d3',
    'deeppink': '#ff1493',
    'deepskyblue': '#00bfff',
    'dimgray': '#696969',
    'dodgerblue': '#1e90ff',
    'firebrick': '#b22222',
    'floralwhite': '#fffaf0',
    'forestgreen': '#228b22',
    'fuchsia': '#ff00ff',
    'gainsboro': '#dcdcdc',
    'ghostwhite': '#f8f8ff',
    'gold': '#ffd700',
    'goldenrod': '#daa520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#adff2f',
    'honeydew': '#f0fff0',
    'hotpink': '#ff69b4',
    'indianred': '#cd5c5c',
    'indigo': '#4b0082',
    'ivory': '#fffff0',
    'khaki': '#f0e68c',
    'lavender': '#e6e6fa',
    'lavenderblush': '#fff0f5',
    'lawngreen': '#7cfc00',
    'lemonchiffon': '#fffacd',
    'lightblue': '#add8e6',
    'lightcoral': '#f08080',
    'lightcyan': '#e0ffff',
    'lightgoldenrodyellow': '#fafad2',
    'lightgreen': '#90ee90',
    'lightgrey': '#d3d3d3',
    'lightpink': '#ffb6c1',
    'lightsalmon': '#ffa07a',
    'lightseagreen': '#20b2aa',
    'lightskyblue': '#87cefa',
    'lightslategray': '#778899',
    'lightsteelblue': '#b0c4de',
    'lightyellow': '#ffffe0',
    'lime': '#00ff00',
    'limegreen': '#32cd32',
    'linen': '#faf0e6',
    'magenta': '#ff00ff',
    'maroon': '#800000',
    'mediumaquamarine': '#66cdaa',
    'mediumblue': '#0000cd',
    'mediumorchid': '#ba55d3',
    'mediumpurple': '#9370db',
    'mediumseagreen': '#3cb371',
    'mediumslateblue': '#7b68ee',
    'mediumspringgreen': '#00fa9a',
    'mediumturquoise': '#48d1cc',
    'mediumvioletred': '#c71585',
    'midnightblue': '#191970',
    'mintcream': '#f5fffa',
    'mistyrose': '#ffe4e1',
    'moccasin': '#ffe4b5',
    'navajowhite': '#ffdead',
    'navy': '#000080',
    'oldlace': '#fdf5e6',
    'olive': '#808000',
    'olivedrab': '#6b8e23',
    'orange': '#ffa500',
    'orangered': '#ff4500',
    'orchid': '#da70d6',
    'palegoldenrod': '#eee8aa',
    'palegreen': '#98fb98',
    'paleturquoise': '#afeeee',
    'palevioletred': '#db7093',
    'papayawhip': '#ffefd5',
    'peachpuff': '#ffdab9',
    'peru': '#cd853f',
    'pink': '#ffc0cb',
    'plum': '#dda0dd',
    'powderblue': '#b0e0e6',
    'purple': '#800080',
    'red': '#ff0000',
    'rosybrown': '#bc8f8f',
    'royalblue': '#4169e1',
    'saddlebrown': '#8b4513',
    'salmon': '#fa8072',
    'sandybrown': '#f4a460',
    'seagreen': '#2e8b57',
    'seashell': '#fff5ee',
    'sienna': '#a0522d',
    'silver': '#c0c0c0',
    'skyblue': '#87ceeb',
    'slateblue': '#6a5acd',
    'slategray': '#708090',
    'snow': '#fffafa',
    'springgreen': '#00ff7f',
    'steelblue': '#4682b4',
    'tan': '#d2b48c',
    'teal': '#008080',
    'thistle': '#d8bfd8',
    'tomato': '#ff6347',
    'turquoise': '#40e0d0',
    'violet': '#ee82ee',
    'wheat': '#f5deb3',
    'white': '#ffffff',
    'whitesmoke': '#f5f5f5',
    'yellow': '#ffff00',
    'yellowgreen': '#9acd32'
}

_default_xcss_vars = {
    # unsafe chars will be hidden as vars
    '$__doubleslash': '//',
    '$__bigcopen': '/*',
    '$__bigcclose': '*/',
    '$__doubledot': ':',
    '$__semicolon': ';',
    '$__curlybracketopen': '{',
    '$__curlybracketclosed': '}',

    # shortcuts (it's "a hidden feature" for now)
    'bg:': 'background:',
    'bgc:': 'background-color:',
}

_default_xcss_opts = {
    'verbosity': 0,
    'compress': 1,
    'short_colors': 0,
    'reverse_colors': 0,
}

_short_color_re = re.compile(r'(?<!\w)#([a-f0-9])\1([a-f0-9])\2([a-f0-9])\3\b', re.IGNORECASE)
_long_color_re = re.compile(r'(?<!\w)#([a-f0-9]){2}([a-f0-9]){2}([a-f0-9]){2}\b', re.IGNORECASE)
_reverse_colors = dict((v, k) for k, v in _colors.items())
for long_k, v in _colors.items():
    # Calculate the different possible representations of a color:
    short_k = _short_color_re.sub(r'#\1\2\3', v).lower()
    rgb_k = _long_color_re.sub(lambda m: 'rgb(%d, %d, %d)' % (int(m.group(1), 16), int(m.group(2), 16), int(m.group(3), 16)), v)
    rgba_k = _long_color_re.sub(lambda m: 'rgba(%d, %d, %d, 1)' % (int(m.group(1), 16), int(m.group(2), 16), int(m.group(3), 16)), v)
    # get the shortest of all to use it:
    k = min([short_k, long_k, rgb_k, rgba_k], key=len)
    _reverse_colors[long_k] = k
    _reverse_colors[short_k] = k
    _reverse_colors[rgb_k] = k
    _reverse_colors[rgba_k] = k
_reverse_colors_re = re.compile(r'(?<!\w)(' + '|'.join(map(re.escape, _reverse_colors))+r')\b', re.IGNORECASE)
_colors_re = re.compile(r'\b(' + '|'.join(map(re.escape, _colors))+r')\b', re.IGNORECASE)

_expr_simple_re = re.compile(r'''
    \#\{.*?\}                   # Global Interpolation only
''', re.VERBOSE)

#_expr_re = re.compile(r'''
#(?<=:)[^\{;}]+
#''', re.VERBOSE)

_expr_re = re.compile(r'''
    (?:^|(?<!\w))               # Expression should'nt have a word before it
    (?:
        (?:[\[\(\-]|\bnot\b)
        (?:[\[\(\s\-]+|\bnot\b)?
    )?                          # ...then any number of opening parenthesis or spaces
    (?:
        (['"]).*?\1             # If a string, consume the whole thing...
    |
        (?:
            \#[0-9a-fA-F]{6}    # Get an hex RGB
        |
            \#[0-9a-fA-F]{3}    # Get an hex RRGGBB
        |
            [\w.%$]+             # ...otherwise get the word, variable or number
        )
        (?:
            [\[\(]              # optionally, then start with a parenthesis
            .*?                 # followed by anything...
            [\]\)][\w%]*        # until it closes, then try to get any units
            [\]\)\s\,]*?        # ...and keep closing other parenthesis and parameters
        )?
    )
    (?:                         # Here comes the other expressions (0..n)
        [\]\)\s\,]*?
        (?:
            [+*/^,]             # Get accepted operators
        |
            (?<=\s)-(?=\s)      # ...minus operator needs spaces
        |
            (?<!\s)-            # or be preceded by a non-space
        |
            and | or
        |
            == | != | [<>]=?    # Other operators for comparisons
        )
        (?:[\[\(\s\-]+|\bnot\b)?
        (?:
            (['"]).*?\2         # If a string, consume the whole thing...
        |
            (?:
                \#[0-9a-fA-F]{6} # Get an hex RGB
            |
                \#[0-9a-fA-F]{3} # Get an hex RRGGBB
            |
                [\w.%$]+         # ...otherwise get the word, variable or number
            )
            (?:
                [\[\(]          # optionally, then  start with a parenthesis
                .*?             # followed by anything...
                [\]\)][\w%]*    # until it closes, then try to get any units
                [\]\)\s\,]*?    # ...and keep closing other parenthesis and parameters
            )?
        )
    )*
    [\]\)\s\,]*?                # ...keep closing parenthesis
    (?:[\]\)\,]+[\w%]*)?        # and then try to get any units afterwards
''', re.VERBOSE)

#_expr_re = re.compile(r'(\[.*?\])([\s;}]|$|.+?\S)') # <- This is the old method, required parenthesis around the expression
_ml_comment_re = re.compile(r'\/\*(.*?)\*\/', re.DOTALL)
_sl_comment_re = re.compile(r'(?<!\w{2}:)\/\/.*')
_zero_units_re = re.compile(r'\b0(' + '|'.join(map(re.escape, _units)) + r')(?!\w)', re.IGNORECASE)

_remove_decls_re = re.compile(r'(@option\b.*?([;}]|$))', re.DOTALL | re.IGNORECASE)
_spaces_re = re.compile(r'\s+')
_expand_rules_space_re = re.compile(r'\s*{')
_collapse_properties_space_re = re.compile(r'([:#])\s*{')

_reverse_default_xcss_vars = dict((v, k) for k, v in _default_xcss_vars.items())
_reverse_default_xcss_vars_re = re.compile(r'(content.*:.*(\'|").*)(' + '|'.join(map(re.escape, _reverse_default_xcss_vars)) + ')(.*\2)')

_blocks_re = re.compile(r'[{},;()\'"]|\n+')

_skip_word_re = re.compile('-?[\w\s#.,:%]*$|[\w\-#.,:%]*$', re.MULTILINE)
_has_code_re = re.compile('''(^|(?<=[{;}]))\s*(?:(\+|@include|@mixin|@if|@else|@for)(?![^(:;}]*['"])|@import)''')

FILEID = 0
POSITION = 1
CODESTR = 2
DEPS = 3
CONTEXT = 4
OPTIONS = 5
SELECTORS = 6
PROPERTIES = 7
PATH = 8

import time, sys
def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print >>sys.stderr, '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

class xCSS(object):
    # configuration:
    construct = 'self'
    short_colors = True
    reverse_colors = True

    def __init__(self):
        pass

    def longest_common_prefix(self, seq1, seq2):
        start = 0
        common = 0
        while start < min(len(seq1), len(seq2)):
            if seq1[start] != seq2[start]:
                break
            if seq1[start] == ' ':
                common = start + 1
            elif seq1[start] in ('#', ':', '.'):
                common = start
            start += 1
        return common

    def longest_common_suffix(self, seq1, seq2):
        return self.longest_common_prefix(seq1[::-1], seq2[::-1])

    def locate_blocks(self, str):
        """
        Returns all code blocks between `{` and `}` and a proper key
        that can be multilined as long as it's joined by `,` or enclosed in
        `(` and `)`.
        Returns the "lose" code that's not part of the block as a third item.
        """
        par = 0
        instr = None
        depth = 0
        skip = False
        thin = None
        i = init = safe = lose = 0
        start = end = None
        str_len = len(str)
        for m in _blocks_re.finditer(str):
            i = m.end(0) - 1
            if instr is not None:
                if str[i] == instr:
                    instr = None
            elif str[i] in ('"', "'"):
                instr = str[i]
            elif str[i] == '(':
                par += 1
                thin = None
                safe = i + 1
            elif str[i] == ')':
                par -= 1
            elif not par and not instr:
                if str[i] == '{':
                    if depth == 0:
                        if i > 0 and str[i-1] == '#':
                            skip = True
                        else:
                            start = i
                            if thin is not None and str[thin:i-1].strip():
                                init = thin
                            if lose < init:
                                losestr = str[lose:init].strip()
                                if losestr:
                                    yield None, None, str[lose:init]
                                lose = init
                            thin = None
                    depth += 1
                elif str[i] == '}':
                    if depth > 0:
                        depth -= 1
                        if depth == 0:
                            if not skip:
                                end = i
                                selectors = str[init:start].strip()
                                codestr = str[start+1:end].strip()
                                if selectors:
                                    yield selectors, codestr, None
                                init = safe = lose = end + 1
                                thin = None
                            skip = False
                elif depth == 0:
                    if str[i] == ';':
                        init = safe = i + 1
                        thin = None
                    elif str[i] == ',':
                        if thin is not None and str[thin:i-1].strip():
                            init = thin
                        thin = None
                        safe = i + 1
                    elif str[i] == '\n':
                        if thin is None and str[safe:i-1].strip():
                            thin = i + 1
                        elif thin is not None and str[thin:i-1].strip():
                            init = i + 1
                            thin = None
        yield None, None, str[lose:]

    def normalize_selectors(self, _selectors, extra_selectors=None, extra_parents=None):
        """
        Normalizes or extends selectors in a string.
        An optional extra parameter that can be a list of extra selectors to be
        added to the final normalized selectors string.
        """
        # Fixe tabs and spaces in selectors
        _selectors = _spaces_re.sub(' ', _selectors)

        if isinstance(extra_selectors, basestring):
            extra_selectors = extra_selectors.split(',')

        if isinstance(extra_parents, basestring):
            extra_parents = extra_parents.split('&')

        parents = set()
        if ' extends ' in _selectors:
            selectors = set()
            for key in _selectors.split(','):
                child, _, parent = key.partition(' extends ')
                child = child.strip()
                parent = parent.strip()
                selectors.add(child)
                parents.update(s.strip() for s in parent.split('&') if s.strip())
        else:
            selectors = set(s.strip() for s in _selectors.split(',') if s.strip())
        if extra_selectors:
            selectors.update(s.strip() for s in extra_selectors if s.strip())
        selectors.discard('')
        if not selectors:
            return ''
        if extra_parents:
            parents.update(s.strip() for s in extra_parents if s.strip())
        parents.discard('')
        if parents:
            return ','.join(sorted(selectors)) + ' extends ' + '&'.join(sorted(parents))
        return ','.join(sorted(selectors))


    def use_vars(self, cont, context=None, options=None):
        xcss_vars = self.xcss_vars.copy()
        xcss_vars.update(context or {})
        vars = xcss_vars.keys()
        try:
            remove_vars_re, interpolate_re = self._contexts[tuple(vars)]
        except KeyError:
            vars1 = []
            vars2 = []
            for var in vars:
                if var[0] == '$':
                    vars1.append(re.escape(var))
                else:
                    vars2.append(re.escape(var))
            remove_vars_re = re.compile(r'(?<![-\w])(((' + '|'.join(vars1) + r')\s*[:=]|(' + '|'.join(vars2) + r')\s*=).*?([;}]|$))')
            interpolate_re = re.compile(r'(?<![-\w])(' + '|'.join(map(re.escape, vars)) + r')(?![-\w])')
            self._contexts[tuple(vars)] = remove_vars_re, interpolate_re

        # remove variables declarations from the rules
        cont = _remove_decls_re.sub('', cont)
        cont = remove_vars_re.sub('', cont)

        cnt = 0
        old_cont = None
        while cont != old_cont and cnt < 5:
            cnt += 1
            old_cont = cont

            # interpolate variables:
            cont = interpolate_re.sub(lambda m: xcss_vars[m.group(0)], cont)

        return cont

    @print_timing
    def compile(self, input_xcss=None):
        # Initialize
        self.rules = []
        self._rules = {}
        self.parts = {}
        self.css_files = []
        self.xcss_vars = _default_xcss_vars.copy()
        self.xcss_opts = _default_xcss_opts.copy()

        self._contexts = {}
        self._replaces = {}

        if input_xcss is not None:
            self.xcss_files = {}
            self.xcss_files['string'] = input_xcss + '\n'
        self.xcss_files = self.xcss_files or {}

        # Compile
        for fileid, str in self.xcss_files.iteritems():
            self.parse_xcss_string(fileid, str)

        # this will manage xCSS rule: child objects inside of a node
        self.parse_children()

        # this will manage xCSS rule: ' extends '
        self.parse_extends()

        # this will manage the order of the rules
        self.manage_order()

        final_cont = ''
        for fileid in self.css_files:
            if fileid != 'string':
                final_cont += '/* Generated from: ' + fileid + ' */\n'
            fcont = self.create_css(fileid)
            final_cont += fcont

        final_cont = self.do_math(final_cont)
        final_cont = self.post_process(final_cont)

        return final_cont

    def load_string(self, str):
        # protects content: "..." strings
        str = _reverse_default_xcss_vars_re.sub(lambda m: m.group(0) + _reverse_default_xcss_vars.get(m.group(2)) + m.group(3), str)

        # removes multiple line comments
        str = _ml_comment_re.sub('', str)

        # removes inline comments, but not :// (protocol)
        str = _sl_comment_re.sub('', str)

        # expand the space in rules
        str = _expand_rules_space_re.sub(' {', str)

        # collapse the space in properties blocks
        str = _collapse_properties_space_re.sub(r'\1{', str)

        return str

    def parse_xcss_string(self, fileid, str):
        str = self.load_string(str)

        self.process_properties(str, self.xcss_vars, self.xcss_opts)

        # give each rule a new copy of the context and its options
        rule = [ fileid, len(self.rules), str, set(), self.xcss_vars, self.xcss_opts, '', None, None ]
        self.rules.append(rule)

    def process_properties(self, codestr, context, options, properties=None, scope=''):
        def _process_properties(codestr, scope):
            codes = [ s.strip() for s in codestr.split(';') if s.strip() ]
            for code in codes:
                if code[0] == '@':
                    code, name = (code.split(None, 1)+[''])[:2]
                    if code == '@options':
                        for option in name.split(','):
                            option, value = (option.split(':', 1)+[''])[:2]
                            option = option.strip().lower()
                            value = value.strip()
                            if option:
                                if value.lower() in ('1', 'true', 't', 'yes', 'y', 'on'):
                                    value = 1
                                elif value.lower() in ('0', 'false', 'f', 'no', 'n', 'off'):
                                    value = 0
                                options[option] = value
                    else:
                        options[code] = name
                else:
                    prop, value = (re.split(r'[:=]', code, 1) + [''])[:2]
                    try:
                        is_var = (code[len(prop)] == '=')
                    except IndexError:
                        is_var = False
                    prop = prop.strip()
                    if prop:
                        value = value.strip()
                        _prop = scope + prop
                        if is_var or prop[0] == '$':
                            if value:
                                context[_prop] = value
                        elif properties is not None and value:
                            properties.append((_prop, value))
        for p_selectors, p_codestr, lose in self.locate_blocks(codestr):
            if lose is not None:
                codestr = lose
                _process_properties(lose, scope)
            elif p_selectors[0] == '@':
                code, name = (p_selectors.split(None, 1)+[''])[:2]
                if code in ('@variables', '@vars'):
                    if name:
                        name =  name + '.' # namespace
                    _process_properties(p_codestr, scope + name)
            elif p_selectors[-1] == ':':
                self.process_properties(p_codestr, context, options, properties, scope + p_selectors[:-1] + '-')

    def parse_children(self):
        pos = 0
        while pos < len(self.rules):
            rule = self.rules[pos]
            if rule[POSITION] is not None:
                #print '='*80
                #for i, r in enumerate(self.rules): print '>' if i == pos else ' ', repr(r[POSITION]), repr(r[SELECTORS]), repr(r[CODESTR][:100]+'...')
                construct = self.construct
                _selectors, _, _parents = rule[SELECTORS].partition(' extends ')
                _selectors = _selectors.split(',')
                if _parents:
                    construct += ' extends ' + _parents # This passes the inheritance to 'self' children
                # Check if the block has nested blocks and work it out:
                if ' {' in rule[CODESTR] or _has_code_re.search(rule[CODESTR]):
                    # manage children or expand children:
                    self.manage_children(pos, rule, _selectors, construct)
            pos += 1

        # prepare maps:
        for pos, rule in enumerate(self.rules):
            if rule[POSITION] is not None:
                rule[POSITION] = pos
                selectors = rule[SELECTORS]
                self.parts.setdefault(selectors, [])
                self.parts[selectors].append(rule)

    def _insert_child(self, pos, rule, p_selectors, c_selectors, c_codestr, extra_context=None, path=None):
        better_selectors = set()
        c_selectors, _, c_parents = c_selectors.partition(' extends ')
        c_selectors = c_selectors.split(',')
        for c_selector in c_selectors:
            for p_selector in p_selectors:
                if c_selector == self.construct:
                    better_selectors.add(p_selector)
                elif '&' in c_selector: # Parent References
                    better_selectors.add(c_selector.replace('&', p_selector))
                elif p_selector:
                    better_selectors.add(p_selector + ' ' + c_selector)
                else:
                    better_selectors.add(c_selector)
        better_selectors = ','.join(sorted(better_selectors))
        if c_parents:
            better_selectors += ' extends ' + c_parents

        if c_selector == self.construct:
            # Context and options for constructors ('self') are the same as the parent
            _context = rule[CONTEXT]
            _options = rule[OPTIONS]
            _deps = rule[DEPS]
        else:
            _deps = set(rule[DEPS])
            _context = rule[CONTEXT].copy()
            _options = rule[OPTIONS].copy()
            _options.pop('@extend', None)
        _context.update(extra_context or {})

        self.process_properties(c_codestr, _context, _options)

        parents = _options.get('@extend')

        if parents:
            parents = parents.replace(',', '&') # @extend can come with comma separated selectors...
            if c_parents:
                better_selectors += '&' + parents
            else:
                better_selectors += ' extends ' + parents

        if '#{' in better_selectors or '$' in better_selectors:
            better_selectors = self.use_vars(better_selectors, _context, _options)
            better_selectors = self.do_math(better_selectors, _expr_simple_re)

        better_selectors = self.normalize_selectors(better_selectors)

        rule[POSITION] = None # Disable this old rule (perhaps it could simply be removed instead??)...
        # ...and insert new rule
        self.rules.insert(pos + 1, [ rule[FILEID], len(self.rules), c_codestr, _deps, _context, _options, better_selectors, None, path or rule[PATH] ])
        return pos + 1

    def manage_children(self, pos, rule, p_selectors, construct):
        fileid, position, codestr, deps, context, options, selectors, properties, path = rule

        rewind = False
        for c_selectors, c_codestr, lose in self.locate_blocks(codestr):
            if rewind:
                if lose is not None:
                    pos = self._insert_child(pos, rule, p_selectors, construct, lose)
                else:
                    pos = self._insert_child(pos, rule, p_selectors, construct, c_selectors + '{' + c_codestr + '}')
                c_selectors = None
            elif lose is not None:
                # This is either a raw lose rule...
                if '@include' in lose or '@import' in lose:
                    new_codestr = []
                    props = [ s.strip() for s in lose.split(';') if s.strip() ]
                    for prop in props:
                        if prop[0] == '+': # expands a '+' at the beginning of a rule as @include
                            code = '@include'
                            name = prop[1:]
                            try:
                                if '(' not in name or name.index(':') < name.index('('):
                                    name = name.replace(':', '(', 1)
                            except ValueError:
                                pass
                        else:
                            code, name = (prop.split(None, 1)+[''])[:2]
                        if rewind:
                            new_codestr.append(prop)
                        elif code == '@include':
                            # It's an @include, insert pending rules...
                            if new_codestr:
                                pos = self._insert_child(pos, rule, p_selectors, construct, ';'.join(new_codestr))
                                new_codestr = []
                            # ...then insert the include here:
                            funct, params = (name.split('(', 1)+[''])[:2]
                            params = params.rstrip(')')
                            params = params and params.split(',') or []
                            vars = {}
                            defaults = {}
                            new_params = []
                            for param in params:
                                param, _, default = param.partition(':')
                                param = param.strip()
                                default = default.strip()
                                if param:
                                    new_params.append(param)
                                    if default:
                                        defaults[param] = default.strip()
                            mixin = rule[OPTIONS].get('@mixin ' + funct + ':' + str(len(new_params)))
                            if mixin:
                                m_params = mixin[0]
                                m_vars = mixin[1].copy()
                                m_codestr = mixin[2]
                                for i, param in enumerate(new_params):
                                    if param in defaults:
                                        m_vars[m_params[i]] = defaults[param]
                                    m_vars[m_params[i]] = param
                                pos = self._insert_child(pos, rule, p_selectors, construct, m_codestr, m_vars)
                                rewind = True
                        elif code == '@import':
                            i_codestr = None
                            if name[0] in ('"', "'"):
                                name = name[1:-1]
                                name = unescape(name)
                            if '..' not in name:
                                try:
                                    filename = os.path.basename(name)
                                    dirname = os.path.join(rule[PATH] or SAAS_ROOT, os.path.dirname(name))
                                    i_codestr = open(os.path.join(dirname, '_'+filename+'.scss')).read()
                                except:
                                    try:
                                        dirname = os.path.join(SAAS_ROOT, os.path.dirname(name))
                                        i_codestr = open(os.path.join(dirname, '_'+filename+'.scss')).read()
                                    except:
                                        pass
                            if i_codestr:
                                i_codestr = self.load_string(i_codestr)
                                pos = self._insert_child(pos, rule, p_selectors, construct, i_codestr, None, dirname)
                                rewind = True
                            else:
                                print 'File not found:',os.path.join(dirname, '_'+filename+'.scss')
                                pass
                                #new_codestr.append(prop) #FIXME: if I remove the comment, the include is added as a new rule again and it loops
                        else:
                            new_codestr.append(prop)
                    if new_codestr:
                        pos = self._insert_child(pos, rule, p_selectors, construct, ';'.join(new_codestr))
                else:
                    pos = self._insert_child(pos, rule, p_selectors, construct, lose)
            elif c_selectors[-1] == ':':
                # ...it was a nested property or varialble, treat as raw
                pos = self._insert_child(pos, rule, p_selectors, construct, c_selectors + '{' + c_codestr + '}')
                c_selectors = None
            elif c_selectors[0] == '@':
                code, name = (c_selectors.split(None, 1)+[''])[:2]
                if code == '@if' or c_selectors.startswith('@else if '):
                    if code != '@if':
                        val = options.get('@if', True)
                        name = c_selectors[9:]
                    else:
                        val = True
                    if val:
                        name = self.use_vars(name, context, options)
                        name = self.do_math(name)
                        val = name and name.split()[0].lower()
                        val = bool(False if not val or val in('0', 'false',) else val)
                        options['@if'] = val
                        if val:
                            pos = self._insert_child(pos, rule, p_selectors, construct, c_codestr)
                    c_selectors = None
                elif code == '@else':
                    val = options.get('@if', True)
                    if not val:
                        pos = self._insert_child(pos, rule, p_selectors, construct, c_codestr)
                    c_selectors = None
                elif code == '@for':
                    var, _, name = name.partition('from')
                    name = self.use_vars(name, context, options)
                    name = self.do_math(name)
                    start, _, end = name.partition('through')
                    if not end:
                        start, _, end = start.partition('to')
                    var = var.strip()
                    try:
                        start = int(float(start.strip()))
                        end = int(float(end.strip()))
                    except ValueError:
                        pass
                    else:
                        for i in range(start, end + 1):
                            pos = self._insert_child(pos, rule, p_selectors, construct, c_codestr, { var: str(i) })
                    c_selectors = None
                elif code == '@mixin':
                    if name:
                        #print name
                        funct, _, params = name.partition('(')
                        funct = funct.strip()
                        params = params.strip('()').split(',')
                        vars = {}
                        defaults = {}
                        new_params = []
                        for param in params:
                            param, _, default = param.partition(':')
                            param = param.strip()
                            default = default.strip()
                            if param:
                                new_params.append(param)
                                if default:
                                    defaults[param] = default.strip()
                        if vars:
                            rename_vars_re = re.compile(r'(?<!\w)(' + '|'.join(map(re.escape, vars)) + r')(?!\w)')
                            c_codestr = rename_vars_re.sub(lambda m: vars[m.group(0)], c_codestr)
                        mixin = [ list(new_params), defaults, c_codestr ]
                        # Insert as many @mixin options as the default parameters:
                        while len(new_params):
                            options['@mixin ' + funct + ':' + str(len(new_params))] = mixin
                            param = new_params.pop()
                            if param not in defaults:
                                break
                        if not new_params:
                            options['@mixin ' + funct + ':0'] = mixin
                    c_selectors = None
                elif code == '@prototype':
                    c_selectors = name # prototype keyword simply ignored (all selectors are prototypes)
            if c_selectors:
                pos = self._insert_child(pos, rule, p_selectors, c_selectors, c_codestr)


    def link_with_parents(self, parent, c_selectors, c_rules):
        """
        Link with a parent for the current child rule.
        If parents found, returns a list of parent rules to the child
        """
        parent_found = None
        for p_selectors, p_rules in self.parts.items():
            _p_selectors, _, _ = p_selectors.partition(' extends ')
            _p_selectors = _p_selectors.split(',')

            new_selectors = set()
            found = False

            # Finds all the parent selectors and parent selectors with another
            # bind selectors behind. For example, if `.specialClass extends .baseClass`,
            # and there is a `.baseClass` selector, the extension should create
            # `.specialClass` for that rule, but if there's also a `.baseClass a`
            # it also should create `.specialClass a`
            for p_selector in _p_selectors:
                if parent in p_selector:
                    # get the new child selector to add (same as the parent selector but with the child name)
                    # since selectors can be together, separated with # or . (i.e. something.parent) check that too:
                    for c_selector in c_selectors.split(','):
                        # Get whatever is different between the two selectors:
                        lcp = self.longest_common_prefix(c_selector, p_selector)
                        if lcp: c_selector = c_selector[lcp:]
                        lcs = self.longest_common_suffix(c_selector, p_selector)
                        if lcs: c_selector = c_selector[:-lcs]
                        # Get the new selectors:
                        prev_symbol = r'(?<![-\w])' if parent[0] not in ('#', '.', ':') else ''
                        post_symbol = r'(?![-\w])'
                        new_parent = re.sub(prev_symbol + parent + post_symbol, c_selector, p_selector)
                        new_selectors.add(new_parent)
                        found = True

            if found:
                # add parent:
                parent_found = parent_found or []
                parent_found.extend(p_rules)

            if new_selectors:
                new_selectors = self.normalize_selectors(p_selectors, new_selectors)
                # rename node:
                if new_selectors != p_selectors:
                    del self.parts[p_selectors]
                    self.parts.setdefault(new_selectors, [])
                    self.parts[new_selectors].extend(p_rules)

                deps = set()
                # save child dependencies:
                for c_rule in c_rules or []:
                    c_rule[SELECTORS] = c_selectors # re-set the SELECTORS for the rules
                    deps.add(c_rule[POSITION])

                for p_rule in p_rules:
                    p_rule[SELECTORS] = new_selectors # re-set the SELECTORS for the rules
                    p_rule[DEPS].update(deps) # position is the "index" of the object

        return parent_found

    def parse_extends(self):
        """
        For each part, create the inheritance parts from the ' extends '
        """
        # To be able to manage multiple extends, you need to
        # destroy the actual node and create many nodes that have
        # mono extend. The first one gets all the css rules
        for _selectors, rules in self.parts.items():
            if ' extends ' in _selectors:
                selectors, _, parent = _selectors.partition(' extends ')
                parents = parent.split('&')
                del self.parts[_selectors]
                for parent in parents:
                    new_selectors = selectors + ' extends ' + parent
                    self.parts.setdefault(new_selectors, [])
                    self.parts[new_selectors].extend(rules)
                    rules = [] # further rules extending other parents will be empty

        cnt = 0
        parents_left = True
        while parents_left and cnt < 10:
            cnt += 1
            parents_left = False
            for _selectors in self.parts.keys():
                selectors, _, parent = _selectors.partition(' extends ')
                if parent:
                    parents_left = True
                    if _selectors not in self.parts:
                        continue # Nodes might have been renamed while linking parents...

                    rules = self.parts[_selectors]

                    del self.parts[_selectors]
                    self.parts.setdefault(selectors, [])
                    self.parts[selectors].extend(rules)

                    parents = self.link_with_parents(parent, selectors, rules)

                    assert parents is not None, "Parent not found: %s (%s)" % (parent, selectors)

                    # from the parent, inherit the context and the options:
                    new_context = {}
                    new_options = {}
                    for parent in parents:
                        new_context.update(parent[CONTEXT])
                        new_options.update(parent[OPTIONS])
                    for rule in rules:
                        _new_context = new_context.copy()
                        _new_context.update(rule[CONTEXT])
                        rule[CONTEXT] = _new_context
                        _new_options = new_options.copy()
                        _new_options.update(rule[OPTIONS])
                        rule[OPTIONS] = _new_options

    def manage_order(self):
        # order rules according with their dependencies
        for rule in self.rules:
            if rule[POSITION] is not None:
                rule[DEPS].add(rule[POSITION]+1)
                # This moves the rules just above the topmost dependency during the sorted() below:
                rule[POSITION] = min(rule[DEPS])
        self.rules = sorted(self.rules, key=lambda o: o[POSITION])

        self.css_files = []
        self._rules = {}
        css_files = set()
        old_fileid = None
        for rule in self.rules:
            fileid, position, codestr, deps, context, options, selectors, properties, path = rule
            #print >>sys.stderr, fileid, position, [ c for c in context if c[1] != '_' ], options.keys(), selectors, deps
            if position is not None:
                self._rules.setdefault(fileid, [])
                self._rules[fileid].append(rule)
                if '#{' in codestr or '$' in codestr:
                    codestr = self.use_vars(codestr, context, options)
                    codestr = self.do_math(codestr, _expr_simple_re)
                rule[PROPERTIES] = properties = []
                self.process_properties(codestr, context, options, properties)
                if properties:
                    if old_fileid != fileid:
                        old_fileid = fileid
                        if fileid not in css_files:
                            css_files.add(fileid)
                            self.css_files.append(fileid)

    def create_css(self, fileid=None):
        """
        Generate the final CSS string
        """
        result = ''
        if fileid:
            rules = self._rules.get(fileid) or []
        else:
            rules = self.rules

        compress = self.xcss_opts.get('compress', 1)
        if compress:
            sc = False
            sp = ''
            tb = ''
            nl = ''
        else:
            sc = True
            sp = ' '
            tb = '\t'
            nl = '\n'

        scope = set()
        open = False
        old_selectors = None
        for rule in rules:
            fileid, position, codestr, deps, context, options, selectors, properties, path = rule
            #print >>sys.stderr, fileid, position, [ c for c in context if c[1] != '_' ], options.keys(), selectors, deps
            if position is not None and properties:
                if old_selectors != selectors:
                    if open:
                        if not sc:
                            if result[-1] == ';':
                                result = result [:-1]
                        result += '}' + nl + nl
                    # feel free to modifie the indentations the way you like it
                    selector = (',' + nl).join(selectors.split(',')) + sp + '{' + nl
                    result += selector
                    old_selectors = selectors
                    open = True
                    scope = set()
                if not compress and options.get('verbosity', 0) > 0:
                    result += tb + '/* file: ' + fileid + ' */' + nl
                    if context:
                        result += tb + '/* vars:' + nl
                        for k, v in context.items():
                            result += tb + tb + k + ' = ' + v + ';' + nl
                        result += tb + '*/' + nl
                for prop, value in properties:
                    if '!default' in value:
                        value = value.replace('!default', '').strip()
                        if prop in scope:
                            continue
                    scope.add(prop)
                    property = tb + prop + ':' + sp + value + ';' + nl
                    result += property
        if open:
            if not sc:
                if result[-1] == ';':
                    result = result [:-1]
            result += '}' + nl
        return result + '\n'


    def do_math(self, content, _expr_re=_expr_re):
        def calculate(result):
            _base_str = result.group(0)

            if _skip_word_re.match(_base_str) or _base_str.startswith('url('):
                if ' and ' not in _base_str and ' or ' not in _base_str and 'not ' not in _base_str:
                    return _base_str

            try:
                better_expr_str = self._replaces[_base_str]
            except KeyError:
                better_expr_str = _base_str

                # If we are in a global variable, we remove
                if better_expr_str[:2] == '#{' and better_expr_str[-1] == '}':
                    better_expr_str = better_expr_str[2:-1]

                # To do math operations, we need to get the color's hex values (for color names)
                # ...also we change brackets to parenthesis:
                better_expr_str = _colors_re.sub(lambda m: _colors.get(m.group(0), m.group(0)), better_expr_str).replace('[', '(').replace(']', ')')

                try:
                    better_expr_str = eval_expr(better_expr_str)
                except ParseException:
                    better_expr_str = _base_str # leave untouched otherwise
                except:
                    better_expr_str = _base_str # leave untouched otherwise
                    #raise

                self._replaces[_base_str] = better_expr_str
            return better_expr_str

        #print >>sys.stderr, _expr_re.findall(content)
        content = _expr_re.sub(calculate, content)
        return content

    def post_process(self, cont):
        # short colors:
        if self.xcss_opts.get('short_colors', 0):
            cont = _short_color_re.sub(r'#\1\2\3', cont)
        # color names:
        if self.xcss_opts.get('reverse_colors', 0):
            cont = _reverse_colors_re.sub(lambda m: _reverse_colors[m.group(0).lower()], cont)
        # zero units out (i.e. 0px or 0em -> 0):
        cont = _zero_units_re.sub('0', cont)
        return cont

import os
import hashlib
import base64
import time
import datetime
import mimetypes
import glob
import math
import operator
import colorsys
from pyparsing import *
ParserElement.enablePackrat()

try:
    from PIL import Image
except ImportError:
    Image = None

################################################################################

def to_str(num):
    if isinstance(num, float):
        return ('%0.03f' % num).rstrip('0').rstrip('.')
    elif isinstance(num, bool):
        return 'true' if num else 'false'
    elif num is None:
        return ''
    return str(num)

def to_float(num):
    if isinstance(num, (float, int)):
        return float(num)
    num = to_str(num)
    try:
        if num and num[-1] == '%':
            return float(num[:-1]) / 100.0
        else:
            return float(num)
    except ValueError:
        return 0.0

hex2rgba = {
    9: lambda c: (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), int(c[7:9], 16)),
    7: lambda c: (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 1.0),
    5: lambda c: (int(c[1]*2, 16), int(c[2]*2, 16), int(c[3]*2, 16), int(c[4]*2, 16)),
    4: lambda c: (int(c[1]*2, 16), int(c[2]*2, 16), int(c[3]*2, 16), 1.0),
}

def escape(str):
    return re.sub(r'(["\'\\])', '\\\\\g<1>', str)

def unescape(str):
    return re.sub(re.escape('\\')+'(.)', "\g<1>", str)


def _rgb(r, g, b, type='rgb'):
    return _rgba(r, g, b, 1.0, type)

def _rgba(r, g, b, a, type='rgba'):
    c = NumberValue(r), NumberValue(g), NumberValue(b), NumberValue(a)

    col = [ c[i].value * 255.0 if (c[i].unit == '%' or c[i].value > 0 and c[i].value <= 1) else
            0.0 if c[i].value < 0 else
            255.0 if c[i].value > 255 else
            c[i].value
            for i in range(3)
          ]
    col += [ 0.0 if c[3].value < 0 else 1.0 if c[3].value > 1 else c[3].value ]
    col += [ type ]
    return ColorValue(col)

def _hsl(h, s, l, type='hsl'):
    return _hsla(h, s, l, 1.0, type)

def _hsla(h, s, l, a, type='hsla'):
    c = NumberValue(h), NumberValue(s), NumberValue(l), NumberValue(a)
    col = [ c[0] if (c[0].unit == '%' or c[0].value > 0 and c[0].value <= 1) else (c[0].value % 360.0) / 360.0 ]
    col += [ c[i].value if (c[i].unit == '%' or c[i].value > 0 and c[i].value <= 1) else
            0.0 if c[i].value < 0 else
            1.0 if c[i].value > 1 else
            c[i].value / 255.0
            for i in range(1, 4)
          ]
    col += [ type ]
    col = ColorValue(tuple([ c * 255.0 for c in colorsys.hls_to_rgb(col[0], col[2], col[1]) ] + [ col[3], type ]))
    return col

def __rgba_add(color, r, g, b, a):
    color = ColorValue(color)
    c = color.value
    a = r, g, b, a
    r = 255.0, 255.0, 255.0, 1.0
    c = [ c[i] + a[i] for i in range(4) ]
    c = [ 0.0 if c[i] < 0 else r[i] if c[i] > r[i] else c[i] for i in range(4) ]
    color.value = tuple(c)
    return color

def _opacify(color, amount):
    a = NumberValue(amount).value
    return __rgba_add(color, 0, 0, 0, a)

def _transparentize(color, amount):
    a = NumberValue(amount).value
    return __rgba_add(color, 0, 0, 0, -a)

def __hsl_add(color, h, s, l):
    color = ColorValue(color)
    c = color.value
    a = h / 360.0, s, l
    h, l, s = list(colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0))
    c = h, s, l
    c = [ 0.0 if c[i] < 0 else 1.0 if c[i] > 1 else c[i] + a[i] for i in range(3) ]
    c = colorsys.hls_to_rgb(((c[0] * 360.0) % 360) / 360.0, c[2], c[1])
    color.value = (c[0] * 255.0, c[1] * 255.0, c[2] * 255.0, color.value[3])
    return color

def _lighten(color, amount):
    a = NumberValue(amount).value
    return __hsl_add(color, 0, 0, a)

def _darken(color, amount):
    a = NumberValue(amount).value
    return __hsl_add(color, 0, 0, -a)

def _saturate(color, amount):
    a = NumberValue(amount).value
    return __hsl_add(color, 0, a, 0)

def _desaturate(color, amount):
    a = NumberValue(amount).value
    return __hsl_add(color, 0, -a, 0)

def _grayscale(color):
    return __hsl_add(color, 0, -1.0, 0)

def _adjust_hue(color, degrees):
    d = NumberValue(degrees).value
    return __hsl_add(color, d, 0, 0)

def _complement(color):
    return __hsl_add(color, 180.0, 0, 0)


def _mix(color1, color2, weight=None):
    """
    Mixes together two colors. Specifically, takes the average of each of the
    RGB components, optionally weighted by the given percentage.
    The opacity of the colors is also considered when weighting the components.

    Specifically, takes the average of each of the RGB components,
    optionally weighted by the given percentage.
    The opacity of the colors is also considered when weighting the components.

    The weight specifies the amount of the first color that should be included
    in the returned color.
    50%, means that half the first color
        and half the second color should be used.
    25% means that a quarter of the first color
        and three quarters of the second color should be used.

    For example:

        mix(#f00, #00f) => #7f007f
        mix(#f00, #00f, 25%) => #3f00bf
        mix(rgba(255, 0, 0, 0.5), #00f) => rgba(63, 0, 191, 0.75)

    """
    # This algorithm factors in both the user-provided weight
    # and the difference between the alpha values of the two colors
    # to decide how to perform the weighted average of the two RGB values.
    #
    # It works by first normalizing both parameters to be within [-1, 1],
    # where 1 indicates "only use color1", -1 indicates "only use color 0",
    # and all values in between indicated a proportionately weighted average.
    #
    # Once we have the normalized variables w and a,
    # we apply the formula (w + a)/(1 + w*a)
    # to get the combined weight (in [-1, 1]) of color1.
    # This formula has two especially nice properties:
    #
    #   * When either w or a are -1 or 1, the combined weight is also that number
    #     (cases where w * a == -1 are undefined, and handled as a special case).
    #
    #   * When a is 0, the combined weight is w, and vice versa
    #
    # Finally, the weight of color1 is renormalized to be within [0, 1]
    # and the weight of color2 is given by 1 minus the weight of color1.
    #
    # Algorithm from the Sass project: http://sass-lang.com/

    c1 = ColorValue(color1).value
    c2 = ColorValue(color2).value
    p = NumberValue(weight).value if weight is not None else 0.5
    p = 0.0 if p < 0 else 1.0 if p > 1 else p

    w = p * 2 - 1
    a = c1[3] - c2[3]

    w1 = ((w if (w * a == -1) else (w + a) / (1 + w * a)) + 1) / 2.0

    w2 = 1 - w1
    q = [ w1, w1, w1, p ]
    r = [ w2, w2, w2, 1 - p ]

    color = ColorValue(None).merge(c1).merge(c2)
    color.value = [ c1[i] * q[i] + c2[i] * r[i] for i in range(4) ]

    return color

def _red(color):
    c = ColorValue(color).value
    return NumberValue(c[0])
def _green(color):
    c = ColorValue(color).value
    return NumberValue(c[1])
def _blue(color):
    c = ColorValue(color).value
    return NumberValue(c[2])
def _alpha(color):
    c = ColorValue(color).value
    return NumberValue(c[3])

def _hue(color):
    c = ColorValue(color).value
    h, l, s = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    ret = NumberValue(h * 360.0)
    return ret
def _saturation(color):
    c = ColorValue(color).value
    h, l, s = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    ret = NumberValue(s)
    ret.units['%'] = 1
    return ret
def _lightness(color):
    c = ColorValue(color).value
    h, l, s = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    ret = NumberValue(l)
    ret.units['%'] = 1
    return ret

################################################################################
# Compass like functionality for sprites and images:
sprite_maps = {}
def _sprite_map(g, *args):
    """
    Generates a sprite map from the files matching the glob pattern.
    Uses the keyword-style arguments passed in to control the placement.
    """
    g = StringValue(g).value

    if not Image:
        raise Exception("Images manipulation require PIL")

    if g in sprite_maps:
        sprite_maps[glob]['_'] = datetime.datetime.now()
    else:
        gutter = 0
        offset_x = 0
        offset_y = 0
        repeat = 'no-repeat'

        files = sorted(glob.glob(MEDIA_ROOT + g))

        if not files:
            return StringValue(None)

        times = [ int(os.path.getmtime(file)) for file in files ]

        key = files + times + [ gutter, offset_x, offset_y, repeat ]
        key = base64.urlsafe_b64encode(hashlib.md5(repr(key)).digest()).rstrip('=').replace('-', '_')
        asset_file = key + '.png'
        asset_path = ASSETS_ROOT + asset_file

        images = tuple( Image.open(file) for file in files )
        names = tuple( os.path.splitext(os.path.basename(file))[0] for file in files )
        files = tuple( file[len(MEDIA_ROOT):] for file in files )
        sizes = tuple( image.size for image in images )
        offsets = []

        if os.path.exists(asset_path):
            filetime = int(os.path.getmtime(asset_path))
            offset = gutter
            for i, image in enumerate(images):
                offsets.append(offset - gutter)
                offset += sizes[i][0] + gutter * 2
        else:

            width = sum(zip(*sizes)[0]) + gutter * len(files) * 2
            height = max(zip(*sizes)[1]) + gutter * 2

            new_image = Image.new(
                mode = 'RGBA',
                size = (width, height),
                color = (0, 0, 0, 0)
            )

            offset = gutter
            for i, image in enumerate(images):
                new_image.paste(image, (offset, gutter))
                offsets.append(offset - gutter)
                offset += sizes[i][0] + gutter * 2

            new_image.save(asset_path)
            filetime = int(time.mktime(datetime.datetime.now().timetuple()))

        url = '%s%s?_=%s' % (MEDIA_URL, asset_file, filetime)
        asset = "url('%s') %dpx %dpx %s" % (escape(url), int(offset_x), int(offset_y), repeat)
        # Use the sorted list to remove older elements (keep only 500 objects):
        if len(sprite_maps) > 1000:
            for a in sorted(sprite_maps, key=lambda a: sprite_maps[a]['_'], reverse=True)[500:]:
                del sprite_maps[a]
        # Add the new object:
        sprite_maps[asset] = dict(zip(names, zip(sizes, files, offsets)))
        sprite_maps[asset]['_'] = datetime.datetime.now()
        sprite_maps[asset]['_f_'] = asset_file
        sprite_maps[asset]['_k_'] = key
        sprite_maps[asset]['_t_'] = filetime
    return StringValue(asset)

def _sprite_map_name(_map):
    """
    Returns the name of a sprite map The name is derived from the folder than
    contains the sprites.
    """
    map = StringValue(map).value
    sprite_map = sprite_maps.get(map, {})
    if sprite_map:
        return StringValue(sprite_map['_k_'])
    return StringValue(None)

def _sprite_file(map, sprite):
    """
    Returns the relative path (from the images directory) to the original file
    used when construction the sprite. This is suitable for passing to the
    image_width and image_height helpers.
    """
    map = StringValue(map).value
    sprite = StringValue(sprite).value
    sprite = sprite_maps.get(map, {}).get(sprite)
    if sprite:
        return StringValue(sprite[1])
    return StringValue(None)

def _sprite(map, sprite, offset_x=None, offset_y=None):
    """
    Returns the image and background position for use in a single shorthand
    property
    """
    map = StringValue(map).value
    sprite = StringValue(sprite).value
    sprite_map = sprite_maps.get(map, {})
    sprite = sprite_map.get(sprite)
    if sprite:
        url = '%s%s?_=%s' % (ASSETS_URL, sprite_map['_f_'], sprite_map['_t_'])
        offset_x = NumberValue(offset_x).value or 0
        offset_y = NumberValue(offset_y).value or 0
        pos = "url('%s') %dpx %dpx" % (escape(url), int(offset_x - sprite[2]), int(offset_y))
        return StringValue(pos)
    return StringValue('0 0')

def _sprite_url(map):
    """
    Returns a url to the sprite image.
    """
    map = StringValue(map).value
    if map in sprite_maps:
        sprite_map = sprite_maps[map]
        url = '%s%s?_=%s' % (ASSETS_URL, sprite_map['_f_'], sprite_map['_t_'])
        return StringValue(url)
    return StringValue(None)

def _sprite_position(map, sprite, offset_x=None, offset_y=None):
    """
    Returns the position for the original image in the sprite.
    This is suitable for use as a value to background-position.
    """
    map = StringValue(map).value
    sprite = StringValue(sprite).value
    sprite = sprite_maps.get(map, {}).get(sprite)
    if sprite:
        offset_x = NumberValue(offset_x).value or 0
        offset_y = NumberValue(offset_y).value or 0
        pos = '%dpx %dpx' % (int(offset_x - sprite[2]), int(offset_y))
        return StringValue(pos)
    return StringValue('0 0')

def _inline_image(image, mime_type=None):
    """
    Embeds the contents of a file directly inside your stylesheet, eliminating
    the need for another HTTP request. For small files such images or fonts,
    this can be a performance benefit at the cost of a larger generated CSS
    file.
    """
    image = StringValue(image).value
    file = MEDIA_ROOT+image
    if os.path.exists(file):
        mime_type = StringValue(mime_type).value or mimetypes.guess_type(file)[0]
        file = open(file, 'rb')
        url = 'data:'+_mime_type+';base64,'+base64.b64encode(file.read())
        inline = "url('%s')" % escape(url)
        return StringValue(inline)
    return StringValue(None)

def _image_url(image):
    """
    Generates a path to an asset found relative to the project's images
    directory.
    """
    file = StringValue(image).value
    path = MEDIA_ROOT + file
    if os.path.exists(path):
        filetime = int(os.path.getmtime(path))
        url = '%s%s?_=%s' % (MEDIA_URL, file, filetime)
        return StringValue(url)
    return StringValue(None)

def _image_width(image):
    """
    Returns the width of the image found at the path supplied by `image`
    relative to your project's images directory.
    """
    if not Image:
        raise Exception("Images manipulation require PIL")
    file = StringValue(image).value
    path = MEDIA_ROOT + file
    if os.path.exists(path):
        image = Image.open(path)
        width = image.size[0]
        ret = NumberValue(width)
        ret.units['px'] = 1
        return ret
    ret = NumberValue(0)
    ret.units['px'] = 1
    return ret

def _image_height(image):
    """
    Returns the height of the image found at the path supplied by `image`
    relative to your project's images directory.
    """
    if not Image:
        raise Exception("Images manipulation require PIL")
    file = StringValue(image).value
    path = MEDIA_ROOT + file
    if os.path.exists(path):
        image = Image.open(path)
        height = image.size[1]
        ret = NumberValue(height)
        ret.units['px'] = 1
        return ret
    ret = NumberValue(0)
    ret.units['px'] = 1
    return ret

################################################################################

def _nth(s, n=None):
    """
    Return the Nth item in the string
    """
    s = StringValue(s)
    n = NumberValue(n).value
    val = s.value
    try:
        s.value = val.split()[int(n) - 1]
    except IndexError:
        pass
    return s

def _percentage(value):
    value = NumberValue(value)
    value.units.clear()
    value.units['%'] = 1
    return value

def _unitless(value):
    value = NumberValue(value)
    value.units.clear()
    return value

def _unquote(s):
    return StringValue(s)

def _quote(s):
    return QuotedStringValue(s)

def _pi():
    return NumberValue(math.pi)

def _convert_to(value, type):
    return value.convert_to(type)

def _inv(value):
    if isinstance(value, NumberValue):
        return value * -1
    return '-' + StringValue(value)

def _and(a, b):
    return a and b
def _or(a, b):
    return a or b
def _not(a):
    return not a

class Value(object):
    def __init__(self, tokens):
        self.value = tokens[0]
        self.tokens = tokens
    @staticmethod
    def _operatorOperands(tokenlist):
        "generator to extract operators and operands in pairs"
        it = iter(tokenlist)
        while 1:
            try:
                yield (it.next(), it.next())
            except StopIteration:
                break
    @staticmethod
    def _merge_type(a, b):
        if a.__class__ == b.__class__:
            return a.__class__
        if isinstance(a, QuotedStringValue) or isinstance(b, QuotedStringValue):
            return QuotedStringValue
        return StringValue
    @staticmethod
    def _wrap(fn):
        """
        Wrapper function to allow calling any function
        using Value objects as parameters.
        """
        def _func(*args):
            merged = None
            _args = []
            for arg in args:
                if merged.__class__ != arg.__class__:
                    if merged is None:
                        merged = arg.__class__(None)
                    else:
                        merged = Value._merge_type(merged, arg)(None)
                merged.merge(arg)
                if isinstance(arg, Value):
                    arg = arg.value
                _args.append(arg)
            ret = merged.value = fn(*_args)
            return merged
        return _func
    @classmethod
    def _do_bitops(cls, first, second, op):
        first = StringValue(first)
        second = StringValue(second)
        k = op(first.value, second.value)
        return first if first.value == k else second
    def __repr__(self):
        return '<%s: %s: %s>' % (self.__class__.__name__, repr(self.value), repr(self.tokens))
    def __lt__(self, other):
        return self._do_cmps(self, other, operator.__lt__)
    def __le__(self, other):
        return self._do_cmps(self, other, operator.__le__)
    def __eq__(self, other):
        return self._do_cmps(self, other, operator.__eq__)
    def __ne__(self, other):
        return self._do_cmps(self, other, operator.__ne__)
    def __gt__(self, other):
        return self._do_cmps(self, other, operator.__gt__)
    def __ge__(self, other):
        return self._do_cmps(self, other, operator.__ge__)
    def __cmp__(self, other):
        return self._do_cmps(self, other, operator.__cmp__)
    def __rcmp__(self, other):
        return self._do_cmps(other, self, operator.__cmp__)
    def __and__(self, other):
        return self._do_bitops(self, other, operator.__and__)
    def __or__(self, other):
        return self._do_bitops(self, other, operator.__or__)
    def __xor__(self, other):
        return self._do_bitops(self, other, operator.__xor__)
    def __rand__(self, other):
        return self._do_bitops(other, self, operator.__rand__)
    def __ror__(self, other):
        return self._do_bitops(other, self, operator.__ror__)
    def __rxor__(self, other):
        return self._do_bitops(other, self, operator.__rxor__)
    def __nonzero__(self):
        return self.value and True or False
    def __add__(self, other):
        return self._do_op(self, other, operator.__add__)
    __radd__ = __add__
    def __div__(self, other):
        return self._do_op(self, other, operator.__div__)
    def __rdiv__(self, other):
        return self._do_op(other, self, operator.__div__)
    def __sub__(self, other):
        return self._do_op(self, other, operator.__sub__)
    def __rsub__(self, other):
        return self._do_op(other, self, operator.__sub__)
    def __mul__(self, other):
        return self._do_op(self, other, operator.__mul__)
    __rmul__ = __mul__
    def convert_to(self, type):
        return self.value.convert_to(type)
    def merge(self, obj):
        if isinstance(obj, Value):
            self.value = obj.value
        else:
            self.value = obj
        return self
    def eval(self, context):
        return self

class BooleanValue(Value):
    def __init__(self, tokens):
        self.tokens = tokens
        if tokens is None:
            self.value = False
        elif isinstance(tokens, ParseResults):
            self.value = tokens[0].lower() in ('true', '1', 'on', 'yes', 't', 'y')
        elif isinstance(tokens, BooleanValue):
            self.value = tokens.value
        elif isinstance(tokens, NumberValue):
            self.value = bool(tokens.value)
        elif isinstance(tokens, (float, int)):
            self.value = bool(tokens)
        else:
            self.value = to_str(tokens).lower() in ('true', '1', 'on', 'yes', 't', 'y')
    def __str__(self):
        return 'true' if self.value else 'false'
    @classmethod
    def _do_cmps(cls, first, second, op):
        first = BooleanValue(first)
        second = BooleanValue(second)
        return op(first.value, second.value)
    @classmethod
    def _do_op(cls, first, second, op):
        first = BooleanValue(first)
        second = BooleanValue(second)
        val = op(first.value, second.value)
        ret = BooleanValue(None).merge(first).merge(second)
        ret.value = val
        return ret
    def merge(self, obj):
        obj = BooleanValue(obj)
        self.value = obj.value
        return self

class NumberValue(Value):
    def __init__(self, tokens):
        self.tokens = tokens
        self.units = {}
        if tokens is None:
            self.value = 0.0
        elif isinstance(tokens, ParseResults):
            self.value = float(tokens[0])
        elif isinstance(tokens, NumberValue):
            self.value = tokens.value
            self.units = tokens.units.copy()
        elif isinstance(tokens, StringValue):
            try:
                if tokens.value and tokens.value[-1] == '%':
                    self.value = to_float(tokens.value[:-1]) / 100.0
                else:
                    self.value = to_float(tokens.value)
            except ValueError:
                self.value = 0.0
        elif isinstance(tokens, (int, float)):
            self.value = float(tokens)
        else:
            try:
                self.value = to_float(to_str(tokens))
            except ValueError:
                self.value = 0.0
    def q__repr__(self):
        return '<%s: %s, %s>' % (self.__class__.__name__, repr(self.value), repr(self.units))
    def __str__(self):
        unit = self.unit
        val = self.value / _conv_factor.get(unit, 1.0)
        val = to_str(val) + unit
        return val
    @classmethod
    def _do_cmps(cls, first, second, op):
        first = NumberValue(first)
        second = NumberValue(second)
        first_type = _conv_type.get(first.unit)
        second_type = _conv_type.get(second.unit)
        if first_type == second_type or first_type is None or second_type is None:
            return op(first.value, second.value)
        else:
            return op(first_type, second_type)
    @classmethod
    def _do_op(cls, first, second, op):
        first = NumberValue(first)
        second = NumberValue(second)
        first_unit = first.unit
        second_unit = second.unit
        if first_unit == '%' and not second_unit:
            second.units['%'] = 1
            second.value /= 100.0
        elif second_unit == '%' and not first_unit:
            first.units['%'] = 1
            first.value /= 100.0
        val = op(first.value, second.value)
        ret = NumberValue(None).merge(first).merge(second)
        ret. value = val
        return ret
    def merge(self, obj):
        obj = NumberValue(obj)
        self.value = obj.value
        for unit, val in obj.units.items():
            self.units.setdefault(unit, 0)
            self.units[unit] += val
        return self
    def convert_to(self, type):
        val = self.value
        if not self.unit:
            val *= _conv_factor.get(type, 1.0)
        ret = NumberValue(val)
        ret.units[type] = 1
        return ret
    @property
    def unit(self):
        unit = ''
        if self.units:
            units = sorted(self.units, key=self.units.get)
            while len(units):
                unit = units.pop()
                if unit and unit != '%':
                    break
            if not unit and '%' in self.units:
                unit = '%'
        return unit

class ColorValue(Value):
    def __init__(self, tokens):
        self.tokens = tokens
        self.types = {}
        self.value = (0, 0, 0, 1)
        if tokens is None:
            self.value = (0, 0, 0, 1)
        elif isinstance(tokens, ParseResults):
            hex = tokens[0]
            self.value = hex2rgba[len(hex)](hex)
            self.types = { 'rgba': 1 }
        elif isinstance(tokens, ColorValue):
            self.value = tokens.value
            self.types = tokens.types.copy()
        elif isinstance(tokens, NumberValue):
            val = tokens.value
            self.value = (val, val, val, 1)
        elif isinstance(tokens, (list, tuple)):
            self.value = tuple(tokens[:4])
            type = tokens[-1]
            if type in ('rgb', 'rgba', 'hsl', 'hsla'):
                self.types = { type: 1 }
        elif isinstance(tokens, (int, float)):
            val = float(tokens)
            self.value = (val, val, val, 1)
        else:
            hex = to_str(tokens)
            try:
                self.value = hex2rgba[len(hex)](hex)
            except:
                try:
                    val = to_float(hex)
                    self.values = (val, val, val, 1)
                except ValueError:
                    try:
                        hex.replace(' ', '').lower()
                        type, _, colors = hex.pertition('(').rstrip(')')
                        if type in ('rgb', 'rgba'):
                            c = tuple(colors.split(','))
                            try:
                                c = [ to_float(c[i]) for i in range(4) ]
                                col = [ 0.0 if c[i] < 0 else 255.0 if c[i] > 255 else c[i] for i in range(3) ]
                                col += [ 0.0 if c[3] < 0 else 1.0 if c[3] > 1 else c[3] ]
                                self.value = tuple(col)
                                self.types = { type: 1 }
                            except:
                                pass
                        if type in ('hsl', 'hsla'):
                            c = colors.split(',')
                            try:
                                c = [ to_float(c[i]) for i in range(4) ]
                                col = [ c[0] % 360.0 ] / 360.0
                                col += [ 0.0 if c[i] < 0 else 1.0 if c[i] > 1 else c[i] for i in range(1,4) ]
                                self.value = tuple([ c * 255.0 for c in colorsys.hls_to_rgb(col[0], col[2], col[1]) ] + [ col[3] ])
                                self.types = { type: 1 }
                            except:
                                pass
                    except:
                        pass

    def convert_to(self, type):
        return self
    def q__repr__(self):
        return '<%s: %s, %s>' % (self.__class__.__name__, repr(self.value), repr(self.types))
    def __str__(self):
        type = self.type
        c = self.value
        if type == 'hsl' or type == 'hsla' and c[3] == 1:
            h, l, s = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
            return 'hsl(%s, %s%%, %s%%)' % (to_str(h * 360.0), to_str(s * 100.0), to_str(l * 100.0))
        if type == 'hsla':
            h, l, s = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
            return 'hsla(%s, %s%%, %s%%, %s)' % (to_str(h * 360.0), to_str(s * 100.0), to_str(l * 100.0), to_str(a))
        if c[3] == 1:
            return '#%02x%02x%02x' % (c[0], c[1], c[2])
        return 'rgba(%d, %d, %d, %s)' % (c[0], c[1], c[2], to_str(c[3]))
    @classmethod
    def _do_cmps(cls, first, second, op):
        first = ColorValue(first)
        second = ColorValue(second)
        return op(first.value, second.value)
    @classmethod
    def _do_op(cls, first, second, op):
        first = ColorValue(first)
        second = ColorValue(second)
        val = [ op(first.value[i], second.value[i]) for i in range(4) ]
        val[3] = (first.value[3] + second.value[3]) / 2
        c = val
        r = 255.0, 255.0, 255.0, 1.0
        c = [ 0.0 if c[i] < 0 else r[i] if c[i] > r[i] else c[i] for i in range(4) ]
        ret = ColorValue(None).merge(first).merge(second)
        ret.value = tuple(c)
        return ret
    def merge(self, obj):
        obj = ColorValue(obj)
        self.value = obj.value
        for type, val in obj.types.items():
            self.types.setdefault(type, 0)
            self.types[type] += val
        return self
    def convert_to(self, type):
        val = self.value
        ret = ColorValue(val)
        ret.types[type] = 1
        return ret
    @property
    def type(self):
        type = ''
        if self.types:
            types = sorted(self.types, key=self.types.get)
            while len(types):
                type = types.pop()
                if type:
                    break
        return type

class QuotedStringValue(Value):
    def __init__(self, tokens):
        self.tokens = tokens
        if tokens is None:
            self.value = ''
        elif isinstance(tokens, ParseResults):
            self.value = tokens[0]
        elif isinstance(tokens, QuotedStringValue):
            self.value = tokens.value
        else:
            self.value = to_str(tokens)
    def convert_to(self, type):
        return QuotedStringValue(self.value + type)
    def __str__(self):
        return '"%s"' % escape(self.value)
    @classmethod
    def _do_cmps(cls, first, second, op):
        first = QuotedStringValue(first)
        second = QuotedStringValue(second)
        return op(first.value, second.value)
    @classmethod
    def _do_op(cls, first, second, op):
        first = QuotedStringValue(first)
        second = QuotedStringValue(second)
        val = op(first.value, second.value)
        ret = QuotedStringValue(None).merge(first).merge(second)
        ret.value = val
        return ret
    def merge(self, obj):
        obj = QuotedStringValue(obj)
        self.value = obj.value
        return self

class StringValue(QuotedStringValue):
    def __str__(self):
        return self.value
    def __add__(self, other):
        other = StringValue(other)
        return StringValue(self.value + '+' + other.value)
    def __radd__(self, other):
        other = StringValue(other)
        return StringValue(other.value + '+' + self.value)

class FunctOp(Value):
    def eval(self, context):
        name = self.tokens[0]

        args = len(self.tokens) - 1
        fn = '%s:%d' % (name, args)

        if args:
            args = [ arg.eval(context) for arg in self.tokens[1:] ]
        if fn not in context['fncs']:
            raise ParseException( fn, len(fn), "Function not found", None )
        fn = context['fncs'][fn]
        return fn(*(args or []))

class SignOp(Value):
    "Class to evaluate expressions with a leading + or - sign"
    def eval(self, context):
        sign = self.value[0]
        val = self.value[1].eval(context)
        mult = { '+' :1, '-': -1 }[sign]
        return mult * val

class UnitOp(Value):
    def eval(self, context):
        unit = self.value[1]
        val = self.value[0].eval(context)
        return val.convert_to(unit)

class MultOp(Value):
    "Class to evaluate multiplication and division expressions"
    def eval(self, context):
        prod = self.value[0].eval(context)
        for op, val in self._operatorOperands(self.value[1:]):
            val = val.eval(context)
            if op == '*':
                prod *= val
            if op == '/':
                prod /= val
        return prod

class AddOp(Value):
    "Class to evaluate addition and subtraction expressions"
    def eval(self, context):
        sum = self.value[0].eval(context)
        for op, val in self._operatorOperands(self.value[1:]):
            val = val.eval(context)
            if op == '+':
                sum += val
            if op == '-':
                sum -= val
        return sum

class ComparisonOp(Value):
    "Class to evaluate comparison expressions"
    opMap = {
        "<" : lambda a,b : a < b,
        "<=" : lambda a,b : a <= b,
        ">" : lambda a,b : a > b,
        ">=" : lambda a,b : a >= b,
        "!=" : lambda a,b : a != b,
        "==" : lambda a,b : a == b,
    }
    def eval(self, context):
        val1 = self.value[0].eval(context)
        for op, val in self._operatorOperands(self.value[1:]):
            fn = ComparisonOp.opMap[op]
            val2 = val.eval(context)
            if not fn(val1, val2):
                break
            val1 = val2
        else:
            return True
        return False

class AndBoolOp(Value):
    def eval(self, context):
        anded = self.value[0].eval(context)
        for op, val in self._operatorOperands(self.value[1:]):
            anded = anded and val.eval(context)

        return anded

class OrBoolOp(Value):
    def eval(self, context):
        ored = self.value[0].eval(context)
        for op, val in self._operatorOperands(self.value[1:]):
            ored = ored or val.eval(context)
        return ored

class NotBoolOp(Value):
    def eval(self, context):
        val = self.value[1].eval(context)
        return not val

fnct = {
    '^': operator.__pow__,
    '+': operator.__add__,
    '-': operator.__sub__,
    '*': operator.__mul__,
    '/': operator.__div__,
    '!': operator.__neg__,
    'not': _not,
    '&&': _and,
    'and': _and,
    '||': _or,
    'or': _or,
    '&': operator.__and__,
    '|': operator.__or__,
    '==': operator.__eq__,
    '!=': operator.__ne__,
    '<=': operator.__le__,
    '>=': operator.__ge__,
    '>=': operator.__lt__,
    '>': operator.__gt__,

    'sprite-map:1': _sprite_map,
    'sprite:2': _sprite,
    'sprite:3': _sprite,
    'sprite:4': _sprite,
    'sprite-map-name:1': _sprite_map_name,
    'sprite-file:2': _sprite_file,
    'sprite-url:1': _sprite_url,
    'sprite-position:2': _sprite_position,
    'sprite-position:3': _sprite_position,
    'sprite-position:4': _sprite_position,

    'inline-image:1': _inline_image,
    'inline-image:2': _inline_image,
    'image-url:1': _image_url,
    'image-width:1': _image_width,
    'image-height:1': _image_height,

    'opacify:2': _opacify,
    'fadein:2': _opacify,
    'fade-in:2': _opacify,
    'transparentize:2': _transparentize,
    'fadeout:2': _transparentize,
    'fade-out:2': _transparentize,
    'lighten:2': _lighten,
    'darken:2': _darken,
    'saturate:2': _saturate,
    'desaturate:2': _desaturate,
    'grayscale:1': _grayscale,
    'adjust-hue:2': _adjust_hue,
    'spin:2': _adjust_hue,
    'complement:1': _complement,
    'mix:2': _mix,
    'mix:3': _mix,
    'hsl:3': _hsl,
    'hsla:4': _hsla,
    'rgb:3': _rgb,
    'rgba:4': _rgba,

    'red:1': _red,
    'green:1': _green,
    'blue:1': _blue,
    'alpha:1': _alpha,
    'opacity:1': _alpha,
    'hue:1': _hue,
    'saturation:1': _saturation,
    'lightness:1': _lightness,

    'nth:2': _nth,
    'first-value-of:1': _nth,

    'percentage:1': _percentage,
    'unitless:1': _unitless,
    'quote:1': _quote,
    'unquote:1': _unquote,
    'escape:1': _unquote,
    'e:1': _unquote,

    'sin:1': Value._wrap(math.sin),
    'cos:1': Value._wrap(math.cos),
    'tan:1': Value._wrap(math.tan),
    'abs:1': Value._wrap(abs),
    'round:1': Value._wrap(round),
    'ceil:1': Value._wrap(math.ceil),
    'floor:1': Value._wrap(math.floor),
    'pi:0': _pi,
    'not:1': _inv,
    '!:1': _inv,
}
for u in _units:
    fnct[u+':2'] = _convert_to

def unitsOperator(token):
    token.insert(0, token[-1])

def unaryOperator(token):
    if isinstance(token[0], basestring):
        print 'u',token

def binaryOperator(token):
    if isinstance(token[0], basestring):
        print 'b',token

def callOperator(token):
    if isinstance(token[0], basestring):
        print 'c',token

def bnf():
    _lpar_ = Suppress('(')
    _rpar_ = Suppress(')')
    _comma_ = Suppress(',')

    _unit_ = oneOf(' '.join(_units))
    _sign_ = oneOf('+ -')
    _mul_ = oneOf('* /')
    _add_ = oneOf('+ -')
    _not_ = CaselessKeyword('not') | Literal('!')
    _or_ = CaselessKeyword('or') | Literal('||')
    _and_ = CaselessKeyword('and') | Literal('&&')
    _cmp_ = oneOf('<= < >= > != ==')

    number = Combine((
            Optional(_sign_) + Word( nums ) + Optional( '.' + Optional( Word( nums ) ) ) |
            '.' + Word( nums )
            ) + Optional(oneOf('e E')+Optional(oneOf('+ -')) +Word(nums)))\
            .setParseAction(NumberValue)

    color  = Combine(
        '#' + (
            Word(hexnums, exact=8) |  # #RRGGBBAA
            Word(hexnums, exact=6) | # #RRGGBB
            Word(hexnums, exact=4) | # #RGBA
            Word(hexnums, exact=3))  # #RGB
        ).setParseAction(ColorValue)

    boolean = (
            CaselessKeyword('true', '-_$' + alphanums) |
            CaselessKeyword('false', '-_$' + alphanums)
        ).setParseAction(BooleanValue)

    qstring = QuotedString("'", escChar='\\', multiline=True)\
        .setParseAction(StringValue)

    ustring = QuotedString('"', escChar='\\', multiline=True)\
        .setParseAction(QuotedStringValue)

    stringliteral = qstring | ustring
    identifier = Word('-_$' + alphas, '-_' + alphanums)
    variable = Word('-_$' + alphas, '-_' + alphanums).setParseAction(StringValue)
    literal = stringliteral | number | boolean | color

    atom = Forward()
    u_expr = Forward()
    not_test = Forward()

    units = Group((atom + _unit_).setParseAction(unitsOperator))
    u_expr = units | atom | (_sign_ + u_expr)
    m_expr = Group((u_expr + ZeroOrMore( _mul_ + u_expr )))
    a_expr = Group((m_expr + ZeroOrMore( _add_ + m_expr )))
    and_expr = Group((a_expr + ZeroOrMore( _and_ + a_expr )))
    or_expr = Group((and_expr + ZeroOrMore( _or_ + and_expr )))
    comparison = Group((or_expr + ZeroOrMore( _cmp_ + or_expr )))
    not_test << (comparison | Group(OneOrMore(( _not_ + not_test ))))
    and_test = Group((not_test + ZeroOrMore( _and_ + not_test )))
    expression = Group((and_test + ZeroOrMore( _or_ + and_test )))
    expression_list = expression + ZeroOrMore( _comma_ + expression )
    call = Group((identifier + _lpar_ + expression_list + _rpar_))
    enclosure = Group((_lpar_ + expression + _rpar_))
    atom << (enclosure | call | literal | variable)
    return OneOrMore(expression)
bnf = bnf()

def eval_tree(node):
    if isinstance(node, ParseResults):
        if len(node) == 1:
            node = eval_tree(node[0])
        elif isinstance(node[0], basestring):
            # Function call:
            fn_name = '%s:%d' % (node[0], len(node) - 1)
            fn = fnct.get(fn_name)
            if not fn: raise ParseException("Function not found: "+ fn_name)
            args = [ eval_tree(n) for n in node[1:] ]
            node = fn(*args)
        elif isinstance(node[1], basestring):
            # Operator:
            args = [ eval_tree(n) for n in node ]
            args.reverse()
            fns = args[1::2]
            args = args[::2]
            arg1 = args.pop()
            while len(args):
                arg2 = args.pop()
                fn_name = fns.pop()
                fn = fnct.get(fn_name)
                if not fn: raise ParseException("Function not found: "+ fn_name)
                arg1 = fn(arg1, arg2)
            node = arg1
        else:
            node = [ eval_tree(n) for n in node ]
    return node

def eval_expr(expr):
    exprs = []

    #print >>sys.stderr, '>>',expr,'<<'
    results = bnf.parseString( expr, parseAll=True)
    for r in results:
        #print >>sys.stderr, r
        exprs.append(eval_tree(r))
    val = ' '.join(str(v) for v in exprs)

    #print >>sys.stderr, '--',val,'--', repr(val)
    return val


__doc__ += """
>>> css = xCSS()

VARIABLES
--------------------------------------------------------------------------------
http://xcss.antpaw.org/docs/syntax/variables

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... @variables {
...     $path = ../img/tmpl1/png;
...     $color1 = #FF00FF;
...     $border = border-top: 1px solid $color1;
... }
... .selector {
...     background-image: url($path/head_bg.png);
...     background-color: $color1;
...     $border;
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.selector {
    background-image: url(../img/tmpl1/png/head_bg.png);
    background-color: #f0f;
    border-top: 1px solid #f0f;
}


NESTING CHILD OBJECTS
--------------------------------------------------------------------------------
http://xcss.antpaw.org/docs/syntax/children

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .selector {
...     a {
...         display: block;
...     }
...     strong {
...         color: blue;
...     }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.selector a {
    display: block;
}
.selector strong {
    color: #00f;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .selector {
...     self {
...         margin: 20px;
...     }
...     a {
...         display: block;
...     }
...     strong {
...         color: blue;
...     }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.selector {
    margin: 20px;
}
.selector a {
    display: block;
}
.selector strong {
    color: #00f;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .selector {
...     self {
...         margin: 20px;
...     }
...     a {
...         display: block;
...     }
...     dl {
...         dt {
...             color: red;
...         }
...         dd {
...             self {
...                 color: gray;
...             }
...             span {
...                 text-decoration: underline;
...             }
...         }
...     }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.selector {
    margin: 20px;
}
.selector a {
    display: block;
}
.selector dl dt {
    color: red;
}
.selector dl dd {
    color: gray;
}
.selector dl dd span {
    text-decoration: underline;
}


EXTENDING OBJECTS
--------------------------------------------------------------------------------
http://xcss.antpaw.org/docs/syntax/extends

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .basicClass {
...     padding: 20px;
...     background-color: #FF0000;
... }
... .specialClass extends .basicClass {}
... ''') #doctest: +NORMALIZE_WHITESPACE
.basicClass,
.specialClass {
    padding: 20px;
    background-color: red;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .basicClass {
...     padding: 20px;
...     background-color: #FF0000;
... }
... .specialClass extends .basicClass {
...     padding: 10px;
...     font-size: 14px;
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.basicClass,
.specialClass {
    padding: 20px;
    background-color: red;
}
.specialClass {
    padding: 10px;
    font-size: 14px;
}

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .specialClass extends .basicClass {
...     padding: 10px;
...     font-size: 14px;
... }
... .specialLink extends .basicClass a {}
... .basicClass {
...     self {
...         padding: 20px;
...         background-color: #FF0000;
...     }
...     a {
...         text-decoration: none;
...     }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.basicClass,
.specialClass {
    padding: 20px;
    background-color: red;
}
.basicClass a,
.specialClass a,
.specialLink {
    text-decoration: none;
}
.specialClass {
    padding: 10px;
    font-size: 14px;
}

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .basicList {
...     li {
...         padding: 5px 10px;
...         border-bottom: 1px solid #000000;
...     }
...     dd {
...         margin: 4px;
...     }
...     span {
...         display: inline-block;
...     }
... }
... .roundBox {
...     some: props;
... }
... .specialClass extends .basicList & .roundBox {}
... ''') #doctest: +NORMALIZE_WHITESPACE
.basicList li,
.specialClass li {
	padding: 5px 10px;
	border-bottom: 1px solid #000;
}
.basicList dd,
.specialClass dd {
	margin: 4px;
}
.basicList span,
.specialClass span {
	display: inline-block;
}
.roundBox,
.specialClass {
	some: props;
}

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .basicList {
...     li {
...         padding: 5px 10px;
...         border-bottom: 1px solid #000000;
...     }
...     dd {
...         margin: 4px;
...     }
...     span {
...         display: inline-block;
...     }
... }
... .specialClass {
...     dt extends .basicList li {}
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.basicList li,
.specialClass dt {
    padding: 5px 10px;
    border-bottom: 1px solid #000;
}
.basicList dd {
    margin: 4px;
}
.basicList span {
    display: inline-block;
}

MATH OPERATIONS
--------------------------------------------------------------------------------
http://xcss.antpaw.org/docs/syntax/math

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... @variables {
...     $color = #FFF555;
... }
... .selector {
...     padding: [5px * 2];
...     color: [#ccc * 2];
...     // lets assume $color is '#FFF555'
...     background-color: [$color - #222 + #101010];
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.selector {
	padding: 10px;
	color: #fff;
	background-color: #ede343;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .selector {
...     padding: [(5px - 3) * (5px - 3)];
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.selector {
	padding: 4px;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .selector {
...     padding: [5em - 3em + 5px]px;
...     margin: [20 - 10] [30% - 10];
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.selector {
	padding: 31px;
	margin: 10 20%;
}


SASS NESTING COMPATIBILITY
--------------------------------------------------------------------------------
http://sass-lang.com/tutorial.html

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... /* style.scss */
... #navbar {
...   width: 80%;
...   height: 23px;
...
...   ul { list-style-type: none; }
...   li {
...     float: left;
...     a { font-weight: bold; }
...   }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
#navbar {
	width: 80%;
	height: 23px;
}
#navbar ul {
	list-style-type: none;
}
#navbar li {
	float: left;
}
#navbar li a {
	font-weight: bold;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... /* style.scss */
... .fakeshadow {
...   border: {
...     style: solid;
...     left: {
...       width: 4px;
...       color: #888;
...     }
...     right: {
...       width: 2px;
...       color: #ccc;
...     }
...   }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.fakeshadow {
	border-style: solid;
	border-left-width: 4px;
	border-left-color: #888;
	border-right-width: 2px;
	border-right-color: #ccc;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... /* style.scss */
... a {
...   color: #ce4dd6;
...   &:hover { color: #ffb3ff; }
...   &:visited { color: #c458cb; }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
a {
	color: #ce4dd6;
}
a:hover {
	color: #ffb3ff;
}
a:visited {
	color: #c458cb;
}


SASS VARIABLES COMPATIBILITY
--------------------------------------------------------------------------------
http://sass-lang.com/tutorial.html

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... /* style.scss */
... $main-color: #ce4dd6;
... $style: solid;
...
... #navbar {
...   border-bottom: {
...     color: $main-color;
...     style: $style;
...   }
... }
...
... a {
...   color: $main-color;
...   &:hover { border-bottom: $style 1px; }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
#navbar {
	border-bottom-color: #ce4dd6;
	border-bottom-style: solid;
}
a {
	color: #ce4dd6;
}
a:hover {
	border-bottom: solid 1px;
}


SASS INTERPOLATION COMPATIBILITY
--------------------------------------------------------------------------------
http://sass-lang.com/tutorial.html

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... /* style.scss */
... $side: top;
... $radius: 10px;
...
... .rounded-#{$side} {
...   border-#{$side}-radius: $radius;
...   -moz-border-radius-#{$side}: $radius;
...   -webkit-border-#{$side}-radius: $radius;
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.rounded-top {
	border-top-radius: 10px;
	-moz-border-radius-top: 10px;
	-webkit-border-top-radius: 10px;
}


SASS MIXINS COMPATIBILITY
--------------------------------------------------------------------------------
http://sass-lang.com/tutorial.html

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... /* style.scss */
...
... @mixin rounded-top {
...   $side: top;
...   $radius: 10px;
...
...   border-#{$side}-radius: $radius;
...   -moz-border-radius-#{$side}: $radius;
...   -webkit-border-#{$side}-radius: $radius;
... }
...
... #navbar li { @include rounded-top; }
... #footer { @include rounded-top; }
... ''') #doctest: +NORMALIZE_WHITESPACE
#navbar li {
	border-top-radius: 10px;
	-moz-border-radius-top: 10px;
	-webkit-border-top-radius: 10px;
}
#footer {
	border-top-radius: 10px;
	-moz-border-radius-top: 10px;
	-webkit-border-top-radius: 10px;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... /* style.scss */
...
... @mixin rounded($side, $radius: 10px) {
...   border-#{$side}-radius: $radius;
...   -moz-border-radius-#{$side}: $radius;
...   -webkit-border-#{$side}-radius: $radius;
... }
...
... #navbar li { @include rounded(top); }
... #footer { @include rounded(top, 5px); }
... #sidebar { @include rounded(left, 8px); }
... ''') #doctest: +NORMALIZE_WHITESPACE
#navbar li {
	border-top-radius: 10px;
	-moz-border-radius-top: 10px;
	-webkit-border-top-radius: 10px;
}
#footer {
	border-top-radius: 5px;
	-moz-border-radius-top: 5px;
	-webkit-border-top-radius: 5px;
}
#sidebar {
	border-left-radius: 8px;
	-moz-border-radius-left: 8px;
	-webkit-border-left-radius: 8px;
}


SASS EXTEND COMPATIBILITY
--------------------------------------------------------------------------------
http://sass-lang.com/docs/yardoc/file.SASS_REFERENCE.html#extend

>>> from xcss import *
>>> css = xCSS()
>>>
>>>
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .error {
...   border: 1px #f00;
...   background-color: #fdd;
... }
... .error.intrusion {
...   background-image: url("/image/hacked.png");
... }
... .seriousError {
...   @extend .error;
...   border-width: 3px;
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.error,
.seriousError {
	border: 1px red;
	background-color: #fdd;
}
.error.intrusion,
.seriousError.intrusion {
	background-image: url("/image/hacked.png");
}
.seriousError {
	border-width: 3px;
}


Multiple Extends
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .error {
...   border: 1px #f00;
...   background-color: #fdd;
... }
... .attention {
...   font-size: 3em;
...   background-color: #ff0;
... }
... .seriousError {
...   @extend .error, .attention;
...   border-width: 3px;
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.error,
.seriousError {
	border: 1px red;
	background-color: #fdd;
}
.attention,
.seriousError {
	font-size: 3em;
	background-color: #ff0;
}
.seriousError {
	border-width: 3px;
}




FROM THE FORUM
--------------------------------------------------------------------------------

http://groups.google.com/group/xcss/browse_thread/thread/6989243973938362#
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... body {
...     _width: expression(document.body.clientWidth > 1440? "1440px" : "auto");
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
body {
	_width: expression(document.body.clientWidth > 1440? "1440px" : "auto");
}


http://groups.google.com/group/xcss/browse_thread/thread/2d27ddec3c15c385#
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... @variables {
...     $ie6 = *html;
...     $ie7 = *:first-child+html;
... }
... $ie6 {
...     .a  { color:white; }
...     .b  { color:black; }
... }
... $ie7 {
...     .a  { color:white; }
...     .b  { color:black; }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
*html .a {
	color: #fff;
}
*html .b {
	color: #000;
}
*:first-child+html .a {
	color: #fff;
}
*:first-child+html .b {
	color: #000;
}


http://groups.google.com/group/xcss/browse_thread/thread/04faafb4ef178984#
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .basicClass {
...     padding: 20px;
...     background-color: #FF0000;
... }
... .specialClass extends .basicClass {
...     padding: 10px;
...     font-size: 14px;
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.basicClass,
.specialClass {
    padding: 20px;
    background-color: red;
}
.specialClass {
    padding: 10px;
    font-size: 14px;
}


ERRORS
--------------------------------------------------------------------------------

http://groups.google.com/group/xcss/browse_thread/thread/5f4f3af046883c3b#
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .some-selector { some:prop; }
... .some-selector-more { some:proop; }
... .parent {
...     self extends .some-selector {
...         height: auto
...     }
...     .children {
...         self extends .some-selector-more {
...             height: autoo
...         }
...     }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.parent,
.some-selector {
	some: prop;
}
.parent .children,
.some-selector-more {
	some: proop;
}
.parent {
	height: auto;
}
.parent .children {
	height: autoo;
}


http://groups.google.com/group/xcss/browse_thread/thread/540f8ad0771c053b#
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .noticeBox {
...     self {
...         background-color:red;
...     }
...     span, p {
...         some: props
...     }
... }
... .errorBox extends .noticeBox {}
... ''') #doctest: +NORMALIZE_WHITESPACE
.errorBox,
.noticeBox {
	background-color: red;
}
.errorBox p,
.errorBox span,
.noticeBox p,
.noticeBox span {
	some: props;
}

http://groups.google.com/group/xcss/browse_thread/thread/b5757c24586c1519#
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .mod {
...     self {
...         margin: 10px;
...     }
...     h1 {
...         font-size:40px;
...     }
... }
... .cleanBox extends .mod {
...     h1 {
...         font-size:60px;
...     }
... }
... .cleanBoxExtended extends .cleanBox {}
... .articleBox extends .cleanBox {}
... ''') #doctest: +NORMALIZE_WHITESPACE
.articleBox,
.cleanBox,
.cleanBoxExtended,
.mod {
	margin: 10px;
}
.articleBox h1,
.cleanBox h1,
.cleanBoxExtended h1,
.mod h1 {
	font-size: 40px;
}
.articleBox h1,
.cleanBox h1,
.cleanBoxExtended h1 {
	font-size: 60px;
}


TESTS
--------------------------------------------------------------------------------
http://sass-lang.com/docs/yardoc/file.SASS_REFERENCE.html
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... a {
...     $color: rgba(0.872536*255, 0.48481984*255, 0.375464*255, 1);
...     color: $color;
...     color: hsl(13.2, 0.661, 0.624);
...     color-hue: hue($color); // 60deg
...     color-saturation: saturation($color); // 60%
...     color-lightness: lightness($color); // 50%
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
a {
	color: #de7b5f;
	color: hsl(13.2, 66.1%, 62.4%);
	color-hue: 13.2;
	color-saturation: 66.1%;
	color-lightness: 62.4%;
}

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .functions {
...     opacify: opacify(rgba(0, 0, 0, 0.5), 0.1); // rgba(0, 0, 0, 0.6)
...     opacify: opacify(rgba(0, 0, 17, 0.8), 0.2); // #001
...
...     transparentize: transparentize(rgba(0, 0, 0, 0.5), 0.1); // rgba(0, 0, 0, 0.4)
...     transparentize: transparentize(rgba(0, 0, 0, 0.8), 0.2); // rgba(0, 0, 0, 0.6)
...
...     lighten: lighten(hsl(0, 0%, 0%), 30%); // hsl(0, 0, 30)
...     lighten: lighten(#800, 20%); // #e00
...
...     darken: darken(hsl(25, 100%, 80%), 30%); // hsl(25, 100%, 50%)
...     darken: darken(#800, 20%); // #200
...
...     saturate: saturate(hsl(120, 30%, 90%), 20%); // hsl(120, 50%, 90%)
...     saturate: saturate(#855, 20%); // #9e3f3f
...
...     desaturate: desaturate(hsl(120, 30%, 90%), 20%); // hsl(120, 10%, 90%)
...     desaturate: desaturate(#855, 20%); // #726b6b
...
...     adjust: adjust-hue(hsl(120, 30%, 90%), 60deg); // hsl(180, 30%, 90%)
...     adjust: adjust-hue(hsl(120, 30%, 90%), -60deg); // hsl(60, 30%, 90%)
...     adjust: adjust-hue(#811, 45deg); // #886a11
...
...     mix: mix(#f00, #00f, 50%); // #7f007f
...     mix: mix(#f00, #00f, 25%); // #3f00bf
...     mix: mix(rgba(255, 0, 0, 0.5), #00f, 50%); // rgba(64, 0, 191, 0.75)
...
...     percentage: percentage(100px / 50px); // 200%
...
...     round: round(10.4px); // 10px
...     round: round(10.6px); // 11px
...
...     ceil: ceil(10.4px); // 11px
...     ceil: ceil(10.6px); // 11px
...
...     floor: floor(10.4px); // 10px
...     floor: floor(10.6px); // 10px
...
...     abs: abs(10px); // 10px
...     abs: abs(-10px); // 10px
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.functions {
    opacify: rgba(0, 0, 0, 0.6);
    opacify: #001;
    transparentize: rgba(0, 0, 0, 0.4);
    transparentize: rgba(0, 0, 0, 0.6);
    lighten: hsl(0, 0, 30%);
    lighten: #e00;
    darken: hsl(25, 100%, 50%);
    darken: #210000;
    saturate: hsl(120, 50%, 90%);
    saturate: #9e3e3e;
    desaturate: hsl(120, 10%, 90%);
    desaturate: #716b6b;
    adjust: hsl(180, 30%, 90%);
    adjust: hsl(60, 30%, 90%);
    adjust: #886a10;
    mix: #7f007f;
    mix: #3f00bf;
    mix: rgba(63, 0, 191, 0.75);
    percentage: 200%;
    round: 10px;
    round: 11px;
    ceil: 11px;
    ceil: 11px;
    floor: 10px;
    floor: 10px;
    abs: 10px;
    abs: 10px;
}

>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .coloredClass {
...     $mycolor: green;
...     padding: 20px;
...     background-color: $mycolor;
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
    .coloredClass {
    	padding: 20px;
    	background-color: green;
    }


>>> css.xcss_files = {}
>>> css.xcss_files['first.css'] = '''
... @options compress:false, short_colors:true, reverse_colors:true;
... .specialClass extends .basicClass {
...     padding: 10px;
...     font-size: 14px;
... }
... '''
>>> css.xcss_files['second.css'] = '''
... @options compress:false, short_colors:true, reverse_colors:true;
... .basicClass {
...     padding: 20px;
...     background-color: #FF0000;
... }
... '''
>>> print css.compile() #doctest: +NORMALIZE_WHITESPACE
/* Generated from: second.css */
.basicClass,
.specialClass {
    padding: 20px;
    background-color: red;
}
/* Generated from: first.css */
.specialClass {
    padding: 10px;
    font-size: 14px;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... a, button {
...     color: blue;
...     &:hover, .some & {
...         text-decoration: underline;
...     }
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
a,
button {
    color: #00f;
}
.some a,
.some button,
a:hover,
button:hover {
    text-decoration: underline;
}


All styles defined for a:hover are also applied to .hoverlink:
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... a:hover { text-decoration: underline }
... .hoverlink { @extend a:hover }
... ''') #doctest: +NORMALIZE_WHITESPACE
.hoverlink,
a:hover {
	text-decoration: underline;
}


http://sass-lang.com/docs/yardoc/file.SASS_REFERENCE.html
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... #fake-links .link {@extend a}
...
... a {
...   color: blue;
...   &:hover {text-decoration: underline}
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
#fake-links .link,
a {
	color: #00f;
}
#fake-links .link:hover,
a:hover {
	text-decoration: underline;
}


>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .mod {
... 	margin: 10px;
... }
... .mod h1 {
... 	font-size: 40px;
... }
... .cleanBox h1 extends .mod {
... 	font-size: 60px;
... }
... ''') #doctest: +NORMALIZE_WHITESPACE
.cleanBox h1,
.mod {
	margin: 10px;
}
.cleanBox h1,
.mod h1 {
	font-size: 40px;
}
.cleanBox h1 {
	font-size: 60px;
}


"""
"""
ADVANCED STUFF, NOT SUPPORTED (FROM SASS):
--------------------------------------------------------------------------------
http://sass-lang.com/docs/yardoc/file.SASS_REFERENCE.html

Any rule that uses a:hover will also work for .hoverlink, even if they have other selectors as well
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... .comment a.user:hover { font-weight: bold }
... .hoverlink { @extend a:hover }
... ''') #doctest: +NORMALIZE_WHITESPACE
.comment a.user:hover,
.comment .hoverlink.user {
	font-weight: bold;
}


Sometimes a selector sequence extends another selector that appears in another
sequence. In this case, the two sequences need to be merged.
While it would technically be possible to generate all selectors that could
possibly match either sequence, this would make the stylesheet far too large.
The simple example above, for instance, would require ten selectors. Instead,
Sass generates only selectors that are likely to be useful.
>>> print css.compile('''
... @options compress:false, short_colors:true, reverse_colors:true;
... #admin .tabbar a { font-weight: bold }
... #demo .overview .fakelink { @extend a }
... ''') #doctest: +NORMALIZE_WHITESPACE
#admin .tabbar a,
#admin .tabbar #demo .overview .fakelink,
#demo .overview #admin .tabbar .fakelink {
	font-weight: bold;
}

--------------------------------------------------------------------------------
"""

if __name__ == "__main__":
    import getopt
    # parse options for module imports
    opts, args = getopt.getopt(sys.argv[1:], 't')
    opts = dict(opts)
    if '-t' in opts:
        import doctest
        doctest.testmod()
    else:
        css = xCSS()
        sys.stdout.write(css.compile(sys.stdin.read()))
