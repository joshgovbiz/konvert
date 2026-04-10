import logging
import os
import sys
import tkinter as tk
import os 
import subprocess 
import time
import customtkinter as ctk
import threading
from PIL import Image
from tkinter import ttk
from tkinter import filedialog

output_text = ""

# Set up log file in same directory as script
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "converter.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)  
    ]
)
logger = logging.getLogger(__name__)

def save_file():

    input_path = text_box.get()                    # get full path from text box
    input_name = os.path.splitext(os.path.basename(input_path))[0]  # extract name only

    save_path = filedialog.asksaveasfilename(
        title="Save File As",
        initialfile=input_name,
        defaultextension=".mp3",        # auto adds extension if user doesn't type it
        filetypes=[("MP3", "*.mp3")]
    )
    if save_path:  # only runs if user didn't cancel
        #logger.info(save_path)  # do your save logic here
        logger.info("Converted " + text_box.get() + " \nto\n" + save_path)
        return save_path;


def browse_file():
    filename = filedialog.askopenfilename(
        title="Select a File",
       # filetypes=[("GSM", "*.gsm"), ("WAV", "*.wav*")]  # customize as needed
       filetypes=[("WAV", "*.wav"), ("GSM", "*.gsm*")]
    )
    if filename:  # only update if user didn't cancel
        text_box.delete(0, tk.END)       # clear existing text
        text_box.insert(0, filename)  
        text_box_out.delete(0, tk.END)     # insert selected filename
        return filename;



def prep():
    #labelDone.place(x=50,y=250)
    text_box_out.delete(0, tk.END) 

    progress_bar.place(x=50, y=300)
    progress_bar.configure(mode="indeterminate")
    progress_bar.start()


def convert_to_mp3(input_path, output_path):
  

    time.sleep(1)  

    try:
        subprocess.run([
            "ffmpeg",
            "-i", input_path,        # input file
            "-y",                    # overwrite output if exists
            output_path              # output file
        ], check=True)
        
        
        output_text = output_path
    
        tk.messagebox.showinfo("Success", f"File converted successfully!\nSaved to: {output_path}")
        text_box_out.insert(0, output_path)
    
    except subprocess.CalledProcessError as e:
        tk.messagebox.showerror("Error", f"Conversion failed!\n{e}")
    
    except FileNotFoundError:
        tk.messagebox.showerror("Error", "ffmpeg not found!\nPlease install ffmpeg and add it to your PATH.")

def button_open():
    save_path = text_box_out.get()
    print(f"save_path: '{save_path}'")          

    output_dir = os.path.dirname(save_path)
    output_dir = output_dir.replace("/", "\\")
    print(f"output_dir: '{output_dir}'")        
    subprocess.Popen(f'explorer "{output_dir}"')

def button_clicked():


    input_path = text_box.get()                    # get full path from text box
    input_name = os.path.splitext(os.path.basename(input_path))[0]  # extract name only
    save_path = filedialog.asksaveasfilename(
        title="Save File As",
        initialfile=input_name,
        defaultextension=".mp3",        # auto adds extension if user doesn't type it
        filetypes=[("MP3", "*.mp3")]
    )
    if save_path:  # only runs if user didn't cancel
          # do your save logic here
        logger.info("\n=====================================\n" + input_path + "\nCONVERTED TO...\n" + save_path + "\n=====================================")
       # return save_path;

       # wherever you stored the save path

    if not input_path or not save_path:
        tk.messagebox.showwarning("Warning", "Please select input and output files first!")
        return
 

    prep()
    convert_to_mp3(input_path, save_path)
    
    progress_bar.stop()
    

    


main_window = tk.Tk()
main_window.geometry("600x400")
main_window.title("Konvert")
main_window.config(bg="#9929EA")


##ASSETS##

##
# traqlogo


label = ctk.CTkLabel(main_window, text="KONVERT", font=("", 40))       
label.place(x=200, y=0)


##PGBAR

progress_bar = ctk.CTkProgressBar(main_window, width=500)
progress_bar.set(0)                  # 0.0 to 1.0

#  (loading animation)
progress_bar.configure(mode="indeterminite")
         

# Stop it when done
progress_bar.stop()


##LABELS
label = tk.Label(main_window,
                 text ="Konvert",
                 font=("Century Gothic", 14, "bold"))
#label.place(x=50,y=0)

labelDone = tk.Label(main_window,
                 text ="STARTING!",
                 font=("Century Gothic", 14, "bold"))

# CREATING BUTTONS TO SELECT INPUT AND TO CONVERT TO OUTPUT
##INPUT
browse_button = ctk.CTkButton(main_window,
                        # Size
                        width=500,
                        height=45,
                        corner_radius=12,          # rounding

                        # Text
                        text="BROWSE FILES",
                        font=("Century Gothic", 14, "bold"),
                        text_color="white",

                        # Colors
                        fg_color="#4E4E4E",         # normal background
                        hover_color="#357abd",       # hover background
                        border_color="#2d6a9f",      # border color
                        border_width=2,
                        command=browse_file)

browse_button.place(x=50, y=100)


##CONVERT / OUTPUT# Rounded button
button = ctk.CTkButton(main_window,
                        # Size
                        width=500,
                        height=45,
                        corner_radius=12,          # rounding

                        # Text
                        text="CONVERT",
                        font=("Century Gothic", 14, "bold"),
                        text_color="white",

                        # Colors
                        fg_color="#363636",         # normal background
                        hover_color="#357abd",       # hover background
                        border_color="#2d6a9f",      # border color
                        border_width=2,

                        # Icon (optional)
                        # image=my_ctk_image,       # CTkImage object
                        # compound="left",          # icon position

                        command=button_clicked)
button.place(y=200, x=50)



##OPENDIR# Rounded button
button_open = ctk.CTkButton(main_window,
                        # Size
                        width=500,
                        height=45,
                        corner_radius=12,          # rounding

                        # Text
                        text="OPEN",
                        font=("Century Gothic", 14, "bold"),
                        text_color="white",

                        # Colors
                        fg_color="#666666",         # normal background
                        hover_color="#357abd",       # hover background
                        border_color="#2d6a9f",      # border color
                        border_width=2,

                        # Icon (optional)
                        # image=my_ctk_image,       # CTkImage object
                        # compound="left",          # icon position

                        command=button_open)
button_open.place(y=350, x=50)

###TEXTBOXES TO SELECT FILE####

# text_box INPUTPATH
text_box = ctk.CTkEntry(main_window,
                         width=500,
                         height=35,
                         corner_radius=8,          # rounding
                         font=("Arial", 12))
text_box.place(x=50, y=150)



# text_box OUTPATH
text_box_out = ctk.CTkEntry(main_window,
                         width=500,
                         height=35,
                         corner_radius=8,          # rounding
                         font=("Arial", 12))
text_box_out.place(x=50, y=250)


####


main_window.mainloop()


