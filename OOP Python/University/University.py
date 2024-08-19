class University:
    def __init__(self):
        self.Name = str(input("Name: "))
        self.Age = int(input("Age: "))
        self.Gender = str(input("Gender: "))
        self.Country = str(input("Country: "))
    def display(self):
        print("Name:", self.Name)
        print("Age:", self.Age)
        print("Gender:", self.Gender)
        print("Country:", self.Country)

class Employee(University):
    def __init__(self):
        super().__init__()
        self.EmployeeID = int(input("ID: "))
        self.Salary = int(input("Salary: "))
        self.Department = str(input("Department: "))
        
    def display(self):
        super().display()  # Display common details
        print("Employee ID:", self.EmployeeID)
        print("Salary:", self.Salary)
        print("Department:", self.Department)

class Student(University):
    def  __init__(self):
        super().__init__()
        self.StudentID = int(input("ID: "))
        self.GPA = float(input("GPA: "))
        self.Major = str(input("Major: "))
        
    def display(self):
        super().display()  # Display common details
        print("Student ID:", self.StudentID)
        print("GPA:", self.GPA)
        print("Major:", self.Major)
 
def main():
    r = str(input("Role : "))
    if  r.lower() == "employee" :
        e = Employee()
        print("----------------------------")
        print("Role : ",r)
        e.display()
    elif r.lower() == "student" :
        s = Student()
        print("----------------------------")
        print(r)
        s.display()
    else:
        print("Invalid role entered.")


main()
