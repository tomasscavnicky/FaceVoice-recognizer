#! /bin/sh

# COMMON
TEST_DATA="PATH"

S_OUTPUT=MFCC_NEURALNTW.output
I_OUTPUT=EIGENFACES_PCA.output
SI_OUTPUT=MFCC_NEURALNTW_EIGENFACES_PCA.output


# SPEECH
NEURAL_NETWORK="SPEECH/NEURAL_NETWORKS/NET_ERR_3_NET"

# IMAGE
TRAIN_DATA="Path_to_train_data"

# ---------------------------------------------------------
# RECOGNIZING DATA

SPEECH/recognize.py $TEST_DATA $NEURAL_NETWORK $S_OUTPUT
IMAGE/somtehing.py

SPEECH_IMAGE/speech_image.py $S_OUTPUT $I_OUTPUT $SI_OUTPUT

echo "Successed"
