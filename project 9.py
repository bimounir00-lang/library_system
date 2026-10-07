import  csv
import pandas as pd
from  datetime import datetime 
class Expense : 
    def __init__(self,id, date, amount, category, description) :
        self.id = id
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description
    @classmethod
    def get (cls,id) :
     categorys = ["food", "transportation", "entertainment", "utilities", "other"]
     while True :
       date = input("what's the date : ")
       try : 
        datetime.strptime(date, "%Y-%m-%d")
        break
       except ValueError :
        print ("invalid date format. Please use YYYY-MM-DD.")
        continue
     while True : 
          amount_input = input("what's the amount : ")
          try : 
            amount = float(amount_input)
            if amount <=0 :
              print ("amount must be positive. Please try again.")
              continue
            break
          except ValueError :
              print ("invalid amount. Please enter a valid number.")
              continue
     while True :
      category = input("what's the category : ")
      try : 
          if category not in categorys :
                raise ValueError ("invalid category. Please choose from the following: food, transportation, entertainment, utilities, other.")
          break
      except ValueError as e :
          print (e)
          continue
     description = input("what's the description : ")
     return cls (id, date, amount_input, category, description)
 
def get_id (): 
 with open ("expenses.txt", "r") as file :
     reader = csv.DictReader(file)
     rows = list(reader)
     if rows : 
         last_id = int(rows[-1]["id"])
         return last_id + 1
     else :
            return 1
def rewrite_expenses(expenses):
 with open("expenses.txt", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "date", "amount", "category", "description"])
                writer.writeheader()
                writer.writerows(expenses)
def main () : 
 expenses = []
 while True :
     print ("1- add expense\n2- view expenses\n3- edit expense\n4- delete expense\n5- the sum of all expenses\n6- the sum of expenses by category\n7-the max, min, and average expenses\n8- the average expenses by day\n9- the  average expenses by month")
     choice = input("what's your choice : ")
     if choice == "1" :
            id = get_id()
            expense = Expense.get(id)
            with open ("expenses.txt", "a", newline="") as file :
                writer =csv.DictWriter(file, fieldnames = [ "id","date", "amount", "category", "description"])
                writer.writerow({ "id": expense.id, "date": expense.date, "amount": expense.amount, "category": expense.category, "description": expense.description})
            break
     elif choice == "2" :
        df = pd.read_csv("expenses.txt")
        sort_choice=input("by date, by category, or by amount?")
        df_sorted = df.sort_values(by=sort_choice)
        print(df_sorted)
        break
     elif choice == "3" :
            id_to_edit = input("Enter the ID of the expense to edit: ")
            with open("expenses.txt", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expenses.append(row)
                for row in expenses : 
                    if row["id"] == id_to_edit :
                        print(f"Current details - Date: {row['date']}, Amount: {row['amount']}, Category: {row['category']}, Description: {row['description']}")
                        new_date = input("Enter new date (leave blank to keep current): ")
                        new_amount = input("Enter new amount (leave blank to keep current): ")
                        new_category = input("Enter new category (leave blank to keep current): ")
                        new_description = input("Enter new description (leave blank to keep current): ")
                        row["date"] = new_date if new_date else row["date"]
                        row["amount"] = new_amount if new_amount else row["amount"]
                        row["category"] = new_category if new_category else row["category"]
                        row["description"] = new_description if new_description else row["description"]
                        break
            rewrite_expenses(expenses)      
            break 
     elif choice == "4" :
        id_to_delete = input("Enter the ID of the expense to delete: ")
        with open("expenses.txt", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
             expenses.append(row)
            for expense in expenses:
                if expense["id"] == id_to_delete:
                    expenses.remove(expense)
                    break
        rewrite_expenses(expenses)
        break
     elif choice == "5" :
         df =pd.read_csv("expenses.txt") 
         total_sum = df["amount"].sum()
         print (f"the sum of all expenses is : {total_sum}")
         break
     elif choice == "6" :
        category = input("Enter the category to calculate the sum for: ")
        df = pd.read_csv("expenses.txt")
        print (f"the sum of expenses is {df.groupby('category')['amount'].sum()[category]}")
        break
     elif choice == "7" :
         df = pd.read_csv("expenses.txt")
         max_expense = df["amount"].max()
         min_expense = df["amount"].min()
         avg_expense = df["amount"].mean()
         print(f"max expense: {max_expense} \n category : {df.loc[df['amount'] == max_expense, 'category'].iloc[0]} , on {df.loc[df['amount'] == max_expense, 'date'].iloc[0]}")
         print(f"min expense: {min_expense} category : {df.loc[df['amount'] == min_expense, 'category'].iloc[0]} , on {df.loc[df['amount'] == min_expense, 'date'].iloc[0]}")
         print(f"average expense: {avg_expense}")
         break
     elif choice == "8" :
         df = pd.read_csv("expenses.txt")
         day = input("Enter the day (YYYY-MM-DD) to calculate the average expenses for: ")
         avg_expense_by_day = df.groupby('date')['amount'].mean()[day]
         print(f"the average expenses on {day} is: {avg_expense_by_day}")
         break
     elif choice == "9" :
         df = pd.read_csv("expenses.txt")
         month = input("Enter the month (YYYY-MM) to calculate the average expenses for: ")
         df["month"] = df["date"].str[:7]
         avg_expense_by_month = df.groupby('month')['amount'].mean()[month]
         print(f"the average expenses in {month} is: {avg_expense_by_month}")
         break
if __name__ == "__main__" :
    main()