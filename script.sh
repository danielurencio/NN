for year in 2010 2011 2012 2013 2014 2015; do
 for month in 1 2 3 4 5 6 7 8 9 10 11 12; do
  for slow in 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24; do
   fast=2;
    while [ `expr $slow - $fast` != 0 ]; do
     node backtest $year $month $fast $slow;
     echo $year $month $fast $slow;
     fast=`expr $fast + 1`;
    done
  done
 done
done
