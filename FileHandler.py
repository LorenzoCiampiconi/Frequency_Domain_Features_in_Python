import scipy.io.wavfile
import numpy
import librosa as lib
from WavInfo import WavInfo

#Define path and useful variables such as the separator used in the file to be queried
read_path = "C:/Users/Lorenzo/Documents/Polimi/Singapore/Sound and Music Computing/Assignment/Final Project/"
output_path = "C:/Users/Lorenzo/Documents/Polimi/Singapore/Sound and Music Computing/Assignment/Final Project/Feauters Extracted"
query_list_file_name = "genre-classification.mf"
output_file_name = "Frequency-Domain.arff"
sep = "\t"
range = 1024
hop = 512

header_lines = ["@RELATION music_speech","@ATTRIBUTE SC_MEAN NUMERIC","@ATTRIBUTE SRO_MEAN NUMERIC",
                "@ATTRIBUTE SFM_MEAN NUMERIC","@ATTRIBUTE PARFFT_MEAN NUMERIC","@ATTRIBUTE FLUX_MEAN NUMERIC",
                "@ATTRIBUTE SC_STD NUMERIC","@ATTRIBUTE SRO_STD NUMERIC","@ATTRIBUTE SFM_STD NUMERIC",
                "@ATTRIBUTE PARFFT_STD NUMERIC","@ATTRIBUTE FLUX_STD NUMERIC","@ATTRIBUTE class {blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock}"]

data = "@DATA"




# This function get an array and fill it with the desired object(WavInfo) by reading from the file
def read_files(wav_list):

    #open the file
    with open(read_path + query_list_file_name, "r") as query_list_file:
        j = 0
        #read each line
        for line in query_list_file:
            print(j)
            #instantiate new WavInfo object
            wav_info = WavInfo()

            #getting file name by cutting the string after "\t"
            wav_info.file_name = line.partition(sep)[0]

            #getting file label by cutting the string before "\t"
            wav_info.label = line.partition(sep)[2].strip('\n')

            #Reading the samples from the wav file
            samples = lib.load(read_path + wav_info.file_name)[0]

            j += 1

            reading = True
            i = 0

            while(reading):
                if(i*hop + range >= len(samples)):
                    reading = False
                else:
                    wav_info.buffers.append(samples[(i*hop):(i*hop) + range])

                i = i + 1





            #adding the object to the list
            wav_list.append(wav_info)

    #returning the list
    return wav_list

#write the output to the desired output_file
def write_output(wav_list):

    #open the file
    with open(output_path + output_file_name, "w") as output_file:

        #print header
        for line in header_lines:
            output_file.write(line + "\n")

        output_file.write(data + "\n")
        #read each object

        i = 0
        for wav_info in wav_list:

            print(i)

            #composing the string to be written, reformatting the float values, first the Means, stripping the "[]"
            line = str(['%.6f' % elem for elem in wav_info.mean_of_features]).strip("[]")
            #second the standard deviations, stripping the "[]"
            line = line + "," + str(['%.6f' % elem for elem in wav_info.std_features]).strip("[]")
            #adding the label {music, speech}
            line = line + "," + wav_info.label

            #remove white space and "'"
            line = line.replace(" ", "").replace("'", "")

            #writing the line on the file
            output_file.write(line + "\n")

            i += 1



