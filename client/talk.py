from gtts import gTTS
import os, tempfile
import simpleaudio as sa
from tkinter import messagebox, Tk

def voice(text = 'Welcome', language = 'en'):
    try:    
        obj = gTTS(text = text.strip(), lang = language, slow = False)
        obj.save('w.mp3')
        os.system("w.mp3")
    except:
        master = Tk()
        master.withdraw()
        messagebox.showerror('Connection Error', 'Failed to connect.\nCheck your internet connection and try again')
        master.destroy()
        master.mainloop()
        exit(0)


if __name__ == "__main__":
    
    text = '''
        Hello
            How
                are 
                            you
                            Sir
                            
                                    !

    '''

    voice(text)