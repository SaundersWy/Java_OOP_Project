# Curtis Saunders, Final Project, CIS 345, 10:30
import csv


class Personnel:

    def __init__(self, acct_num, name, pin, balance, p_type):
        """Personnel Attributes"""
        self.__acct_num = acct_num
        self._name = name
        self.__pin = pin
        self.__balance = balance
        self._p_type = p_type

    @property
    def acct_num(self):
        return self.__acct_num

    @acct_num.setter
    def acct_num(self, num):
        if len(num) != 6:
            print('Enter 6 numbers.')
        else:
            self.__acct_num = num

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def pin(self):
        return self.__pin

    @pin.setter
    def pin(self, new_pin):
        if len(new_pin) != 4:
            print('Enter 4 numbers.')
        else:
            self.__pin = new_pin

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, new_bal):
        self.__balance = new_bal

    @property
    def p_type(self):
        return self._p_type

    @p_type.setter
    def p_type(self, pt):
        if len(pt) == 1:
            if pt != 'C' or pt != 'E':
                self._p_type = pt
            else:
                print('Invalid Type: Enter C or E')
        else:
            print('Type needs to be 1 letter: C or E')


# Account #, Name, Pin, Balance, Type

cust1 = Personnel('000001', 'Wyatt', '1010', 10000000.00, 'C')
cust2 = Personnel('123456', 'Will', '6969', 50000.00, 'C')
cust3 = Personnel('246810', 'Aqura', '6667', 2.50, 'C')
cust4 = Personnel('088212', 'Chloe', '5892', 10000.00, 'C')
cust5 = Personnel('441121', 'Brayden', '2437', 12340.00, 'C')
emp1 = Personnel('000002', 'Manager', '1234', 0.00, 'E')

personnel_list = [cust1, cust2, cust3, cust4, cust5, emp1]
csv_list = [['Account #', 'Name', 'PIN #', 'Balance', 'Personnel Type']]

for x in personnel_list:
    csv_list.append([x.acct_num, x.name, x.pin, x.balance, x.p_type])

# for x in csv_list:
#     print(x)

# Creates csv file for all personnel
'''
with open('personnel.csv', 'w', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerows(csv_list)
'''
