from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import math
import random


Builder.load_file("design.kv")
class Calc_Input(TextInput):
    def insert_text(self,substring,from_undo=False):
        allowed=['7','8','9','4','5','6','1','2','3','.','0','%','*','/','+','-']
        if not substring in allowed:
            return super().insert_text("",from_undo=from_undo)
        else:
            return super().insert_text(substring,from_undo=from_undo)
class Calc_window(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        numbers=['7','8','9','4','5','6','1','2','3','.','0','%']
        symbols=['-','(','AC','\u00f7',')','mod','\u00d7\u00b2','\u03c0','\u221A']
        other_symbols=['C','\u00d7','+']
        self.symbol=self.ids.other_sym
        self.num=self.ids.nums
        self.see=self.ids.display
        self.other_symbol=self.ids.one_sym
        myquotes=open("quote.txt",encoding="utf8")
        self.myquotes=myquotes.readlines()
       
        
        
        for number in numbers:
            btn=Button(text=number,background_normal="",background_color=(1,0.7,0.4,1))
            btn.bind(on_release=self.echo_num)
            btn.height=.25
            self.num.add_widget(btn)
            
        for symbol in symbols:
            btn=Button(text=symbol,background_normal="",background_color=(1,0.6,0.2,1))
            btn.height=.25
            btn.bind(on_release=self.echo_num)
            self.symbol.add_widget(btn)
        equal=Button(text='=',background_normal="",background_color=(0,0.5,0,1),size_hint_y=.3)
        equal.bind(on_release=self.answer)
        self.ids.syms.add_widget(equal)
        for other_symbol in other_symbols:
            height=.25
            if other_symbol=="+":
                height=.5
            btn=Button(text=other_symbol,background_normal="",background_color=(1,0.5,0,1),size_hint_y=height)
            btn.bind(on_release=self.echo_num)
            self.other_symbol.add_widget(btn)
        
    def echo_num(self,instance):
        
        if instance.text=="AC":
            self.see.text=""
            self.ids.question.text=" "
            self.ids.eq.text=""
            self.ids.answerss.text=" "
        elif instance.text=="C":
            self.see.text=self.see.text[:-1]
        elif instance.text=="%":
            symbol_count=[]
            symbol_count.append(self.see.text.rfind('+'))
            symbol_count.append(self.see.text.rfind('-'))
            symbol_count.append(self.see.text.rfind('\u00d7'))
            symbol_count.append(self.see.text.rfind('\u00f7'))
            count=max(symbol_count)
            if count < 0:
                query=(round(float((self.see.text))/100,2))
                self.see.text=str(query)
            else:
                percent=round(float(self.see.text[count+1:])/100,2)
                self.see.text=self.see.text[:count+1]+str(percent)
        
        elif instance.text=="\u221A":
            symbol_count=[]
            symbol_count.append(self.see.text.rfind('+'))
            symbol_count.append(self.see.text.rfind('-'))
            symbol_count.append(self.see.text.rfind('\u00d7'))
            symbol_count.append(self.see.text.rfind('\u00f7'))
            count=max(symbol_count)
            if count < 0 and len(self.see.text)>0:
                query=(round(math.sqrt(float((self.see.text))),2))
                self.see.text=str(query)
            else:
                if len(self.see.text[count+1:])> 0:
                    percent=round(math.sqrt(float(self.see.text[count+1:])),2)
                    self.see.text=self.see.text[:count+1]+str(percent)
                else:
                    pass
        elif instance.text=="\u00d7\u00b2":
            self.see.text=self.see.text+"\u00b2"
        else:
            self.see.text=self.see.text+instance.text
        

    def answer(self,text):
        texts=self.see.text
        before_ans=self.replaces(texts)
        bracket=[]
        open=0
        close=0
        brac=0
        coats=self.myquotes
        self.ids.hack.text=random.choice(coats)
        #self.ids.hack.text=random.choice(self.quotes)
        
        if before_ans[-1]=="(":
            before_ans=before_ans[:-1]
        if before_ans[0]==")":
            before_ans=before_ans[1:]
        for i in before_ans:
            if i =="(" or i ==")":
                bracket.append(i)
            if len(bracket)>0:
                for i in bracket:
                    if i=="(":
                        open=+1
                    if i==")":
                        close=+1
                if open>close:
                    while brac < open-close:
                        before_ans=before_ans+")"
                        brac=+1
                if close>open:
                    while brac < close-open:
                        before_ans="(" + before_ans
                        brac=+1
        sym_error=["+","/","-","*"]
        if before_ans[-1] in sym_error:
            before_ans=before_ans[:-1]
                 
        if len(before_ans)==0:
            pass
        elif before_ans[0]=="%":
            pass
        else:
            try:
                ans=eval(before_ans)
                self.ids.question.text=self.see.text
                self.ids.eq.text="="
                self.ids.answerss.text=str(ans)
                self.see.text=str(ans)
                    
                
            except SyntaxError:
                pass
       
           
            
    
    def replaces(self,texts):
        res=texts.replace('\u00f7','/').replace('\u00b2','**2').replace('\u03c0',str(math.pi)).replace('\u221A','**0.5').replace('\u00d7','*').replace('mod','%')
        
        
        return res
    
    
    
    
    
    
    
    
        
class Calculator(App):
    def build(self):
        
        return Calc_window()

if __name__=="__main__":
    Calculator().run()
    