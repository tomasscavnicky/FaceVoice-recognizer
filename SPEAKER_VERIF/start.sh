#! /bin/sh

rm -f OUTPUT.txt
./train.py ../DATA/target_train/ ../DATA/non_target_train/ ../DATA/target_dev/ ../DATA/non_target_dev/ 
