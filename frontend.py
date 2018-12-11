from tkinter import * #import tkinter library (despkot interface)
import backend
import os
import http.client
import json
import subprocess




creds = 'tempfile.temp'
def Illness_Drug():
    e4.delete(0,END)
    e4.insert(END,e5.get())
    e6.delete(0,END)
    e6.insert(END,selected_tuple_2)
    search_window.destroy()

def Search_Illness():
    global list2,Illness_text,e5,search_window,e10
    search_window=Tk() #create a window
    Illness_text=StringVar()
    e5=Entry(search_window,textvariable=Illness_text)
    e5.grid(row=0,column=1)


    b1=Button(search_window,text="Search Illness", width=12,command=get_events)
    b1.grid(row=0,column=0, sticky=W)

    b2=Button(search_window,text="Add", width=12,command=Illness_Drug)
    b2.grid(row=13,column=0)


    b3=Button(search_window,text="Cancel", width=12, command=search_window.destroy)
    b3.grid(row=13,column=1)

    list2=Listbox(search_window, height=6,width=35, fg="blue", selectbackground="black")
    list2.grid(row=2,column=0, columnspan=2)

    l11=Label(search_window,text="Reactions")
    l11.grid(row=11,column=0)

    Reactions=StringVar()
    e10=Entry(search_window,textvariable=Reactions, width=35)
    e10.grid(row=12,column=0, columnspan=2)

    list2.bind('<<ListboxSelect>>',get_selected_row_2)

    sb2=Scrollbar(search_window)
    sb2.grid(row=2,column=2,rowspan=6)

    list2.configure(yscrollcommand=sb2.set)
    sb2.configure(command=list2.yview)

    search_window.mainloop()

def server():
    subprocess.Popen("server.py", shell=True)

def Signup(): # This is the signup definition,
    global pwordE # These globals just make the variables global to the entire script, meaning any definition can use them
    global nameE
    global roots

    roots = Tk() # This creates the window, just a blank one.
    roots.title('Signup') # This renames the title of said window to 'signup'
    intruction = Label(roots, text='Please Enter new Credidentials\n') # This puts a label, so just a piece of text saying 'please enter blah'
    intruction.grid(row=0, column=0, sticky=E) # This just puts it in the window, on row 0, col 0. If you want to learn more look up a tkinter tutorial :)

    nameL = Label(roots, text='New Centername: ') # This just does the same as above, instead with the text new username.
    pwordL = Label(roots, text='New Password: ') # ^^
    nameL.grid(row=1, column=0, sticky=W) # Same thing as the instruction var just on different rows. :) Tkinter is like that.
    pwordL.grid(row=2, column=0, sticky=W) # ^^

    nameE = Entry(roots) # This now puts a text box waiting for input.
    pwordE = Entry(roots, show='*') # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
    nameE.grid(row=1, column=1) # You know what this does now :D
    pwordE.grid(row=2, column=1) # ^^

    signupButton = Button(roots, text='Signup', command=FSSignup) # This creates the button with the text 'signup', when you click it, the command 'fssignup' will run. which is the def
    signupButton.grid(columnspan=2, sticky=W)
    roots.mainloop() # This just makes the window keep open, we will destroy it soon

def FSSignup():
    with open(creds, 'w') as f: # Creates a document using the variable we made at the top.
        f.write(nameE.get()) # nameE is the variable we were storing the input to. Tkinter makes us use .get() to get the actual string.
        f.write('\n') # Splits the line so both variables are on different lines.
        f.write(pwordE.get()) # Same as nameE just with pword var
        f.close() # Closes the file
    roots.destroy()
    Login()

def Login():
    global nameEL
    global pwordEL # More globals :D
    global rootA

    rootA = Tk() # This now makes a new window.
    rootA.title('Login') # This makes the window title 'login'

    intruction = Label(rootA, text='Please Login\n') # More labels to tell us what they do
    intruction.grid(sticky=E) # Blahdy Blah

    nameL = Label(rootA, text='Centername: ') # More labels
    pwordL = Label(rootA, text='Password: ') # ^
    nameL.grid(row=1, sticky=W)
    pwordL.grid(row=2, sticky=W)

    nameEL = Entry(rootA) # The entry input
    pwordEL = Entry(rootA, show='*')
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)

    loginB = Button(rootA, text='Login', command=CheckLogin) # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(columnspan=2, sticky=W)


    rootA.mainloop()


