from gui.Gui import MyWindow
from PyQt5 import QtWidgets
from consultas import unpack
from typing import Generator
from Consultas.customexceptions import BadQuerry, WrongInput, MovieError
import sys
import itertools


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()

    def process_query(self, queries):
        for i in range(len(queries)):
            try:
                self.process_answer_p(unpack(queries[i]), i)
            except MovieError as err:
                self.process_answer_p(err, i)
            except BadQuerry as err:
                self.process_answer_p(err, i)
            except WrongInput as err:
                self.process_answer_p(err, i)

    def process_answer_p(self, answer, index):
        if isinstance(answer, list):
            self.print_list_querie(answer)
        elif isinstance(answer, Generator):
            self.print_generator_querie(answer)
        elif (isinstance(answer, MovieError) or isinstance(answer, BadQuerry)
              or isinstance(answer, WrongInput)):
            self.add_answer(answer.print_error())
        elif not answer:
            pass

    def process_answer_w(self, answer, index):
        if isinstance(answer, list):
            self.write_list_querie(answer, index)
        elif isinstance(answer, Generator):
            self.write_generator_querie(answer, index)
        elif (isinstance(answer, MovieError) or isinstance(answer, BadQuerry)
              or isinstance(answer, WrongInput)):
            self.write_error(answer.print_error(), index)
        elif not answer:
            pass

    def save_file(self, queries):
        with open("resultados.txt", "w", encoding="utf-8") as infile:
            infile.write("--------DCC MOVIE DATABASE--------\n")
        for i in range(len(queries)):
            try:
                self.process_answer_w(unpack(queries[i]), i)
            except MovieError as err:
                self.process_answer_w(err, i)
            except BadQuerry as err:
                self.process_answer_w(err, i)
            except WrongInput as err:
                self.process_answer_w(err, i)

    def write_error(self, answer, index):
        with open("resultados.txt", "a", encoding="utf-8") as infile:
            infile.write(answer)

    def write_generator_querie(self, answer, index):
        with open("resultados.txt", "a", encoding="utf-8") as infile:
            header, answer = itertools.tee(answer, 2)
            infile.write("\n---------- CONSULTA {} ----------\n".format(index
                                                                      + 1))
            infile.write(", ".join(list(next(header))))
            infile.write("\n")
            for line in answer:
                infile.write(", ".join([data for data in line.values()]))
                infile.write("\n")

    def print_generator_querie(self, answer):
        header, answer = itertools.tee(answer, 2)
        self.add_answer(", ".join(list(next(header))))
        self.add_answer("\n")
        for line in answer:
            self.add_answer(", ".join([data for data in line.values()]))
            self.add_answer("\n")

    def write_list_querie(self, answer, index):
        with open("resultados.txt", "a", encoding="utf-8") as infile:
            infile.write(", ".join(answer))
            infile.write("\n")

    def print_list_querie(self, answer):
        self.add_answer(", ".join(answer))
        self.add_answer("\n")


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)

    sys.__excepthook__ = hook

    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
