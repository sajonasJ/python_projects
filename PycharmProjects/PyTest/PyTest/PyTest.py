import os
import re
import sys
import time
import string
import socket
import getpass
import datetime

_test_data = {
  "W111" : ["7,5,1;300,450,100;246,879,623", "13 35;850 13500000;1748 134713782"],
  "W112" : ["4,9,2;72,3,0;3006,4201,7762", "5;25;4989"],
  "W113" : ["5,9,0;7,12,2;10,8,1", "45;98;90"],
  "W114" : ["590;7122;1081", "5:90;71:22;10:81"],
  "W115" : ["2,3,3;1,5,4;4,1,1", "11;21;5"],
  "W116" : ["0,1,40;0,3,20;0,16,40;0,33,20", "100;200;1000;2000"],
  "W121" : ["100;200;1000;2000", "0 1 40;0 3 20;0 16 40;0 33 20"],
  "W122" : ["1330;2213;0830", "1 o'clock;10 o'clock;8 o'clock"],
  "W123" : ["13,24,30,2,40,40", "16 5 10"],
  "W124" : ["1,24,30,1,2,40,40;1,24,30,1,2,40,40", "4 5 10 1;4 5 10 1"],
  "W125" : ["10;20;30;40;60;65;66", "1 2 0 0 0;1 1 1 0 0;1 1 0 0 0;1 0 1 0 0;0 2 0 0 0;0 1 1 1 0;0 1 1 0 4"],
  "W126" : ["9; 5; 7; 8", "11106; 6170; 8638; 9872"],
  "W131" : ["True,True;True,False;False,True;False,False", "False;False;False;True"],
  "W132" : ["True,True;True,False;False,True;False,False", "False;False;True;False"],
  "W133" : ["True,True;True,False;False,True;False,False", "True;False;False;True"],
  "W134" : ["12;0;-8", "True;False;False"],
  "W135" : ["120,-1;-1,120;2,120;-1,100;-2,-2;120,120", "True;True;False;False;False;False"],
  "W136" : ["True,50;True,-5;False,50;False,200;False,-10;False,-5", "True;False;False;True;False;True"],
  "W141" : ["13,20,10;20,19,10;20,10,13;1,20,12;19,20,12;12,20,19;12,9,20;12,18,20;14,2,20;4,2,20;11,22,22", "True;True;True;False;True;True;False;True;True;False;False"],
  "W142" : ["10,50;20,5;100,20;30,20;2,0;16,-5", "True;False;True;False;True;False"],
  "W143" : ["10,50;20,5;100,20;-5,20;-5,12;-10,0", "False;True;True;False;True;True"],
  "W144" : ["12,99;21,12;8,99;99,10;20,20;21,21;9,9", "True;True;False;True;True;False;False"],
  "W145" : ["5,False;11,False;11,True;10,False;10,True;9,False;9,True;1,False;1,True;0,False;0,True;-1,False", "True;False;True;True;True;True;False;True;True;False;True;False"],
  "W146" : ["1,2,4,False;1,2,1,False;1,1,2,True;3,2,4,False;2,3,4,False;3,2,4,True;4,2,2,True;4,5,2,True;2,4,6,True;7,9,10,False;7,5,6,True;4,7,5,True", "True;False;True;False;True;True;False;False;True;True;True;False"],
  "W151" : ["3,12;10,4;3,3", "12;10;3"],
  "W152" : ["-10;23;50;78;128", "Illegal Grade;Failed;Passed;Passed;Illegal Grade"],
  "W153" : ["3,2,1;2,3,1;1,2,3;3,3,3;3,3,1;3,1,3;1,3,3", "3 ;3 ;3 ;3 ;3 ;3 ;3 "],
  "W154" : ["9,1,0;9,2,0;6,1,4;6,1,5;10,0,0;15,0,5;5,15,5;4,11,1;13,2,3;8,4,3;8,4,2;8,4,1", "10;0;10;0;10;5;10;5;5;0;10;0"],
  "W155" : ["60,False;65,False;65,True;80,False;85,False;85,True;70,False;75,False;75,True;40,False;40,True;90,False", "0;1;0;1;2;1;1;1;1;0;0;2"],
  "W156" : ["False,False,False;False,False,True;True,False,False;True,True,False;False,True,False;True,True,True", "True;False;False;True;True;False"],
  "W161" : ["12000;30000;80000", "600;1750;12500"],
  "W162" : ["19;10;21;22;25;30", "2;11;0;2;8;18"],
  "W163" : ["2,4,6;4,6,2;4,6,3;6,2,4;6,2,8;2,2,2;2,2,3;9,10,11;10,9,11;10,9,9;2,4,4;2,2,4;3,6,12;12,3,6", "True;True;False;True;False;True;False;True;True;False;False;False;False;False"],
  "W164" : ["1,False;5,False;0,False;6,False;0,True;6,True;1,True;3,True;5,True", "7:00;7:00;10:00;10:00;off;off;10:00;10:00;10:00"],
  "W165" : ["1,2,3;1,3,2;2,1,3;2,3,1;3,1,2;3,2,1", "123;123;123;123;123;123"],
  "W166" : ["1,2,10;1,2,3;4,1,3;4,5,3;4,3,5;-1,10,0;0,-1,10;10,10,8;10,8,9;8,9,10;8,9,7;8,6,9", "True;False;True;False;False;True;True;True;False;False;False;True"],
  "W171" : ["", "1 2 3 4 5 6 7 8 9 10"],
  "W172" : ["", "10 11 12 13 14 15 16 17 18 19 20"],
  "W173" : ["10;20", "55;210"],
  "W174" : ["10;20", "55 55;210 210"],
  "W175" : ["", "2002 2009 2016 2023 2037 2044 2051 2058 2072 2079 2086 2093"],
  "W176" : ["100;150;180", "18;22;24"],
  "W181" : ["hello;hi;h;kitten;java;j", "he;hi;h@;ki;ja;j@"],
  "W182" : ["hello;ab;h;candy;code", "hehehe;ababab;hhh;cacaca;cococo"],
  "W183" : ["last,chars;yo,java;kitten,hi;k,zip;kitten,zip", "ls;ya;ki;kp;kp"],
  "W184" : ["hello;abcdefh;ab;a;kitten;hi;hiya", "he;ab;ab;a;ki;hi;hi"],
  "W185" : ["hello,hi;hi,hello;aaa,b;b,aaa;aaa,1234;aaa,bb;a,bb;bb,a;xyz,ab", "hihellohi;hihellohi;baaab;baaab;aaa1234aaa;bbaaabb;abba;abba;abxyzab"],
  "W186" : ["Hello;java;hi;code;cat;12345;chocolate;bricks", "lloHe;vaja;hi;deco;tca;34512;ocolatech;icksbr"],
  "W191" : ["Chocolate,4;Chocolate,3;IceCream,2;IceCream,1;IceCream,0;xyz,3;Java,4;Java,1", "ChocChoChC;ChoChC;IcI;I;;xyzxyx;JavaJavJaJ;J"],
  "W192" : ["Miracle,2;abcdefg,2;abcdefg,3;Chocolate,3;Chocolates,3;Chocolates,4;Chocolates,100", "Mrce;aceg;adg;Cca;Ccas;Coe;C"],
  "W193" : ["xxggxx;xxgxx;xxggyygxx;g;gg;xxgggxyz;xxggxyg;xxggxygg;mgm;mggm;yyygggxyy", "True;False;False;False;True;True;False;True;False;True;True"],
  "W194" : ["Hello,3;Hello,2;Hello,1;Hello,0;abc,3;1234,2;1234,3", "llollollo;lolo;o;;abcabcabc;3434;234234234"],
  "W195" : ["Word,X,3;This,And,2;This,And,1;Hi,-n,2;A,B,5;abc,XX,3;abc,XX,2;abc,XX,1;XYZ,a,2", "WordXWordXWord;ThisAndThis;This;Hi-nHi;ABABABABA;abcXXabcXXabc;abcXXabc;abc;XYZaXYZ"],
  "W196" : ["edited;edit;ed;jj;jjj;jjjj;jjjk;x;java;javaja", "True;False;True;True;True;True;False;False;False;True"],
  "W1A1" : ["Hiabc,abc;AbC,HiaBc;abc,abXabc;Hiabc,abcd;Hiabc,bc;Hiabcx,bc;abc,abc;xyz,12xyz;yz,12xz;Z,12xz;12,12;abcXYZ,abcDEF;ab,ab12;ab,12ab", "True;True;True;False;True;False;True;True;False;True;True;False;False;True"],
  "W1A2" : ["badxx;xbadxx;xxbadxx;code;bad;ba;xba;xbad;badyy", "True;True;False;False;True;False;False;True;True"],
  "W1A3" : ["catdog;catcat;1cat1cadodog;catxxdogxxdog;catxdogxdogxcat;catxdogxdogxca;dogdogcat;dogogcat;dog;cat;ca;c", "True;False;True;False;True;False;False;True;False;False;True;True"],
  "W1A4" : ["abc,cat;dog,cat;pig,g;pig,doggy", "abcat;dogcat;pig;pigdoggy"],
  "W1A5" : ["Hello,Hi;Hello,java;java,Hello;abc,x;x,abc", "loHi;ellojava;javaello;cx;xc"],
  "W1A6" : ["Hello;java;away;axy;abc;xby;ab;ax;axb;aaa;xbc;bbb;bazz;ba;abxyz;hi;his;xz;zzz", "llo;va;aay;ay;abc;by;ab;a;ab;aa;bc;bb;zz;;abxyz;;s;;z"],
  "W2B1" : ["", "7226"],
  "W2B2" : ["", "73057"],
  "W2B3" : ["../dataFiles/deblank.txt", "Original is 2582 chars, deblanked is 2253 chars"],
  "W1C2" : ["3,1,2,6;4,6,1,2,3;3,3,2,1;3,3,6,1;2,3,6;1,6;1,3", "True;True;False;False;True;True;False"],
  "W1C3" : ["2,2,5;2,4,3;2,4,5;2,2,2;2,3,2;2,3,3;2,7,7;2,3,9;2,9,5", "True;True;False;True;True;True;False;True;False"],
  "W1C4" : ["3,1,2,3,2,7,3;3,1,2,3,3,7,3,2;3,1,2,3,2,1,3;3,1,2,3,1,1;3,1,2,3,1,2", "True;False;True;True;False"],
  "W1C5" : ["2,1,2,2,3,4;2,3,4,2,1,2;2,1,1,2,1,2;2,2,1,2,1,1;2,2,2,2,1,3;2,1,3,2,2,2;2,6,7,2,3,1", "3 4;3 4;1 2;2 1;2 2;1 3;6 7"],
  "W1C6" : ["7,1,0,1,0,0,1,1;3,3,3,2;3,2,2,2;3,3,2,2;5,1,1,0,1,0;1,1;2,1,2;2,2,1;0", "0 0 0 1 1 1 1;2 3 3;2 2 2;2 2 3;0 0 1 1 1;1;2 1;2 1;"],
  "W1D1" : ["2,1,2,2,3,4;2,4,4,2,2,2;2,9,2,2,3,4", "1 2 3 4;4 4 2 2;9 2 3 4"],
  "W1D2" : ["3,1,2,3;3,2,3,5;3,1,2,1;3,3,2,1;3,2,2,3;3,2,3,3", "1 2 0;2 0 5;1 2 1;3 2 1;2 2 0;2 0 3"],
  "W1D3" : ["3,4,5,6;2,1,2;1,3;1,0;3,7,7,7;3,3,1,4;2,2,4", "0 0 0 0 0 6;0 0 0 2;0 3;0 0;0 0 0 0 0 7;0 0 0 0 0 4;0 0 0 4"],
  "W1D4" : ["2,2,2;2,3,3;2,2,3;2,3,2;2,4,5;1,2;1,3;1,0;2,3,4", "True;True;False;False;False;False;False;False;False"],
  "W1D5" : ["4,10,3,5,6;4,7,2,10,9;4,2,10,7,2;2,2,10;2,10,2;2,10,0;2,2,3;2,2,2;1,2;6,5,1,6,1,9,9;4,7,6,8,5;7,7,7,6,8,5,5,6", "7;8;8;8;8;10;1;0;0;8;3;3"],
  "W1D6" : ["3,1,3,2;3,3,1,2;5,3,1,4,5,2;5,3,1,4,5,6;6,3,1,4,1,6,2;6,2,1,4,1,6,2;5,2,1,4,1,6;3,3,5,9;3,5,1,3;3,2,1,2;1,2;2,1,1;1,1;1,0", "True;True;True;False;True;True;False;False;False;True;False;False;False;False"],
  "W1E1" : ["4,1,2,3,4;6,7,1,2,3,4,9;2,1,2;4,5,2,4,7;6,9,0,4,3,9,1", "2 3;2 3;1 2;2 4;4 3"],
  "W1E2" : ["4,2,1,3,5;4,2,1,2,5;4,2,4,2,5;5,1,2,1,2,1;5,3,9,9,9,3;1,2;1,2;1,2;1,1;0;4,9,7,2,9;6,9,7,2,9,2,2;7,9,7,2,9,2,2,6", "True;False;True;False;True;False;False;False;False;False;False;False;True"],
  "W1E3" : ["3,1,2,3;3,5,77,9;3,7,0,0;3,1,2,1;3,0,0,1", "2 3 1;77 9 5;0 0 7;2 1 1;0 1 0"],
  "W1E4" : ["3,1,2,3;4,1,2,3,1;3,1,2,1;1,7;0;2,7,7", "False;True;True;True;False;True"],
  "W1E5" : ["3,0,2,4;3,1,2,3;3,1,2,4;4,2,7,2,8;4,2,7,1,8;4,3,7,2,8;4,2,7,2,1;2,1,2;2,2,2;1,2;1,3;1,0", "True;False;False;True;False;False;False;False;True;True;False;True"],
  "W1E6" : ["5,1,2,3,4,100;7,1,1,5,5,10,8,7;6,-10,-4,-2,-4,-2,0;5,5,3,4,6,2;5,5,3,4,0,100;5,100,0,5,3,4;3,4,0,100;5,0,2,3,4,100;3,1,1,100;3,7,7,7;3,1,7,8;5,4,4,4,4,5;5,4,4,4,1,5;5,6,4,8,12,3", "3;5;-3;4;4;4;4;3;1;7;7;4;4;6"],
  "W1F1" : ["5,2,1,2,3,4;3,2,2,0;3,1,3,5;1,0;4,11,9,0,1;4,2,11,9,0;1,2;3,2,5,12", "3;3;0;1;1;2;1;2"],
  "W1F2" : ["4,1,3,1,4;7,1,3,1,4,4,3,1;4,3,2,2,4;6,3,2,3,2,4,4;7,2,3,2,3,2,4,4;3,3,1,4;3,3,4,1;3,1,1,1;1,1;0;5,7,3,7,7,4;6,3,1,4,3,1,4;6,3,1,1,3,4,4", "1 3 4 1;1 3 4 1 1 3 4;3 4 2 2;3 4 3 4 2 2;2 3 4 3 4 2 2;3 4 1;3 4 1;1 1 1;1;;7 3 4 7 7;3 4 1 3 4 1;3 4 1 3 4 1"],
  "W1F3" : ["3,1,2,2;3,4,4,1;5,4,4,1,2,2;4,1,2,3,4;3,3,5,9;5,1,2,3,4,4;4,2,2,3,4;6,1,2,3,2,2,4;7,1,2,3,2,2,4,4;2,1,2;2,2,2;2,4,4;1,2;1,0", "True;True;False;False;False;True;True;True;False;False;True;True;False;False"],
  "W1F4" : ["3,1,2,3;3,11,5,9;3,2,11,3;3,11,3,3;3,11,11,3;2,2,2;3,2,11,2;3,0,0,1", "3 3 3;11 11 11;3 3 3;11 11 11;11 11 11;2 2;2 2 2;1 1 1"],
  "W1F5" : ["3,1,2,3,3,2,3,10;3,1,2,3,3,2,3,5;3,1,2,3,3,2,3,3;2,5,3,2,5,5;2,5,3,2,4,4;2,5,3,2,3,3;2,5,3,2,2,2;2,5,3,2,1,1;2,5,3,2,0,0;1,4,1,4;1,4,1,5", "2;3;2;1;2;1;1;1;0;0;1"],
  "W1F6" : ["6,1,2,2,3,4,4;5,1,1,2,1,1;5,1,1,1,1,1;3,1,2,3;10,2,2,1,1,1,2,1,1,2,2;11,0,2,2,1,1,1,2,1,1,2,2;12,0,0,2,2,1,1,1,2,1,1,2,2;13,0,0,0,2,2,1,1,1,2,1,1,2,2;0", "2;2;1;0;4;4;5;5;0"],
  "W1G1" : ["6,1,2,2,3,4,4;5,1,1,2,1,1;5,1,1,1,1,1;3,1,2,3;10,2,2,1,1,1,2,1,1,2,2;11,0,2,2,1,1,1,2,1,1,2,2;12,0,0,2,2,1,1,1,2,1,1,2,2;13,0,0,0,2,2,1,1,1,2,1,1,2,2;0", "2;2;1;0;4;4;5;5;0"],
  "W1H1" : ["Hello,World;EXTREME;Steal,Broom", "Xello Xorld Hello World ello orld;XXXXXXX ETREME ;Xteal Xroom Steal Broom teal room"],
  "W1H2" : ["hello;xxyy;aaaa;aaab;aa;a;noadjacent;abba;abbba", "hel*lo;x*xy*y;a*a*a*a;a*a*ab;a*a;a;noadjacent;ab*ba;ab*b*ba"],
  "W1H3" : ["7,1,0,1,0,0,1,1;3,3,3,2;3,2,2,2;3,3,2,2;5,1,1,0,1,0;1,1;2,1,2;2,2,1;0", "0 0 0 1 1 1 1;2 3 3;2 2 2;2 2 3;0 0 1 1 1;1;2 1;2 1;"],
  "W1H4" : ["4,0,5,0,3;4,0,4,0,3;3,0,1,0;3,0,1,5;3,0,2,0;1,1;1,0;0;6,7,0,4,3,0,2;6,7,0,4,3,0,1;6,7,0,4,3,0,0;6,7,0,1,0,0,7", "5 5 3 3;3 4 3 3;1 1 0;5 1 5;0 2 0;1;0;;7 3 4 3 0 2;7 3 4 3 1 1;7 3 4 3 0 0;7 7 1 7 7 7"],
  "W1H5" : ["2,3,2,2,4,5", "3 2 4 5"],
  "W1H6" : ["3,1,2,3;3,11,5,9;3,2,11,3;3,11,3,3;3,11,11,3;2,2,2;3,2,11,2;3,0,0,1", "3 3 3;11 11 11;3 3 3;11 11 11;11 11 11;2 2;2 2 2;1 1 1"],
  "W1I1" : ["4,1,4,1,4;4,1,4,2,4;2,1,1;2,4,1;1,2;1,0;4,1,4,1,3;3,3,1,3;1,1;1,4;2,3,4;3,1,3,4;3,1,1,1;4,1,1,1,5;4,4,1,4,1", "True;False;True;True;False;False;False;False;True;True;False;False;True;False;True"],
  "W1I2" : ["2,3,2;2,4,5;2,3,5;2,5,2", "True;False;True;True"],
  "W1I3" : ["3,2,3,2;3,2,4,5;3,2,3,5;3,2,5,2", "3 2 2;4 5 2;3 5 2;5 2 2"],
  "W1I4" : ["5,5,3,3,3,2,2,4;5,5,3,6,7,2,0,1;5,5,3,3,3,2,0,4", "1;1;2"],
  "W1I5" : ["catdog;catcat;1cat1cadodog;catxxdogxxdog;catxdogxdogxcat;catxdogxdogxca;dogdogcat;dogogcat;dog;cat;ca;c", "True;False;True;False;True;False;False;True;False;False;True;True"],
  "W1I6" : ["5,5,3,3,3,2,2,4;5,5,3,6,7,2,0,1;5,5,3,3,3,2,0,4", "1;0;2"],
  "W1J1" : ["2,3,2,2,4,5;2,4,5,2,3,2;2,3,4,2,4,3", "4 5;4 5;3 4"],
  "W1J2" : ["Miracle,2;abcdefg,2;absdefg,3", "Mrce;aceg;adg"],
  "W1J3" : ["abXYabc,1;abXYabc,2;abXYabc,3;xyzxyxyxy,2;xyzxyxyxy,3;Hi12345Hi6789Hi10,1;Hi12345Hi6789Hi10,2;Hi12345Hi6789Hi10,3;Hi12345Hi6789Hi10,4;a,1;aa,1;ab,1", "True;True;False;True;False;True;True;True;False;False;True;False"],
  "W1J4" : ["4,1,3,1,4;7,1,3,1,4,4,3,1;4,3,2,2,4;6,3,2,3,2,4,4;7,2,3,2,3,2,4,4;3,3,1,4;3,3,4,1;3,1,1,1;1,1;0;5,7,3,7,7,4;6,3,1,4,3,1,4;6,3,1,1,3,4,4", "1 3 4 1;1 3 4 1 1 3 4;3 4 2 2;3 4 3 4 2 2;2 3 4 3 4 2 2;3 4 1;3 4 1;1 1 1;1;;7 3 4 7 7;3 4 1 3 4 1;3 4 1 3 4 1"],
  "W1J5" : ["3,1,2,2;4,1,2,1,2;3,2,1,2;4,2,2,1,2;1,3;2,4,1;3,2,2,2;3,2,2,6;4,2,4,2,2;5,2,1,2,2,2;2,1,2;1,0;4,3,3,2,2;4,5,2,5,2", "True;False;False;True;False;False;True;True;True;True;False;False;True;False"],
  "W1J6" : ["5,5,3,3,2,1,2,4;5,5,3,6,7,2,0,1;5,5,3,3,3,2,0,4", "True;True;False"],
  "W1K1" : ["3,1,7,7;4,1,7,1,7;5,1,7,1,1,7;5,7,7,1,1,7;6,2,7,2,2,7,2;6,2,7,2,2,7,7;6,7,2,7,2,2,7;6,7,2,6,2,2,7;3,7,7,7;3,7,1,7;3,7,1,1;2,1,2;2,1,7;1,7", "True;True;False;True;False;True;True;False;True;True;False;False;False;False"],
  "W1K2" : ["3,1,2,3;4,1,2,3,4;3,2,3,4;4,1,1,4,4;4,2,2,4,4;4,2,3,4,1;3,2,1,1;2,1,4;1,2;2,2,1;1,1;1,4;1,0;4,1,1,1,1;4,9,4,4,1;4,4,2,3,1;4,4,2,3,5;3,4,4,2;3,1,4,4", "True;False;True;False;True;False;True;False;True;True;True;True;True;True;False;False;True;True;False"],
  "W1K3" : ["5,3,1,3,1,3;4,3,1,3,3;5,3,4,3,3,4;6,1,3,1,3,1,2;6,1,3,1,3,1,3;5,1,3,3,1,3;8,1,3,1,3,1,3,4,3;7,3,4,3,4,3,4,4;3,3,3,3;2,1,3;1,3;1,1", "True;False;False;False;True;False;False;True;False;False;False;False"],
  "W1K4" : ["5,5,3,3,3,2,2,4;5,5,3,6,7,2,0,1;5,5,7,3,4,2,0,4", "0;0;2"],
  "W1K5" : ["codex;xxhixx;xhixhix;hiy;h;x;xxx;yyhxyi;hihi", "codey;yyhiyy;yhiyhiy;hiy;h;y;yyy;yyhyyi;hihi"],
  "W1K6" : ["abcXXXabc,3;xxxabyyyycd,4;a,2;XXXabc,3;XXXXabc,4;XXXXXabc,4;222abyyycdXXX,3;abYYYabXXXXXab,4;abYYXabXXYXXab,2;abYyXabXXYXXab,2;122abhhh2,2", "1;1;0;1;1;2;3;2;3;2;3"],
  "W1L1" : ["3,1,7,7;4,1,7,1,7;5,1,7,1,1,7;5,7,7,1,1,7;6,2,7,2,2,7,2;6,2,7,2,2,7,7;6,7,2,7,2,2,7;6,7,2,6,2,2,7;3,7,7,7;3,7,1,7;3,7,1,1;2,1,2;2,1,7;1,7", "True;True;False;True;False;True;True;False;True;True;False;False;False;False"],
  "W1M1" : ["3,1,7,7;4,1,7,1,7;5,1,7,1,1,7;5,7,7,1,1,7;6,2,7,2,2,7,2;6,2,7,2,2,7,7;6,7,2,7,2,2,7;6,7,2,6,2,2,7;3,7,7,7;3,7,1,7;3,7,1,1;2,1,2;2,1,7;1,7", "True;True;False;True;False;True;True;False;True;True;False;False;False;False"],
  'zzzz' : ['1','1']}

