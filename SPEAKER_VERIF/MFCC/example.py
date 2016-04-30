from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav


(rate,sig) = wav.read("../../DATA/target_train/m430_01_p03_i0_0.wav")
print(type(rate))
print(type(sig))
	
mfcc_feat = mfcc(sig,rate)
fbank_feat = logfbank(sig,rate)

print(fbank_feat[1:3,:])
