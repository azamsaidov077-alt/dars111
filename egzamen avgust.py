
import re
# USER CLASS
class User:
    def __init__(self, name, phone, login, password, role):
        self.name = name
        self.phone = phone
        self.login = login
        self.password = password
        self.role = role


# STUDENT CLASS
class Student(User):
    def __init__(self, name, phone, login, password):
        super().__init__(name, phone, login, password, role="student")
        self.group = None
        self.homeworks = {}  # {homework: grade or None}

    def view_homework(self):
        print(f" {self.name} ning uy vazifalari:")
        if not self.homeworks:
            print(" hali uyga vazifa berilmagan")
        else:
            for hw, grade in self.homeworks.items():
                print(f" - {hw}: {grade if grade else 'baholanmagan'}")


# TEACHER CLASS
class Teacher(User):
    def __init__(self, name, phone, login, password):
        super().__init__(name, phone, login, password, role="teacher")
        self.groups = []

    def view_groups(self):
        print(f"{self.name} guruhlari:")
        if not self.groups:
            print("sizga bironta guruh biriktirilmagan")
        else:
            for g in self.groups:
                print(f" - {g.name} ({len(g.students)} student)")

    def view_students(self):
        for g in self.groups:
            print(f" {g.name} studentlari:")
            if not g.students:
                print("Student yoq")
            for s in g.students:
                print(f" - {s.name}")

    def give_homework(self, homework):
        for g in self.groups:
            for student in g.students:
                student.homeworks[homework] = None
            print(f"{g.name} guruhiga '{homework}' uyga vazifa berildi")

    def grade_student(self, group_name, student_name, homework, grade):
        group = next((g for g in self.groups if g.name == group_name), None)
        if group:
            student = next((s for s in group.students if s.name == student_name), None)
            if student:
                if homework in student.homeworks:
                    student.homeworks[homework] = grade
                    print(f"{student.name} ga '{homework}' uchun {grade} baho qoyildi")
                else:
                    print(" bu studentga bunday uyga vazifa berilmagan")
            else:
                print(" student topilmadi")
        else:
            print(" sizga bunday guruh biriktirilmagan")


 # GROUP CLASS
class Group:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        student.group = self
        self.students.append(student)


# ADMIN CLASS
class Admin(User):
    def __init__(self, name, phone, login, password):
        super().__init__(name, phone, login, password, role="admin")
        self.teachers = []
        self.students = []
        self.groups = []

    def add_teacher(self, teacher, group=None):
        self.teachers.append(teacher)
        if group:
            teacher.groups.append(group)
        # print(f"teacher {teacher.name} qoshildi.")

    def add_student(self, student, group):
        self.students.append(student)
        group.add_student(student)
        # print(f" student {student.name} guruhga ({group.name}) qoshildi.")

    def add_group(self, group):
        self.groups.append(group)
        # print(f" guruh {group.name} yaratildi.")

    def delete_teacher(self, name):
        self.teachers = [t for t in self.teachers if t.name != name]
        # print(f" teacher {name} ochirildi.")

    def delete_student(self, name):
        self.students = [s for s in self.students if s.name != name]
        # print(f"️ student {name} ochirildi.")

    def delete_group(self, name):
        self.groups = [g for g in self.groups if g.name != name]
        # print(f" guruh {name} ochirildi.")

    def view_statistics(self):
        print(" STATISTIKA 📊")
        print(f" teachers soni: {len(self.teachers)}")
        for t in self.teachers:
            if t.groups:
                for g in t.groups:
                    print(f" - {t.name} ({g.name})")
            else:
                print(f" - {t.name} ( guruh yoq)")

        print(f" guruhlar soni: {len(self.groups)}")
        for g in self.groups:
            print(f" - {g.name} -> {len(g.students)} student")

        print(f" students soni: {len(self.students)}")
        for s in self.students:
            print(f" - {s.name} ({s.group.name if s.group else ' guruh yoq'})")