_blanks = {"[" : " ", "]" : " ", "," : " ", "(" : " ", ")" : " ", "'" : " "}

def _replace(string, substitutions):
  substrings = sorted(substitutions, key=len, reverse=True)
  regex = re.compile('|'.join(map(re.escape, substrings)))
  return regex.sub(lambda match: substitutions[match.group(0)], string)

def _prRed(skk, end = " "): _print("\033[01m\033[91m{}\033[00m" .format(skk), end = end)
def _prGreen(skk, end = " "): _print("\033[01m\033[32m{}\033[00m" .format(skk), end = end)
def _prBlue(skk, end = " "): _print("\033[04m\033[01m\033[34m{}\033[00m" .format(skk), end = end)

def _deblank(s):
  result = ""
  for c in s:
    if c != " ":
      result += c
  return result

class PyTest:
  def init(self):
    filename_in = sys.argv[0]
#    slash = "\\"
#    if os.name == "posix": slash = "/"
#    slash_last = filename_in.rfind(slash)
#    slash_before = filename_in[:slash_last].rfind(slash)
#    self.project_name = filename_in[slash_before + 1 : slash_last]
#    self.program_name = filename_in[slash_last + 1 : -3]
    self.log_filename = "PyTest.log"
    if len(filename_in) <= 7:
      self.program_name = filename_in[:-3]
    else:
      self.program_name = filename_in[-7:-3]
    dt = str(datetime.datetime.now())
    dt = dt[:dt.index(".")]
    self.log_line = socket.gethostname() + "," +\
                    getpass.getuser() + "," +\
                    self.program_name + ","
    self.offset = 0
    for c in getpass.getuser():
      self.offset += ord(c)
    if filename_in.find("_test") != -1: return
    fin = open(filename_in)
    filename_test = filename_in[:-3] + "_test.py"
    fout = open(filename_test, "w")
    in_program = False
    for line in fin:
      if line.startswith("##////"): continue
      if line.find("from PyTest import *") != -1:
        fout.write(line)
        in_program = True
        fout.write("for test in _tests(" + "'" + filename_test[:-8] + "'" + "):\n")
        fout.write("  try:\n")
      else:
        if in_program: fout.write("    ")
        fout.write(line)
    fout.write("\n    _check()\n" +
                 "  except:\n" +
                 "    _check(newline = False)\n" +
                 "    import sys\n" +
                 "    type, obj, tb = sys.exc_info()\n" +
                 "    msg = 'Error: ' + str(type)[8:-2] + ' at line ' + str(tb.tb_lineno)\n"
                 "    _prRed(msg)\n" +
                 "    _print()\n" +
                 "    _logit(msg)\n" +
                 "    exit(0)\n" +
                 "_logit()\n")
    fout.close()
    try:
      exec(open(filename_test).read())
    except:
      type, obj, tb = sys.exc_info()
      if str(type)[8:-2] != "SystemExit":
        msg = "Error: " + str(type)[8:-2] + " at line " + str(tb.tb_lineno)
        _prRed(msg, end = "\n")
        self.logit(msg)
    os.remove(filename_test)
    exit(0)

  def tests(self, filename):
    line = _test_data[filename[-4:]][0]
    self.test_total = line.count(";") + 1
    self.test_count = 0
    self.save_inputs = line.split(";")
    max = 0
    for i in range(len(self.save_inputs)):
      self.save_inputs[i] = self.save_inputs[i].strip()
      if len(self.save_inputs[i]) > max: max = len(self.save_inputs[i])
    for i in range(len(self.save_inputs)):
      self.save_inputs[i] += (max - len(self.save_inputs[i])) * " "
    self.inputs = line.replace(";", ",") + ","
    self.inputs = self.inputs.split(",")
    self.input_index = 0
    line = _test_data[filename[-4:]][1]
    self.save_expected = line.split(";")
    max = 0
    for i in range(len(self.save_expected)):
      self.save_expected[i] = self.save_expected[i].strip()
      if len(self.save_expected[i]) > max: max = len(self.save_expected[i])
    for i in range(len(self.save_expected)):
      self.save_expected[i] += (max - len(self.save_expected[i])) * " "
    self.outputs = line.split(";")
    for i in range(len(self.outputs)):
      self.outputs[i] = self.outputs[i].replace(" ", "").strip()
    self.output_index = 0
    return [i for i in range(self.test_total)]

  def input(self):
    self.input_index += 1
    try:
      return self.inputs[self.input_index - 1]
    except:
      _prRed("Error: No more input data")
      exit(0)

  def check(self, data, newline):
    global _log_line
    passed = True
    try:
      passed = _deblank(data) == _deblank(self.outputs[self.output_index])
      self.output_index += 1
    except:
      _prRed("Error: Too much output")
      exit(0)
    if self.test_count == 0:
      _prBlue("Results")
      if self.test_total >= 9: _print(" ", end = "")
      _print("      | ", end = "")
      _prBlue("Input")
      _print(max((len(self.save_inputs[0]) - 5), 0) * " " + "| ", end = "")
      _prBlue("Expected")
      _print(max((len(self.save_expected[0]) - 8), 0) * " " + "| ", end = "")
      _prBlue("Program")
      _print("")
    _prGreen("Test") if passed else _prRed("Test")
    if self.test_count + 1 < 10 and self.test_total >= 9: _print(" ", end = "")
    _prGreen(self.test_count + 1) if passed else _prRed(self.test_count + 1)
    _prGreen("Passed") if passed else _prRed("Failed")
    _print("|", end = " ")
    _print(self.save_inputs[self.test_count].replace(",", " ") +
           max((5 - len(self.save_inputs[0])), 0) * " ", end = " | ")
    _print(self.save_expected[self.test_count] +
           max((8 - len(self.save_expected[0])), 0) * " ", end = " |")
    _print(" " + _replace(str(data), _blanks).replace("  ", " "), end = "")
    if newline: _print("")
    if passed:
      self.log_line += "P"
    else:
      self.log_line += "F"
    self.test_count += 1

  def logit(self, msg = ""):
    log_file = open(self.log_filename, "a")
    if msg != "": self.log_line += msg
    self.log_line += ","
    try:
      dt = time.ctime(os.path.getmtime(self.program_name + ".py"))
    except:
      dt = "Missing file " + self.program_name + ".py"
    self.log_line += dt + ","
    eline = ""
