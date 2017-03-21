#!python
import sys
import os
import wave
import numpy as np

from vad import VoiceActivityDetector

def save_wav(begin, end , inputfile, outputfile):
    inf = wave.open(inputfile, "rb")
    params = inf.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    str_data = inf.readframes(nframes)
    wave_data = np.fromstring(str_data, dtype=np.short)

    time = np.arange(0, nframes) * (1.0 / framerate)
    f  = wave.open(outputfile, "wb")
    print begin, end
    print begin*framerate, end*framerate
    result_data = wave_data[int(begin*framerate):int(end*framerate)]
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(framerate)
    f.writeframes(result_data.tostring())
    f.close()


def split_wavs(inputfile, basedir):
    v = VoiceActivityDetector(inputfile)
    raw_detection = v.detect_speech()
    speech_labels = v.convert_windows_to_readible_labels(raw_detection)
    out_file_list = []
    
    begin = speech_labels[0]["speech_begin"]
    last_end = speech_labels[0]["speech_end"]
    valid_begin = begin
    valid_end = last_end
    num = len(speech_labels)
    i = 0
    for labels in speech_labels[1:]:
        i += 1
        end = labels["speech_end"]
        if end - begin > 59:
            valid_end = last_end
            valid_begin = begin
            print valid_begin, valid_end
            outputfile = os.path.join(basedir, "out_"+str(i)+".wav")
            save_wav(valid_begin, valid_end, inputfile, outputfile)
            out_file_list.append(outputfile)
        elif end - begin > 50:
            valid_end = end
            valid_begin = begin 
            print valid_begin, valid_end
            outputfile = os.path.join(basedir, "out_"+str(i)+".wav")
            save_wav(valid_begin, valid_end, inputfile, outputfile)
            out_file_list.append(outputfile)

            if i < num: 
                begin = speech_labels[i+1]["speech_begin"]

    if valid_end < speech_labels[-1]["speech_end"]:
        valid_begin= begin
        valid_end = speech_labels[-1]["speech_end"]
        print begin , speech_labels[-1]["speech_end"]
        outputfile = os.path.join(basedir, "out_"+str(i)+".wav")
        save_wav(valid_begin, valid_end, inputfile, outputfile)
        out_file_list.append(outputfile)
    return out_file_list


if __name__ == "__main__":
    split_wavs(inputfile, basedir)