# LOGIN FUNKSIYASI
def login(role, admin):
    login_input = input("login: ")
    password_input = input("parol: ")

    if role == "admin" and login_input == admin.login and password_input == admin.password:
        return admin
    elif role == "teacher":
        return next((t for t in admin.teachers if t.login == login_input and t.password == password_input), None)
    elif role == "student":
        return next((s for s in admin.students if s.login == login_input and s.password == password_input), None)
    return None



admin = Admin("Super Admin", "998900000000", "Admin", "1234")


teacher1 = Teacher("Ali", "123", "Ali", "1234")
teacher2 = Teacher("Vali", "456", "Vali", "1234")
group1 = Group("Python")
group2 = Group("Java")

admin.add_group(group1)
admin.add_group(group2)
admin.add_teacher(teacher1, group1)
admin.add_teacher(teacher2, group2)

student1 = Student("Aziz", "111", "Aziz", "1234")
student2 = Student("Laziz", "222", "Laziz", "1234")
admin.add_student(student1, group1)
admin.add_student(student2, group2)



while True:
    print("\n=== TIZIMGA XUSH KELIBSIZ ===")
    print("1. admin")
    print("2. teacher")
    print("3. student")
    print("0. chiqish")

    choice = input("tanlang: ")

    if choice == "0":
        print("dasturdan chiqildi.")
        break

    role = "admin" if choice == "1" else "teacher" if choice == "2" else "student"

    user = login(role, admin)
    if not user:
        print(" Login yoki parol xato")
        continue

    # ADMIN PANEL
    if user.role == "admin":
        while True:
            print(f" admin: {user.name}")
            print("1. teacher qo‘shish")
            print("2. group qoshish")
            print("3. student qoshish")
            print("4. statistikani korish")
            print("5. teacher ochirish")
            print("6. group ochirish")
            print("7. student ochirish")
            print("0. orqaga")

            c = input("tanlang: ")
            if c == "1":
                name = input("ismi: ")
                phone = input("telefon: ")
                login_ = input("login: ")
                parol = input("parol: ")
                group_name = input("qaysi guruhga biriktirsin (yo‘q bo‘lsa ENTER): ")
                group = next((g for g in admin.groups if g.name == group_name), None) if group_name else None
                teacher = Teacher(name, phone, login_, parol)
                admin.add_teacher(teacher, group)
            elif c == "2":
                name = input("guruh nomi: ")
                admin.add_group(Group(name))
            elif c == "3":
                name = input("ismi: ")
                phone = input("telefon: ")
                login_ = input("login: ")
                parol = input("parol: ")
                group_name = input("qaysi guruhga qoshilsin: ")
                group = next((g for g in admin.groups if g.name == group_name), None)
                if group:
                    student = Student(name, phone, login_, parol)
                    admin.add_student(student, group)
                else:
                    print(" Bunday guruh topilmadi")
            elif c == "4":
                admin.view_statistics()
            elif c == "5":
                name = input("qaysi teacher ochirilsin: ")
                admin.delete_teacher(name)
            elif c == "6":
                name = input("qaysi group ochirilsin: ")
                admin.delete_group(name)
            elif c == "7":
                name = input("qaysi student ochirilsin: ")
                admin.delete_student(name)
            elif c == "0":
                break

    # TEACHER PANEL
    elif user.role == "teacher":
        while True:
            print(f" teacher: {user.name}")
            print("1. guruhlarni korish")
            print("2. studentlarni korish")
            print("3. uyga vazifa berish")
            print("4. studentga baho qoyish")
            print("0. orqaga")

            c = input("tanlang: ")
            if c == "1":
                user.view_groups()
            elif c == "2":
                user.view_students()
            elif c == "3":
                homework = input("uyga vazifa: ")
                user.give_homework(homework)
            elif c == "4":
                group_name = input("guruh nomi: ")
                student_name = input("student ismi: ")
                homework = input("uy vazifa: ")
                grade = input("baho: ")
                user.grade_student(group_name, student_name, homework, grade)
            elif c == "0":
                break

    # STUDENT PANEL
    elif user.role == "student":
        while True:
            print(f" student: {user.name}")
            print("1. uyga vazifalarimni korish")
            print("0. orqaga")

            c = input("tanlang: ")
            if c == "1":
                user.view_homework()
            elif c == "0":
                break

