import customtkinter
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox
import os
import subprocess
from customtkinter import filedialog
from ctk_scrollable_dropdown import *
from PIL import Image, ImageTk


def typeallow():
    file_type=[]
    for i in range(20):
          string=""
          string1=""
          if(0<i<10):
                string=".E0"+str(i)
                string1=".e0"+str(i)
          elif(i>=10 and i!=0):
                string=".E"+str(i)
                string1=".e"+str(i)
          tupla=("Encase", string)
          tupla2=("Encase", string1)
          file_type.append(tupla)
          file_type.append(tupla2)
    return file_type

def change_appearance_mode_event(self):
        customtkinter.set_appearance_mode(appearance_mode_optionemenu.get())


def create(name, ops, files):
   os_not_efi=["WindowsXP", "WindowsXP_64", "Windows2003", "Windows2003_64", "WindowsVista", "Windows7", "Windows7_64"]
   esecuzione=os.popen("sudo ls '/root/VirtualBox VMs/' ")
   risultati=esecuzione.read().split("\n")
   if (len(files)==0):
            messagebox.showerror(title=None, message="No file selected!")
   elif (name==""):
            messagebox.showerror(title=None, message="Insert a valid name!")
   elif (ops==""):
            messagebox.showerror(title=None, message="Select an operative system!")
   elif (name in risultati):
            messagebox.showerror(title=None, message="Existing VM with this name. Change it!")

   else:
            command="sudo VBoxManage createvm --name " + name +" --ostype "+ ops + " --register"
            out=subprocess.run(command, capture_output=True, shell=True)
            if(ops in os_not_efi):
                 command2= "sudo VBoxManage modifyvm " + name + " --cpus 2 --memory 1700 --vram 70 --firmware bios --rtcuseutc=on"
            else:
                 command2= "sudo VBoxManage modifyvm " + name + " --cpus 2 --memory 1700 --vram 70 --firmware efi --rtcuseutc=on"
            out=subprocess.run(command2, capture_output=True, shell=True)
            filess= ''.join(files)
            try:
                command4="sudo mkdir /mnt/"+name
                out=subprocess.run(command4, capture_output=True, shell=True)
            except:
                pass
            file_path=os.path.splitext(files[0])[0]
            file_name = file_path.split('/')[-1]
            command3="sudo xmount --in ewf " + filess + " --out vmdk --cache ./disk_cache /mnt/"+name+""
            out=subprocess.run(command3, capture_output=True, shell=True)
            command5="sudo VBoxManage internalcommands createrawvmdk -filename '/root/VirtualBox VMs/"+name+"/"+name+".vmdk' -rawdisk '/mnt/"+name+"/"+file_name+".dd'"
            out=subprocess.run(command5, capture_output=True, shell=True)
            command6="sudo VBoxManage storagectl "+name+" --name 'SATA Controller' --add sata --controller IntelAHCI --portcount 1 --bootable on"
            out=subprocess.run(command6, capture_output=True, shell=True)
            command7="sudo VBoxManage storageattach "+name+"  --storagectl 'SATA Controller' --device 0 --port 0 --type hdd --medium '/root/VirtualBox VMs/"+name+"/"+name+".vmdk'"
            out=subprocess.run(command7, capture_output=True, shell=True)
            response=messagebox.askquestion("Success!", "Do you want to start the newly created case virtual machine?", options="yes")
            if (response=="yes"):
                command8="sudo VBoxManage startvm "+name
                out=subprocess.run(command8, capture_output=True, shell=True)

def openvm(name):
   command="sudo VBoxManage startvm "+name
   out=subprocess.run(command, capture_output=True, shell=True)
   if(out.stderr):
     messagebox.showerror(title=None, message="Please, check the image is mounted")