#    for c in self.log_line:
#      eline += chr((ord(c) + self.offset) % 240 + 12)
    log_file.write(self.log_line + "\n")
    log_file.close()
    self.selector()

  def selector(self, all = False):
    status = {}
    fail_counts = {}
    pass_counts = {}
    log_times = {}
    times = {}
    computers = []
    users = []
    projects = []
    log_file = open(self.log_filename, "r")
    for line in log_file:
#      line = ""
#      for c in eline:
#        line += chr((ord(c) - self.offset) % 240 - 12)
      data = line.split(",")
      if data[0] not in computers:
        computers.append(data[0])
      if data[1] not in users:
        users.append(data[1])
#      if data[2] not in projects:
#        projects.append(data[2])
      name = data[2]
      if name.startswith("W"):
        tests = data[3]
        log_times[name] = data[4]
        if tests.find("Error:") == -1:
          status[name] = tests.find("F") == -1
          if status[name]:
            pass_counts[name] = pass_counts.get(name, 0) + 1
          else:
            fail_counts[name] = fail_counts.get(name, 0) + 1
        else:
          status[name] = False
          fail_counts[name] = fail_counts.get(name, 0) + 1
    line_count = 0
    completed = 0
    original_time = None
    for key in sorted(_test_data.keys()):
      if key in status:
        try:
          times[key] = time.ctime(os.path.getmtime(key + ".py"))
        except:
          times[key] = "Missing file " + key + ".py"
