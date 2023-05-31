#CHATROOM
#client.py
#AUTHOR - Sagar Mishra

#importing all the modules
import socket
import threading
from tkinter import *
from tkinter import ttk
from tkinter import font, messagebox ,scrolledtext, filedialog
from time import strftime 
from PIL import ImageTk, Image
import os, shelve, re, webbrowser
from talk import voice

FORMAT = "utf-8"

def connecting(Ip, port):
    global client
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    port = int(port) 
    client.connect((Ip,port)) 

class GUI:
    def __init__(self):
 
        self.root = Tk()
        self.root.withdraw()
        
        #LOGIN
        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry("400x350")
        self.login.configure(bg="#fcffea")
        self.login.resizable(width= False , height= False)

        #HEADING
        self.head= Label(self.login, text = "LOGIN PAGE", font = "Seria 15 bold",bg="#075E54", fg="white")
        self.head.place(relwidth = 1, relheight=0.1)
     
        #DP LABEL
        #creating db for image
        if not os.path.exists("user_login_dir"):
            os.makedirs("user_login_dir")

        #check if shelve already exist if not initialize it
        if 'user_login_details.bak' not in os.listdir("user_login_dir"):
            self.login_shelf = shelve.open(r"user_login_dir\user_login_details")
            self.login_shelf['default_image'] = 'assets\a.jpg' #default image
            self.login_shelf['user_dp'] = None
            self.login_shelf['user_name'] = None
            
        else:
            self.login_shelf = shelve.open(r"user_login_dir\user_login_details")
            
        #setting default image
        if self.login_shelf['user_dp'] == None:
            self.img_f = self.login_shelf['default_image']  #default image
        else:
            self.img_f = self.login_shelf['user_dp']
        
        self.dp = Label(self.login, bg = "red", image = self.loading(self.img_f), width = 50, height = 35)
        self.dp.bind('<Button-1>', self.load_dp)
        self.dp.place(relx = 0.45, rely = 0.15)
        
        #IP LABEL
        self.Ip =Label(self.login,text="IP :",pady=10,bg="#fcffea",font=('calibri', 12, 'bold'))
        self.Ip.place(relx=0.2,rely=0.25)
        
        #IP ENTRY
        self.Server_Ip =Entry(self.login,width=20,borderwidth=2, fg="dark green",font=('calibri', 12, 'bold'))
        self.Server_Ip.place(relx=0.35 ,rely=0.28)
        self.Server_Ip.focus()
        
        #PORT LABEL
        self.Port=Label(self.login,text="PORT :",pady=10, bg="#fcffea",font=('calibri', 12, 'bold'))
        self.Port.place(relx=0.2,rely=0.35)
        
        #PORT ENTRY
        self.port_var = IntVar() 
        self.Server_port = Entry(self.login, textvariable = self.port_var,width=20,borderwidth=2, fg ="dark red", font=('calibri', 12, 'bold'))
        self.Server_port.place(relx=0.35 ,rely=0.38)
        
        #NAME LABEL
        self.label_name=Label(self.login,text="Name :",pady=10, bg= "#fcffea", font=('calibri', 12, 'bold'))
        self.label_name.place(relx=0.2,rely=0.45)
        
        #NAME ENTRY
        self.Client_Name=Entry(self.login,width=20,borderwidth=2,fg="dark blue" ,font=('calibri', 12, 'bold'))
        self.Client_Name.place(relx=0.35 ,rely=0.48)   
       
        #CONNECT BUTTON
        self.loadimage = ImageTk.PhotoImage(Image.open("assets\login.png"))
        Command= lambda event: [connecting(self.Server_Ip.get(),self.Server_port.get()),self.main_window(self.Client_Name.get(),self.Server_Ip.get(),self.Server_port.get())]
        self.connect_button=Button(self.login,image=self.loadimage,padx=10, bg = "grey", bd = 0)
        #self.connect_button.pack(side="top")
        self.connect_button.bind('<Return>', Command)
        self.connect_button.bind('<Button-1>', Command)
        self.connect_button.place(relx=0.4,rely=0.58)
        
        self.login.protocol("WM_DELETE_WINDOW", self.close_login)
        self.root.option_add("*tearOff", False)
        self.root.protocol("WM_DELETE_WINDOW", self.Close)
        
        self.root.mainloop()
     
    def close_login(self):
        self.root.destroy()
    
    def loading(self, image):
        self.pic = Image.open(image)
        self.resize = self.pic.resize((50, 35), Image.ANTIALIAS)
        self.new_pic = ImageTk.PhotoImage(self.resize)
        return self.new_pic
        
    def load_dp(self, event):
        self.image_filename = filedialog.askopenfilename(initialdir = "../pictures/", title = "Select a File", filetypes = (("jpeg files", "*jpg"), ("png files", "*.png"), ("gif files", "*.gif"),("bitmap file", "*bmp")))
        if not self.image_filename:
            self.image_filename = self.img_f
        
        self.dp.config( image = self.loading(self.image_filename) )
        self.login_shelf['user_dp'] = self.image_filename
        self.img_f = self.login_shelf['user_dp']
        
    
    def preview(self, event):
        self.image_win = Toplevel()
        self.image_win.title("User DISPLAY PICTURE")
        self.image_win.geometry("630x550+200+50")
        self.image_win.config(bg = "black")
        
        self.image_win.resizable(width = False, height = False)
        self.image_win.focus()
        self.image_win.overrideredirect(True)
  
        self.full_pic = Image.open(self.img_f)
        self.full_resize = self.full_pic.resize((600, 480), Image.ANTIALIAS)
        self.full_picture = ImageTk.PhotoImage(self.full_resize)
        self.image_view = Label(self.image_win, image = self.full_picture, bg = "black")
        self.image_view.place(relx = 0.023,rely = 0.027)
        self.change_dp = Button(self.image_win, borderwidth = 0, text = "Change Wallpaper", padx = 2, pady = 2)
        self.change_dp.bind('<Button-1>', self.update_dp)
        self.change_dp.place(relx = 0.4, rely = 0.94)
        
        self.image_win.bind('<Escape>', lambda event: self.preview_destroy(event))
        
    
    def preview_destroy(self, event):
        self.image_win.destroy()
    
    def update_dp(self, event):
        self.load_dp(event)
        self.dp.config(image = self.loading(self.img_f))
        
        self.full_pic = Image.open(self.img_f)
        self.full_resize = self.full_pic.resize((600, 480), Image.ANTIALIAS)
        self.full_picture = ImageTk.PhotoImage(self.full_resize)
    
     
    def main_window(self, name,IP,PORT): 
        self.login.destroy() 
        self.chat_room(name,IP,PORT)
        rcv = threading.Thread(target=self.receive) 
        rcv.start() 

    def Close(self):
        # save the data to the file before quitting
        self.save_data()
        self.res = messagebox.askyesno(title="Exit", message="Are you sure you want to close ?")
        if self.res:
            client.close()
            self.root.destroy()
    
    #save data
    def save_data(self):
        if not os.path.exists('chat data'):
            os.makedirs('chat data')
        
        with open(r"chat data\usr_chat_data.txt",'w') as f:
            f.write(self.display_msg.get(1.0, END))
   
    #load data
    def load_data(self):
        if not os.path.exists(r'chat data\usr_chat_data.txt'):
            return
        
        with open(r"chat data\usr_chat_data.txt",'r') as f:
            self.display_msg.insert(END, f.read())
    
    #delete the chat
    def delete_chat(self):
        # add warning message box here
        self.clr = messagebox.askyesno(title="Clear", message=" Your entire data will be lost !")
        if self.clr:
            self.display_msg.config(state = NORMAL)
            self.display_msg.delete(1.0, END)
            self.display_msg.config(state = DISABLED)
    
    def user_profile(self):
        
        self.profile = Toplevel()
        self.profile.geometry("300x355+1010+30")
        self.profile.configure(bg="#2c2f33")
        self.profile.resizable(width= False , height= False)
        self.profile.focus()
        self.profile.overrideredirect(True)
       

       #HEADING
        self.head= Label(self.profile, text = "Profile", font = "Calibri 15 bold italic",bg="#075E54", fg="white")
        self.head.place(relwidth = 1, relheight=0.1)
        
        self.view_dp = Image.open(self.img_f)
        self.view_dp_modify= self.view_dp.resize((295, 200), Image.ANTIALIAS)
        self.profile_pic = ImageTk.PhotoImage(self.view_dp_modify)
        self.profile_label = Label(self.profile, image = self.profile_pic, height = 200, width = 295)
        self.profile_label.place(relx = 0, rely = 0.1)

        #NAME LABEL
        self.label_name=Label(self.profile,text="Username",fg= "white", bg= "#2c2f33", font=('calibri',9, 'bold italic'))
        self.label_name.place(relx=0.3,rely=0.7)
        self.Client_Name=Label(self.profile,bg= "#2c2f33", text = self.name,fg="#128C7E" ,font=('calibri', 12, 'bold '))
        self.Client_Name.place(relx=0.3 ,rely=0.74)   
       
        #IP LABEL
        self.Ip =Label(self.profile,text="Ip",bg="#2c2f33",fg= "white",font=('calibri', 9, 'bold italic'))
        self.Ip.place(relx=0.1,rely=0.83)
        self.Server_Ip =Label(self.profile, bg= "#2c2f33", fg="#128C7E",font=('calibri', 12, 'bold'),text= self.IP)
        self.Server_Ip.place(relx=0.1 ,rely=0.88)
        self.Server_Ip.focus()
        
        #PORT LABEL
        self.Port=Label(self.profile,text="Port",fg= "white", bg="#2c2f33",font=('calibri', 9, 'bold italic'))
        self.Port.place(relx=0.6,rely=0.83)
        self.Server_port = Label(self.profile, text= self.PORT,bg= "#2c2f33", fg ="#128C7E", font=('calibri', 12, 'bold'))
        self.Server_port.place(relx=0.6 ,rely=0.88)

        self.brand_name= Label(self.profile, text= "CHATROOM", bg= "#2c2f33", fg ="white",font=('calibri', 10, 'bold'),anchor = 'se')
        self.brand_name.place( relx= 0.079, rely = 0.95)
       
        self.brand_logo= Image.open("assets\icon.jpg")
        self.brand_logo_modify= self.brand_logo.resize((16,16), Image.ANTIALIAS)
        self.brand_pic = ImageTk.PhotoImage(self.brand_logo_modify)
        self.brand_label = Label(self.profile, image = self.brand_pic, height = 16, width = 16, bg="#2c2f33")
        self.brand_label.place(relx = 0.021, rely = 0.95)
       
        #CLOSE BUTTON
        self.profile.bind('<Escape>', lambda event: self.profile_destroy(event))
        
    
    #DESTROY PROFILE 
    def profile_destroy(self, event):
        self.profile.destroy()
    
    def find_text(self,event):
        self.find_master = Toplevel()
        self.find_master.title('Find')
        self.find_master.geometry('300x50+1010+100')
        
        self.find_master.overrideredirect(True)
        
        self.find_frame = Frame(self.find_master,bg ='#23272a' )
        self.find_frame.pack()
        
        self.find_label = Label(self.find_frame, text = 'Find', font = ('Calibri', 12, 'bold'),bg="#23272a",fg= "white")
        self.find_label.grid(row = 0, column = 0, pady = 10, padx = 2)
        self.find_value = Entry(self.find_frame, width = 40)
        self.find_value.grid(row = 0, column = 1, pady = 10, padx = 10)
        self.find_value.focus_set()
        
        def find_func(event):
            self.display_msg.tag_remove('found', '1.0', END) 
            s = self.find_value.get()
            
            if (s):
                idx = '1.0'
                while True:
                    idx = self.display_msg.search(s, idx, nocase = 1, stopindex = END)
                    if not idx: break
                    
                    lastidx = "%s +%dc" %(idx, len(s))
                    self.display_msg.tag_add('found', idx, lastidx)
                    idx = lastidx
                    
                self.display_msg.tag_config('found', background = "white", foreground = 'black')
            self.find_value.focus_set()
    
        
        self.find_value.bind('<Return>', find_func)
        self.find_master.bind('<Escape>', self.find_destroy)
   
    
    def find_destroy(self, event):
        self.display_msg.tag_remove('found', '1.0', END) 
        self.find_master.destroy()
     
    
    def text_to_speech(self):
        try:
            self.selected_text = self.display_msg.get(SEL_FIRST, SEL_LAST)
        except TclError:
            self.selected_text = 'please select the text to speak'
            
        #search for the names and remove it from the text to avoid any issue in reading by gtts
        name_regex = re.compile(r'\s*\w+:')
        name_listed = name_regex.findall(self.selected_text)
        for val in name_listed:
            self.selected_text = self.selected_text.replace(val, '')
        voice(self.selected_text) #calling func to speak
    
    def web_search(self):
        
        #search the web for the highlighted text
        try:
            self.search_text = self.display_msg.get(SEL_FIRST, SEL_LAST)
        except TclError:
            self.search_text = ''
        if self.search_text:
            self.browse = webbrowser.get()
            self.browse.open(f'https://google.com/search?q={self.search_text}') 
        
    
    def start(self):
        self.canva.destroy()
        self.root.after(0, self.root.overrideredirect, False)
        self.root.config(menu = self.main_menu)
        self.main_frame.place(relwidth = 1, relheight = 1)
    
    
    
    def chat_room(self,name,IP,PORT):
        #TIME
        def time(): 
            string = strftime('%H:%M:%S %p') 
            time_label.config(text = string) 
            time_label.after(1000, time)
        
        self.name = name 
        self.IP = IP
        self.PORT= PORT
        #CHATROOM
        self.root.deiconify() 
        self.root.title("CHATROOM")
        self.icon = ImageTk.PhotoImage(Image.open('assets\icon.jpg'))
        self.root.iconphoto(False, self.icon)
     
        self.root.overrideredirect(True)
     
        self.root.geometry("800x600+200+30")
        self.root.resizable(width = False, height = False)
        self.root.configure(bg = "#000000") 
        
        #main frame
        self.main_frame = Frame(self.root, bg = "black", width = 800, height = 600)
        #welcome canva
        self.canva = Canvas(self.root, height = 600, width = 800, bg = "dark grey", highlightthickness = 0)
        self.canva.pack()
        self.welcome_img = ImageTk.PhotoImage(Image.open("assets\icon.ico"))
        self.canva.create_image(390,130, anchor = N, image = self.welcome_img)
        self.canva.create_text(395, 420, fill = "black", font = "Times 40 italic bold", text = "CHATROOM")
        self.canva.after(1500, self.start)
        
        #creating menu
        self.main_menu = Menu(self.root)
        #creating setting sub_menu
        self.option_menu = Menu(self.main_menu)
        self.main_menu.add_cascade(label = "Settings", menu = self.option_menu)
        self.option_menu.add_command(label = "User Profile", command = self.user_profile)
        self.option_menu.add_separator()
        self.option_menu.add_command(label = "Clear chat", command = self.delete_chat)
        self.option_menu.add_command(label = "Change Profile Picture", command = lambda: self.update_dp(' '))
        self.option_menu.add_command(label = "Find", command = lambda: self.find_text(' '),accelerator="Ctrl+F")
        self.option_menu.add_command(label = "Text to speech", command = self.text_to_speech)
        self.option_menu.add_command(label = "Web Search", command = self.web_search)
        self.option_menu.add_separator()
        self.option_menu.add_command(label = "Exit", command = self.Close)
        
        
        #top frame
        self.top_frame = Frame(self.main_frame, bg = "#7289da",pady = 5) 
        self.top_frame.place(relwidth = 1, relheight = 0.085) 
        
        self.top_label = Label(self.top_frame, bg = "#7289da", fg = "white", text = self.name , font = ('calibri', 25, 'bold'),pady = 5) 
        self.top_label.place(relx = 0.35 ,rely = 0.08,relwidth= 0.25, relheight=0.85)
        
        time_label = Label(self.top_frame, font = ('calibri', 12, 'bold'), foreground = 'white', background='#7289da',pady=5) 
        time_label.pack(anchor = 'ne') 
        tm= threading.Thread(target = time) 
        tm.start()
        
        #selecting image 

        self.dp = Label(self.top_frame, bg = "red", image = self.loading(self.img_f), width = 50, height = 35)
        self.dp.bind('<Double-1>', self.preview)
        
        self.dp.place(relx = 0.025, rely = 0.0)
        
        #display frame
        self.display_frame = Frame(self.main_frame, bg = "#000000")
        self.display_frame.place(relheight = 0.795,relwidth = 1,rely = 0.086)
        
        #display box
        self.display_msg = Text(self.display_frame, bg = "#2c2f33", fg = "#ffffff", font = "calibri 12", padx = 5, pady = 5) 
        self.display_msg.place(relheight = 1,relwidth = 0.98)
        self.load_data()  # call to load the saved data
        
        #bottom frame
        self.bottom_frame = Frame(self.main_frame, bg = "#394852",height = 72) 
        self.bottom_frame.place(relwidth = 1, rely = 0.8795) 
        
        def send_message_using_key(event):
            self.sendButton(event, self.input_msg.get('1.0', END))
            
        
        #MESSAGE ENTRY
        self.input_msg = scrolledtext.ScrolledText(self.bottom_frame, bg = "#23272a", fg = "#EAECEE", font = "Helvetica 13") 
        self.input_msg.place(relwidth = 0.86, relheight = 0.7,rely = 0.175, relx = 0.01) 
        self.input_msg.focus() 
        self.input_msg.bind('<Shift_R>',lambda event : send_message_using_key(event)) 
        
        
        #SEND BUTTON
        self.img = ImageTk.PhotoImage(Image.open("assets\send.jpg"))
        self.input_button = Button(self.bottom_frame, image = self.img, font = "Helvetica 10 bold", bg = "#42466b")
        self.input_button.place(relx = 0.89,rely = 0.175, relheight = 0.7, relwidth = 0.082) 
        self.display_msg.config(cursor = "arrow") 
        self.input_button.bind('<Button-1>', lambda event : self.sendButton(event,self.input_msg.get('1.0', END)))

        #scroll bar
        
        self.scrollbar = Scrollbar(self.display_frame)
        self.scrollbar.pack(side = RIGHT, fill = Y)
        
        self.scrollbar.place(relheight = 1, relx = 0.98) 
        self.scrollbar.config(command = self.display_msg.yview) 
        self.display_msg.config(state = DISABLED)
        

    #COMMAND
    def sendButton(self,event, msg): 
        self.display_msg.config(state = DISABLED) 
        self.msg=msg 
        self.input_msg.delete("1.0", END) 
        snd= threading.Thread(target = self.sendMessage) 
        snd.start() 

    #RECIEVE MESSAGE
    def receive(self): 
        while True: 
            try: 
                message = client.recv(1024).decode(FORMAT)
                if message == 'NICK': 
                    client.send(self.name.encode(FORMAT)) 
                else: 
                    self.display_msg.config(state = NORMAL) 
                    self.display_msg.insert(END, message) 
                    
                    self.display_msg.config(state = DISABLED) 
                    self.display_msg.see(END) 
            except: 
                client.close() 
                break
        
    #SEND MESSAGE
    def sendMessage(self): 
        self.display_msg.config(state=DISABLED) 
        while True: 
            message = (f"{self.name}: {self.msg}") 
            client.send(message.encode(FORMAT))	 
            break

#START
g = GUI()
g.login_shelf.close()
exit()
