from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import operator

from CalculatorUI import Ui_Calculator

#ตอนนี้ใช้งานได้แค่ + - x / AC = ครับ อาจมีการเปลี่ยนแปลงแบบแผนใหม่ในอนาคต

READY = 0
INPUT = 1


class MainWindow(QMainWindow, Ui_Calculator):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # numbers.
        for n in range(0, 10):
            getattr(self, 'Number%s' % n).pressed.connect(lambda v=n: self.input_number(v))

        # operations.
        self.PlusButton.pressed.connect(lambda: self.operation(operator.add))
        self.MinusButton.pressed.connect(lambda: self.operation(operator.sub))
        self.MultiplyButton.pressed.connect(lambda: self.operation(operator.mul))
        self.DivideButton.pressed.connect(lambda: self.operation(operator.truediv)) 

        self.EqualButton.pressed.connect(self.equals)


        self.AllClearButton.pressed.connect(self.reset)



        self.memory = 0
        self.reset()

        self.show()

    def display(self):
        self.lcdNumber.display(self.stack[-1])

    def reset(self):
        self.state = READY
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def memory_store(self):
        self.memory = self.lcdNumber.value()

    def memory_recall(self):
        self.state = INPUT
        self.stack[-1] = self.memory
        self.display()

    def input_number(self, v):
        if self.state == READY:
            self.state = INPUT
            self.stack[-1] = v
        else:
            self.stack[-1] = self.stack[-1] * 10 + v

        self.display()

    def operation(self, op):
        if self.current_op:
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = op

    def operation_pc(self):
        self.state = INPUT
        self.stack[-1] *= 0.01
        self.display()

    def equals(self):
        if self.state == READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            self.stack = [self.current_op(*self.stack)]
            self.current_op = None
            self.state = READY
            self.display()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("PyQt Calculator")

    window = MainWindow()
    app.exec_()