def CheckLogin():
    with open(creds) as f:
        global uname, pword
        data = f.readlines() # This takes the entire document we put the info into and puts it into the data variable
        uname = data[0].rstrip() # Data[0], 0 is the first line, 1 is the second and so on.
        pword = data[1].rstrip() # Using .rstrip() will remove the \n (new line) word from before when we input it
        f.close()


        if nameEL.get() == uname and pwordEL.get() == pword: # Checks to see if you entered the correct data.
                rootA.destroy()
                window()
        else:
            r = Tk()
            r.title('D:')
            r.geometry('150x50')
            rlbl = Label(r, text='\n[!] Invalid Login')
            rlbl.pack()
            r.mainloop()

OPENFDA_API_URL = "api.fda.gov"
OPENFDA_API_EVENT="/drug/event.json"


def reaction(event):
    reactions = ''
    for reaction in event["patient"]["reaction"]:
        reactions+=  reaction["reactionmeddrapt"] + ','
    reactions = reactions[:-1]
    return reactions

def get_selected_row_2(event):
    global selected_tuple_2, reactions
    index=list2.curselection()[0]
    selected_tuple_2=list2.get(index)
    reactions = list_dict[index][selected_tuple_2]
    print(reactions)
    print(index)
    e10.delete(0,END)
    e10.insert(END,reactions)




def get_events():
    global events, list_dict
    illness=e5.get()
    print(illness)
    conn = http.client.HTTPSConnection(OPENFDA_API_URL)
    conn.request("GET",OPENFDA_API_EVENT+"?search=patient.drug.drugindication:" +illness +"&limit=10")
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data1 = r1.read()
    data = data1.decode("utf8")
    events= json.loads(data)
    drugs=[]
    try:
        for event in events["results"]:
            try:
                reactionmeddrapt = reaction(event)
                for patient in event["patient"]["drug"]:
                    medicinalproduct=patient["medicinalproduct"]
                    try:
                        drugindication=patient["drugindication"]

                        if drugindication==e5.get():
                            drugs+=[ 'Drug : ' + medicinalproduct + ' - ' + 'Adverse reaction :' + reactionmeddrapt]
                    except:
                        print("hello")
            except:
                print("Hello")

    except:
        if events["error"]["code"]=="SERVER_ERROR":
            r = Tk()
            r.title('D:')
            r.geometry('150x50')
            rlbl = Label(r, text='\n PLEASE FILL OUT THE BOX')
            rlbl.pack()
            r.mainloop()

        elif  events["error"]["code"]=="NOT_FOUND":
            r = Tk()
            r.title('D:')
            r.geometry('150x50')
            rlbl = Label(r, text='\nILLNESS NOT FOUND')
            rlbl.pack()
            r.mainloop()

    filtered_list=[]
    a = 'Off label use'
    b = 'Incorrect route of drug administration'
    for raw in drugs:
        ar=raw.split('-')
        adverse_reactions = ar[1].split(':')
        possible_reactions = adverse_reactions[1]
        list_possible_reactions = possible_reactions.split(',')
        if (a not in list_possible_reactions) and (b not in list_possible_reactions):
            filtered_list += [raw]


    list2.delete(0,END)
    print(filtered_list)
    list_dict = []
    for raw in filtered_list:
        ar=raw.split('-')
        adverse_reactions = ar[1].split(':')
        reactions = adverse_reactions[1]
        drugs= ar[0].split(':')
        drug = drugs[1]
        dict1= {drug:reactions}
        print (dict1)
        list_dict += [dict1]

        list2.insert(END,drug)




