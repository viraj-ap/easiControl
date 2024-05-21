from tkinter import *                       #pip install psutil
from tkinter import ttk                     #pip install screen-brightness-control
from tkinter import ttk, messagebox         #pip install ctypes-callable
import tkinter as tk                        #pip install comtypes
from tkinter import filedialog              #pip install pycaw
import platform                             #pip install geopy
import psutil                               #pip install timezonefinder
#brightness                                 #pip install pytz
import screen_brightness_control as pct     #pip install tkcalendar
#audio                                      #pip install PyAutoGUI
from ctypes import cast, POINTER            #pip install requests
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
#clock
from time import strftime
#calendar
from tkcalendar import*
#open google
import pyautogui
import subprocess
import webbrowser as wb
import random
import ast

root=Tk()
root.title('Login')
root.geometry('850x500+300+170')
root.configure(bg="#fff")
root.resizable(False,False)
button_mode=True
def signin():
    username=user.get()
    password=code.get()

    file=open('datasheet.txt','r')
    d=file.read()
    r=ast.literal_eval(d)
    file.close()
    print(r.keys())
    print(r.values())
    
    if username in r.keys() and password==r[username]:
        
        screen=Toplevel(root)
        screen.title("App")
        screen.geometry('850x500+300+170')
        screen.resizable(False,False)
        screen.configure(bg="#292e2e")

        #################&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        image_icon = PhotoImage(file="icon.png")
        screen.iconphoto(False, image_icon)
        Body=Frame(screen, width=900, height=600, bg="#d6d6d6")
        Body.pack(pady=20, padx=20)
        #image_icon.place()

        LHS=Frame (Body, width=310,height=435, bg="#f4f5f5", highlightbackground="#adacb1", highlightthickness=1) 
        LHS.place(x=10,y=10)

        #logo
        photo=PhotoImage(file='laptop.png')
        myimage=Label (LHS, image=photo, background="#f4f5f5") 
        myimage.place(x=2,y=20)
        my_system = platform.uname()
        l1=Label(LHS, text = my_system.node, bg ="#f4f5f5", font=("Acumin Variable Concept" , 15 , "bold"),justify="center")
        l1.place(x=20,y=200)

        l2=Label(LHS, text = f"Version{my_system.version}", bg ="#f4f5f5", font=("Acumin Variable Concept" , 8 , "bold"),justify="center")
        l2.place(x=20,y=225)

        l3=Label(LHS, text = f"System{my_system.system}", bg ="#f4f5f5", font=("Acumin Variable Concept" ,15 , "bold"),justify="center")
        l3.place(x=20,y=250)

        l4=Label(LHS, text = f"Machine{my_system.machine}", bg ="#f4f5f5", font=("Acumin Variable Concept" , 15 , "bold"),justify="center")
        l4.place(x=20,y=285)

        l5=Label(LHS, text = f"Total RAM installed{round(psutil.virtual_memory().total/10000000000,2)} GB", bg ="#f4f5f5", font=("Acumin Variable Concept" , 15 , "bold"),justify="center")
        l5.place(x=20,y=310)

        l6=Label(LHS, text = f"Processor{my_system.processor}", bg ="#f4f5f5", font=("Acumin Variable Concept" , 7 , "bold" ),justify="center")
        l6.place(x=20,y=340)

        #------------------------
        RHS = Frame(Body, width = 470 , height = 230 , bg="#f4f5f5", highlightbackground = "#adacb1" , highlightthickness=1)
        RHS.place(x=330 ,y=10 )

        system=Label (RHS, text='System', font=("Acumin Variable Concept", 15), bg="#f4f5f5") 
        system.place(x=10,y=10)

        #----------Battery--------------#
        def convertTime(seconds):
            minutes,seconds=divmod(seconds,60)
            hours,minutes =divmod(minutes,60)
            return"%d:%02d:%02d"% (hours,minutes,seconds)
            
        def none():
            global battery_png
            global battery_label
            battery=psutil.sensors_battery()
            percent=battery.percent
            time=convertTime(battery.secsleft)
            
            lbl.config(text=f"{percent}%")
            lbl_plug.config(text=f'Plug in:{(battery.power_plugged)}')
            lbl_time.config(text=f'{time}remaining')
            
            battery_label=Label(RHS,background='#f4f5f5')
            battery_label.place(x=15,y=50)
            
            lbl.after(1000,none)
            
            if battery.power_plugged==True:
                battery_png=PhotoImage(file="charging.png")
                battery_label.config(image=battery_png)
            else:
                battery_png=PhotoImage(file="battery.png")
                battery_label.config(image=battery_png)
            
               
        lbl=Label(RHS,font=("Acumin Variable Concept",30,"bold"),bg="#f4f5f5") 
        lbl.place(x=200,y=40)
        lbl_plug=Label(RHS,font=("Acumin Variable Concept",10),bg='#f4f5f5') 
        lbl_plug.place(x=20,y=100)
        lbl_time=Label(RHS,font=("Acumin Variable Concept",15),bg='#f4f5f5') 
        lbl_time.place(x=200,y=100)

        none()      
        #----------speaker------------------
        lbl_speaker=Label(RHS,text="Speaker: ",font=('arial',10,'bold'), bg="#f4f5f5")
        lbl_speaker.place(x=10,y=150) 
        volume_value=tk.DoubleVar()

        def get_current_volume_value():
            return"{: .2f}".format(volume_value.get())
            
        def volume_changed(event):
            device=AudioUtilities.GetSpeakers()
            interface=device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL, None)
            volume=cast(interface, POINTER (IAudioEndpointVolume))
            volume.SetMasterVolumeLevel(-float(get_current_volume_value()),None)

        style=ttk.Style()
        style.configure('TScale',background='#f4f5f5')    

        volume=ttk.Scale(RHS,from_=60,to=0,orient='horizontal',command=volume_changed,variable=volume_value)
        volume.place(x=90,y=150)    
        volume.set(20)

        #------------------BRIGHTNESS------------------
        lbl_brightness=Label(RHS, text='Brightness', font=("arial",10,"bold"),bg="#f4f5f5")
        lbl_brightness.place(x=10, y=190)

        current_value=tk.DoubleVar()

        def get_current_value():
            return '{: .2f}'.format(current_value.get())

        def brightness_changed(event):
            pct.set_brightness(get_current_value())

        style=ttk.Style()
        style.configure('TScale',background='#f4f5f5')  
            
        brightness=ttk.Scale(RHS,from_=0,to=100, orient='horizontal',command=brightness_changed,variable=current_value)
        brightness.place(x=90,y=190)

        #-------------
        RHB=Frame(Body, width = 470 , height = 190 , bg="#f4f5f5", highlightbackground = "#adacb1" , highlightthickness=1)
        RHB.place(x=330 ,y=250 )
        #----------------------

        def weather():
            app1=Toplevel()
            app1.geometry("850x500+300+170")
            app1.title("Weather")
            app1.configure(bg="white")
            app1.resizable(False,False)
            
            #icon
            image_icon=PhotoImage(file="App1.png")
            app1.iconphoto(False, image_icon)
            
            def getWeather():
                try:
                    city=textfield.get()
                    geolocator=Nominatim(user_agent="geoapiExercises") 
                    location=geolocator.geocode(city) 
                    obj= TimezoneFinder()
                    result= obj.timezone_at(lng=location.longitude,lat=location.latitude)
                    
                    home=pytz.timezone(result)
                    local_time=datetime.now(home) 
                    current_time=local_time.strftime("%I:%M %p")
                    clock.config(text=current_time) 
                    name.config(text="CURRENT WEATHER") 
                    
                    #weather
                    api="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=646824f2b7b86caffec1d0b16ea77f79"
                    json_data = requests.get(api).json()
                    condition = json_data['weather'][0]['main'] 
                    description= json_data['weather'][0]['description'] 
                    temp = int(json_data['main']['temp']-273.15) 
                    pressure = json_data['main']['pressure'] 
                    humidity= json_data['main']['humidity'] 
                    wind= json_data['wind']['speed']

                    t.config(text=(temp, "°"))
                    c.config(text=(condition, "|","FEELS", "LIKE", temp, "°"))
                    
                    w.config(text=wind)
                    h.config(text=humidity)
                    d.config(text=description)
                    p.config(text=pressure)
                    
                except Exception as e:
                    messagebox.showerror("Weather App", "Invalid Entry!")            
            #searchbox
            Search_image=PhotoImage(file="search.png")
            myimage=Label(app1, image=Search_image, bg="white")
            myimage.place(x=20, y=20)
            
            textfield=tk.Entry(app1, justify = "center" , width=17 , font= ("poppins" , 25,"bold"), bg="#404040",border=0, fg="white")
            textfield.place(x=50, y=40)
            textfield.focus()
            
            Search_icon = PhotoImage(file="search_icon.png")
            myimage_icon= Button(app1, image=Search_icon,borderwidth=0,cursor="hand2", bg="#404040",command=getWeather )
            myimage_icon.place(x=400, y=34)
            
            
            #logo
            Logo_image=PhotoImage(file="logo.png")
            logo=Label(app1,image=Logo_image,bg="white")
            logo.place(x=150,y=130)
            
            #bottom box
            Frame_image=PhotoImage(file="box.png")
            frame_myimage=Label(app1, image=Frame_image , bg = 'white')
            frame_myimage.pack(padx=5, pady=5, side=BOTTOM)
            
            #time
            name=Label (app1, font=('arial', 15, 'bold'), bg="white")
            name.place(x=30,y=100)
            clock= Label (app1, font = ('Helvetica', 20), bg="white") 
            clock.place(x=30,y=130)
            #label
            label1=Label (app1, text="WIND", font=("Helvatica", 15, 'bold'), fg="white", bg="#1ab5ef") 
            label1.place (x=110, y=400) 
            
            label2=Label (app1, text="HUMIDITY", font=("Helvatica", 15, 'bold'), fg="white", bg="#1ab5ef") 
            label2.place (x=250, y=400) 
            
            
            label3=Label (app1, text="DESCRIPTION", font=("Helvatica", 15, 'bold'), fg="white", bg="#1ab5ef")
            label3.place(x=410, y=400)
            
            label4 = Label (app1, text="PRESSURE", font=("Helvatica", 15, 'bold'), fg="white", bg="#1ab5ef") 
            label4.place(x=630, y=400)
            
            t=Label (app1, font = ('arial', 70, 'bold'), fg="red", bg='white')
            t.place (x=407,y=150)
            
            c=Label (app1, font=('arial', 15, 'bold'), bg='white') 
            c.place(x=407,y=250)
            
            w=Label (app1, text="...", font = ('arial', 20, 'bold'), bg="#1ab5ef")
            w.place(x=120,y=430) 
            
            h=Label (app1, text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
            h.place(x=280,y=430)
            
            d=Label (app1, text="...", font=('arial', 20, 'bold'), bg="#1ab5ef")
            d.place(x=430, y=430) 
            
            p=Label(app1, text="..." , font = ('arial', 20, 'bold'), bg="#1ab5ef")
            p.place(x=670, y=430)
            
            app1.mainloop()
        #----------------------
        def clock():
            app2=Toplevel()
            app2.geometry("850x110+300+10")
            app2.title("Clock")
            app2.configure(bg="#292e2e")
            app2.resizable(False,False)
            
            #icon
            image_icon=PhotoImage(file="App2.png")
            app2.iconphoto(False, image_icon)
            
            def clock():
                text=strftime("%H:%M:%S %p")
                lbl.config(text=text)
                lbl.after(1000,clock)
                
            lbl=Label(app2, font=("digital-7",50,"bold"),width=20, bg="#f4f5f5", fg="#292e2e")
            lbl.pack(anchor="center", pady=20)
            clock()
                
            app2.mainloop()
        #---------------------------------
        def calendar():
            app3=Toplevel()
            app3.geometry("300x300+-10+10")
            app3.title("Calendar")
            app3.configure(bg="#292e2e")
            app3.resizable(False,False) 
            #icon 
            image_icon=PhotoImage (file="App3.png") 
            app3.iconphoto (False, image_icon)
            
            mycal =Calendar (app3, setmode=' day', date_pattern='d/m/yy') 
            mycal.pack(padx=15, pady=35)
            
            app3.mainloop()
        #---------------
        
        def mode():
            global button_mode
            if button_mode:
                LHS.config(bg="#292e2e") 
                myimage.config(bg="#292e2e")
                l1.config(bg="#292e2e", fg="#d6d6d6")
                l2.config(bg="#292e2e", fg="#d6d6d6")
                l3.config(bg="#292e2e", fg="#d6d6d6")
                l4.config(bg="#292e2e", fg="#d6d6d6") 
                l5.config(bg="#292e2e", fg="#d6d6d6")
                l6.config(bg="#292e2e", fg="#d6d6d6")
                
                RHB.config(bg="#292e2e")
                app1.config(bg="#292e2e")
                app2.config(bg="#292e2e") 
                app3.config(bg="#292e2e")
                app4.config(bg="#292e2e")
                app5.config(bg="#292e2e")
                app6.config(bg="#292e2e")
                app7.config(bg="#292e2e")
                app8.config(bg="#292e2e")
                app9.config(bg="#292e2e")
                app10.config(bg="#292e2e")
                apps.config(bg="#292e2e", fg="#d6d6d6")
                button_mode=False
            else:
                LHS.config(bg="#f4f5f5") 
                myimage.config(bg="#f4f5f5")
                l1.config(bg="#f4f5f5", fg="#292e2e")
                l2.config(bg="#f4f5f5", fg="#292e2e") 
                l3.config(bg="#f4f5f5", fg="#292e2e")
                l4.config(bg="#f4f5f5", fg="#292e2e") 
                l5.config(bg="#f4f5f5", fg="#292e2e")
                l6.config(bg="#f4f5f5", fg="#292e2e")
                
                RHB.config(bg="#f4f5f5") 
                app1.config(bg="#f4f5f5")
                app2.config(bg="#f4f5f5")
                app3.config(bg="#f4f5f5") 
                app4.config(bg="#f4f5f5")
                app5.config(bg="#f4f5f5") 
                app6.config(bg="#f4f5f5")
                app7.config(bg="#f4f5f5") 
                app8.config(bg="#f4f5f5") 
                app9.config(bg="#f4f5f5")
                app10.config(bg="#f4f5f5")
                apps.config(bg="#f4f5f5",fg="#292e2e")
                
                button_mode= True
        #------------------------------------
        apps=Label(RHB,text='Apps', font=('Acumin Variable Concept', 15), bg='#f4f5f5') 
        apps.place(x=10,y=10)  

        def game():
            app5=Toplevel()
            app5.geometry("300x500+1050+170")
            app5.title("Dice")
            app5.resizable(False,False)
            
            #icon
            image_icon=PhotoImage (file='App5.png') 
            app5.iconphoto(False,image_icon)
            ludo_image=PhotoImage (file="ludo back.png") 
            Label (app5, image=ludo_image). pack()
            label=Label (app5, text='', font=("times", 150))  
            label.pack()
            
            def roll():
                dice=['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685'] 
                label.configure(text = f'{random.choice(dice)}{random.choice(dice)}', fg="#29232e") 
                label.pack()
                
            btn_image=PhotoImage(file="ludo button.png")
            btn=Button(app5, image=btn_image, bg="#dee2e5", command=roll) 
            btn.pack(padx=10, pady=10)
            app5.mainloop()       
        #----------------------------
        app1_image=PhotoImage (file='App1.png') 
        app1=Button(RHB, image=app1_image, bd=0 ,command=weather) 
        app1.place(x=15,y=50)
        #-------------------
        def Instagram():
            wb.register('Instagram', None)
            wb.open("https://www.instagram.com/")
            
        #--------------------
        app2_image=PhotoImage (file='App2.png') 
        app2=Button(RHB, image=app2_image, bd=0 ,command=clock) 
        app2.place(x=100,y=50)

        app3_image=PhotoImage (file='App3.png') 
        app3=Button(RHB, image=app3_image, bd=0 ,command=calendar) 
        app3.place(x=185,y=50)
        
        app4_image=PhotoImage(file='App4.png') 
        app4=Button(RHB, image=app4_image, bd=0, command=mode) 
        app4.place(x=270,y=50)

        app5_image=PhotoImage (file='App5.png') 
        app5=Button (RHB, image=app5_image, bd=0, command=game) 
        app5.place(x=355,y=50)
        #---------------
        def close_window():
            screen.destroy()
            
        #-------------------

        app6_image=PhotoImage (file='App6.png') 
        app6=Button(RHB, image=app6_image, bd=0, command=Instagram) 
        app6.place(x=15,y=120)

        def file():
            subprocess.Popen(r'explorer /select, "C:\path\of\folder\file"')

        app7_image=PhotoImage (file='App7.png') 
        app7=Button(RHB, image=app7_image, bd=0, command=file) 
        app7.place(x=100,y=120)

        def close_apps():
            wb.register('chrome', None)
            wb.open("https://www.youtube.com/")
            
        app8_image=PhotoImage(file='App8.png') 
        app8=Button(RHB, image=app8_image, bd=0, command=close_apps) 
        app8.place(x=185,y=120)

        def crome():
            wb.register('chrome', None) 
            wb.open('https://www.google.com/')

        app9_image=PhotoImage(file="App9.png")
        app9=Button(RHB, image=app9_image,bd=0, command=crome)
        app9.place(x=270,y=120)

        app10_image=PhotoImage(file="App10.png")
        app10=Button(RHB, image=app10_image,bd=0, command=close_window)
        app10.place(x=355,y=120)
        #--------------------------
        screen.mainloop()

        ############&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

        
        
    else:
        messagebox.showerror('Invalid','invalid username or password')


#######@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def signup_command():
    window=Toplevel(root)
    window.title("SignUp")
    window.geometry("925x500+300+200")
    window.configure(bg="#fff")
    window.resizable(False,False)

    def signup():
        username=user.get()
        password=code.get()
        confirm_password=confirm_code.get()

        if password==confirm_password:
            try:
                file=open('datasheet.txt','r+')
                d=file.read()
                r=ast.literal_eval(d)

                dict2={username:password}
                r.update(dict2)
                file.truncate(0)
                file.close()

                file=open('datasheet.txt','w')
                w=file.write(str(r))

                messagebox.showinfo('Signup','Sucessfully sign up')
                window.destroy()

            except:
                file=open('datasheet.txt','w')
                pp=str({'Username':'password'})
                file.write(pp)
                file.close()

        else:
            messagebox.showerror('Invalid',"Both Password Should match")

    def sign():
        window.destroy()

    img = PhotoImage(file='photoin.png')
    Label(window,image=img,border=0,bg='white').place(x=50,y=90)

    frame=Frame(window,width=350,height=390,bg="#fff")
    frame.place(x=480,y=50)

    heading=Label(frame,text='Sign up',fg='#57a1f8',bg='white',font=('Microsoft yaHei UI Light',23,'bold'))
    heading.place(x=100,y=5)

#####------------------------------------------------------------
    def on_enter(e):
        user.delete(0,'end')
    def on_leave(e):
        if user.get()=='':
            user.insert(0,'Username')

    user = Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft yaHei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind('<FocusIn>',on_enter)
    user.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
######--------------------------------------------------

    def on_enter(e):
        code.delete(0,'end')
    def on_leave(e):
        if code.get()=='':
            code.insert(0,'Password')

    code = Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft yaHei UI Light',11))
    code.place(x=30,y=150)
    code.insert(0,'Password')
    code.bind('<FocusIn>',on_enter)
    code.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#####--------------------------------------------------------

    def on_enter(e):
        confirm_code.delete(0,"end")
    def on_leave(e):
        if confirm_code.get()=='':
            confirm_code.insert(0,'confirm Password')

    confirm_code = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft yaHei UI Light',11))
    confirm_code.place(x=30,y=220)
    confirm_code.insert(0,'confirm Password')    
    confirm_code.bind("<FocusIn>",on_enter)
    confirm_code.bind("<FocusOut>",on_leave)
    

    Frame(frame,width=295,height=2,bg="black").place(x=25,y=247)

######--------------------------------------------------

    Button(frame,width=39,pady=7,text="Sign Up",bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
    label=Label(frame,text='I have an account',fg='black',bg='white',font=('Microsoft yaHei UI Light',9))
    label.place(x=90,y=340)

    signin=Button(frame,width=6,text='Sign In',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=sign)
    signin.place(x=200,y=340)
    
    window.mainloop()


#####@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22

        
img = PhotoImage(file='photoin.png')
Label(root,image=img,bg='white').place(x=50,y=50)

frame=Frame(root,width=350,height=350,bg="white")
frame.place(x=480,y=70)

heading=Label(frame,text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft yaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

user = Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft yaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')

code = Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft yaHei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

Button(frame,width=39,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
label=Label(frame,text="Don't have an account?",bg='white',font=('Microsoft yaHei UI Light',9))
label.place(x=75,y=270)

sign_up=Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
sign_up.place(x=215,y=270)

root.mainloop()
