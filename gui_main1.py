#coding:utf-8

#
# A GUI for threetube1.py
# by tkinter
#
#--------------------------------------------------------------
#  Using 
# Python 3.10.4, 64bit on Win32 (Windows 10)
# numpy 1.22.3
# scipy 1.8.0
#  -----------

import os
import sys
import re
import argparse


import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.font import Font

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from scipy.io.wavfile import write as wavwrite

from threetube1 import *
from glottal import *
from HPF import *

class GUI_App(ttk.Frame):
    def __init__(self, master=None):
        self.frame=ttk.Frame.__init__(self,master)
        #
        self.amp1=None
        self.freq=None
        self.peaks=None
        #
        self.open_file_init_dir=os.getcwd()
        self.save_file_init_dir=os.getcwd()
        self.save_wav_init_dir= os.getcwd()
        #
        self.enable_print = True
        #
        self.create_widgets()
        
        # rediect piint out to Text 
        sys.stdout= self.StdoutRedirector(self.text)
    
    
    
    def create_widgets(self,):
        #######################################################################################
        self.frame0=ttk.Frame(self.frame)
        self.frame0.pack(side=tk.LEFT)
        fig = plt.figure()
        self.make_draw()
        self.canvas = FigureCanvasTkAgg(fig, self.frame0)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        
        
        
        #######################################################################################
        self.frame1=ttk.Frame(self.frame)
        
        # open file
        gyou=0
        openfile_buttonb1 = ttk.Button(self.frame1, text='load length area', width=20, command=self.open_file_button1_clicked)
        openfile_buttonb1.grid(row=gyou, column=0, sticky=(W))
        self.openfile1= StringVar()
        self.openfile1.set('')
        
        savefile_buttonb1 = ttk.Button(self.frame1, text='save length area', width=20, command=self.save_file_button1_clicked)
        savefile_buttonb1.grid(row=gyou, column=1, sticky=(W))
        self.savefile1= StringVar()
        self.savefile1.set('')
        
        
        self.frame1.pack(fill = X)
        
        #######################################################################################
        
        self.frame2=ttk.Frame(self.frame)
        # Entry label
        gyou=0
        #self.label1= ttk.Label(self.frame2, text='Total tube  length [cm]',width=20)
        self.entry1= ttk.Entry(self.frame2)
        self.entry1.insert(0,'10')
        self.length_buttonb1 = ttk.Button(self.frame2, text='Adjust total length', width=20, command= self.length_button1_clicked)
        #self.label1.grid(row=gyou, column=1)
        self.entry1.grid(row=gyou, column=1)
        #gyou=gyou+1
        self.length_buttonb1.grid(row=gyou, column=0)
        
        # track bar
        DEF_to1=20
        DEF_itv1=5
        gyou=gyou+1
        self.label21= ttk.Label(self.frame2, text="Length 1 [cm]")
        self.var_scale21 = tk.DoubleVar()
        self.var_scale21.set(13) #10.7) #9)
        self.scale21 = tk.Scale(self.frame2,variable=self.var_scale21,orient=tk.HORIZONTAL,tickinterval=DEF_itv1, from_=1,to=DEF_to1,resolution=0.1,length=200,)
        self.label21.grid(row=gyou, column=0)
        self.scale21.grid(row=gyou, column=1)
        
        
        gyou=gyou+1
        self.label22= ttk.Label(self.frame2, text="Length 2 [cm]")
        self.var_scale22 = tk.DoubleVar()
        self.var_scale22.set(13) #0.7) #8)
        self.scale22 = tk.Scale(self.frame2,variable=self.var_scale22,orient=tk.HORIZONTAL,tickinterval=DEF_itv1, from_=1,to=DEF_to1,resolution=0.1,length=200,)
        self.label22.grid(row=gyou, column=0)
        self.scale22.grid(row=gyou, column=1)
        
        
        gyou=gyou+1
        self.label23= ttk.Label(self.frame2, text="Length 3 [cm]")
        self.var_scale23 = tk.DoubleVar()
        self.var_scale23.set(13) #10.7) #5.6)
        self.scale23 = tk.Scale(self.frame2,variable=self.var_scale23,orient=tk.HORIZONTAL,tickinterval=DEF_itv1, from_=1,to=DEF_to1,resolution=0.1,length=200,)
        self.label23.grid(row=gyou, column=0)
        self.scale23.grid(row=gyou, column=1)
        
        
        self.frame2.pack(fill = X)
        
        
        
        #######################################################################################
        
        self.frame3=ttk.Frame(self.frame)
        
        # track bar
        
        DEF_to2=30
        DEF_itv2=10
        gyou=0
        self.label31= ttk.Label(self.frame3, text="Area 1 [cm^2]")
        self.var_scale31 = tk.DoubleVar()
        self.var_scale31.set(0.1) #0.5) # 1)
        self.scale31 = tk.Scale(self.frame3,variable=self.var_scale31,orient=tk.HORIZONTAL,tickinterval=DEF_itv2, from_=0.1,to=DEF_to2,resolution=0.1,length=200,)
        self.label31.grid(row=gyou, column=0)
        self.scale31.grid(row=gyou, column=1)
        
        
        gyou=gyou+1
        self.label32= ttk.Label(self.frame3, text="Area 2 [cm^2]")
        self.var_scale32 = tk.DoubleVar()
        self.var_scale32.set(2.1) #5) #7)
        self.scale32 = tk.Scale(self.frame3,variable=self.var_scale32,orient=tk.HORIZONTAL,tickinterval=DEF_itv2, from_=0.1,to=DEF_to2,resolution=0.1,length=200,)
        self.label32.grid(row=gyou, column=0)
        self.scale32.grid(row=gyou, column=1)
        
        DEF_to3=50
        DEF_itv3=10
        gyou=gyou+1
        self.label33= ttk.Label(self.frame3, text="Area 3 [cm^2]")
        self.var_scale33 = tk.DoubleVar()
        self.var_scale33.set(30) #20) #3)
        self.scale33 = tk.Scale(self.frame3,variable=self.var_scale33,orient=tk.HORIZONTAL,tickinterval=DEF_itv3, from_=0.1,to=DEF_to3,resolution=0.1,length=200,)
        self.label33.grid(row=gyou, column=0)
        self.scale33.grid(row=gyou, column=1)
        
        self.frame3.pack(fill = X)
        
        #######################################################################################
        self.frame4=ttk.Frame(self.frame)
        
        # Entry label
        gyou=0
        self.label40= ttk.Label(self.frame4, text='starting[Hz]',width=13)
        self.entry40= ttk.Entry(self.frame4)
        self.entry40.insert(0,'440')
        self.label40.grid(row=gyou, column=0)
        self.entry40.grid(row=gyou, column=1)
        
        gyou=gyou+1
        self.label41= ttk.Label(self.frame4, text='octave',width=13)
        self.entry41= ttk.Entry(self.frame4)
        self.entry41.insert(0,'2')
        self.label41.grid(row=gyou, column=0)
        self.entry41.grid(row=gyou, column=1)
        
        gyou=gyou+1
        self.label42= ttk.Label(self.frame4, text='resolution',width=13)
        self.entry42= ttk.Entry(self.frame4)
        self.entry42.insert(0,'6')
        self.label42.grid(row=gyou, column=0)
        self.entry42.grid(row=gyou, column=1)
        
        gyou=gyou+1
        self.label43= ttk.Label(self.frame4, text='sampling rate',width=13)
        self.entry43= ttk.Entry(self.frame4)
        self.entry43.insert(0,'48000')
        self.label43.grid(row=gyou, column=0)
        self.entry43.grid(row=gyou, column=1)
        
        self.frame4.pack(fill = X)      
        
        ######################################################################################
        
        self.frame6=ttk.Frame(self.frame)
        # button
        gyou=0
        self.button1 = ttk.Button(self.frame6, text='compute frequency response', width = 30, command=self.button1_clicked)
        self.button1.grid(row=gyou, column=0)
        
        savewav_buttonb1 = ttk.Button(self.frame6, text='save generated wav', width=25, command=self.save_wav_button1_clicked)
        savewav_buttonb1.grid(row=gyou, column=1) #, sticky=(W))
        self.savewav1= StringVar()
        self.savewav1.set('')
        
        
        self.frame6.pack(fill = X)
        
        
        #######################################################################################
        self.frame7=ttk.Frame(self.frame)
        # text
        gyou=0
        f = Font(family='Helvetica', size=8)
        tv1 = StringVar()
        self.text = Text(self.frame7, height=3, width=45)
        self.text.configure(font=f)
        self.text.grid(row=gyou, column=0, sticky=(N, W, S, E))
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame7, orient=VERTICAL, command=self.text.yview)
        self.text['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=gyou, column=1, sticky=(N, S))
        
        
        self.frame7.pack(side=LEFT)
        #######################################################################################
        
        
    def button1_clicked(self,):
        #
        #self.button1['text']=('in process')
        #self.button1.configure(state=DISABLED)
        self.text.delete('1.0','end') # clear TEXT BOX AT ONCE
        if self.enable_print:
            print ('button1 was clicked')
            print ('Total tube length ', self.entry1.get())
            print ('L1', self.scale21.get())
            print ('L2', self.scale22.get())
            print ('L3', self.scale23.get())
            print ('A1', self.scale31.get())
            print ('A2', self.scale32.get())
            print ('A3', self.scale33.get())
            print ('staring[Hz]', int(self.entry40.get()))
            print ('octave', int(self.entry41.get()))
            print ('resolution', int(self.entry42.get()))
            print ('sampling rate', int(self.entry43.get()))
        #
        L1=self.scale21.get()
        L2=self.scale22.get()
        L3=self.scale23.get()
        A1=self.scale31.get()
        A2=self.scale32.get()
        A3=self.scale33.get()
        A440=int(self.entry40.get())
        octave= int(self.entry41.get())
        resolution=int(self.entry42.get())
        sampling_rate=int(self.entry43.get())
        
        # insatnce
        self.threetube_o  =  Class_ThreeTube(L3, A3, L1, L2, A1, A2, sampling_rate=sampling_rate,A440=A440,octave=octave,resolution=resolution)
        self.amp1, self.freq=self.threetube_o.H1()
        self.peaks=self.threetube_o.get_peaks(self.amp1)
        print (self.freq[self.peaks])
        
        #
        self.make_draw()
        #canvas = FigureCanvasTkAgg(fig, self.frame0)
        self.canvas.draw()
        #canvas.get_tk_widget().pack()
        
        # destruct instance
        del self.threetube_o
        
    def length_button1_clicked(self,):
        #
        if self.enable_print:
            print ('length_button1 was clicked. Each length be adjusted.')
            TL_tgt=float(self.entry1.get())
            L1=self.scale21.get()
            L2=self.scale22.get()
            L3=self.scale23.get()
            TL_now=L1+L2+L3
            self.scale21.set(L1 * TL_tgt / TL_now )
            self.scale22.set(L2 * TL_tgt / TL_now )
            self.scale23.set(L3 * TL_tgt / TL_now )
        
        
        
    def make_draw(self,):
        #
        #fig = plt.figure()
        plt.cla()
        
        plt.xlabel('Hz')
        plt.ylabel('dB')
        plt.title('frequency response')
        if self.amp1 is not None:
            plt.plot(self.freq, self.amp1)
            for i in self.peaks:
                plt.plot(self.freq[i], self.amp1[i], "x")
                plt.text(self.freq[i], self.amp1[i], str(int(self.threetube_o.f_list[i])))
            
        else:
            dummy=np.linspace(0,100,100)
            plt.plot(dummy)
        
        plt.grid(which='both', axis='both')
        #fig.tight_layout()
        
        
    def open_file_button1_clicked(self,):
        file_name = filedialog.askopenfilename(filetypes = [("text", ".txt")], initialdir=self.open_file_init_dir)
        if file_name:
            self.openfile1.set(file_name)
            self.open_file_init_dir= os.path.dirname(file_name)
            if self.enable_print:
                print ('openfile ', self.openfile1.get())
            
            try:
                with open(file_name, 'rt') as f:
                    lines0 = f.read().splitlines()
                    
                    self.scale21.set( float(lines0[0]) ) # L1
                    self.scale22.set( float(lines0[1]) ) # L2
                    self.scale23.set( float(lines0[2]) ) # L3
                    
                    self.scale31.set( float(lines0[3]) ) # A1
                    self.scale32.set( float(lines0[4]) )# A2
                    self.scale33.set( float(lines0[5]) ) # A3
                    
                    f.close()
            except:
               print ('read error')
                
                
    def save_file_button1_clicked(self,):
        file_name = filedialog.asksaveasfilename(filetypes = [("text", ".txt")],initialdir=self.save_file_init_dir, defaultextension = "wav")
        if file_name:
            self.savefile1.set(file_name)
            self.save_file_init_dir= os.path.dirname(file_name)
            if self.enable_print:
                print ('savefile ', self.savefile1.get())
            
            try:
                with open(file_name, 'w') as f:
                    
                    f.write( str(self.scale21.get()) +'\n') # L1
                    f.write( str(self.scale22.get()) +'\n') # L2
                    f.write( str(self.scale23.get()) +'\n') # L3
                    
                    f.write( str(self.scale31.get()) +'\n') # A1
                    f.write( str(self.scale32.get()) +'\n') # A2
                    f.write( str(self.scale33.get()) +'\n') # A3
                    
                    f.close()
            except:
               print ('write error')
    
    
    def save_wav_button1_clicked(self,):
        file_name = filedialog.asksaveasfilename(filetypes = [("WAV", ".wav")],initialdir=self.save_wav_init_dir, defaultextension = "wav")
        if file_name:
            self.savewav1.set(file_name)
            self.save_wav_init_dir= os.path.dirname(file_name)
            if self.enable_print:
                print ('save wav ', self.savewav1.get())
            
            L1=self.scale21.get()
            L2=self.scale22.get()
            L3=self.scale23.get()
            A1=self.scale31.get()
            A2=self.scale32.get()
            A3=self.scale33.get()
            A440=int(self.entry40.get())
            octave= int(self.entry41.get())
            resolution=int(self.entry42.get())
            sampling_rate=int(self.entry43.get())
            
            # insatnce
            threetube_o  =  Class_ThreeTube(L3, A3, L1, L2, A1, A2,sampling_rate=sampling_rate, A440=A440,octave=octave,resolution=resolution)
            
            glo=Class_Glottal(sampling_rate=sampling_rate)   # instance as glottal voice source
            hpf=Class_HPF(sampling_rate=sampling_rate)       # instance for mouth radiation effect
            
            #
            yg_repeat=glo.make_N_repeat(repeat_num=50) # input source of three tube model
            y2tm=threetube_o.process(yg_repeat)
            yout=hpf.iir1(y2tm)
            
            yout=yout / max(abs(yout)) * np.power(10, -3/20) # peak as -3dB FS
            
            #
            wavwrite( file_name, sampling_rate, ( yout * 2 ** 15).astype(np.int16))
            print ('save ', file_name) 
            
            # destruct instance
            del threetube_o
            del glo
            del hpf
    
    
    
    class IORedirector(object):
        def __init__(self, text_area):
            self.text_area = text_area
            self.line_flag = False
            
    class StdoutRedirector(IORedirector):
        def write(self,st):
            if 0: # esc-r
                # check if there is num/num in st
                if re.search(r' \d+/\d+',st) is not None:
                    #
                    if not self.line_flag:  # start...
                        self.text_area.insert('end',  st)
                        self.text_area.insert('end', "\n") # make index up
                        self.line_flag=True
                    else:
                        # delete last 1 line 
                        self.text_area.delete("end-2l", "end-1l")
                        #
                        self.text_area.insert('end', st)
                        self.text_area.insert('end', "\n") # make index up
                else:
                    #self.text_area.insert('end', pos +'>' + st)
                    self.text_area.insert('end',  st )
                    if st != "":
                        self.line_flag = False  # reset line_flag
            else:
                self.text_area.insert('end',  st)
            
            self.text_area.see("end")
        
        
        def flush(self):
            pass




def quit_1(root_window):
    root_window.quit()
    root_window.destroy()


sys.stdout= sys.__stdout__


if __name__ == '__main__':
    #
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", lambda :quit_1(root))
    root.title('three tube model')
    
    app=GUI_App(master=root)
    app.mainloop()
