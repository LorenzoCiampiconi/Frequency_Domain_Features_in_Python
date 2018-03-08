import numpy
import math
import scipy

L = 0.85

#definition of the function that calculate SC
#for each buffer of the wav_info object

def calculate_SC(wav_info):
    #create a sequence [0,1,2,3,...,N] | N = len of a Buffer
    n_seq = list(range(0, len(wav_info.abs_buffers_dft[0])))

    #calculate for each buffer SC by the definition
    for buffer_dft in wav_info.abs_buffers_dft:
        #calculate the sum at the numerator
        ksum = numpy.sum(n_seq * buffer_dft)
        #calculate the sum at the denominator
        sum = numpy.sum(buffer_dft)
        #append the division of the two sum, by the definition of SC
        SC = ksum/sum
        wav_info.SC.append(SC)

#definition of the function that calculate SRO
#for each buffer of the wav_info object
def calculate_SRO(wav_info):

    # calculate for each buffer SC by the definition
    for buffer_dft in wav_info.abs_buffers_dft:

        #sum the sample of the dft buffer
        sum = numpy.sum(buffer_dft)

        sum1 = 0
        k = 0
        #counting the k steps before the SRO condition is reached
        while(L * sum > sum1):
            sum1 = sum1 + buffer_dft[k]
            k = k + 1

        #one step must be ignored as the k = k + 1 will be
        #called before checking the condition
        SRO = k - 1

        #append SRO for this buffer
        wav_info.SRO.append(SRO)

#definition of the function that calculate SFM
#for each buffer of the wav_info object
def calculate_SFM(wav_info):

    #calculate for each buffer SFM by the definition
    for buffer_dft in wav_info.abs_buffers_dft:
        #sum the samples of the dft buffer
        sum = numpy.sum(buffer_dft)
        #sum of the ln for each samples of the dft buffer
        ln_sum = numpy.sum(numpy.log(buffer_dft))
        #explicit len of the buffer
        n = len(buffer_dft)
        #calculate SFM by definition and append it
        SFM = (numpy.exp(ln_sum/n)) / (sum/n)
        wav_info.SFM.append(SFM)


def calculate_PARFFT(wav_info):

    #define a function to calculate RMS given a sequence of samples
    def calculate_RMS(samples):

        # calculate the power of 2 for each samples
        samples_power_of_2 = samples ** 2

        # sum of the samples power to 2
        sample_sum = (numpy.sum(samples_power_of_2))

        # returning the value of the square root of the sum divided by the number of sample
        return math.sqrt((sample_sum) / len(samples_power_of_2))

    RMS = []


    # find the maximum of the samples absolute value for each buffer
    buffers_max = []

    # calculate for each buffer RMS and the maximum by the definition
    for dft_samples in wav_info.abs_buffers_dft:
        RMS.append(calculate_RMS(dft_samples))
        buffers_max.append(max(dft_samples))

    i = 0
    # calculate for each buffer PARFFT by the definition
    for RMS in RMS:
        wav_info.PARFFT.append(buffers_max[i] / RMS)
        i = i + 1


#definition of the function that calculate SF
#for each buffer of the wav_info object
def calculate_SF(wav_info):
    #defining an array: [a0,...an-1] all ai = 0,
    #n = len of a buffer
    zeros = [0] * len(wav_info.abs_buffers_dft[0])

    #reshaping to permit concatenation
    zeros = numpy.reshape(zeros,(1,513))

    #adding the zeros buffer at the first row of the buffer matrix
    shifted =  numpy.concatenate((zeros, wav_info.abs_buffers_dft), axis = 0)
    #calculating SF for each buffer by the definition
    for i in range(1, len(shifted)):
        #construct an array of Hs defined in the SF definition
        a = abs(shifted[i]) - abs(shifted[i-1])
        array_H = numpy.where(a < 0, 0, a)
        #sum of the Hs to get SF and append it
        SF = numpy.sum(list(array_H))
        wav_info.SF.append(SF)



