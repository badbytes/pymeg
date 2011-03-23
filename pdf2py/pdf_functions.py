class compute:
    def fft(self):
        from meg import fftmeg
        self.results.fft = fftmeg.calc(self.data.data_block ,1/self.hdr.header_data.sample_period, epochs=self.data.numofepochs)
    def filter(self, band=None, order=None, Wn=None):
        #Band = low, high, bp
        from meg import filtfilt
        self.filtereddata = filtfilt.calc(self.data.data_block, 1/self.data.hdr.header_data.sample_period , Wn, order, band)
    def badchan(self, thresh=3, maxhz=200, powernotch='yes'):
        from meg import badchannels
        #fftnull, badch, badchcomparison = badchannels.calc(datapdf, fft.pow, ch,thresh=2, freqarray=fft.freq,minhz=3, maxhz=200, powernotch='yes')
        #REWRITE BADCHANNEL STUFF
    def ica(self, numcomponents):
        import mdp
        ica = mdp.nodes.FastICANode(numcomponents)
        ica.train(self.data.data_block)
        comp = ica.execute(self.data.data_block)

    def offset_correct(self, start=0, end=-1):
        from meg import offset
        self.results.offsetcorrecteddata = offset.correct(self.data.data_block, start=start, end=end)
