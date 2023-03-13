from PyTest import *
##//////////////////////////// PROBLEM STATEMENT ///////////////////////////////
## Given a list of integers and start & end indexes into the list, print      //
## True if, between the start and end indices (inclusive), every integer in   //
## the list  is followed by a smaller integer. The start and end index will   //
## both be valid indexes into the list  with start less than or equal to end. //
##                                                                            //
## Use one function to read the list  and another function to check that every//
## integer in the list  with an index betwen start and end (inclusive) is     //
## followed by a smaller integer.                                             //
##    5, 3, 3, 2, 1,  2, 4 -> True                                            //
##    5, 3, 6, 7, 2,  0, 1 -> True                                            //
##    5, 3, 3, 3, 2,  0, 4 -> False                                           //
##//////////////////////////////////////////////////////////////////////////////
