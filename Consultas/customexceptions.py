class BadQuerry(Exception):
    def __init__(self, name):
        super().__init__(str(name))
        self.name = name

    def print_error(self):
        print("BadQuerry: {}".format(self.name))


class WrongInput(Exception):
    def __init__(self, function, param, value):
        super().__init__("{}, {}, {}".format(function, param, value))
        self.function = function
        self.param = param
        self.value = value

    def print_error(self):
        return "WrongInput: {}, {}, {}".format(self.function, self.param, self.value)


class MovieError(Exception):
    def __init__(self, function, movie, column):
        Exception.__init__(self, ("{}, {}, {}".format(function, movie, column)))
        self.function = function
        self.movie = movie
        self.column = column

    def print_error(self):
        return "MovieError: {}, {}, {}".format(self.function, self.movie, self.column)
