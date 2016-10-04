import csv

input_file_name = 'random_2500.csv'
output_file_name = 'random_2500_classified.csv'
data = []

nice_but_check_length = [
    ' function not implemented',
    'Method too long',
    'Too many arguments',
    'Repetitive code',
    'hardcoded',
    'Lazy class',
    'cyclomatic complexity',
    'Long Function',
    'Conditional Complexity',
    'Too few public methods',
    'Too many branches',
    'Too large function',
    'too much branching',
    'Duplicated Code',
    'global variables used',
    'Redefining',
    'Too many param',
    'Code duplication',
    'no-self-use',
    'Commented Code',
    'not used at all',
    'short identifier',
    'Dead code',
    'Unreachable code',
    'Duplication of code',
    'repetition of code',
    'hard-coded',
    'hardcoded',
    'hard-coding',
    'hardcoding',
    'code repetition',
    'too many public methods',
    'Combinitorial Explosion',
    'Combinatorial Explosion',
    'many local variable',
    'many statements',
    'many return statements',
    'spread across multiple modules',
    'hard code',
    'use of literals',
    'Orphan Variable',
    'Orphan constant',
    'Orphan class',
    'method is too long',
    'method is long',
    'method too long',
    'class too large',
    'method too large',
    'Modularisation',
    'many instance attributes',
    'should be <=',
    'too short class',
    'Encapsulation',
    'Uncommunicative',
    'too many literals',
    'Indecent exposure',
    'class ie missing',
    'Dead Code',
    'modularity',
    'no private members',
    'code is repeated',
    'data abstraction',
    'Long method',
    'Polymorphism',
    'Redundant Code',
    ' nested ',
    'separate file',
    'Large Class',
    'Long class',
    'God Class',
    'intimacy',
    'Refused bequest',
    'not been implemented',
    'not implemented'
]
pep8_direct = [
    'Invalid method name (PEP-8 Violation)',
    'mixed-indentation',
    'Missing module docstring',
    'Invalid variable name',
    'Unused import ',
    'lines have been duplicated',
    'constants should be uppercase',
    'Invalid attribute name',
    'Bad indentation',
    'Missing method docstring',
    'should be a function docstring',
    'Follow: http://pylint-messages.wikidot.com',
    '[E265]',
    '[E302]',
    'import statements inside function',
    'Wildcard import',
    'Missing docstring',
    'Missing class docstring',
    'Missing function docstring',
    'indentation problems',
    'Docstring missing',
    'Docstrings absent',
    'Invalid class name',
    'invalid-name',
    'Invalid method name',
    'Invalid class name',
    'Invalid constant name',
    'Invalid variable name',
    'Invalid argument name',
    'data hinding',
    'Function docsting',
    'Missing Doctring',
    'proper comments',
    'Redefined',
    'docstring',
    'capitals',
    'capital letter',
    'used the sprites directly',
    'readability',
    'debugging'
]
bad_comment = [
    'line too long',
    'long line',
    'trailing whitespace',
    'No need for a parenthesis',
    'end of file [W391]',
    'Unused imports',
    'Unnecessary space',
    'Unused variable',
    'Method definition not according to PEP-8 standards',
    'Exactly one space required',
    'Bad whitespace',
    'Exactly one space is required',
    '[E231]',
    'one space around both sides',
    'imported, but never used',
    'Unnecessary paren',
    'unnecessary outer parenthesis',
    'Too many whitespace',
    'one space after',
    '[F403]',
    'space allowed after bracket',
    'space after bracket',
    'space around assignment',
    'Unnecessary Trailing spaces',
    'whitespace around operator',
    'missing whitespace',
    '[E225]',
    'no whitespace before',
    'no space before',
    '[F401]',
    'imported but never used',
    'one whitespace should be added',
    'Expected 2 blank lines',
    'surrounded by a single space',
    'Indentation',
    'Multiple spaces after',
    'bad-whitespace',
    '[E712]',
    'standards comparison to True',
    'space character after',
    'Not according to PEP-8 strandards',
    'PEP-8 standard violation',
    'imports should be in separate lines',
    'Imports should be on new line',
    'PEP-8 Violation',
    'space missing after',
    'whitespacing',
    'PEP8 violation',
    'blank lines',
    'white space',
    'whitespace',
    'Wildcard',
    'imports'
]
nouse_comment = [
    'Bad code smells',
    'Bad code smell',
    'Code rating :'
]

def autoclassify(comment):
    comment = comment.lower().strip()
    if len(comment.split(' ')) > 15:
        for ex in nice_but_check_length:
            ex = ex.lower()
            if ex in comment:
                return 5
    for ex in nice_but_check_length:
        ex = ex.lower()
        if ex in comment:
            print 'Can be 4 directly.'
            return 4
    for ex in pep8_direct:
        ex = ex.lower()
        if ex in comment:
            return 3
    for ex in bad_comment:
        ex = ex.lower()
        if ex in comment:
            return 2
    for ex in nouse_comment:
        ex = ex.lower()
        if ex == comment:
            return 1
    return 0

with open(input_file_name, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

counter = 0
for row in data:
    # already classified if >2
    counter += 1
    if len(row) > 2:
        continue
    else:
        tool_name = row[1]
        comment = row[0]
        print '--------- [' + str(counter) + '] Tool#' + tool_name + '  -----------\n\n'
        print comment
        print '\n\n'
        rate = ""
        auto = autoclassify(comment)
        if auto > 0:
            rating = auto
            print 'Automatically classified as : ' + str(auto)
        else:
            rating = int(raw_input('Rate this comment (1-5): '))
        row.append(rating)
        ## flush to output file
        with open(output_file_name, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)