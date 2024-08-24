# IBES_selected
Selected IBES data for research EC


1. unzip.py (to unzip raw file to dta file)

remark:
1.  For estimates —> no way to link estimate to analyst id like the other tables (TP, and Rec). DO i miss something? or is it not a big deal later. 
2.  what does this dataset do?

TICKER	CUSIP	CNAME	OFTIC	HMKTCD	MSCIPF	USFIRM	SDATES	EDATES
0	0000	NaN	TALMER BANCORP	IPO-TL	NaN	NaN	1.0	2014-02-08	2014-02-12
1	0000	87482X10	TALMER BANCORP	TLMR	TLMR	NaN	1.0	2014-02-12	2014-03-10
2	0000	87482X10	TALMER BANCORP	TLMR	TLMR	NaN	1.0	2014-03-10	2014-05-12
3	0000	87482X10	TALMER BANCORP	TLMR	TLMR	0.0	1.0	2014-05-12	NaN
4	0001	26878510	EP ENERGY	EPE	EPE	NaN	1.0	2014-02-08	2014-02-26

3. Statistics regarding: 

a. 11812 distinctive analysts
       COUNT_RECOM  COUNT_TP
count        11812     11812
mean            32       139
std             58       295
min              0         0
25%              2         2
50%              9        18
75%             38       123
max           1733      3866

b. 19359 distinctive (analyst, broker) pair, on average one analyst works or has worked for 2 brokers 
       COUNT_RECOM  COUNT_TP
count        19359     19359
mean            19        85
std             38       204
min              0         0
25%              1         1
50%              6        11
75%             23        69
max           1733      3040

c. 174053 distinctive (analyst, stock) coverage pair, means per analyst, they cover about 15 stocks
       COUNT_RECOM_x  COUNT_TP
count         174053         174053
mean               2              9
std                2             13
min                0              0
25%                1              1
50%                1              5
75%                3             12
max               73            258

d. 204545 distinctive (analyst, broker, stock) coverage pair
       COUNT_RECOM  COUNT_TP
count       204545    204545
mean             1         8
std              1        11
min              0         0
25%              1         1
50%              1         4
75%              2        10
max             73       228

For recommendations / tp: broker amount: about 800

e. looking at c. and d., does it look normal that most of the analysts do not cover same stocks anymore when they changed employer (broker)? i think it is strange...

f. unique id... analyst name, 

scenario:
IBES data

name          ID     --> name'   BROKER   coveraging stock
ZHU H.    x123       ZHU H.1     gs
ZHU H.    x234       ZHU H.2     jp
ZHU H.    x345       ZHU H.3     citi

CIQ data
full name     BROKER
ZHU HONG      gs
ZHU Heng      jp
ZHu Hang      citi

with the plague of names

step 1. 
same name+initial, with different ids. --> 

step 2. 
with broker name -->

