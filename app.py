import tkinter as tk
import json
import difflib

# starting variables
data = json.load(open("data.json"))
root = tk.Tk()  # root widget for the main app
root.resizable(False, False)  # make app windows solid, not allowing for resizing
root.winfo_toplevel().title("Simple Dictionary")
startValueWord = "A word"
startValueDefinition = "A definition"
autoCorrect = tk.IntVar()

# finds a word and it's definition in data.json file
def translate(w):
    # formatting depending on if a word has more than 1 definition
    if len(data[w]) == 1:
        out = "\n>>>" + data[w][0] + "\n"
        answerDefinition.configure(text = out)
    else:
        out = ""
        for x in data[w]:
            out += "\n>>>" + x + "\n"
        answerDefinition.configure(text = out)


def searchF():
    # get what is in searchInput when "Search" button is pressed
    w = searchInput.get()
    w = w.strip()
    answerWord.configure(text = w)
    # try to find a definition, if not then try to find similar words
    try:
        translate(w)
    except Exception as e:
        # try to get the closest match if it exists
        if difflib.get_close_matches(w, data) and (autoCorrect.get()==1):
            corr = difflib.get_close_matches(w, data, 1)
            answerWord.configure(text=corr[0])
            translate(corr[0])
        elif difflib.get_close_matches(w, data) and (autoCorrect.get()==0):
            answerWord.configure(text="Word not found. Did you mean one of those instead:")
            closeMatches = ''
            for x in difflib.get_close_matches(w, data):
                closeMatches += '\n>>>' + x + '\n'
            answerDefinition.configure(text=closeMatches)
        else:
            err = str(e) + " is not a valid input."
            answerDefinition.configure(text=err)


# main app canvas
canvas = tk.Canvas(root, height=900, width=1200, bg="black")
canvas.pack()


# frame widget based on a canvas
frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.75, relx=0.1, rely=0.1)


# text label showing app name
creditstext = tk.Label(frame, text="Mini Dictionary App\nMade by Bartłomiej Szeliga\n\n"
                                   "How to use:\n\nEnter a word (CASE SENSITIVE) and click on 'Search'.\n",
                       width=100, bg="#b6b6b6")
creditstext.pack()


# user input
searchInput = tk.Entry(root)
searchInput.pack()

searchAutoCorrect = tk.Checkbutton(root, text="Correct me in case of typo", variable=autoCorrect)
searchAutoCorrect.pack()

searchButton = tk.Button(root, text="Search", command=searchF)
searchButton.pack()


# word and its definition is shown here
answerWord = tk.Label(frame, text=startValueWord, bg="white", pady=10)
answerWord.pack()

breakline = tk.Frame(frame, bg="black", height=1, width=400)
breakline.pack()

answerDefinition = tk.Label(frame, text=startValueDefinition, bg="white", wraplength=800)
answerDefinition.pack()


# main app loop
root.mainloop()
