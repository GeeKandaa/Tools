import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from subprocess import Popen, PIPE
from os import path
import os

#DEBUG
#import logging, sys
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
#logging.debug('A debug message!')
#logging.info('We processed %d records', len(processed_records))

##########################################################
#   # Main Window
class Window(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.master = master
        self.init_window()
   # Instantiation
    def init_window(self):
      
    # Initialisation
        self.master.title("GitTool")
        self.master.geometry("1000x800")
        self.master.resizable(width=0, height=0)
        self.pack(fill=tk.BOTH, expand=1)

    # Menu Bar
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
       # File menu
        file = tk.Menu(menu)
        file.add_command(label="Set 'studio' Repository", command=cmd.set_repo)
        file.add_command(label="Exit", command=cmd.client_exit)
        menu.add_cascade(label="File", menu=file)
       # Help menu
        help = tk.Menu(menu)
        help.add_command(label="About", command=cmd.client_exit)
        help.add_command(label="Documentation", command=cmd.client_exit)
        menu.add_cascade(label="Help", menu=help)

    # Main holder
        self.main = tk.PanedWindow(self, orient="horizontal", bd=0, bg = refer2.BACKGROUND)
        self.main.pack(expand=1, fill = tk.BOTH)
       # Text Display
        self.display = displayholder(self.main)
        self.main.add(self.display)
       # UI Buttons
        self.btns = Button_Holder(self.main)
        self.main.add(self.btns)
        self.btns.init_self()
       # Traffic Light Display
        self.light_display = trafficLight(self.main)
        self.main.add(self.light_display)

    # First run complete
        refer2.firstTime = False

  # Class Functions:
   # Mode dinstinction
    def clearScreen(self):
        self.main.forget(self.display)
        self.main.forget(self.light_display)
        self.main.forget(self.btns)
    def setGeometry(self, x,y):
        self.master.geometry( str(x) +"x"+ str(y) )
        self.width = x
        self.height = y
   # Mode function
    def switch_mode(self):
        self.clearScreen()
        if refer2.mini_mode:
            self.setGeometry(300,350)
         # Generate Mini Layout
           # Regenerate Buttons
            self.btns = Button_Holder(self.main)
            self.btns.init_self()
           # Add Buttons
            self.main.add(self.btns)
            self.main.paneconfigure(self.btns, minsize=self.width*2/3)
           # Regenerate Light
            self.light_display = trafficLight(self.main)
           # Add Light
            self.main.add(self.light_display)
            self.main.paneconfigure(self.light_display, minsize=self.width*1/3)
        else:
            self.setGeometry(1000,800)
         # Generate Maxi Layout
           # Add Display
            self.main.add(self.display)
            self.main.paneconfigure(self.display, minsize=self.width*4/6)
           # Regenerate Buttons       
            self.btns = Button_Holder(self.main)
            self.btns.init_self()
           # Add Buttons
            self.main.add(self.btns)
            self.main.paneconfigure(self.btns, minsize=self.width/6)
           # Regenerate Light
            self.light_display = trafficLight(self.main)
           # Add Light
            self.main.add(self.light_display)
            self.main.paneconfigure(self.light_display, minsize=self.width/6)
        app.update()        
#########################################################
#   # UI Element Classes:
class trafficLight(tk.Canvas):
    def __init__(self, master=None):
        self.do_Blink = False
        tk.Canvas.__init__(self, master, bd =5, relief="groove", bg = refer2.BACKGROUND)
        if refer2.firstTime:
            self.light = self.create_oval(0, 0, 0, 0, fill="red" )
        else:
            app.update_idletasks()
            h = master.winfo_height()
            w = master.winfo_width()*1/3
            if refer2.mini_mode:
                self.light = self.create_oval( w/2-27, h/2-27, w/2+23, h/2+23, fill="red" )
            else:
                self.light = self.create_oval(w/2-87-50,h/2-25-50,w/2-87+50,h/2-25+50, fill="red")
            self.updateLight()
    def updateLight(self):
        clr = refer2.colour
        if clr == "BLINK":
            self.do_Blink = False
            self.after(350, self.SetUp_Blink)
        else:
            self.itemconfig(self.light, fill=clr)
    def SetUp_Blink(self):
        self.do_Blink = True
        self.blink()
    def dont_Blink(self):
        self.do_Blink=False
    def blink(self):
        if self.do_Blink:
            current_colour = self.itemcget(self.light, "fill")
            new_colour = "red" if current_colour == "orange" else "orange"
            self.itemconfigure(self.light, fill=new_colour)
            self.after(300, self.blink)
class Button_Holder(tk.LabelFrame):
    def __init__(self,master=None):
        tk.LabelFrame.__init__(self, master, text="Git Commands", bd=0, bg = refer2.BACKGROUND)
        self.btn_spec = [("Check Status", cmd.check_status), 
        ("De-Chaff", cmd.double_chaff), 
        ("Reset Branch", cmd.reset_branch), 
        ("New Branch", cmd.new_branch), 
        ("Switch Branch", cmd.branch_switch), 
        (refer2.alt_mode_string(), cmd.toggle_mode),
        ("Quit", cmd.client_exit)]
        
    def init_self(self):
        for i in range(0, len(self.btn_spec)):
            txt, cmd = self.btn_spec[i]
            if refer2.mini_mode:
                btn = tk.Button(self, text=txt, font=("Helvetica","10","bold"), height=int(1), command=cmd, bg = refer2.FOREGROUND, fg = refer2.BACKGROUND )
            else:
                btn = tk.Button(self, text=txt, font=("Helvetica","16","bold"), height=int(2), command=cmd, bg = refer2.FOREGROUND, fg = refer2.BACKGROUND )    
            btn.pack(side = tk.TOP, fill=tk.X, expand =1)
class displayholder(tk.PanedWindow):
    def __init__(self,master=None):
        self.master = master
        tk.PanedWindow.__init__(self, master, bd=0, orient="vertical", bg = refer2.BACKGROUND)
        #Status Windows
        status1 = tk.LabelFrame(self, text="Studio", bg = refer2.BACKGROUND)
        status2 = tk.LabelFrame(self, text="Shared_Code", bg = refer2.BACKGROUND)
        self.add(status1)
        self.add(status2)
        #Status Window Text Display
        self.stat1 = DynText(status1)
        self.stat2 = DynText(status2)
        self.stat1.pack(side = tk.TOP, expand=1,fill=tk.BOTH)
        self.stat2.pack(side = tk.TOP, expand=1,fill=tk.BOTH)
class DynText(tk.Text):
    def __init__(self,master=None):
        tk.Text.__init__(self, master, bg="#000000", fg="#FFFFFF", state="disabled")

    def set_text(self, strings):
        self.configure(state="normal")
        self.delete(1.0,tk.END)
        self.insert(tk.END,strings)
        self.configure(state="disabled")

##########################################################
#   # Commands
class Commands():
    def __init__(self):
        self.exists = True
   # Menu Commands
    def client_exit(self):
        exit()
    def set_repo(self):
        file_path = filedialog.askdirectory()
        if file_path != '':
            repo.set_repo(file_path)
   
   # App Commands
    def light_on(self, state):
        if state == "clean":
            app.light_display.dont_Blink()
            colour = "green"
        elif state == "dirty":
            app.light_display.dont_Blink()
            colour = "orange"
        elif state == "error":
            colour = "BLINK"
        refer2.colour = colour
        app.light_display.updateLight()
    def toggle_mode(self):
        refer2.switch_mode()
        app.switch_mode()

   # Git Button Commands
    def check_status(self):
        # Parse output for light_display
        git_command = ['git', 'status', '--porcelain']
        os.chdir(repo.path)
        (output_studio, err_int) = self.Git_Command_sub(git_command)
        os.chdir(repo.shared_path)
        (output_shared, err_int) = self.Git_Command_sub(git_command)
        if output_studio == b'' and output_shared == b'':
            self.light_on("clean")
        else:
            self.light_on("dirty")
        # Display output for text display
        git_command = ['git', 'status']
        self.Git_Command_Studio(git_command, 1)
        self.Git_Command_Shared(git_command, 1)
        # INTEGRITY CHECK
        repo.check_integrity()
    def check_status_is_clean(self, function_string_id):
        git_command = ['git', 'status', '--porcelain']
        os.chdir(repo.path)
        (output_studio,err_int_studio) = self.Git_Command_sub(git_command)
        os.chdir(repo.shared_path)
        (output_shared,err_int_shared) = self.Git_Command_sub(git_command)

        if output_studio != b'' or output_shared != b'':
            if output_studio != b'':
                msg_studio ="Unstaged changes in 'studio':\n"
                msg_studio+=output_studio.decode("utf-8")
                app.display.stat1.set_text(msg_studio)
            else:
                app.display.stat1.set_text("Studio repository clean.")
            if output_shared !=b'':
                msg_shared ="Unstaged changes in 'shared_code':\n"
                msg_shared+=output_shared.decode("utf-8")
                app.display.stat2.set_text(msg_shared)
            else:
                app.display.stat2.set_text("Shared_Code repository clean.")
            messagebox.showwarning(function_string_id, "Please ensure your repo is clean.")
            return False
        else:
            return True

    def double_chaff(self):
        os.chdir(repo.path +r"\..\GitTool\Spine")
        git_command = ["doublechaff.bat",repo.path]
        app.display.stat1.set_text("Dechaffing..\nThis may take some time.")
        app.display.stat2.set_text("(It's not frozen, just busy..)")
        app.update_idletasks()
        (output,err_int) = self.Git_Command_sub(git_command)
        app.display.stat1.set_text(output)
        app.display.stat2.set_text("Repo dechaffed.")

    def new_branch(self):
        if self.check_status_is_clean("Cannot create new branch"):
            self.new_branch_sub()
            self.check_status()
    def new_branch_sub(self):
        to_branch = simpledialog.askstring("New Branch", "Please enter the new branch.")
        from_branch = simpledialog.askstring("New Branch", "Please enter the source branch.")
        if to_branch is not None:
            if from_branch is not None:
                git_command = [['git', 'checkout', from_branch],['git', 'fetch'],['git','pull','origin',from_branch]]
                self.Git_Command_Shared(git_command)
                self.Git_Command_Studio(git_command)   
                git_command = [['git','checkout','-b',to_branch],['git','push','origin',to_branch],['git','branch','-u','origin/'+to_branch]]
                self.Git_Command_Shared(git_command)
                self.Git_Command_Studio(git_command)

    def branch_switch(self):
            if self.check_status_is_clean("Cannot switch branch"):
                self.branch_switch_sub()
                self.check_status()
    def branch_switch_sub(self):
        to_branch = simpledialog.askstring("Switch Branch", "Please enter desired branch.")
        if to_branch is not None:
            git_command = [['git', 'checkout', to_branch],['git', 'pull', 'origin', to_branch]]
            self.Git_Command_Shared(git_command)
            self.Git_Command_Studio(git_command)

    def reset_branch(self):
        git_command = ['git', 'reset', 'head', '--h']                
        self.Git_Command_Shared(git_command, 1)
        self.Git_Command_Studio(git_command, 1)

   # Git Communicate
    def Git_Command_Studio(self, git_commands, result = 0):
        os.chdir(repo.path)
        if isinstance(git_commands[0], list):
            for cmds in git_commands:
                (output,err_int) = self.Git_Command_sub(cmds)
                if result == 0:
                    app.display.stat1.set_text(err_int)
                else:
                    app.display.stat1.set_text(output)
                # Select case?
                root.update()
        else:
            (output,err_int) = self.Git_Command_sub(git_commands)
            if result == 0:
                app.display.stat1.set_text(err_int)
            else:
                app.display.stat1.set_text(output)
    def Git_Command_Shared(self, git_commands, result = 0):
        os.chdir(repo.shared_path)
        if isinstance(git_commands[0], list):
            for cmds in git_commands:
                (output,err_int) = self.Git_Command_sub(cmds)
                if result == 0:
                    app.display.stat2.set_text(err_int)
                else:
                    app.display.stat2.set_text(output)
                root.update()
        else:
            (output,err_int) = self.Git_Command_sub(git_commands)
            if result == 0:
                app.display.stat2.set_text(err_int)
            else:
                app.display.stat2.set_text(output)
    def Git_Command_sub(self, order):
            git_query = Popen(order, shell=True, stdout=PIPE, stderr=PIPE)
            (output,err_int) = git_query.communicate()
            return (output, err_int)

##########################################################
    # Class #5; Display Dictionary
class UI_Comm():
    def __init__(self):
        self.dict = {}
        self.BACKGROUND = "#939371"
        self.FOREGROUND = "#424242"
        self.mini_mode = False
        self.firstTime  = True
        self.colour = "red"
    def switch_mode(self):
        self.mini_mode = not self.mini_mode
    def alt_mode_string(self):
        if self.mini_mode:
            return "Maxi Mode"
        else:
            return "Mini Mode"

###########################################################
    # Class #6; Repo Details
class RepoDetails():
    def __init__(self):
        init_path = os.getcwd() + r"\..\studio"
        if os.path.isdir(init_path) and os.path.isdir(init_path + r"\shared_code"):
            self.path = init_path
            self.shared_path = init_path + r"\shared_code"
        else:
            messagebox.showwarning("Warning", "Repo could not be found, please manually set repo directory.")
    def check_integrity(self):
        cmds = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        os.chdir(self.path)
        (output_studio,err_int) = cmd.Git_Command_sub(cmds)
        os.chdir(self.shared_path)
        (output_shared,err_int) = cmd.Git_Command_sub(cmds)
        if err_int != b'' or str(output_shared) != str(output_studio):
            cmd.light_on("error")
    def set_repo(self,path):
        set_failed = False
        msg = "Repo could not be set:"
        if not os.path.isdir(path+r"\..\studio"):
            msg = msg + "\n - studio directory missing."
            set_failed = True
        if not os.path.isdir(path + r"\shared_code"):
            msg = msg + "\n - shared_code directory missing."
            set_failed = True
        if set_failed:
            messagebox.showwarning("Warning",msg)
        else:
            self.path = path
            self.shared_path = path +r"\shared_code"
            messagebox.showinfo("Congrats ;)","Repo set succesfully.")

# Root window generation
cmd = Commands()
root = tk.Tk()
root.configure(bg = "#737331")
# print(root.configure())
repo = RepoDetails()
refer2 =  UI_Comm()
app = Window(root)
app.update_idletasks()
app.switch_mode()
root.mainloop()