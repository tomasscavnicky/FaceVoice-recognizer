#! /bin/sh

# Spustí klasifikaci nad testovanými daty všemi typmi klasifikátorů

# COMMON
TEST_DATA="../EVAL/"

S_OUTPUT=Audio_Mfcc_NeuralNet
I_OUTPUT=Image_Eigenfaces_Pca
SI_OUTPUT=Both_Mfcc_NeuralNet_Eigenfaces_Pca


# SPEECH
NEURAL_NETWORK="SRC/SPEECH/NEURAL_NETWORKS/SPEAKER_NTW1_NET"

# IMAGE
TRAIN_DATA="Path_to_train_data"

# ---------------------------------------------------------
# RECOGNIZING DATA

SRC/SPEECH/speaker_recognition.py $TEST_DATA $NEURAL_NETWORK $S_OUTPUT
SRC/IMAGE/image_recognition.py $TEST_DATA $I_OUTPUT

SRC/SPEECH_IMAGE/speech_image.py $S_OUTPUT $I_OUTPUT $SI_OUTPUT

echo "Successed"
