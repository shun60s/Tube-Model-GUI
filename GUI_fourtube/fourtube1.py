#coding:utf-8

#
# Four Tube Model, A python Class to calculate frequecny response and process reflection transmission of resonance tube
#


import numpy as np
from matplotlib import pyplot as plt
from scipy import signal # version > 1.2.0

# Check version
#  Python 3.10.4, 64bit on Win32 (Windows 10)
#  numpy 1.21.6
#  scipy 1.8.0
#  matplotlib  3.5.2

class Class_FourTube(object):
    def __init__(self, L1, L2, L3, L4, A1, A2, A3, A4, rg0=0.95, rl0=0.9 ,sampling_rate=48000,A440=440,octave=2,resolution=4):
        # initalize Tube length and Tube area
        self.L1= L1 # set list of 1st tube's length by unit is [cm]
        self.A1= A1 # set list of 1st tube's area by unit is [cm^2]
        self.L2= L2 # set list of 2nd tube's length by unit is [cm]
        self.A2= A2 # set list of 2nd tube's area by unit is [cm^2]
        self.L3= L3 # set list of 3rd tube's length by unit is [cm]
        self.A3= A3 # set list of 3rd tube's area by unit is [cm^2]
        self.L4= L4 # set list of 4th tube's length by unit is [cm]
        self.A4= A4 # set list of 4th tube's area by unit is [cm^2]
        C0=35000.0  # speed of sound in air, round 35000 cm/second
        self.sr= sampling_rate
        self.tu1=self.L1 / C0   # delay time in 1st tube
        self.tu2=self.L2 / C0   # delay time in 2nd tube
        self.tu3=self.L3 / C0   # delay time in 3rd tube
        self.tu4=self.L4 / C0   # delay time in 4th tube
        self.r1=( self.A2 - self.A1) / ( self.A2 + self.A1)  # reflection coefficient between 1st tube and 2nd tube
        self.r2=( self.A3 - self.A2) / ( self.A3 + self.A2)  # reflection coefficient between 2nd tube and 3rd tube
        self.r3=( self.A4 - self.A3) / ( self.A4 + self.A3)  # reflection coefficient between 3rd tube and 4th tube
        self.rg0=rg0 # rg is reflection coefficient between glottis and 1st tube
        self.rl0=rl0 # reflection coefficient between 3rd tube and mouth
        
        #
        self.A440=A440
        self.num_octave=octave
        self.onkai_resolution=resolution
        
    def fone(self, xw):
        # calculate one point of frequecny response
        yi= 0.5 * ( 1.0 +  self.rg0 ) * ( 1.0 +  self.r1)  * ( 1.0 +  self.r2)  * ( 1.0 +  self.r3)  * ( 1.0 +  self.rl0 ) * \
            np.exp( -1.0j * (  self.tu1 +  self.tu2 +  self.tu3 + self.tu4 ) * xw) 
        # yb
        yb1= 1.0 +  self.r2 *  self.r1 *  np.exp( -2.0j *  self.tu2 * xw )  # 2.3
        yb1= yb1 +  self.r3  *  self.r2 *  np.exp( -2.0j *  self.tu3 * xw )  # 1.2
        yb1= yb1 +  self.rl0 *  self.r3 *  np.exp( -2.0j *  self.tu4 *  xw )  # 0
        yb2=        self.r3  *  self.r1 *  np.exp( -2.0j * ( self.tu2 +  self.tu3) * xw ) # 2.2
        yb2= yb2 +  self.rl0 *  self.r2  *  np.exp( -2.0j * ( self.tu3 +  self.tu4) *  xw )  # 1.1
        yb3=  self.rl0 *  self.r3 *  self.r2 *  self.r1 *  np.exp( -2.0j * ( self.tu2 +  self.tu4) *  xw ) # 2.4
        yb4=  self.rl0 *  self.r1 * np.exp( -2.0j * ( self.tu2 +  self.tu3 +  self.tu4) *  xw ) # 2.1
        
        yb31= self.rg0 * self.rl0  * np.exp( -2.0j * ( self.tu1 + self.tu2 +  self.tu3 +  self.tu4) *  xw ) # 3.1
        yb32= self.rg0 * self.r3 * np.exp( -2.0j * ( self.tu1 + self.tu2 +  self.tu3 ) *  xw ) # 3.2
        yb41= self.rg0 * self.r2 * np.exp( -2.0j * ( self.tu1 + self.tu2 ) *  xw ) # 4.1
        yb42= self.rg0 * self.r2 * self.r3 * self.rl0 * np.exp( -2.0j * ( self.tu1 + self.tu2 + self.tu4) *  xw ) # 4.2
        yb51= self.rg0 * self.r1 * np.exp( -2.0j * self.tu1  *  xw ) # 5.1
        yb52= self.rg0 * self.r1 * self.r3 * self.rl0 * np.exp( -2.0j * ( self.tu1 + self.tu4 ) *  xw ) # 5.2
        yb53= self.rg0 * self.r1 * self.r2 * self.rl0 * np.exp( -2.0j * ( self.tu1 + self.tu3 + self.tu4 ) *  xw ) # 5.3
        yb54= self.rg0 * self.r1 * self.r2 * self.r3 * np.exp( -2.0j * ( self.tu1 + self.tu3 ) *  xw ) # 5.4
        
        yb= yb1 + yb2 + yb3 + yb4 + yb31 + yb32 + yb41 + yb42 + yb51 + yb52 + yb53 + yb54    
        
        val= yi/yb
        return np.sqrt(val.real ** 2 + val.imag ** 2)
        
        
    def H0(self, freq_low=100, freq_high=5000, Band_num=256):
        # get Log scale frequecny response, from freq_low to freq_high, Band_num points
        amp=[]
        freq=[]
        bands= np.zeros(Band_num+1)
        fcl=freq_low * 1.0    # convert to float
        fch=freq_high * 1.0   # convert to float
        delta1=np.power(fch/fcl, 1.0 / (Band_num)) # Log Scale
        bands[0]=fcl
        #print ("i,band = 0", bands[0])
        for i in range(1, Band_num+1):
            bands[i]= bands[i-1] * delta1
            #print ("i,band =", i, bands[i]) 
        for f in bands:
            amp.append(self.fone(f * 2.0 * np.pi))
        return   np.log10(amp) * 20, bands # = amp value, freq list
        
    def get_f_list(self,SHOW=True):
        #self.onkai_resolution=4 #　分解能
        num_onkai=12 * self.onkai_resolution #  何音階
        #self.num_octave=2 #　何オクターブ
        #self.A440=440     #  開始周波数
        base1=np.power(2, 1/num_onkai)
        num0=num_onkai * self.num_octave
        self.f_list=np.logspace(0, num0, num=num0+1, base=base1) * self.A440
        if SHOW:
            print (self.f_list)
    
    def get_f_linear_list(self,SHOW=True):
        #self.onkai_resolution=4 #　分解能
        #self.num_octave=2 #　何オクターブ
        #self.A440=440     #  開始周波数
        f_end=np.power(2, self.num_octave) * self.A440 # 終了周波数
        self.f_list=np.linspace(self.A440, f_end, int( (f_end - self.A440)/self.onkai_resolution  + 1  ) )
        if SHOW:
            print (self.f_list)
        
    def H1(self,):
        self.get_f_list(SHOW=False)
        self.f_amp=self.fone(self.f_list * 2.0 * np.pi)
        
        return  np.log10(self.f_amp) * 20, self.f_list # = amp value, freq list
        
    def H1_linear(self,SHOW=False):
        self.get_f_linear_list(SHOW=SHOW)
        self.f_amp=self.fone(self.f_list * 2.0 * np.pi)
        
        return  np.log10(self.f_amp) * 20, self.f_list # = amp value, freq list
        
    def get_peaks(self,amp1):
        MIN_HIGH= 0.4   # ピークの最小高さ
        #MIN_DIS= 0.000001    # 最小の周辺距離
        MIN_WIDTH= 1 # 最小の周辺幅
        self.peaks, _ = signal.find_peaks(amp1, height= MIN_HIGH * max(amp1),width= MIN_WIDTH) #, distance= MIN_DIS * n , width= MIN_WIDTH * n)
        return self.peaks
        
    def process(self, yg ):
        # process reflection transmission of resonance tube: yg is input, y2tm is output
        M1= round( self.tu1 * self.sr ) + 1  # for precision, higher sampling_rate is better
        M2= round( self.tu2 * self.sr ) + 1  # for precision, higher sampling_rate is better
        M3= round( self.tu3 * self.sr ) + 1  # for precision, higher sampling_rate is better
        M4= round( self.tu4 * self.sr ) + 1  # for precision, higher sampling_rate is better
        M1= int(M1)
        M2= int(M2)
        M3= int(M3)
        M4= int(M4)
        ya1=np.zeros(M1)
        ya2=np.zeros(M1)
        yb1=np.zeros(M2)
        yb2=np.zeros(M2)
        yc1=np.zeros(M3)
        yc2=np.zeros(M3)
        yd1=np.zeros(M4)
        yd2=np.zeros(M4)
        y2tm=np.zeros(len(yg))
        
        for tc0 in range(len(yg)):
            for i in range((M1-1),0,-1): # process one step
                ya1[i]=ya1[i-1]
                ya2[i]=ya2[i-1]
            for i in range((M2-1),0,-1): # process one step
                yb1[i]=yb1[i-1]
                yb2[i]=yb2[i-1]    
            for i in range((M3-1),0,-1): # process one step
                yc1[i]=yc1[i-1]
                yc2[i]=yc2[i-1]    
            for i in range((M4-1),0,-1): # process one step
                yd1[i]=yd1[i-1]
                yd2[i]=yd2[i-1]    
            # calculate reflection
            ya1[0]= ((1. + self.rg0 ) / 2.) * yg[tc0] + self.rg0 * ya2[-1]
            ya2[0]= -1. * self.r1 *  ya1[-1]  +  ( 1. - self.r1 ) * yb2[-1]
            
            yb1[0]= ( 1 + self.r1 ) * ya1[-1] + self.r1 * yb2[-1]
            yb2[0]=  -1. * self.r2  * yb1[-1] + ( 1. - self.r2 ) * yc2[-1]
            
            yc1[0]= ( 1 + self.r2 ) * yb1[-1] + self.r2 * yc2[-1]
            yc2[0]=  -1. * self.r3  * yc1[-1] + ( 1. - self.r3 ) * yd2[-1]
            
            yd1[0]= ( 1 + self.r3 ) * yc1[-1] + self.r3 * yd2[-1]
            yd2[0]=  -1. * self.rl0  * yd1[-1]
            
            y2tm[tc0]= (1 + self.rl0) * yd1[-1]
            
        return y2tm

if __name__ == '__main__':
    
    
    # insatnce
    tube  =  Class_FourTube(3., 8.8, 1.5, 1.4, 1.0, 8.4, 237., 11.6 , sampling_rate=48000)
    
    # draw
    fig = plt.figure()
    
    #
    plt.xlabel('Hz')
    plt.ylabel('dB')
    plt.title('frequency response')
    #amp1, freq=tube_o.H0(freq_high=5000, Band_num=256)
    #amp1, freq=tube_o.H1()  # log scale
    amp1, freq=tube_o.H1_linear() #SHOW=True)
    peaks=tube_o.get_peaks(amp1)
    
    plt.plot(freq, amp1)
    plt.plot(freq[peaks], amp1[peaks], "x")
    plt.grid(which='both', axis='both')
    
    #
    fig.tight_layout()
    plt.show()