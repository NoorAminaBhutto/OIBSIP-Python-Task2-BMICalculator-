import argparse, datetime, sqlite3, tkinter as tk
from tkinter import ttk, messagebox

DB = "bmi_history.db"

def calculate_bmi(weight, height):
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be greater than zero.")
    bmi = weight / height**2
    category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
    return bmi, category

def connect():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY, name TEXT, weight REAL, height REAL,
        bmi REAL, category TEXT, recorded_at TEXT)""")
    return con

def save(name, weight, height, bmi, category):
    with connect() as con:
        con.execute("INSERT INTO records(name,weight,height,bmi,category,recorded_at) VALUES(?,?,?,?,?,?)",
                    (name, weight, height, bmi, category, datetime.datetime.now().isoformat(timespec="seconds")))

def history(name):
    with connect() as con:
        return con.execute("SELECT weight,height,bmi,category,recorded_at FROM records WHERE name=? ORDER BY recorded_at", (name,)).fetchall()

def cli():
    while True:
        try:
            name = input("Name: ").strip() or "Guest"
            weight = float(input("Weight (kg): "))
            height = float(input("Height (m): "))
            bmi, category = calculate_bmi(weight, height)
            print(f"BMI: {bmi:.2f} | Category: {category}")
            if input("Save record? (y/n): ").lower().strip() == "y":
                save(name, weight, height, bmi, category)
                print("Saved locally.")
            if input("Another calculation? (y/n): ").lower().strip() != "y": break
        except ValueError:
            print("Invalid input. Use positive numeric values.")
        except sqlite3.Error as e:
            print("Database error:", e)
        except (EOFError, KeyboardInterrupt):
            print("\\nGoodbye!")
            break

class App:
    def __init__(self, root):
        self.root=root; root.title("BMI Calculator | Python Programming"); root.geometry("700x540")
        self.name=tk.StringVar(); self.weight=tk.StringVar(); self.height=tk.StringVar()
        self.result=tk.StringVar(value="Enter your details and select Calculate BMI.")
        self.colors={"Underweight":"#2563eb","Normal":"#15803d","Overweight":"#c2410c","Obese":"#b91c1c"}
        frame=ttk.Frame(root,padding=22); frame.pack(fill="both",expand=True)
        ttk.Label(frame,text="BMI CALCULATOR",font=("Arial",20,"bold")).pack(anchor="w")
        ttk.Label(frame,text="Calculate BMI, save records, and view history.").pack(anchor="w",pady=(3,16))
        form=ttk.LabelFrame(frame,text="Your details",padding=14); form.pack(fill="x")
        for i,(label,var) in enumerate([("Name",self.name),("Weight (kg)",self.weight),("Height (m)",self.height)]):
            ttk.Label(form,text=label).grid(row=i,column=0,sticky="w",padx=(0,12),pady=7)
            ttk.Entry(form,textvariable=var).grid(row=i,column=1,sticky="ew",pady=7)
        form.columnconfigure(1,weight=1)
        ttk.Button(form,text="Calculate BMI",command=self.calculate).grid(row=3,column=0,sticky="ew",pady=(12,0),padx=(0,8))
        ttk.Button(form,text="View History",command=self.show_history).grid(row=3,column=1,sticky="ew",pady=(12,0))
        self.label=tk.Label(frame,textvariable=self.result,font=("Arial",14,"bold"),fg="#334155",pady=18)
        self.label.pack(fill="x")
        ttk.Label(frame,text="BMI is a general adult screening measure, not a medical diagnosis.").pack(anchor="w")
        row=ttk.Frame(frame); row.pack(fill="x",pady=14)
        ttk.Button(row,text="Show BMI Trend Chart",command=self.chart).pack(side="left")
        ttk.Button(row,text="Clear Fields",command=self.clear).pack(side="left",padx=8)

    def calculate(self):
        name=self.name.get().strip()
        if not name:
            messagebox.showerror("Input error","Please enter a name."); return
        try:
            w=float(self.weight.get()); h=float(self.height.get()); bmi,cat=calculate_bmi(w,h)
        except ValueError:
            messagebox.showerror("Input error","Enter valid numbers. Weight and height must be greater than zero."); return
        self.result.set(f"BMI: {bmi:.2f}   |   Category: {cat}"); self.label.config(fg=self.colors[cat])
        try: save(name,w,h,bmi,cat)
        except sqlite3.Error as e:
            messagebox.showerror("Database error",f"Calculated but could not save record.\\n{e}"); return
        messagebox.showinfo("Saved","BMI calculated and record saved locally.")

    def show_history(self):
        name=self.name.get().strip()
        if not name: messagebox.showwarning("Name required","Enter a name first."); return
        try: rows=history(name)
        except sqlite3.Error as e: messagebox.showerror("Database error",str(e)); return
        win=tk.Toplevel(self.root); win.title("BMI History — "+name); win.geometry("760x320")
        tree=ttk.Treeview(win,columns=("date","weight","height","bmi","category"),show="headings")
        for key,title,width in [("date","Recorded at",200),("weight","Weight kg",100),("height","Height m",100),("bmi","BMI",90),("category","Category",140)]:
            tree.heading(key,text=title); tree.column(key,width=width,anchor="center")
        tree.pack(fill="both",expand=True,padx=12,pady=12)
        for w,h,b,c,d in rows: tree.insert("","end",values=(d.replace("T"," "),f"{w:.1f}",f"{h:.2f}",f"{b:.2f}",c))
        if not rows: messagebox.showinfo("No records","No records found for "+name+".")

    def chart(self):
        name=self.name.get().strip()
        if not name: messagebox.showwarning("Name required","Enter a name first."); return
        try: rows=history(name)
        except sqlite3.Error as e: messagebox.showerror("Database error",str(e)); return
        if len(rows)<2: messagebox.showinfo("More data needed","Save at least two records for this name."); return
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8,4.5)); plt.plot(range(1,len(rows)+1),[r[2] for r in rows],marker="o")
            plt.xticks(range(1,len(rows)+1),[r[4][:10] for r in rows],rotation=30,ha="right")
            plt.title("BMI Trend for "+name); plt.xlabel("Record"); plt.ylabel("BMI")
            plt.grid(True,alpha=.3); plt.tight_layout(); plt.show()
        except ImportError: messagebox.showerror("Matplotlib missing","Run: python -m pip install matplotlib")
        except Exception as e: messagebox.showerror("Chart error",str(e))

    def clear(self):
        self.name.set(""); self.weight.set(""); self.height.set("")
        self.result.set("Enter your details and select Calculate BMI."); self.label.config(fg="#334155")

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--cli",action="store_true"); args=parser.parse_args()
    if args.cli: cli(); return
    try:
        root=tk.Tk(); App(root); root.mainloop()
    except tk.TclError as e:
        print("Could not open Tkinter GUI. In Google Colab, use: python bmi_calculator.py --cli")
        print(e)

if __name__=="__main__": main()
