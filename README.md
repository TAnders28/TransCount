# TransCount
Authors: Tom Anders(tanders28@vt.edu) and Spencer Beery(sbeery3@vt.edu)


The transistor_counter.py python 3 file provides a means of analyzing Dataflow and Structural level verilog files for transistor count from the Linux CLI, producing verbose output describing the features contained in each module of the file. 

Usage:

python3 transistor_counter.py (optional) --f=filename

If a file is not specified, the default set in line 421 is used.

This will print to console an in depth description of each module in the verilog file, including deduced transistor count, with the top level module printed last.

Included are 2 test files: function_unit.v and test1.v
