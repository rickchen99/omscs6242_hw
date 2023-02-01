"""
cse6242 s22
wrangling.py - utilities to supply data to the templates.

This file contains a pair of functions for retrieving and manipulating data
that will be supplied to the template for generating the table. """
import csv
from ctypes import sizeof
from turtle import shape

def username():
    return 'gburdell3'

def data_wrangling():
    with open('data/movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = list()
        # Feel free to add any additional variables
        ...
        
        # Read in the header
        for header in reader:
            break
        
        # Read in each row
        for index, row in enumerate(reader):
            #index start at zero, break the for loop when index is at 100th enumeration
            if index > 99:
                break
            table.append(row)

            
            # Only read first 100 data rows - [2 points] Q5.a
            ...
        
        # Order table by the last column - [3 points] Q5.b
        ...
        #using the built-in sorting function to sort last column, convert to float first
        sorted_table = sorted(table,key = lambda x :float(x[-1]),reverse=True)
        #print(f'size of sorted table is {len(sorted_table)}')
        #print(f'first row is {sorted_table[0]}')
    return header, sorted_table

