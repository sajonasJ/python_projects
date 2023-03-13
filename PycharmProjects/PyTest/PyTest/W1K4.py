from PyTest import *
##//////////////////////////// PROBLEM STATEMENT ///////////////////////////////
## Given a list of integers and start & end indexes into the list, print      //
## the number of times where, between the start and end indices (inclusive),  //
## an integer in the list  is followed by a larger integer. The start and     //
## end index will both be valid indexes into the list  with start less than   //
## or equal to end.                                                           //
##                                                                            //
## Use one function to read the list and another function to count the number //
## of times where an integer in the list with an index betwen start and end   //
## (inclusive) is followed by a larger integer.                               //
##   5, 3, 3, 3, 2,  2, 4 -> 0                                                //
##   5, 3, 6, 7, 2,  0, 1 -> 0                                                //
##   5, 7, 3, 4, 2,  0, 4 -> 2                                                //
##//////////////////////////////////////////////////////////////////////////////
