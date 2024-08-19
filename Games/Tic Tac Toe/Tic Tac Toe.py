import os  # استيراد مكتبة os لتنظيف الشاشة
import time
import random

class Player:  # تعريف الكلاس Player
    def __init__(self):  # دالة البدء مع معلومات النفس والرمز
        self.name = ""
        self.symbol = ""
        self.score = 0

    def choose_name(self):  # اختيار اسم اللاعب
        name = input("Name: ")  # استقبال اسم اللاعب من المستخدم
        self.name = name

    def choose_symbol(self):  # اختيار الرمز
        while True:
            symbol = input("X/O: ").upper()  # استقبال الرمز من المستخدم وتحويله لأحرف كبيرة
            if symbol == "X" or symbol == "O":  # التأكد من أن الرمز صحيح
                self.symbol = symbol  # تعيين الرمز
                break
            print("Invalid Symbol")  # إذا كان الرمز غير صحيح
    def increase_score(self):
        self.score += 1

class Menu:  # تعريف الكلاس Menu
    def display_main_menu(self):  # عرض قائمة اللعبة الرئيسية
        self.main_menu = '''
X-O Game
1. Play Game  
2. Exit Game  
Enter Num: '''  # القائمة الرئيسية للعبة
        choose = input(self.main_menu)  # استقبال اختيار المستخدم
        return choose
    
    def multiplayer_menu(self):
        self.player_menu = '''
1. 1 Player  
2. 2 Player  
Enter Num: '''  # القائمة الرئيسية للعبة
        choose = input(self.player_menu)  # استقبال اختيار المستخدم
        return choose
    
    def display_endgame_menu(self):  # عرض قائمة نهاية اللعبة
        self.end_menu = '''
1. Play Again  
2. Exit Game 
Enter Num: '''  # قائمة نهاية اللعبة
        choose = input(self.end_menu)  # استقبال اختيار المستخدم
        return choose
    
class Board:  # تعريف الكلاس Board
    def __init__(self):  # دالة البدء مع إعداد اللوحة
        self.board = [str(i) for i in reversed(range(1, 10))]  # تهيئة اللوحة بالأرقام من 1 إلى 9

    def display_board(self):  # عرض اللوحة
        for i in reversed(range(0, 9, 3)):  # الاستدعاء لكل ثلاثة خانات
            print("          |          ".join([" " if cell.isdigit() else cell for cell in self.board[i:i+3]]))  # طباعة الصفوف باستبدال الأرقام بخانات فارغة
            print("           |                     |")
            if i > 0:
                print("-"*50)  # طباعة خطوط الفصل

    def correct_choose(self, choose, symbol):  # التحقق من صحة الاختيار
        if self.board[choose-1].isdigit():  # التحقق مما إذا كانت الخانة خالية
            return True
        print("Invalid Input")  # إذا كان الاختيار غير صحيح
        return False

    def update_board(self, choose, symbol):  # تحديث اللوحة بالرمز
        if self.correct_choose(choose, symbol):  # التحقق من صحة الاختيار
            self.board[choose-1] = symbol  # تحديث اللوحة بالرمز
            
    def reset_board(self):  # إعادة تهيئة اللوحة
        self.board = [str(i) for i in range(1, 10)]  # إعادة تهيئة اللوحة بالأرقام من 1 إلى 9