def function(attr, frame, button):
    optionlist=["VBoxBS_64", "JRockitVE", "QNX", "L4", "Netware", "DOS", "MacOS1012_64", "MacOS1011_64", "MacOS1010_64", "MacOS109_64",
                    "MacOS108_64", "MacOS107_64", "MacOS106_64", "MacOS106", "MacOS", "OS2", "OS2Arca0S", "WindowsXP", "WindowsXP_64"
                    , "Windows2003", "Windows2003_64", "WindowsVista", "WindowsVista_64", "Windows2008_64", "Windows2008", "Windows7", "Windows7_64", "Windows8", "Windows8_64", "Windows81", "Windows81_64", "Windows2012_64", "Windows10", 
                    "Windows10_64", "Windows2016_64", "Windows2019_64", "Windows11_64", "WindowsNT_64", "WindowsNT", "Linux22", "Linux24", "Linux24_64", "Linux26", "Linux26_64", "ArchLinux", "ArchLinux_64", "Debian", "Debian_64", "Fedora", 
                    "Fedora_64", "Gentoo", "Gentoo_64", "Mandriva", "Mandriva_64", "Oracle", "Oracle_64", "RedHat", "RedHat_64", "OpenSUSE", "OpenSUSE_64", "Turbolinux", "Turbolinux_64", "Ubuntu",
                    "Ubuntu_64", "Xandros", "Xandros_64", "Linux", "Linux_64"]
    file_type=typeallow()
    
    optionlist.sort()

    if(attr=="Create new case"):
      for widget in frame.winfo_children():
         widget.grid_forget()
      files=filedialog.askopenfilenames(title="Select EXX files", filetypes=file_type)
      title_app=customtkinter.CTkLabel(frame, text="Selected files:", font=customtkinter.CTkFont(size=20))
      title_app.grid(row=0, column=0, padx=10, pady=(20, 10))
      text_files=customtkinter.CTkTextbox(frame, corner_radius=5,height=80, width=300)
      text_files.grid(row=1, column=0, padx=(20, 20), pady=(10, 10), sticky="ew")
      if(len(files)!=0):
         for i in range(len(files)):
            text_files.insert('end',files[i])
            text_files.insert('end', "\n")
      else:
         text_files.insert('end', "No file selected!")
      text_files.configure(state="disabled")
      label_name = customtkinter.CTkLabel(frame, text="Case name:")
      label_name.grid(row=2, column=0, padx=(20, 20), pady=(10, 10), sticky="w")
      entry_name = customtkinter.CTkEntry(frame, width=300, placeholder_text="Insert here the VM's name")
      entry_name.grid(row=2, column=0, padx=(20, 20), pady=(10, 10), sticky="e")
      label_os = customtkinter.CTkLabel(frame, text="Operating System:")
      label_os.grid(row=3, column=0, padx=(20, 20), pady=(10, 10), sticky="w")
      combo=customtkinter.CTkComboBox(frame,  corner_radius=4, width=300, hover=FALSE)
      CTkScrollableDropdown(combo, values=optionlist, autocomplete=TRUE)
      combo.grid(row=3, column=0, padx=(20, 20), pady=(10, 10), sticky="e")
      button_create=customtkinter.CTkButton(frame, text="Create", font=customtkinter.CTkFont(size=18, weight="bold"), command=lambda: create(entry_name.get(), combo.get(), files))
      button_create.grid(row=5, column=0, padx=20, pady=10)
      
      
    else:
      for widget in frame.winfo_children():
         widget.grid_forget()
      esec=os.popen("sudo ls '/root/VirtualBox VMs/'")
      listVm=esec.read().split("\n")
      listVm.remove("")
      title_app=customtkinter.CTkLabel(frame, text="Choose and open an existing case:", font=customtkinter.CTkFont(size=20))
      title_app.grid(row=0, column=0, padx=10, pady=(20, 10))
      OptionMenu1=customtkinter.CTkOptionMenu(frame, values=listVm, font=customtkinter.CTkFont(size=16)) 
      OptionMenu1.grid(row=1, column=0, padx=20, pady=10)
      button_select1=customtkinter.CTkButton(frame, text="Open", font=customtkinter.CTkFont(size=18, weight="bold"), command=lambda: openvm(OptionMenu1.get()))
      button_select1.grid(row=2, column=0, padx=20, pady=10)

      
    
      

#MAIN
os.popen("sudo apt-get update -y")
os.popen("sudo apt-get install -y xmount")
customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("blue") 
window = customtkinter.CTk()


window.iconbitmap("/home/sara/Desktop/Tesi project/1_eCF_icon.ico")
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure((2, 3), weight=0)
window.grid_rowconfigure((0, 1, 2), weight=1)
frame=customtkinter.CTkFrame(window, width=180, corner_radius=0)
frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
frame.grid_rowconfigure(4, weight=1)


window.title("EnCase2VM")
window.minsize(700, 600)
window.maxsize(700,600)
title_app=customtkinter.CTkLabel(frame, text="EnCase2VM", font=customtkinter.CTkFont(size=30, weight="bold"), text_color="#2271b3")
title_app.grid(row=0, column=0, padx=20, pady=(20, 10))
OptionMenu=customtkinter.CTkOptionMenu(frame, values=["Open new case", "Create new case"], font=customtkinter.CTkFont(size=16)) 
OptionMenu.grid(row=1, column=0, padx=20, pady=10)
button_select=customtkinter.CTkButton(frame, text="Start", font=customtkinter.CTkFont(size=18, weight="bold"), command=lambda: function(OptionMenu.get(), slider_progressbar_frame, button_select))
button_select.grid(row=3, column=0, padx=20, pady=10)
appearance_mode_label = customtkinter.CTkLabel(frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(frame, values=["Light", "Dark", "System"], command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))


slider_progressbar_frame = customtkinter.CTkFrame(window, fg_color="transparent")
slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
slider_progressbar_frame.grid_columnconfigure(0, weight=1)
slider_progressbar_frame.grid_rowconfigure(4, weight=1)

im = Image.open('/home/sara/Desktop/Tesi project/1_eCF_icon.ico')
photo = ImageTk.PhotoImage(im)
window.wm_iconphoto(True, photo)

window.mainloop()



