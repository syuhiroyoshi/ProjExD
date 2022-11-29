import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn=event.widget
    txt=btn["text"]
    entry.insert(tk.END,txt)

def click_eqall(event):#=の実施
    eqn=entry.get()
    res=eval(eqn)
    entry.delete(0,tk.END)
    entry.insert(tk.END,str(res))

def click_clear(event):#1字削除する.
    cl=entry.get()
    cll=cl[:-1]
    entry.delete(0,tk.END)
    entry.insert(tk.END,str(cll))

def click_alclear(event):#すべて削除
    entry.delete(0,tk.END)
    entry.insert(tk.END)



if __name__ == '__main__':
    bt = tk.Tk()
    bt.geometry("300x420")

    entry = tk.Entry(bt,justify="right",width=10,font=("Times New Roman",40))
    entry.grid(row=0,column=0,columnspan=4)

    r,c=1,1
    for i,num in enumerate(["/","*","-","+",9,8,7,6,5,4,3,2,1,0],1):
        btn =tk.Button(bt,text=num,font=("Times New Roman",15),width=3,command=button_click)
        btn.bind("<1>",button_click)
        btn.grid(row=r,column=c,padx=10,pady=10)
        if i%3==0:
            r+=1
            c=0
        c+=1


    btn=tk.Button(bt,text="AC",font=("Times New Roman",15))
    btn.bind("<1>",click_alclear)
    btn.grid(row=6,column=1,padx=10,pady=10) #padxは外側の横の隙間を指定します。padyは外側の縦の隙間を指定します。

    btn=tk.Button(bt,text="C",font=("Times New Roman",15),width=3)
    btn.bind("<1>",click_clear)
    btn.grid(row=6,column=2,padx=10,pady=10)

    btn=tk.Button(bt,text="=",font=("Times New Roman",15),width=3)
    btn.bind("<1>",click_eqall)
    btn.grid(row=5,column=3,padx=10,pady=10)

    #btn=tk.Button(bt,text="x²",font=("Times New Roman",15),width=3) #二乗したいけど時間がない
    #btn.bind("<1>",click_clear)
    #btn.grid(row=6,column=3,padx=10,pady=10)

    bt.mainloop()

