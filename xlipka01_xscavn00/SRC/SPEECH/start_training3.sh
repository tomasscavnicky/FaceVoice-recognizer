#! /bin/sh

# Trenuje klasifikator na tranovacich datech

TARGET_TRAIN="../../../DATA3/target_train/"
TARGET_DEV="../../../DATA3/target_dev/"
NON_TARGET_TRAIN="../../../DATA3/non_target_train/"
NON_TARGET_DEV="../../../DATA3/non_target_dev/"

NEURAL_FOLDER="NEURAL_NETWORKS"
NEURAL_NAME="SPEAKER_NTW_NEE"

./train.py $TARGET_TRAIN $NON_TARGET_TRAIN $TARGET_DEV $NON_TARGET_DEV $NEURAL_FOLDER $NEURAL_NAME
