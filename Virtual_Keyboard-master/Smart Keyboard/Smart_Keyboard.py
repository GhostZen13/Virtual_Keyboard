from tensorflow.keras.models import load_model
import json
import numpy as np
from tkinter import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-m", "--model", dest="mymodel", help="Open specified file")
parser.add_argument("-f", "--dict", dest="mydict", help="Open specified file")

args = parser.parse_args()
mymodel = args.mymodel
mydict = args.mydict
    
model = load_model('smart_predict.hdf5')#load prediction model
with open('dict.json') as json_file:  
    data_dict = json.load(json_file)#load dictionary of vocablary
    
    
def prediction(list):#
    if len(list) == 1:
            list = ['pad']+list
    list1=[]
    print(list)
    j = len(data_dict)+1
    for i in list:
        try:
            list1.append(data_dict[i.lower()])    
        except KeyError:
            list1.append(np.random.choice(len(data_dict.keys()),1)[0])
            print('not in dict')
            with open('dict.json','r',encoding="utf-8")as final_data:
              append_data = {i:j}
              new_val = json.loads(final_data.read())
              new_val.update(append_data)
              print("Data added to Dictionary")
              with open("dict.json","w",encoding="utf-8")as curr_key:
                curr_key.write(final_val)
                
            
    if len(list1) > 1:
        result = model.predict(np.expand_dims(np.array(list1),axis=0))[0]
        results = sorted(range(len(result)), key=lambda i: result[i], reverse=True)[:3]
        return tokens_to_string(results)
    else:
        return 'not in dictionary'


def all_possible(word):#for autocorrect, splits word in many combinations
    splits = []
    for i in range(len(word),0,-1):
        splits.append(word[:i])
        splits.append(word[i:])
    for j in range(1,len(word)):
        splits.append(word[1:j])
        splits.append(word[j:1])
    
    splits.sort(key=len,reverse=True)
    best_list = []
    list(filter(None, splits))
    for i in splits:
        for j in data_dict.keys():
            if j != 'pad':
                if i in j:
                    best_list.append(j)
    
    while len(best_list) < 3 :
        best_list.append(best_list[0])
    return best_list

idx = data_dict
inverse_map = dict(zip(idx.values(), idx.keys()))
def tokens_to_string(tokens):
    # Map from tokens back to words.
    words = [inverse_map[token] for token in tokens if token != 0]
    
    # Concatenate all words.
    
    text = " ".join(words)
    return text
#tkinter gui keyboard
class keyboard(object):
    def __init__(self):
        self.r = Tk()
        self.r.geometry('565x80')
        self.btn_text1 = StringVar()
        self.btn_text2 = StringVar()
        self.btn_text3 = StringVar()
       
        self.text_window = Text(self.r, height=3, width=65)
        self.text_window.grid(row=0,columnspan=3)
        self.L1 = Button(self.r, text="Send",command=self.dump_data()).grid(row=0,column=3)
        self.L2 = Button(self.r,textvariable=self.btn_text1,width=23,command=self.button1_pressed).grid(row=1,column=0)
        self.L3 = Button(self.r,textvariable=self.btn_text2,width=23,command=self.button2_pressed).grid(row=1,column=1)
        self.L4 = Button(self.r,textvariable=self.btn_text3,width=23,command=self.button3_pressed).grid(row=1,column=2)
        
        self.r.bind("<Key>",self.correction)
        self.r.bind("<space>",self.update_buttons)
        self.r.bind("<Control_L>",self.button1_pressed)
        self.r.bind("<Return>",self.dump_data)
        self.r.mainloop()
    
    @property
    def current_text(self):
        return self.text_window.get("1.0",END)
        
    def correction(self,event=None):
        if len(self.current_text) > 1:
            corrected_words = all_possible(self.current_text.split()[-1])
            self.set_buttons(corrected_words)

    def set_buttons(self,string):
        self.btn_text1.set(string[0])
        self.btn_text2.set(string[1])
        self.btn_text3.set(string[2])

    def update_buttons(self,event=None):
        words = self.current_text.split()
        result = prediction(words[-2:])
        self.set_buttons(result.split())


    def deletion(self,button):
        length = len(self.current_text)
        length_2 = len(self.current_text.split()[-1])+1
        self.text_window.delete('1.0'+' + '+str(length-length_2)+'chars',END)
        self.text_window.insert(END,button.get())

    def button1_pressed(self,event=None):
        if self.current_text.split(' ')[-1] == '\n':
            self.text_window.insert(END,self.btn_text1.get())
        else:
            self.deletion(self.btn_text1)
            
    def button2_pressed(self,event=None):
        if self.current_text.split(' ')[-1] == '\n':
            self.text_window.insert(END,self.btn_text2.get())
        else:
            self.deletion(self.btn_text2)

    def button3_pressed(self,event=None):
        if self.current_text.split(' ')[-1] == '\n':
            self.text_window.insert(END,self.btn_text3.get())
        else:
            self.deletion(self.btn_text3)

    def dump_data(self,event=None):
        with open('new_data_dump.txt','a') as f:
            f.write(self.text_window.get("1.0",END))
        self.text_window.delete(1.0,END)

if __name__ == "__main__":
    print('Starting')
    keyboard()
