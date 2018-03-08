import FileHandler
import Calculator
import numpy
import scipy.signal as ssg
import scipy.fftpack as sfft

divisor = 32768.0

#Main function to run the program
def Main():
    print("Program Started")
    #declaration of_array to store the wav files' data
    wav_list = []

    print("Reading")
    #calling function to read the file that contains the wav files to be read
    wav_list = FileHandler.read_files(wav_list)
    print("Done")


    print("Calculating")

    #Dividing the samples by the desired divisor
    for wav_file_info in wav_list:
        wav_file_info.buffers = numpy.divide(wav_file_info.buffers, divisor)

    hamming_window = ssg.hamming(1024)

    for wav_file_info in wav_list:
        wav_file_info.buffers = wav_file_info.buffers*hamming_window

    for wav_file_info in wav_list:
        i = 0
        for buffer in wav_file_info.buffers:
            buffer_dft = sfft.fft(buffer)
            l = int((len(buffer_dft) / 2))
            wav_file_info.abs_buffers_dft.append(numpy.absolute(buffer_dft[0:l + 1]))
            i = i + 1

    for wav_info in wav_list:
        # Calculate Spectral Centroid for each buffers
        Calculator.calculate_SC(wav_info)
        # Calculate Mean for the SC values of the buffers and add to the list of mean calculated for features
        wav_info.mean_of_features.append(numpy.mean(wav_info.SC))
        # Calculate STD for the SC values of the buffers and add to the list of std calculated for features
        wav_info.std_features.append(numpy.std(wav_info.SC))

    for wav_info in wav_list:
        # Calculate Spectral Roll-Off for each buffer
        Calculator.calculate_SRO(wav_info)
        # Calculate Mean for the SRO values of the buffers and add to the list of mean calculated for features
        wav_info.mean_of_features.append(numpy.mean(wav_info.SRO))
        # Calculate STD for the SRO values of the buffers and add to the list of std calculated for features
        wav_info.std_features.append(numpy.std(wav_info.SRO))

    for wav_info in wav_list:
        # Calculate Spectral Flatness Measure for each buffer
        Calculator.calculate_SFM(wav_info)
        # Calculate Mean for the SFM values of the buffers and add to the list of mean calculated for features
        wav_info.mean_of_features.append(numpy.mean(wav_info.SFM))
        # Calculate STD for the SFM values of the buffers and add to the list of std calculated for features
        wav_info.std_features.append(numpy.std(wav_info.SFM))

    for wav_info in wav_list:
        # Calculate Peak-to-average ratio for each buffer
        Calculator.calculate_PARFFT(wav_info)
        # Calculate Mean for the PARFFT values of the buffers and add to the list of mean calculated for features
        wav_info.mean_of_features.append(numpy.mean(wav_info.PARFFT))
        # Calculate STD for the PARFFT values of the buffers and add to the list of std calculated for features
        wav_info.std_features.append(numpy.std(wav_info.PARFFT))


    for wav_info in wav_list:
        # Calculate Spectral Flux
        Calculator.calculate_SF(wav_info)
        # Calculate Mean for the SF values of the buffers and add to the list of mean calculated for features
        wav_info.mean_of_features.append(numpy.mean(wav_info.SF))
        # Calculate STD for the SF values of the buffers and add to the list of std calculated for features
        wav_info.std_features.append(numpy.std(wav_info.SF))

    print("Done")

    print("Writing File")

    #Calling the function to output the results
    FileHandler.write_output(wav_list)

    print("Done")


Main()








