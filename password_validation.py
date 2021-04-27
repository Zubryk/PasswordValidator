import os
import string

with open(os.path.join(os.pardir, "d:/My projects/5 term/TZI/Rozraha/password_dictionary.txt"), 'r') as f:
    password_dictionary = set(f.read().split('\n'))

class PasswordCheck:
    def __init__(self, password):
        self.password_dictionary = password_dictionary
        self.password = password
        self.password_length = len(password)

        self.score = sum((
            self.__length_score(),
            self.__upper_score(),
            self.__lower_score(),
            self.__numbers_score(),
            self.__special_score(),
            self.__letters_only_score(),
            self.__numbers_only_score(),
            self.__repeats_score(),
            self.__consecutives_score(),
            self.__sequential_letters_score(),
            self.__sequential_numbers_score()
        ))

    def __char_type_count(self, ctype):
        cnt = 0
        for char in self.password:
            if char in ctype:
                cnt += 1

        return cnt

    def __length_score(self):

        return self.password_length * 4

    def __upper_score(self):
        n_upper = self.__char_type_count(string.ascii_uppercase)
        
        if n_upper > 0:
            return (self.password_length - n_upper) * 2
        
        return 0

    def __lower_score(self):
        n_lower = self.__char_type_count(string.ascii_lowercase)
        
        if n_lower > 0:
            return (self.password_length - n_lower) * 2
        
        return 0

    def __numbers_score(self):
        n_numbers = self.__char_type_count(string.digits)

        return n_numbers * 4

    def __special_score(self):
        n_special = self.__char_type_count(string.punctuation)

        return n_special * 6

    def __letters_only_score(self):
        letters_cnt = self.__char_type_count(string.ascii_letters)
        
        if self.password_length ==  letters_cnt:

            return - self.password_length

        return 0

    def __numbers_only_score(self):
        numbers_cnt = self.__char_type_count(string.digits)
        
        if self.password_length ==  numbers_cnt:

            return - self.password_length

        return 0   
    
    def __repeats_score(self):
        n_repeats = self.password_length - len(set(self.password))

        return -n_repeats

    def __consecutives_score(self):
        char_types = {
            string.ascii_lowercase: 0,
            string.ascii_uppercase: 0,
            string.digits   : 0,
            }

        for c1, c2 in zip(self.password, self.password[1:]):
            
            for char_type in char_types:
                if c1 in char_type and c2 in char_type:
                    char_types[char_type] += 1
        
        return -2 * sum(char_types.values())

    def __sequential_numbers_score(self):
        sequential_number_count = 0
        
        for i in range(1000):
            if str(i) + str(i + 1) in self.password:
                sequential_number_count += 2

        return -sequential_number_count * 2

    def __sequential_letters_score(self):
        password = self.password.lower()
        
        sequential_letter_count = 0

        seeing = False
        for c1, c2 in zip(password, password[1:]):
            if ord(c1)+1 == ord(c2) and c1 in string.ascii_lowercase[:-1]:
                sequential_letter_count += 1

                if not seeing:
                    sequential_letter_count += 1
                    seeing = True
            else:
                seeing = False
        
        sequential_letter_count -= 2 

        if sequential_letter_count > 0:

            return sequential_letter_count * -2 
        
        return 0

    def get_score(self):
        return self.score

    def get_complexity(self):
        if self.score < 20:
            return 'Дуже слабкий'
        elif self.score < 40:
            return 'Слабкий'
        elif self.score < 60:
            return 'Добрий'
        elif self.score < 80:
            return 'Сильний'

        return 'Дуже сильний'

    def check_requirements(self):
        flag = True
        u = 0
        s = 0
        d = 0
        p = 0

        if self.password_length < 8:
            flag = False
            #return "Пароль занадто короткий"
        if self.password in self.password_dictionary:
            flag = False
            #return "Пароль виявлено у відкритому словнику"
        
        if self.__char_type_count(string.ascii_uppercase) > 0:
            u += 1
        if  self.__char_type_count(string.ascii_lowercase) > 0:
            s += 1
        if self.__char_type_count(string.digits) > 0:
            d += 1
        if self.__char_type_count(string.punctuation) > 0:
            p += 1

        if u + s + d + p < 3:
            flag = False

        if self.get_score() < 40:
            flag = False

        return u, s, d, p