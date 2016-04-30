#! /bin/sh

# Trenuje klasifikator na tranovacich datech

TARGET_TRAIN="../../../DATA/target_train/"
TARGET_DEV="../../../DATA/target_dev/"
NON_TARGET_TRAIN="../../../DATA/non_target_train/"
NON_TARGET_DEV="../../../DATA/non_target_dev/"

NEURAL_FOLDER="NEURAL_NETWORKS"
NEURAL_NAME="SPEAKER_NTW"

./train.py $TARGET_TRAIN $NON_TARGET_TRAIN $TARGET_DEV $NON_TARGET_DEV $NEURAL_FOLDER $SPEECH_NTW