def window():
    global window
    global list1, e1,e2,e3,e4,e6,e7
    global Patient_text, Doctor_text, Data_text, Codeillness_text, Drug_text, Telefone_text
    window=Tk() #create a window
    window.title(uname)
    l1=Label(window,text="Patient")
    l1.grid(row=0,column=0)

    b1=Button(window,text="★", width=1,command=Search_Illness)
    b1.grid(row=1,column=4)

    b1=Button(window,text="Open Web",command=server)
    b1.grid(row=3,column=1)

    l2=Label(window,text="Doctor")
    l2.grid(row=0,column=2)

    l3=Label(window,text="Date")
    l3.grid(row=1,column=0)

    title=Label(window,text="Appoiment dates")
    title.grid(row=3,column=0)


    l4=Label(window,text="illness")
    l4.grid(row=1,column=2)

    l6=Label(window, text="Drug")
    l6.grid(row=2,column=0)

    l7=Label(window,text="telefone")
    l7.grid(row=2,column=2)

    Patient_text=StringVar()
    e1=Entry(window,textvariable=Patient_text)
    e1.grid(row=0,column=1)

    Doctor_text=StringVar()
    e2=Entry(window,textvariable=Doctor_text)
    e2.grid(row=0,column=3)

    Data_text=StringVar()
    e3=Entry(window,textvariable=Data_text)
    e3.grid(row=1,column=1)

    Codeillness_text=StringVar()
    e4=Entry(window,textvariable=Codeillness_text)
    e4.grid(row=1,column=3)

    Drug_text=StringVar()
    e6 = Entry(window, textvariable=Drug_text)
    e6.grid(row=2,column=1)

    Telefone_text=StringVar()
    e7= Entry(window,textvariable=Telefone_text)
    e7.grid(row=2,column=3)

    list1=Listbox(window, height=6,width=45, fg="blue", selectbackground="black")
    list1.grid(row=3,column=0,rowspan=6, columnspan=2)

    sb1=Scrollbar(window)
    sb1.grid(row=3,column=2,rowspan=10,sticky=W)

    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)

    list1.bind('<<ListboxSelect>>',get_selected_row)#Cada vez que la lista es selecionada se ejecuta el comando
    b1=Button(window,text="View all", width=15, command=view_command)
    b1.grid(row=4,column=3,columnspan=2)

    b2=Button(window,text="Search entry", width=15, command=search_command)
    b2.grid(row=5,column=3,columnspan=2)

    b3=Button(window,text="Add entry", width=15, command=add_command)
    b3.grid(row=6,column=3,columnspan=2)

    b4=Button(window,text="Update", width=15, command=update_command)
    b4.grid(row=7,column=3,columnspan=2)

    b5=Button(window,text="Delete", width=15, command=delete_command)
    b5.grid(row=8,column=3,columnspan=2)

    b6=Button(window,text="Close", width=15, command=window.destroy)
    b6.grid(row=8,column=0,sticky=W)

    rmuser = Button(window, text='Delete User', fg='red', width=15, command=DelUser) # This makes the deluser button. blah go to the deluser def.
    rmuser.grid(row=8,column=1,sticky=W)

    window.mainloop()

def view_command():
    list1.delete(0,END)
    for row in backend.view():
        list1.insert(END,row)

def search_command():
    list1.delete(0,END)
    for row in backend.search(Patient_text.get(), Doctor_text.get(), Data_text.get(), Codeillness_text.get(), Drug_text.get(), Telefone_text.get()):
        list1.insert(END,row)

def add_command():
    backend.insert(Patient_text.get(), Doctor_text.get(), Data_text.get(), Codeillness_text.get(), Drug_text.get(), Telefone_text.get())
    list1.delete(0,END)
    list1.insert(END, Patient_text.get(), Doctor_text.get(), Data_text.get(), Codeillness_text.get(),Drug_text.get(), Telefone_text.get())

def get_selected_row(event):#comando que se ejecuta cada vez que la lista es selecionada, actualizando la variable selected_tuple
    global selected_tuple
    index=list1.curselection()[0]
    selected_tuple=list1.get(index)
    e1.delete(0,END)
    e1.insert(END,selected_tuple[1])
    e2.delete(0,END)
    e2.insert(END,selected_tuple[2])
    e3.delete(0,END)
    e3.insert(END,selected_tuple[3])
    e4.delete(0,END)
    e4.insert(END,selected_tuple[4])
    e6.delete(0,END)
    e6.insert(END,selected_tuple[5])
    e7.delete(0,END)
    e7.insert(END,selected_tuple[6])




def update_command():
    backend.update(selected_tuple[0], Patient_text.get(), Doctor_text.get(), Data_text.get(), Codeillness_text.get(),Drug_text.get(),Telefone_text.get())
    view_command()

def delete_command():
    backend.delete(selected_tuple[0])#como la variable esta globalizada no es necesario obtener el return
    view_command()

def DelUser():

    window.destroy() # Destroys the login window
    os.remove('tempfile.temp') # Removes the file
    Signup() # And goes back to the start!



if os.path.isfile(creds):
    Login()
else: # This if else statement checks to see if the file exists. If it does it will go to Login, if not it will go to Signup :)
    Signup()