class Game(Player, Board, Menu):  # تعريف الكلاس Game
    def __init__(self):  # دالة البدء مع إعداد اللعبة
        self.board = Board()  # إعداد اللوحة
        self.players = [Player(), Player()]  # إعداد اللاعبين
        self.menu = Menu()  # إعداد القائمة
        self.current_player_index = 0  # تحديد مؤشر اللاعب الحالي
        self.history = []  # قائمة لتخزين تاريخ الحركات

    def start_game(self):  # بدء اللعبة
        choose = self.menu.display_main_menu()  # عرض قائمة اللعبة الرئيسية

        if choose == "1":  # إذا اختار المستخدم لعب اللعبة
            player = self.multiplayer_menu()
            if player == "1" :
                self.setup_1_player()
                self.play_game_1_player()
            elif player == "2" :
                self.setup_2_player()  # إعداد اللاعبين
                self.play_game_2_player()  # بدء اللعبة
        elif choose == "2":  # إذا اختار المستخدم الخروج من اللعبة
            self.quit_game()  # الخروج من اللعبة
        else:  # إذا كان الاختيار غير صحيح
            print("Invalid choice")  # طباعة رسالة

    def setup_1_player(self):
        for num, player in enumerate(self.players, start=1):
            if num == 2:
                player.name = "Computer"
                player.symbol = "O"
                break
            player.choose_name()
            player.choose_symbol()
        os.system("cls")

    def play_game_1_player(self):
        while True:
            self.play_turn_1_player()
            if self.check_win():
                print(f"Player: {self.players[self.current_player_index - 1].name} wins")
                self.save_history(f"Player: {self.players[self.current_player_index - 1].name} wins")
                choose = self.display_endgame_menu()
                if choose == "1":
                    self.restart_game()
                elif choose == "2":
                    self.quit_game()
            elif self.check_draw():
                print("It's a draw!")
                self.save_history("It's a draw!")
                choose = self.display_endgame_menu()
                if choose == "1":
                    self.restart_game()
                elif choose == "2":
                    self.quit_game()

    def play_turn_1_player(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"{player.name}'s turn ({player.symbol})")
        if player.name == "Computer":
            cell_choose = random.randint(1, 9)
            while not self.board.correct_choose(cell_choose, player.symbol):
                cell_choose = random.randint(1, 9)
        else:
            while True:
                try:
                    cell_choose = int(input("Choose a Cell: "))
                    if 1 <= cell_choose <= 9 and self.board.correct_choose(cell_choose, player.symbol):
                        break
                    else:
                        print("Invalid choice, try again")
                except ValueError:
                    print("Invalid input. Please choose a number between 1 and 9")

        self.board.update_board(cell_choose, player.symbol)
        self.history.append(f"Player: {player.name} ({player.symbol}) choose Cell: {cell_choose}")
        os.system("cls")
        self.switch_player()
        


    def setup_2_player(self):  # إعداد اللاعبين
        for num, player in enumerate(self.players, start=1):  # الاستعداد لتهيئة كل لاعب
            print(f"Player {num}")  # طباعة رقم اللاعب
            player.choose_name()  # اختيار اسم اللاعب
            player.choose_symbol()  # اختيار الرمز
        os.system("cls")  # تنظيف الشاشة

    def play_game_2_player(self):  # بدء اللعبة
        while True:  # حلقة اللعب الرئيسية
            self.play_turn_2_player()  # بدء الدور
            if self.check_win():  # التحقق من الفوز
                print(f"Player: {self.players[self.current_player_index - 1].name} wins")  # إذا فاز اللاعب
                self.save_history(f"Player: {self.players[self.current_player_index - 1].name} wins")  # حفظ التاريخ مع رسالة الفوز
                choose                 = self.menu.display_endgame_menu()  # عرض قائمة نهاية اللعبة
                if choose == "1":  # إذا اختار المستخدم اللعب مرة أخرى
                    self.restart_game()  # إعادة بدء اللعبة
                elif choose == "2":  # إذا اختار المستخدم الخروج من اللعبة
                    self.quit_game()  # الخروج من اللعبة
                else:  # إذا كان الاختيار غير صحيح
                    print("Invalid choice")  # طباعة رسالة
            elif self.check_draw():  # التحقق من التعادل
                print("It's a draw!")  # إذا كانت التعادل
                self.save_history("It's a draw!")  # حفظ التاريخ مع رسالة التعادل
                choose = self.menu.display_endgame_menu()  # عرض قائمة نهاية اللعبة
                if choose == "1":  # إذا اختار المستخدم اللعب مرة أخرى
                    self.restart_game()  # إعادة بدء اللعبة
                elif choose == "2":  # إذا اختار المستخدم الخروج من اللعبة
                    self.quit_game()  # الخروج من اللعبة
                else:  # إذا كان الاختيار غير صحيح
                    print("Invalid choice")  # طباعة رسالة

    def play_turn_2_player(self):  # بدء الدور
        player = self.players[self.current_player_index]  # الحصول على لاعب الدور الحالي
        self.board.display_board()  # عرض اللوحة
        print(f"{player.name}'s turn ({player.symbol})")  # طباعة دور اللاعب
        while True:  # حلقة الدور
            try:
                cell_choose = int(input("Choose a Cell: "))  # استقبال الخانة التي اختارها اللاعب
                if 1 <= cell_choose <= 9 and self.board.correct_choose(cell_choose, player.symbol):  # التحقق من صحة الخانة المختارة
                    self.board.update_board(cell_choose, player.symbol)  # تحديث اللوحة بالرمز المختار
                    self.history.append(f"Player: {player.name} ({player.symbol}) choose Cell: {cell_choose}")  # إضافة الحركة إلى التاريخ
                    os.system("cls")
                    break
                else:  # إذا كان الاختيار غير صحيح
                    print("Invalid choice, try again")  # طباعة رسالة
            except ValueError:  # في حالة حدوث خطأ في التحويل
                print("Invalid input. Please choose a number between 1 and 9")  # طباعة رسالة

        self.switch_player()  # التبديل إلى اللاعب التالي

    def switch_player(self):  # التبديل إلى اللاعب التالي
        self.current_player_index = (self.current_player_index + 1) % 2  # تغيير مؤشر اللاعب الحالي

    def check_win(self):  # التحقق من الفوز
        win_case = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]  # الحالات الممكنة للفوز
        score_1 = 0
        score_2 = 0
        for win in win_case:  # الاستعداد للتحقق من كل حالة فوز
            if self.board.board[win[0]] == self.board.board[win[1]] == self.board.board[win[2]] in ["X", "O"]:  # التحقق من توافق الرموز
                self.board.display_board()
                winner = self.players[self.current_player_index - 1]
                winner.increase_score()  # Increase the score of the winning player
                return True  # في حالة الفوز
        return False  # في حالة عدم الفوز

    def check_draw(self):  # التحقق من التعادل
        return all(not cell.isdigit() for cell in self.board.board)  # إذا كانت جميع الخانات ممتلئة ولم يحدث فوز

    def restart_game(self):  # إعادة بدء اللعبة
        self.board.reset_board()  # إعادة تهيئة اللوحة
        self.current_player_index = 0  # تحديد اللاعب الأول
        self.start_game()  # بدء اللعبة من جديد

    def quit_game(self):  # الخروج من اللعبة
        print("Thank You For Playing")  # رسالة شكر
        exit()  # الخروج من البرنامج
    
    def save_history(self, result):  # حفظ تاريخ اللعبة
        file_path = r"D:\Projecrs\VS Code\Python\Games\Tic Tac Toe\history.txt"
        with open(file_path, "a") as file:
            file.write("\n".join(self.history))  # كتابة الحركات إلى الملف
            file.write(f"\n{result}\n")  # كتابة النتيجة إلى الملف
            file.write("="*20 + "\n")  # فصل بين الألعاب

start_game = Game().start_game()  # بدء اللعبة

