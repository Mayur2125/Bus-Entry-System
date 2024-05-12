from tkinter import*
from tkinter import ttk
import pymysql
class Bus:
    def __init__(self,root):
        self.root=root 
        self.root.title("BUS MANAGEMENT SYSTEM")
        self.root.geometry("1300x700+0+0")
        var=IntVar()


        title=Label(self.root,text="BUS MANAGEMENT",bd=10,relief=GROOVE,font=("times new roman",40,"bold"),bg="cadet blue",fg="black")
        title.pack(side=TOP,fill=X)



#===============================variables=================================================================
        self.date_time_var=StringVar()

        self.Bus_no_var=StringVar()
        self.Bus_status_var=StringVar()
        bus_s=var.get()

        







        
        
#==========================================manage==========================================================
        Manage_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="cadet blue")
        Manage_Frame.place(x=20,y=100,width=500,height=560)
        
        m_title=Label(Manage_Frame,text="MANAGE BUS",bg="cadet blue",fg="black",font=("times new roman",30,"bold"))
        m_title.grid(row=0,columnspan=2,pady=20)

        
        lbl_bno=Label(Manage_Frame,text=" Bus Number ",bg="white",fg="black",font=("times new roman",20,"bold"))
        lbl_bno.grid(row=3,column=0,pady=10,padx=20,sticky="w")

        combo_bno=ttk.Combobox(Manage_Frame,textvariable=self.Bus_no_var,font=("times new roman",15,"bold"))
        combo_bno['values']=("Bus 1(MH12-AB-123)","Bus 2(MH12-PQ-563)","Bus 3(MH12-FY-105)","Bus 4(MH12-XB-582)","Bus 5(MH12-GH-453)","Bus 6(MH12-JK-802)")
        combo_bno.grid(row=3,column=1,pady=10,padx=20)


        lbl_bno=Label(Manage_Frame,text=" Bus Status    ",bg="white",fg="black",font=("times new roman",20,"bold"))
        lbl_bno.grid(row=5,column=0,pady=10,padx=20,sticky="w")


        combo_bno=ttk.Combobox(Manage_Frame,textvariable=self.Bus_status_var,font=("times new roman",15,"bold"), state="readonly")
        combo_bno['values']=("Departed","Arrived")
        combo_bno.grid(row=5,column=1,pady=10,padx=20)
       
       


#======================================Button=============================================================         

        btn_Frame=Frame(Manage_Frame,bd=4,relief=RIDGE,bg="cadet blue")
        btn_Frame.place(x=40,y=450,width=410)

        Addbtn=Button(btn_Frame,text="ADD",width=10,height=2,command=self.add_bus_info).grid(row=0,column=0,padx=10,pady=10)
        updatebtn=Button(btn_Frame,text="UPDATE",width=10,height=2,command=self.update_data).grid(row=0,column=1,padx=10,pady=10)
        dltbtn=Button(btn_Frame,text="DELETE",width=10,height=2,command=self.delete_data).grid(row=0,column=2,padx=10,pady=10)
        clrbtn=Button(btn_Frame,text="CLEAR",width=10,height=2,command=self.clear).grid(row=0,column=3,padx=10,pady=10)


        

#=================================================Form====================================================
        Detail_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="cadet blue")
        Detail_Frame.place(x=550,y=110,width=710,height=560)
        detail_title=Label(Detail_Frame,text="Bus Record",bg="cadet blue",fg="black",font=("times new roman",25,"bold"))
        detail_title.grid(row=0,columnspan=2,pady=0,padx=200)
        savebtn=Button(Detail_Frame,text="SAVE",width=10,height=1).grid(row=0,column=3,padx=10,pady=5)

        


#============================================table==========================================================
        table_Frame=Frame(Detail_Frame,bd=4,relief=RIDGE,bg="cadet blue")
        table_Frame.place(x=10,y=40,width=680,height=510)
        scroll_x=Scrollbar(table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(table_Frame,orient=VERTICAL)


        self.bus_table=ttk.Treeview(table_Frame,columns=("Bus Number","Bus Status"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.bus_table.xview)
        scroll_y.config(command=self.bus_table.yview)

        self.bus_table.heading("Bus Number",text="Bus Number")
        self.bus_table.heading("Bus Status",text="Bus Status")
        self.bus_table['show']='headings'
        self.bus_table.pack(fill=BOTH,expand=1)
        self.bus_table.bind("<ButtonRelease-1>",self.get_cursor)
        
        self.fetch_data()
        
    def add_bus_info(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="data")
        cur=con.cursor()
        cur.execute("insert into record values(%s,%s)",(self.Bus_no_var.get(),
                                                        self.Bus_status_var.get()))
        con.commit()
        self.fetch_data()
        self.clear()
        con.close()
        
    def fetch_data(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="data")
        cur=con.cursor()
        cur.execute("select * from record")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.bus_table.delete(*self.bus_table.get_children())
            for row in rows:
                self.bus_table.insert("",END,values=row)
            con.commit()
        con.close()

    def clear(self):
        self.date_time_var.set("")
        self.Bus_no_var.set("")
        self.Bus_status_var.set("")

    def get_cursor(self,ev):
        cursor_row=self.bus_table.focus()
        content=self.bus_table.item(cursor_row)
        row=content["values"]

        #self.date_time_var.set(row[0])
        self.Bus_no_var.set(row[0])
        self.Bus_status_var.set(row[1])

    def update_data(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="data")
        cur=con.cursor()
        cur.execute("update record set Bus_Number=%s where Bus_Status=%s ",(self.Bus_no_var.get(),
                                                                            self.Bus_status_var.get()))
                                                
        
        con.commit()
        self.fetch_data()
        self.clear()
        con.close()


        
    def delete_data(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="data")
        cur=con.cursor()
        cur.execute("delete from record where Date_Time=%s",self.date_time_var.get())
        con.commit()
        con.close()
                             
                    
        
    
       
        
root=Tk()
ob=Bus(root)
root.mainloop()
