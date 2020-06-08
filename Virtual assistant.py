import speech_recognition as sr
import webbrowser
import playsound
import os
import sys
import time
import random
from gtts import gTTS
from googletrans import Translator
import smtplib
from time import ctime
from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import askcolor
import pygame
import sys
import math
from tkinter import ttk
import os

r= sr.Recognizer()
def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            Joe_speak(ask)
        audio=r.listen(source)
        voice_data=''
        try:
            voice_data=r.recognize_google(audio)
        except sr.UnknownValueError:
            Joe_speak("Sorry, I did not get that.")
        except sr.RequestError:
            Joe_speak("Sorry my speech service is down")
        return voice_data
    
def Joe_speak(audio_string):
    tts=gTTS(text=audio_string, lang="en")
    r=random.randint(1, 1000000)
    audio_file="audio-"+str(r)+".mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_file)
    os.remove(audio_file)
        
def respond(voice_data):
    if "what is your name" in voice_data:
        Joe_speak("My name is Darcy")
    if "encrypt" in voice_data:
        def encrypter(string, shift):   
            ciper=""
            for char in string:
                if char=='':
                    ciper=ciper+ciper
                elif char.isupper():
                    ciper=ciper+chr((ord(char)+shift-65)%26+65)
                else:
                    ciper=ciper+chr((ord(char)+shift-97)%26+97)
            return ciper   
        text=input("Enter text ")
        print("Enter a key")
        sec_key=int(input())
        print("The encrypted message is:",encrypter(text, sec_key))
    if "decrypt" in voice_data:
        def decrypter(string, shift):   
            ciper=""
            for char in string:
                if char=='':
                    ciper=ciper+ciper
                elif char.isupper():
                    ciper=ciper+chr((ord(char)+shift-65)%26+65)
                else:
                    ciper=ciper+chr((ord(char)+shift-97)%26+97)
            return ciper   
        text=input("Enter text ")
        print("Enter a key")
        sec_key=int(input())
        sec_key=-sec_key
        print("The decrypted message is:",decrypter(text, sec_key))
    if "sudoko solver" in voice_data:
        Joe_speak("It is now opening")
        from solver import solve, valid
        import time
        pygame.font.init()
        
        
        class Grid:
            board = [
                [7, 8, 0, 4, 0, 0, 1, 2, 0],
                [6, 0, 0, 0, 7, 5, 0, 0, 9],
                [0, 0, 0, 6, 0, 1, 0, 7, 8],
                [0, 0, 7, 0, 4, 0, 2, 6, 0],
                [0, 0, 1, 0, 5, 0, 9, 3, 0],
                [9, 0, 4, 0, 6, 0, 0, 0, 5],
                [0, 7, 0, 3, 0, 0, 0, 1, 2],
                [1, 2, 0, 0, 0, 7, 4, 0, 0],
                [0, 4, 9, 2, 0, 6, 0, 0, 7]
            ]
        
            def __init__(self, rows, cols, width, height):
                self.rows = rows
                self.cols = cols
                self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
                self.width = width
                self.height = height
                self.model = None
                self.selected = None
        
            def update_model(self):
                self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
        
            def place(self, val):
                row, col = self.selected
                if self.cubes[row][col].value == 0:
                    self.cubes[row][col].set(val)
                    self.update_model()
        
                    if valid(self.model, val, (row,col)) and solve(self.model):
                        return True
                    else:
                        self.cubes[row][col].set(0)
                        self.cubes[row][col].set_temp(0)
                        self.update_model()
                        return False
        
            def sketch(self, val):
                row, col = self.selected
                self.cubes[row][col].set_temp(val)
        
            def draw(self, win):
                # Draw Grid Lines
                gap = self.width / 9
                for i in range(self.rows+1):
                    if i % 3 == 0 and i != 0:
                        thick = 4
                    else:
                        thick = 1
                    pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
                    pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)
        
                # Draw Cubes
                for i in range(self.rows):
                    for j in range(self.cols):
                        self.cubes[i][j].draw(win)
        
            def select(self, row, col):
                # Reset all other
                for i in range(self.rows):
                    for j in range(self.cols):
                        self.cubes[i][j].selected = False
        
                self.cubes[row][col].selected = True
                self.selected = (row, col)
        
            def clear(self):
                row, col = self.selected
                if self.cubes[row][col].value == 0:
                    self.cubes[row][col].set_temp(0)
        
            def click(self, pos):
                """
                :param: pos
                :return: (row, col)
                """
                if pos[0] < self.width and pos[1] < self.height:
                    gap = self.width / 9
                    x = pos[0] // gap
                    y = pos[1] // gap
                    return (int(y),int(x))
                else:
                    return None
        
            def is_finished(self):
                for i in range(self.rows):
                    for j in range(self.cols):
                        if self.cubes[i][j].value == 0:
                            return False
                return True
        
        
        class Cube:
            rows = 9
            cols = 9
        
            def __init__(self, value, row, col, width ,height):
                self.value = value
                self.temp = 0
                self.row = row
                self.col = col
                self.width = width
                self.height = height
                self.selected = False
        
            def draw(self, win):
                fnt = pygame.font.SysFont("comicsans", 40)
        
                gap = self.width / 9
                x = self.col * gap
                y = self.row * gap
        
                if self.temp != 0 and self.value == 0:
                    text = fnt.render(str(self.temp), 1, (128,128,128))
                    win.blit(text, (x+5, y+5))
                elif not(self.value == 0):
                    text = fnt.render(str(self.value), 1, (0, 0, 0))
                    win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        
                if self.selected:
                    pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)
        
            def set(self, val):
                self.value = val
        
            def set_temp(self, val):
                self.temp = val
        
        
        def redraw_window(win, board, time, strikes):
            win.fill((255,255,255))
            # Draw time
            fnt = pygame.font.SysFont("comicsans", 40)
            text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
            win.blit(text, (540 - 160, 560))
            # Draw Strikes
            text = fnt.render("X " * strikes, 1, (255, 0, 0))
            win.blit(text, (20, 560))
            # Draw grid and board
            board.draw(win)
        
        
        def format_time(secs):
            sec = secs%60
            minute = secs//60
            hour = minute//60
        
            mat = " " + str(minute) + ":" + str(sec)
            return mat
        
        
        def main():
            win = pygame.display.set_mode((540,600))
            pygame.display.set_caption("Sudoku")
            board = Grid(9, 9, 540, 540)
            key = None
            run = True
            start = time.time()
            strikes = 0
            while run:
        
                play_time = round(time.time() - start)
        
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            key = 1
                        if event.key == pygame.K_2:
                            key = 2
                        if event.key == pygame.K_3:
                            key = 3
                        if event.key == pygame.K_4:
                            key = 4
                        if event.key == pygame.K_5:
                            key = 5
                        if event.key == pygame.K_6:
                            key = 6
                        if event.key == pygame.K_7:
                            key = 7
                        if event.key == pygame.K_8:
                            key = 8
                        if event.key == pygame.K_9:
                            key = 9
                        if event.key == pygame.K_DELETE:
                            board.clear()
                            key = None
                        if event.key == pygame.K_RETURN:
                            i, j = board.selected
                            if board.cubes[i][j].temp != 0:
                                if board.place(board.cubes[i][j].temp):
                                    print("Success")
                                else:
                                    print("Wrong")
                                    strikes += 1
                                key = None
        
                                if board.is_finished():
                                    print("Game over")
                                    run = False
        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        clicked = board.click(pos)
                        if clicked:
                            board.select(clicked[0], clicked[1])
                            key = None
        
                if board.selected and key != None:
                    board.sketch(key)
        
                redraw_window(win, board, play_time, strikes)
                pygame.display.update()
        
        
        main()
        pygame.quit()
    if "Tell me the time" in voice_data:
         Joe_speak(ctime()) 
    if "open path finder" in voice_data:
        Joe_speak("It is opening now")
        screen = pygame.display.set_mode((800, 800))
    
        class spot:
            def __init__(self, x, y):
                self.i = x
                self.j = y
                self.f = 0
                self.g = 0
                self.h = 0
                self.neighbors = []
                self.previous = None
                self.obs = False
                self.closed = False
                self.value = 1
        
            def show(self, color, st):
                if self.closed == False :
                    pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
                    pygame.display.update()
        
            def path(self, color, st):
                pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
                pygame.display.update()
        
            def addNeighbors(self, grid):
                i = self.i
                j = self.j
                if i < cols-1 and grid[self.i + 1][j].obs == False:
                    self.neighbors.append(grid[self.i + 1][j])
                if i > 0 and grid[self.i - 1][j].obs == False:
                    self.neighbors.append(grid[self.i - 1][j])
                if j < row-1 and grid[self.i][j + 1].obs == False:
                    self.neighbors.append(grid[self.i][j + 1])
                if j > 0 and grid[self.i][j - 1].obs == False:
                    self.neighbors.append(grid[self.i][j - 1])
        
        
        cols = 50
        grid = [0 for i in range(cols)]
        row = 50
        openSet = []
        closedSet = []
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        grey = (220, 220, 220)
        w = 800 / cols
        h = 800 / row
        cameFrom = []
        
        # create 2d array
        for i in range(cols):
            grid[i] = [0 for i in range(row)]
        
        # Create Spots
        for i in range(cols):
            for j in range(row):
                grid[i][j] = spot(i, j)
        
        
        # Set start and end node
        start = grid[12][5]
        end = grid[3][6]
        # SHOW RECT
        for i in range(cols):
            for j in range(row):
                grid[i][j].show((255, 255, 255), 1)
        
        for i in range(0,row):
            grid[0][i].show(grey, 0)
            grid[0][i].obs = True
            grid[cols-1][i].obs = True
            grid[cols-1][i].show(grey, 0)
            grid[i][row-1].show(grey, 0)
            grid[i][0].show(grey, 0)
            grid[i][0].obs = True
            grid[i][row-1].obs = True
        
        def onsubmit():
            global start
            global end
            st = startBox.get().split(',')
            ed = endBox.get().split(',')
            start = grid[int(st[0])][int(st[1])]
            end = grid[int(ed[0])][int(ed[1])]
            window.quit()
            window.destroy()
        
        window = Tk()
        label = Label(window, text='Start(x,y): ')
        startBox = Entry(window)
        label1 = Label(window, text='End(x,y): ')
        endBox = Entry(window)
        var = IntVar()
        showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
        
        submit = Button(window, text='Submit', command=onsubmit)
        
        showPath.grid(columnspan=2, row=2)
        submit.grid(columnspan=2, row=3)
        label1.grid(row=1, pady=3)
        endBox.grid(row=1, column=1, pady=3)
        startBox.grid(row=0, column=1, pady=3)
        label.grid(row=0, pady=3)
        
        window.update()
        mainloop()
        
        pygame.init()
        openSet.append(start)
        
        def mousePress(x):
            t = x[0]
            w = x[1]
            g1 = t // (800 // cols)
            g2 = w // (800 // row)
            acess = grid[g1][g2]
            if acess != start and acess != end:
                if acess.obs == False:
                    acess.obs = True
                    acess.show((255, 255, 255), 0)
        
        end.show((255, 8, 127), 0)
        start.show((255, 8, 127), 0)
        
        loop = True
        while loop:
            ev = pygame.event.get()
        
            for event in ev:
                if event.type == pygame.QUIT:
                    pygame.quit()
                if pygame.mouse.get_pressed()[0]:
                    try:
                        pos = pygame.mouse.get_pos()
                        mousePress(pos)
                    except AttributeError:
                        pass
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        loop = False
                        break
        
        for i in range(cols):
            for j in range(row):
                grid[i][j].addNeighbors(grid)
        
        def heurisitic(n, e):
            d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
            #d = abs(n.i - e.i) + abs(n.j - e.j)
            return d
        
        
        def main():
            end.show((255, 8, 127), 0)
            start.show((255, 8, 127), 0)
            if len(openSet) > 0:
                lowestIndex = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[lowestIndex].f:
                        lowestIndex = i
        
                current = openSet[lowestIndex]
                if current == end:
                    print('done', current.f)
                    start.show((255,8,127),0)
                    temp = current.f
                    for i in range(round(current.f)):
                        current.closed = False
                        current.show((0,0,255), 0)
                        current = current.previous
                    end.show((255, 8, 127), 0)
        
                    Tk().wm_withdraw()
                    result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance \n to the path is ' + str(temp) + ' blocks away, \n would you like to re run the program?'))
                    if result == True:
                        os.execl(sys.executable,sys.executable, *sys.argv)
                    else:
                        ag = True
                        while ag:
                            ev = pygame.event.get()
                            for event in ev:
                                if event.type == pygame.KEYDOWN:
                                    ag = False
                                    break
                    pygame.quit()
        
                openSet.pop(lowestIndex)
                closedSet.append(current)
        
                neighbors = current.neighbors
                for i in range(len(neighbors)):
                    neighbor = neighbors[i]
                    if neighbor not in closedSet:
                        tempG = current.g + current.value
                        if neighbor in openSet:
                            if neighbor.g > tempG:
                                neighbor.g = tempG
                        else:
                            neighbor.g = tempG
                            openSet.append(neighbor)
        
                    neighbor.h = heurisitic(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
        
                    if neighbor.previous == None:
                        neighbor.previous = current
            if var.get():
                for i in range(len(openSet)):
                    openSet[i].show(green, 0)
        
                for i in range(len(closedSet)):
                    if closedSet[i] != start:
                        closedSet[i].show(red, 0)
            current.closed = True
        
        
        while True:
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                pygame.quit()
            pygame.display.update()
            main()
    if "search" in voice_data:
        search=record_audio("What do you want to search for")
        url="https://google.com/search?q="+search
        webbrowser.get().open(url)
        Joe_speak("Here is what I found for"+search)  
    if "find location" in voice_data:
        location=record_audio("What is the location?")
        url="https://google.nl/maps/place/"+ location + '/&amp;'
        webbrowser.get().open(url)
        Joe_speak("Here is the location of " + location)
    if "Hi Darcy" in voice_data:
        Joe_speak("Hello, it is nice to meet you")
    if "open website" in voice_data:
        website=record_audio("What is the website you wish to open")
        webbrowser.open(website)
        Joe_speak("Website has opened successfully")
    if "calculate" in voice_data:
        google_calci="https://www.google.com/search?sxsrf=ALeKk024yeqqla7BkJNNJlWKqawy-F9IEg%3A1589001042762&source=hp&ei=Uju2Xqa4LKeX4-EPv6mG8A8&q=calculator&oq=calc&gs_lcp=CgZwc3ktYWIQAxgAMgQIIxAnMgQIABBDMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BQgAEIMBOgcIABCDARBDOgcIIxDqAhAnUNIKWKclYJwwaARwAHgAgAGjAogB1wmSAQUwLjcuMZgBAKABAaoBB2d3cy13aXqwAQo&sclient=psy-ab"
        webbrowser.open(google_calci)
        Joe_speak("The calculater has opened succesfully")
    if "How old are you?" in voice_data:
        Joe_speak("I am as old as you")
    if "painter" in voice_data:
        Joe_speak("Painter app is opening")
        class Paint(object):
        
            DEFAULT_PEN_SIZE = 5.0
            DEFAULT_COLOR = 'black'
        
            def __init__(self):
                self.root = Tk()
        
                self.pen_button = Button(self.root, text='pen', command=self.use_pen)
                self.pen_button.grid(row=0, column=0)
        
                self.brush_button = Button(self.root, text='brush', command=self.use_brush)
                self.brush_button.grid(row=0, column=1)
        
                self.color_button = Button(self.root, text='color', command=self.choose_color)
                self.color_button.grid(row=0, column=2)
        
                self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
                self.eraser_button.grid(row=0, column=3)
        
                self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
                self.choose_size_button.grid(row=0, column=4)
        
                self.c = Canvas(self.root, bg='white', width=600, height=600)
                self.c.grid(row=1, columnspan=5)
        
                self.setup()
                self.root.mainloop()
        
            def setup(self):
                self.old_x = None
                self.old_y = None
                self.line_width = self.choose_size_button.get()
                self.color = self.DEFAULT_COLOR
                self.eraser_on = False
                self.active_button = self.pen_button
                self.c.bind('<B1-Motion>', self.paint)
                self.c.bind('<ButtonRelease-1>', self.reset)
        
            def use_pen(self):
                self.activate_button(self.pen_button)
        
            def use_brush(self):
                self.activate_button(self.brush_button)
        
            def choose_color(self):
                self.eraser_on = False
                self.color = askcolor(color=self.color)[1]
        
            def use_eraser(self):
                self.activate_button(self.eraser_button, eraser_mode=True)
        
            def activate_button(self, some_button, eraser_mode=False):
                self.active_button.config(relief=RAISED)
                some_button.config(relief=SUNKEN)
                self.active_button = some_button
                self.eraser_on = eraser_mode
        
            def paint(self, event):
                self.line_width = self.choose_size_button.get()
                paint_color = 'white' if self.eraser_on else self.color
                if self.old_x and self.old_y:
                    self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                       width=self.line_width, fill=paint_color,
                                       capstyle=ROUND, smooth=TRUE, splinesteps=36)
                self.old_x = event.x
                self.old_y = event.y
        
            def reset(self, event):
                self.old_x, self.old_y = None, None
        
        
        if __name__ == '__main__':
            Paint()
    if "send email" in voice_data:
        def send_mail():
            Joe_speak("Who is the sender of this email?")
            sender=input()
            passcode="ftzyoirmasfuhakt"
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender,passcode)
            Joe_speak("What is the subject of your email?")
            subject=record_audio()
            Joe_speak("What is the body of your email?")
            body=record_audio()
            msg=f"subject: {subject}\n\n{body}"
            Joe_speak("Who is the reciever of this email?")
            rec=input()
            server.sendmail(
                 sender,
                 rec,
                 msg)
            server.quit() 
            gmail="www.gmail.com"
            Joe_speak("Do you want to open Gmail")
            x=record_audio()
            if x=="yes":
                webbrowser.open(gmail)
                Joe_speak("This email has been sent")
            if x=="no":
                Joe_speak('This email has been sent')
        send_mail()