#        if times[key] != log_times[key]:
#          _print("\nDifferent log time:", key, times[key], log_times[key])
        fc = 0
        pc = 0
        try:
          fc = str(fail_counts[key])
        except:
          fc = "0"
        try:
          pc = str(pass_counts[key])
        except:
          pc = "0"
        if status[key]:
          _prGreen(key + "(", end = "")
          _prRed(fc, end = "")
          _prGreen("/" + pc + ")")
          completed += 1
        else:
          _prRed(key + "(", end = "")
          _prRed(fc + "/", end = "")
          _prGreen(pc, end = "")
          _prRed(")")
        line_count += 1
        if line_count % 6 == 0: _print()
      elif all and key.startswith("W1"):
        _print(key + "      ", end = "")
        line_count += 1
        if line_count % 6 == 0: _print()
      elif key != "zzzz":
        if original_time == None:
          try:
            original_time = time.ctime(os.path.getmtime(key + ".py"))
          except:
            original_time = "Missing file " + key + ".py"
#        elif original_time != time.ctime(os.path.getmtime(key + ".py")):
#          _print("\nOriginal different:", key, original_time, time.ctime(os.path.getmtime(key + ".py")))
    _print()
    _prBlue("Attempted " + str((len(status) * 100) // len(_test_data)) + "%" +
           ", Completed " + str((completed * 100) // len(_test_data)), end = "\n")
#    +"%, Computers: " +
#           " ".join(computers) + ", Users: " + " ".join(users) + ", Projects: " + " ".join(projects))
    log_file.close()

  def log(self):
    log_file = open(self.log_filename, "r")
    for line in log_file:
#      line = ""
#      for c in eline:
#        line += chr((ord(c) - self.offset) % 240 - 12)
      _print(line)
    log_file.close()

_tester = PyTest()

def input(prompt = ""):
  return _tester.input()

_print = print
_line = ""
def print(*out, sep = "", end = " "):
  global _line
  for i in range(len(out)):
    if type(out[i]) is list:
      for j in range(len(out[i])):
        _line += str(out[i][j]) + end
    else:
      _line += str(out[i]) + end

def _check(newline = True):
  global _line
  _tester.check(_line, newline)
  _line = ""

def _logit(msg = ""):
  _tester.logit(msg)

def log():
  _tester.log()

def selector():
  _tester.selector(all = True)

def _tests(filename):
  return _tester.tests(filename)

_tester.init()
