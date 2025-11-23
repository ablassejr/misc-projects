#!/bin/bash
if [[ -e myFile ]]; then
   print "Path Exists!\n"
   if [[ -L myFile ]]; then
      print "\tIs a Symlink\n"
      if [[ -d myFile ]]; then
	 print "\t\tTo a Directory\n"
      fi
      if [[ -f myFile ]]; then
	 print "\t\tTo a file\n"
      fi
      fi
    if [[ -d myFile ]]; then
      print "\tIs a Directory\n"
    fi
       if [[ -f myFile ]]; then
	  print"\tIs a File\n"
       fi
  else 
    print "Path Invalid"
fi