#password has been sent to ftzyoirmasfuhakt
    if "translate" in voice_data:
        Joe_speak("What is the starting language?")
        start_lang=record_audio()
        Joe_speak("What is the final language?")
        final_lang=record_audio()
        Joe_speak("What is the sentance?")
        sent=record_audio()
        translator=Translator()
        trans_sent=translator.translate(sent, src=start_lang, dest=final_lang)
        Joe_speak(trans_sent.text)
    if "can you talk" in voice_data:
        Joe_speak("Yes I can talk  like a human")
    if "open my contacts" in voice_data:
        Joe_speak("Your contacts are now opening")
        root = Tk()
        root.title("Phone Book")
        root.geometry("900x600")
        
        tframe = Frame(root)
        tframe.pack(side = TOP)
        
        v0 = StringVar()
        v1 = StringVar()
        v2 = StringVar()
        v3 = StringVar()
        v4 = StringVar()
        v5 = StringVar()
        v6 = StringVar()
        v7 = StringVar()
        v8 = StringVar()
        id_no = StringVar()
        s0 = StringVar()
        
        
        def save_in_file():
            global mlist
        
            global a0, a1, a2, a3, a4
        
            a0 = id_no.get()
            a1 = v5.get()
            a2 = v6.get()
            a3 = v7.get()
            a4 = v8.get()
        
            mlist = [a0,a1,a2,a3,a4]
            with open("db.txt", 'w') as f:
                for i in mlist:
                    f.write(i + '|')
                f.write('\n')
        
        
        def save_in_file2():
            global nlist
            nlist = []
            m = v0.get()
            a = v1.get()
            b = v2.get()
            c = v3.get()
            d = v4.get()
        
            nlist = [m, a, b, c, d]
        
            with open("db.txt", 'a+') as f:
                for i in nlist:
                    f.write(i + '|')
                f.write('\n')
        
        
        def add_number():
        
            global window2
            window2 = Toplevel(root)
            window2.geometry("900x600")
            window2.title("Add Contact")
            root.withdraw()
            btn4 = Button(window2, text="Back to the main menu", font=("arial", 8, "bold"), width=20, command=add_back)
            btn4.pack(side = LEFT)
        
            ttframe = Frame(window2)
            ttframe.pack(side = TOP)
            bbframe = Frame(window2)
            bbframe.pack(side = TOP)
        
            lbl = Label(ttframe, text="Contact ID", fg="black", font=("arial", 12, "bold"))
            lbl.grid(row=0, column=0, sticky=E)
            entry = Entry(ttframe, bd=7, textvariable=v0)
            entry.grid(row=0, column=1, sticky=W)
        
            lbl2 = Label(ttframe, text="First Name", fg="black", font=("arial", 12, "bold"))
            lbl2.grid(row = 1,column = 0,sticky = E)
            entry1 = Entry(ttframe, bd=7,textvariable = v1)
            entry1.grid(row = 1,column = 1,sticky = W)
        
            lbl3 = Label(ttframe, text="Last Name", fg="black", font=("arial", 12, "bold"))
            lbl3.grid(row = 2,column = 0,sticky = E)
            entry2 = Entry(ttframe, bd=7,textvariable = v2)
            entry2.grid(row = 2,column = 1,sticky = W)
        
            lbl4 = Label(ttframe, text="Phone Number", fg="black", font=("arial", 12, "bold"))
            lbl4.grid(row = 3,column = 0,sticky = E)
            entry3 = Entry(ttframe, bd=7,width = 25,textvariable = v3)
            entry3.grid(row = 3,column = 1)
        
            lbl5 = Label(ttframe, text="Address", fg="black", font=("arial", 12, "bold"))
            lbl5.grid(row = 4,column = 0,sticky = E)
            entry4 = Entry(ttframe, bd=7,width = 25,textvariable = v4)
            entry4.grid(row = 4,column = 1)
        
            btns = Button(bbframe,text = "Save info",fg = 'red',font = ("arial",12,"bold"),command = save_in_file2)
            btns.pack(side = LEFT)
        
        
        def add_back():
        
            window2.withdraw()
            root.deiconify()
        
        
        def edit_number():
        
            global window3
            window3 = Toplevel(root)
            window3.geometry("900x600")
            window3.title("Edit Contact")
            tttframe = Frame(window3)
            tttframe.pack(side = TOP)
            root.withdraw()
            btn5 = Button(window3, text="Back to the main menu", font=("arial", 8, "bold"), width=20, command=edit_back)
            btn5.pack(side = LEFT)
        
            lbl01 = Label(tttframe, text="Enter the contact ID you wish to edit",fg="black", font=("arial", 12, "bold"))
            lbl01.grid(row=0, column=0, sticky=E)
            entry01 = Entry(tttframe, bd=7, textvariable = id_no)
            entry01.grid(row=0, column=1, sticky=W)
        
            def edit_check():
        
                    global a0, a1, a2, a3, a4,x,v5,v6,v7,v8
                    with open("db.txt", 'r') as f:
        
                        y = f.readlines()
        
                        x = y[0].split("|")
        
                        a0 = x[0]
                        a1 = x[1]
                        a2 = x[2]
                        a3 = x[3]
                        a4 = x[4]
        
                        if id_no.get() == a0 or id_no.get() == nlist[0]:
        
                            lbl10 = Label(tttframe, text="First Name", fg="black", font=("arial", 12, "bold"))
                            lbl10.grid(row=2, column=0, sticky=E)
                            entry10 = Entry(tttframe, bd=7, text=a1,textvariable = v5)
                            entry10.grid(row=2, column=1, sticky=W)
        
                            lbl11 = Label(tttframe, text="Last Name", fg="black", font=("arial", 12, "bold"))
                            lbl11.grid(row=3, column=0, sticky=E)
                            entry11 = Entry(tttframe, bd=7, text=a2,textvariable = v6)
                            entry11.grid(row=3, column=1, sticky=W)
        
                            lbl13 = Label(tttframe, text="Phone Number", fg="black", font=("arial", 12, "bold"))
                            lbl13.grid(row=4, column=0, sticky=E)
                            entry13 = Entry(tttframe, bd=7, text=a3,textvariable = v7)
                            entry13.grid(row=4, column=1, sticky=W)
        
                            lbl14 = Label(tttframe, text="Address", fg="black", font=("arial", 12, "bold"))
                            lbl14.grid(row=5, column=0, sticky=E)
                            entry14 = Entry(tttframe, bd=7, text=a4,textvariable = v8)
                            entry14.grid(row=5, column=1, sticky=W)
        
            btns = Button(tttframe,text = "Click here to save your edit", command=save_in_file)
            btns.grid(row = 5,column = 8)
        
            btncheck = Button(window3, text="Click here to edit your contact", command=edit_check)
            btncheck.pack(side=TOP)
        
            def display():
        
                global a0, a1, a2, a3, a4,x
        
                with open("db.txt", 'r') as f:
                    z = f.readlines()
                    x = z[0].split("|")
                    a0 = x[0]
                    a1 = x[1]
                    a2 = x[2]
                    a3 = x[3]
                    a4 = x[4]
        
        
        
                window3.withdraw()
                window99 = Toplevel(root)
                window99.geometry("900x600")
                window99.title("Display Saved Contacts")
                frame99 = Frame(window99)
                frame99.pack()
        
                lbl03 = Label(frame99, text="Contact ID", fg="black", font=("arial", 12, "bold"))
                lbl03.grid(row=2, column=0, sticky=E)
                lbl04 = Label(frame99, bd=7, text=a0)
                lbl04.grid(row=2, column=1, sticky=W)
        
                lbl03 = Label(frame99, text="First Name", fg="black", font=("arial", 12, "bold"))
                lbl03.grid(row=3, column=0, sticky=E)
                lbl04 = Label(frame99, bd=7, text=a1)
                lbl04.grid(row=3, column=1, sticky=W)
        
                lbl05 = Label(frame99, text="Last Name", fg="black", font=("arial", 12, "bold"))
                lbl05.grid(row=4, column=0, sticky=E)
                lbl06 = Label(frame99, bd=7, text=a2)
                lbl06.grid(row=4, column=1, sticky=W)
        
                lbl07 = Label(frame99, text="Phone Number", fg="black", font=("arial", 12, "bold"))
                lbl07.grid(row=5, column=0, sticky=E)
                lbl08 = Label(frame99, bd=7, text=a3)
                lbl08.grid(row=5, column=1, sticky=W)
        
                lbl09 = Label(frame99, text="Address", fg="black", font=("arial", 12, "bold"))
                lbl09.grid(row=6, column=0, sticky=E)
                lbl10 = Label(frame99, bd=7, text=a4)
                lbl10.grid(row=6, column=1, sticky=W)
        
                buttonq = Button(frame99,text = "Quit",fg = 'red',command = root.destroy)
                buttonq.grid(row = 8,column = 4)
        
                def edit_back2():
        
                    window99.withdraw()
                    window3.deiconify()
                buttonback = Button(frame99,text = "Back",fg = 'red',command = edit_back2)
                buttonback.grid(row = 8,column = 2)
        
            display = Button(window3, text="Click here to display saved contacts", command=display)
            display.pack()
        
        
        def edit_back():
        
            window3.withdraw()
            root.deiconify()
        
        
        def delete_number():
        
            global window4
            window4 = Toplevel(root)
            window4.geometry("900x600")
            window4.title("Delete Contact")
            root.withdraw()
            btn6 = Button(window4, text="Back to the main menu", font=("arial", 8, "bold"), width=20, command=delete_back)
            btn6.pack(side=LEFT)
        
            def deleted():
        
                with open("db.txt", 'w') as f:
                    f.writelines("")
        
                messagebox.showinfo("Info", "Contacts Deleted!!")
        
            btnd = Button(window4, text="Click here to delete all the contacts", font=("arial", 8, "bold"),
                          command = deleted)
        
            btnd.pack(side=LEFT)
        
        
        def delete_back():
        
            window4.withdraw()
            root.deiconify()
        
        
        def search_number():
        
            global window5
            window5 = Toplevel(root)
            framez = Frame(window5)
            framez.pack(side = RIGHT)
            window5.geometry("900x600")
            window5.title("Search Contact")
            root.withdraw()
            btn66 = Button(window5, text="Back to the main menu", font=("arial", 8, "bold"), width=20, command=search_back)
            btn66.pack(side=LEFT)
        
            def searched():
        
                if s0.get() == a0 or s0.get() == nlist[0]:
        
                    messagebox.showinfo("Info", "Contact Found")
        
                else:
        
                    messagebox.showinfo("Info","Contact Not Found")
        
            btn98 = Button(window5, text="search for contact", font=("arial", 8, "bold"), command=searched)
            btn98.pack(side=LEFT)
            lbl77 = Label(framez, text="Enter the id of contact first", font=("arial", 8, "bold"))
            lbl77.pack(side=LEFT)
        
            entry68 = Entry(framez,textvariable = s0, font=("arial", 8, "bold"))
            entry68.pack(side=LEFT)
        
        
        def search_back():
        
            window5.withdraw()
            root.deiconify()
        
        
        lbl0 = Label(tframe,text = "Phone Book App",font = ("arial",20,"bold"),fg = "steel blue")
        lbl0.pack(side = TOP)
        
        lframe = Frame(root)
        lframe.pack(side = LEFT)
        
        bframe = Frame(root)
        bframe.pack(side = BOTTOM)
        
        lbl1 = Label(lframe,text = "Choose one of those options",font = ("arial",15,"bold"),fg = "red")
        lbl1.grid(row = 0,column = 0)
        
        
        btn1 = Button(lframe,text = "Add Contact",font = ("arial",12,"bold"),width = 12,command = add_number)
        btn1.grid(row = 10,column = 4)
        
        btn2 = Button(lframe,text = "Edit Contact",font = ("arial",12,"bold"),width = 12,command = edit_number)
        btn2.grid(row = 10,column = 6)
        
        btn3 = Button(lframe,text = "Delete Contact",font = ("arial",12,"bold"),width = 12,command = delete_number)
        btn3.grid(row = 10,column = 8)
        
        btn33 = Button(lframe,text = "Search Contact",font = ("arial",12,"bold"),width = 12,command = search_number)
        btn33.grid(row = 10,column = 10)
        
        btn7 = Button(bframe,text = "Quit",font = ("arial",15,"bold"),width = 18,fg = "red",command = root.destroy)
        btn7.pack(side = LEFT)
        
        root.mainloop()
        if "find weather" in voice_data:
            Joe_speak("Weather App is openning")
            import tkinter as tk
            import requests
            
            HEIGHT = 500
            WIDTH = 600
            
            def test_function(entry):
            	print("This is the entry:", entry)
            
            # api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
            # a4aa5e3d83ffefaba8c00284de6ef7c3
            
            def format_response(weather):
            	try:
            		name = weather['name']
            		desc = weather['weather'][0]['description']
            		temp = weather['main']['temp']
            
            		final_str = 'City: %s \nConditions: %s \nTemperature (°F): %s' % (name, desc, temp)
            	except:
            		final_str = 'There was a problem retrieving that information'
            
            	return final_str
            
            def get_weather(city):
            	weather_key = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
            	url = 'https://api.openweathermap.org/data/2.5/weather'
            	params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
            	response = requests.get(url, params=params)
            	weather = response.json()
            
            	label['text'] = format_response(weather)
            
            
            
            root = tk.Tk()
            
            canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="yellow")
            canvas.pack()
            
            frame = tk.Frame(root, bg='#80c1ff', bd=5, )
            frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
            
            entry = tk.Entry(frame, font=40)
            entry.place(relwidth=0.65, relheight=1)
            
            button = tk.Button(frame, text="Get Weather", font=40, command=lambda: get_weather(entry.get()))
            button.place(relx=0.7, relheight=1, relwidth=0.3)
            
            lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
            lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
            
            label = tk.Label(lower_frame)
            label.place(relwidth=1, relheight=1)
            
            root.mainloop()
    if "where do you live"in voice_data:
        Joe_speak("I live where you live")
    if "end" in voice_data:
        Joe_speak(" Goodbye!Sorry That you are leaving")
        sys.exit()  

time.sleep(1) 
Joe_speak("Hi my name is darcy. How can I help you?")
#Joe_speak("It is important to note thet if you want to send an email then the password has been set to ftzyoirmasfuhakt")
while(1):      
    voice_data=record_audio()
    respond(voice_data)