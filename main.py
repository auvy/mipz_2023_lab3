from fileops import listfiles
from loc     import loc_lines

from config  import LIBPATH

def main():
  files = listfiles(LIBPATH)
      
  code_lines      = 0
  empty_lines     = 0
  comment_lines   = 0
  physical_lines  = 0
  logical_lines   = 0
  
  for f in files:
    res = loc_lines(f)
    
    code_lines     += res["code"]
    empty_lines    += res["empty"]
    comment_lines  += res["comment"]
    logical_lines  += res["logical"]
    physical_lines += res["physical"]
  
  print(f'code:          {code_lines}')
  print(f'empty:         {empty_lines}')
  print(f'comment:       {comment_lines}')
  print(f'logical:       {logical_lines}')
  print(f'physical:      {physical_lines}')
  print(f'comment level: {comment_lines/code_lines}')


main()