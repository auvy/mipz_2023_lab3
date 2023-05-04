import re
from fileops import read_lines

# keywords
STATEMENTS_LOGICAL = [
  "if",
  "elif",
  "else",
  "try",
  "catch",
  "with"
]

STATEMENTS_ITERATION = [
  "for",
  "while"
]

STATEMENTS_SOLITARY = [
  "break",
  "continue",
  "pass"
]

REGEX_DECLARATION = '.*(def.*\(.*\)).*'
REGEX_CALL        = '.*\(.*'
REGEX_ASSIGNMENT  = ".*[^=]=[^=].*"


def is_empty_line(line):
  # isspace doesnt work too well
  return len(line.strip()) == 0


def count_logical(lines):
  logical_lines = 0
  for line in lines:
    logical_lines += logical_line(line)
  return logical_lines


# python does not have:
# - compiler directives
# - goto
# - scopes inside braces

def logical_line(line):
  logical_lines = 0
  line = line.strip()

  # logical lines
  arr = line.split()
  for s in STATEMENTS_LOGICAL:
    if s in line.split():
      logical_lines += arr.count(s)
      
  # iteration    
  for s in STATEMENTS_ITERATION:
    if s in line.split():
      logical_lines += arr.count(s)
  
  # jump, solitary (jump without return + pass)
  for s in STATEMENTS_SOLITARY:
    arr = line.split()
    if len(arr) == 1 and s == arr[0]:
      logical_lines += 1  
  
  # return
  if "return" in arr:
    logical_lines += 1  

  # expression: function call
  if re.match(REGEX_CALL, line) and not re.match(REGEX_ASSIGNMENT, line):
    logical_lines += 1 

  # expression: assignment
  if re.match(REGEX_ASSIGNMENT, line):
    logical_lines += 1
    
  # block delimiting
  # if : in line.strip() is last, we interpret it as a block (+1)
  # i couldn't be bothered to count spaces and idents and tabs as python does it
  if line.strip().endswith(":"):
    logical_lines += 1
  
  return logical_lines


def count_loc(lines):
  # because a docstring can span multiple lines
  # i have to feed all the lines into function.
  
  # this may not necessarily be the correct way
  # i just looked at the table from the lecture
  # and did what i could in python
  
  code_lines    = 0
  comment_lines = 0
  empty_lines   = 0
  
  logical_lines = 0
  
  docstring = False
  blockstring = False
  
  for line in lines:
    line = line.strip()
    
    if not docstring and not blockstring and not line.startswith("#"):
      logical_lines += logical_line(line)

    if   line.startswith("#") \
      or docstring and not (line.startswith('"""') or line.startswith("'''")) \
      or (line.startswith("'''") and line.endswith("'''") and len(line) >3)   \
      or (line.startswith('"""') and line.endswith('"""') and len(line) >3)   :
      comment_lines += 1
      
      
    if   line.endswith("(") and not blockstring \
      or line.startswith(")") and not blockstring:
      blockstring = not blockstring

    # when docstrings are declared as variables
    elif line.endswith("'''") and not docstring \
      or line.endswith('"""') and not docstring :
      comment_lines += 1
      docstring = not docstring

    # this is either a starting or ending docstring
    elif line.startswith('"""') or line.startswith("'''") :
      comment_lines += 1
      docstring = not docstring
    
    elif is_empty_line(line)  :
      empty_lines += 1

    else:
      # print("code")
      code_lines += 1

  return {
    "code"      : code_lines,
    "empty"     : empty_lines,
    "comment"   : comment_lines,
    "physical"  : len(lines),
    "logical"   : logical_lines
  }


def is_comment(line):
  return line.strip().startswith('#')


def loc_lines(filepath):
  lines = read_lines(filepath)
  
  res = count_loc(lines)
  return res
  # print(res)