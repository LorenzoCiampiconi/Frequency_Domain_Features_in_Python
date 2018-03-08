class WavInfo:
    def __init__(self):
        #file name
        self.file_name = ''

        #label
        self.label = ''

        #samples of the wav file
        self.buffers = []

        # dft of the buffers
        self.abs_buffers_dft = []

        # Spectral Centroid for each buffer
        self.SC = []

        # Spectral Roll-Off for each buffer
        self.SRO = []

        # Spectral Flatness Measure for each buffer
        self.SFM = []

        # Peak-to-average Ratio for each buffer
        self.PARFFT = []

        # Spectral Flux for each buffer
        self.SF= []

        #mean of each feature
        self.mean_of_features = []

        #mstd of each feature
        self.std_features = []