# FileSplit
Split a file into smaller subfiles.
# This is DEFINITELY, TOTALLY not so that you can split a big file into little files to get around certain chat services' maximum file upload limits without paying.

usage: Split files into subfiles. [-h] [-c COUNT] [-g | --glue | --no-glue]
                                  [-o [OUT]] [-i INPUT] [-s MAXSIZE]
                                  [-v | --version | --no-version]

options:

  -h, --help            show this help message and exit
  
  -c, --count COUNT     How many files the file should be split into.
  
  -g, --glue, --no-glue
  
                        'Glue' subfiles back into their original file.
                        
  -o, --out [OUT]       Where to store output of --glue'd files. Default=FileSplit.out.
                        
  -i, --input INPUT     Input file/dir to split/glue. Defaults to PWD.
  
  -s, --maxsize MAXSIZE
  
                        How large each output file can get in bytes.
                        
  -v, --version, --no-version
  
                        Print version information and exit.
