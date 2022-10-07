import socket
from threading import Thread
from tkinter import *

# nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")


class gui:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        self.login = Toplevel()
        self.login.title("login screen")
        self.login.configure(width=400, height=400)
        self.login.resizable(width=False, height=False)
        self.message = Label(self.login, text="Please login to continue",
                             justify=CENTER, font=("monospace", 15))
        self.message.place(relheight=0.15, relx=0.2, rely=0.07)

        self.label = Label(self.login, text="name:", font=("monospace", 15))
        self.label.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entry = Entry(self.login, font=("monospace", 15))
        self.entry.place(relheight=0.12, relwidth=0.4, relx=0.35, rely=0.2)
        self.entry.focus()

        self.goButton = Button(self.login, text="continue", font=(
            "monospace", 15), command=lambda: self.nextpg(self.entry.get()))
        self.goButton.place(relx=0.4, rely=0.55)

        self.window.mainloop()

    def nextpg(self, name):
        self.login.destroy()
        self.chatScreen(name)
        recieve = Thread(target=self.recv)
        recieve.start()

    def chatScreen(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title("chat screen")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg="lightcyan")

        self.header = Label(self.window, bg="lightcyan", fg="black",
                            text=self.name, font=("monospace", 15), pady=5)
        self.header.place(relwidth=1)
        self.headerLine = Label(self.window, width=450, bg="white")
        self.headerLine.place(relwidth=1, relheight=0.05, rely=0.07)

        self.textBox = Text(self.window, width=20, height=2, bg="black",
                            fg="white", font=("monospace", 15), padx=5, pady=5)
        self.textBox.place(relwidth=1, relheight=0.745, rely=0.08)

        self.buttonName = Label(self.window, bg="yellow", height=80)
        self.buttonName.place(relwidth=1, rely=0.825)

        self.textMsg = Entry(self.buttonName, bg="red",
                             fg="black", font=("monospace", 15))
        self.textMsg.place(relwidth=1, relheight=0.06, relx=0.011, rely=0.008)
        self.textMsg.focus()

        self.buttonMsg = Button(self.buttonName, text="send button", font=(
            "monospace", 15), width=20, bg="blue", fg="white", command=lambda: self.sendData(self.textMsg.get()))
        self.buttonMsg.place(relwidth=0.22, relheight=0.06,
                             relx=0.77, rely=0.008)

        self.textBox.config(cursor="arrow")

        scrollbar = Scrollbar(self.textBox)
        scrollbar.place(relheight=1, relx=0.97)
        scrollbar.config(command=self.textBox.yview)

        self.textBox.config(state=DISABLED)

    def sendData(self, message):
        self.textBox.config(state=DISABLED)
        self.message=message
        self.textMsg.delete(0,END)
        send=Thread(target=self.write)
        send.start()

    def showMsg(self,message):
        self.textBox.config(state=NORMAL)
        self.textBox.insert(END,message+"\n")
        self.textBox.config(state=DISABLED)
        self.textBox.see(END)
    
    def recv(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMsg(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.textBox.config(state=DISABLED)
        while True:
            message = '{}: {}'.format(self.name,self.message)
            client.send(message.encode('utf-8'))
            self.showMsg(message)
            break

g = gui()


