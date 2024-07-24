import tkinter as tk
from tkinter import messagebox as mb
import sqlite3

def execute_query(query, params=()):
    conn = sqlite3.connect('expense_tracker.db')
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all_from_expenses():
    conn = sqlite3.connect('expense_tracker.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expense_tracker')
    expenses = c.fetchall()
    conn.close()
    return expenses

def add_expense():
    name_text, amount_text = name.get("1.0", tk.END).strip(), amount.get("1.0", tk.END).strip()
    if name_text and amount_text:
        try:
            execute_query('CREATE TABLE IF NOT EXISTS expense_tracker (name TEXT, amount REAL)')
            execute_query('INSERT INTO expense_tracker (name, amount) VALUES (?, ?)', (name_text, float(amount_text)))
            mb.showinfo('Success!', 'Expense added successfully!')
            name.delete("1.0", tk.END)
            amount.delete("1.0", tk.END)
        except Exception as e:
            mb.showerror('Error', f'Error adding expense: {e}')
    else:
        mb.showerror('Error', 'Please enter name and amount')

def display_expenses():
    try:
        expenses = fetch_all_from_expenses()
        display_window = tk.Toplevel(root)
        display_window.title('All Expenses')
        display_text = tk.Text(display_window, width=50, height=20, font=('Arial', 14))
        display_text.pack(padx=20, pady=20)
        for expense in expenses:
            display_text.insert(tk.END, f"Name: {expense[0]}, Amount: {expense[1]}\n\n")
        display_text.configure(state='disabled')
    except Exception as e:
        mb.showerror('Error', f'Error displaying expenses: {e}')

def delete_expenses():
    try:
        expenses = fetch_all_from_expenses()
        delete_window = tk.Toplevel(root)
        delete_window.title('Delete Expenses')
        vars_list = []
        for expense in expenses:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(delete_window, text=f"Name: {expense[0]}, Amount: {expense[1]}", variable=var)
            checkbox.pack(anchor=tk.W)
            vars_list.append((var, expense))
        def delete_selected():
            try:
                for var, expense in vars_list:
                    if var.get() == 1:
                        execute_query('DELETE FROM expense_tracker WHERE name=? AND amount=?', expense)
                mb.showinfo('Success!', 'Expense(s) deleted successfully!')
                delete_window.destroy()
            except Exception as e:
                mb.showerror('Error', f'Error deleting expense: {e}')
        delete_button = tk.Button(delete_window, text='Delete Selected', command=delete_selected)
        delete_button.pack(pady=10)
    except Exception as e:
        mb.showerror('Error', f'Error deleting expenses: {e}')

def calculate_statistics():
    try:
        expenses = fetch_all_from_expenses()
        if expenses:
            total_expenses = sum(expense[1] for expense in expenses)
            average_expense = total_expenses / len(expenses)
            mb.showinfo('Statistics', f'Total Expenses: {total_expenses:.2f}\nAverage Expense: Rs.{average_expense:.2f}')
        else:
            mb.showinfo('Statistics', 'No expenses!')
    except Exception as e:
        mb.showerror('Error', f'Error calculating statistics: {e}')

root = tk.Tk()
tk.Label(root, text='Expense Tracker', font=('Arial', 40, "bold", "underline"), fg='green').pack(pady=20)
root.title('Expense Tracker')
root.geometry("700x600")

tk.Label(root, text='Expense:', font=('Arial', 20)).pack(pady=10)
name = tk.Text(root, width=25, font=('Arial', 18), height=1)
name.pack(pady=10)

tk.Label(root, text='Amount:', font=('Arial', 20)).pack(pady=10)
amount = tk.Text(root, width=25, font=('Arial', 18), height=1)
amount.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

buttons = [
    {'text': 'Add Expense', 'command': add_expense, 'row': 0, 'column': 0},
    {'text': 'Display Expenses', 'command': display_expenses, 'row': 0, 'column': 1},
    {'text': 'Delete Expenses', 'command': delete_expenses, 'row': 1, 'column': 0},
    {'text': 'Calculate Statistics', 'command': calculate_statistics, 'row': 1, 'column': 1}
]

for button in buttons:
    tk.Button(button_frame, text=button['text'], command=button['command'], font=('Arial', 12), width=15, height=2).grid(row=button['row'], column=button['column'], padx=10)

root.mainloop()