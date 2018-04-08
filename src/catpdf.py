#!/usr/bin/env python
import sys
from PyPDF2 import PdfFileMerger

def concatenate_pdfs(output_filename, pdf_files):
  merger = PdfFileMerger()
  for pdf in pdf_files:
      merger.append(pdf)
  merger.write(output_filename)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    print "Usage: {0}: output.pdf in1.pdf [in2.pdf ...]".format(sys.argv[0])
    exit(1)
  concatenate_pdfs(sys.argv[1], sys.argv[2:])



