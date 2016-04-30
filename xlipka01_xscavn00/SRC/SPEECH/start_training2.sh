#! /bin/sh

# Trenuje klasifikator na tranovacich datech

TARGET_TRAIN="../../../DATA2/target_train/"
TARGET_DEV="../../../DATA2/target_dev/"
NON_TARGET_TRAIN="../../../DATA2/non_target_train/"
NON_TARGET_DEV="../../../DATA2/non_target_dev/"

NEURAL_FOLDER="NEURAL_NETWORKS"
NEURAL_NAME="SPEAKER_NTW_ALL_DATA"

./train.py $TARGET_TRAIN $NON_TARGET_TRAIN $TARGET_DEV $NON_TARGET_DEV $NEURAL_FOLDER $NEURAL_NAME
