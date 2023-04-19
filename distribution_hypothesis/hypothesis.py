import matplotlib.pyplot as plt
import numpy as np
import csv
from itertools import combinations
from scipy.integrate import quad


class FileFormatError(Exception):
    pass


# Set up data for a hypothesis from a CSV-file
def set_up(file_path: str) -> list:
    with open(file_path, newline='') as csvfile:
        f = csv.reader(csvfile, delimiter=',')
        rows = []
        for row in f:
            rows.append(row)
        if (len(rows) != 2) or (len(rows[0]) != len(rows[1])):
            raise FileFormatError
        res = []
        for i in range(len(rows[0])):
            if len(rows[0][i].split('-')) == 1:
                rows[0][i] = f"{rows[0][i]}-{rows[0][i]}"
        for i in range(len(rows[0])):
            item = (rows[0][i], int(rows[1][i]))
            res.append(item)
        return res


class Hypothesis:
    def __init__(self, file: str, default: int = 5):
        try:
            self.data = set_up(file)
            self.default = default # a default distribution to check
            
            # read the table of chi square critical values
            with open('chi-square-crit.csv', newline='') as csvfile:
                f = csv.reader(csvfile, delimiter=',')
                rows = []
                for row in f:
                    rows.append(row)
            self.chi_square_crit = rows
            self.represent_as_a_table() # show data

        except FileNotFoundError:
            print("File not found.")
            return
        except FileFormatError:
            print("Invalid file format. It must have exactly 2 rows with equal number of items")
            return
        except ValueError:
            print("Invalid type of an item.")
            return
    
    # average value of data
    def average(self):
        middles = []
        frequencies = []
        for i in self.data:
            a, b = i[0].split('-')
            middles.append((float(a) + float(b)) / 2)
            frequencies.append(i[1])
        s = 0
        for i in range(len(middles)):
            s += middles[i] * frequencies[i]
        return s / sum(frequencies)
    
    # calculate the dispersion
    def dispersion(self):
        av = self.average()
        middles = []
        frequencies = []
        for i in self.data:
            a, b = i[0].split('-')
            middles.append((float(a) + float(b)) / 2)
            frequencies.append(i[1])
        s = 0
        for i in range(len(middles)):
            item = np.power((middles[i] - av), 2) * frequencies[i]
            s += item
        return s / sum(frequencies)
        
    # fill table with data
    def populate_table(self):
        data = []
        for i in range(1, 4):
            row = []
            for item in self.data:
                try:
                    row.append(round(item[i], 3))
                except IndexError:
                    row.append(' ')
            data.append(row)
        return data

    # show a table that contains data as rows
    def represent_as_a_table(self):
        fig, ax = plt.subplots()
        ax.set_axis_off()
        rows = ["ni", "pi", "npi"]
        cols = []
        for i in self.data:
            if len(set(i[0].split('-'))) == 1:
                cols.append(i[0].split('-')[0])
            else:
                cols.append(i[0])
        data = self.populate_table()
        ax.table(
            cellText=data,
            rowLabels=rows,
            colLabels=cols,
            cellLoc='center',
            loc='upper left'
        )
        plt.show()

    def plot_polygon(self):
        print("Here is the distribution polygon: ")
        middles = []
        frequencies = []
        for i in self.data:
            a, b = i[0].split('-')
            middles.append((float(a) + float(b)) / 2)
            frequencies.append(i[1])
        plt.plot(np.array(middles), np.array(frequencies))
        plt.show()

    def choose_hypothesis(self) -> int:
        self.plot_polygon()
        while True:
            print("Choose distribution:\n1. Binomial\n2. Poisson\n3. Uniform\n4. Exponential\n5. Normal\n")
            distribution = input("Enter the number: ")
            try:
                distribution = int(distribution)
                if distribution not in range(1, 6):
                    print("Please enter a valid number.")
                    continue
                else:
                    return distribution
            except ValueError:
                if distribution == '':
                    return self.default
                else:
                    print("Please enter a number.")

    def binomial(self, j, params) -> float:
        i = j + 1
        comb = combinations(np.random.rand(len(self.data))-1, i)
        c = 0
        for _ in comb:
            c += 1
        return c * np.power(params[0], i) * np.power((1 - params[0]), (len(self.data) - i))

    def poisson(self, j, params) -> float:
        i = j + 1
        return np.power(np.e, (-1 * params[0])) * (np.power(params[0], i) / np.math.factorial(i))

    def uniform(self, i, params) -> float:
        left, right = self.data[i][0].split('-')
        left, right = float(left), float(right)
        if left == right:
            return 1 / (params[1] - params[0])
        elif left < params[0] or right < params[0]:
            return 0
        elif left >= params[1] or right >= params[1]:
            return 1
        else:
            return (right - left) / (params[1] - params[0])

    def exponential(self, i, params) -> float:
        left, right = self.data[i][0].split('-')
        left, right = float(left), float(right)
        if left == right:
            return params[0] * np.exp(-params[0] * left)
        elif left < 0 or right < 0:
            return 0
        else:
            return np.exp(-params[0] * left) - np.exp(-params[0] * right)

    def normal(self, i, params) -> float:
        left, right = self.data[i][0].split('-')
        left, right = float(left), float(right)

        total = 0
        for j in self.data:
            total += j[1]
        mu = params[0]
        sigma = params[1]
        if left == right:
            return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp((-1*(left-mu)**2)/(2*sigma**2))
        f = lambda t: np.exp(-1/2 * ((t-mu) / sigma)**2)
        return (1/(sigma * np.sqrt(2 * np.pi))) * quad(f, left, right)[0]

    # decorator. you pass the distribution, and it calculates Pi for all.
    def pi(self, distribution, params) -> list[tuple]:
        new_data = []
        s = 0
        for i in range(len(self.data)-1):
            new_data.append((self.data[i][0], self.data[i][1], distribution(i, params)))
            s += new_data[-1][2]
        new_data.append((self.data[-1][0], self.data[-1][1], 1-s, 2))
        return new_data
        
    # calculates all of the pi
    def p(self, distribution):
        params = self.params(distribution)
        print(params)
        if distribution == 1:
            self.data = self.pi(distribution=self.binomial, params=params)
        elif distribution == 2:
            self.data = self.pi(distribution=self.poisson, params=params)
        elif distribution == 3:
            self.data = self.pi(distribution=self.uniform, params=params)
        elif distribution == 4:
            self.data = self.pi(distribution=self.exponential, params=params)
        elif distribution == 5:
            self.data = self.pi(distribution=self.normal, params=params)
        return len(params)

    def params(self, distribution):
        while True:
            answer = input("Do you want to enter parameters?[y/n]")
            if (answer == 'n') or (answer == ''):
                if distribution == 1:
                    return [self.average() / float(self.data[-1][0].split('-')[0])]
                elif distribution == 2:
                    return [self.average()]
                elif distribution == 3:
                    return [self.average() - np.sqrt(3) * np.sqrt(self.dispersion()),
                            self.average() + np.sqrt(3) * np.sqrt(self.dispersion())]
                elif distribution == 4:
                    return [1 / self.average()]
                elif distribution == 5:
                    return [self.average(), np.sqrt(self.dispersion())]
            elif answer == 'y':
                while True:
                    if distribution == 1:
                        try:
                            p = float(input('p = '))
                            if (p < 0) or (p > 1):
                                print("Please enter a correct parameter.")
                                continue
                            return [p]
                        except ValueError:
                            print("Please enter a number.")
                            continue
                    elif distribution == 2:
                        try:
                            la = float(input('lambda = '))
                            if la <= 0:
                                print("Please enter a correct parameter.")
                                continue
                            return [la]
                        except ValueError:
                            print("Please enter a number.")
                            continue
                    elif distribution == 3:
                        try:
                            a = float(input('a = '))
                            b = float(input('b = '))
                            return [a, b]
                        except ValueError:
                            print("Please enter a number.")
                            continue
                    elif distribution == 4:
                        try:
                            la = float(input('lambda = '))
                            if la <= 0:
                                print("Please enter a correct parameter.")
                                continue
                            return [la]
                        except ValueError:
                            print("Please enter a number.")
                            continue
                    elif distribution == 5:
                        try:
                            a = float(input('a = '))
                            s = float(input('s = '))
                            return [a, s]
                        except ValueError:
                            print("Please enter a number.")
                            continue
            else:
                print("Enter y or n.")

    # just calculate npi = ni * pi
    def npi(self):
        n = 0
        for i in self.data:
            n += i[1]

        for i in range(len(self.data)):
            item = self.data[i]
            self.data[i] = (item[0], item[1], item[2], n*item[2])

    # check if ni>5, npi>=10. else join intervals.
    def fix_intervals(self):
        print("Fixing intervals if needed...")
        new_intervals = [self.data[0]]
        for i in range(1, len(self.data)):
            if (self.data[i][1] <= 5) or (self.data[i][3] < 10):
                item = (
                    f"{new_intervals[-1][0].split('-')[0]}-{self.data[i][0].split('-')[1]}",
                    new_intervals[-1][1] + self.data[i][1],
                    new_intervals[-1][2] + self.data[i][2],
                    new_intervals[-1][3] + self.data[i][3]
                )
                new_intervals[-1] = item
            else:
                new_intervals.append(self.data[i])
        while (new_intervals[0][1] <= 5) or (new_intervals[0][3] < 10):
            try:
                item = (
                    f"{new_intervals[0][0].split('-')[0]}-{new_intervals[1][0].split('-')[1]}",
                    new_intervals[1][1] + new_intervals[0][1],
                    new_intervals[1][2] + new_intervals[0][2],
                    new_intervals[1][3] + new_intervals[0][3]
                )
                new_intervals[1] = item
                new_intervals.pop(0)
            except IndexError:
                print("Invalid data.")
                return
        self.data = new_intervals
        print('Done.')

    # calculate chi square empirical
    def x_emp(self) -> float:
        res = 0
        for i in range(len(self.data)):
            item = self.data[i]
            res += ((item[1] - item[3])**2)/item[3]
        return res

    # calculate chi square critical
    def x_crit(self, s) -> float:
        alphas = [0.99, 0.975, 0.95, 0.9, 0.1, 0.05, 0.025, 0.01]
        selection = ''
        for i in range(len(alphas)):
            selection += f'{i+1}. {alphas[i]}\n'
        while True:
            alpha_index = input(selection + "Choose alpha(1 to 8) or leave it default:")
            if alpha_index == '':
                alpha_index = 6
                break
            else:
                try:
                    alpha_index = int(alpha_index) - 1
                    if (alpha_index < 0) or (alpha_index > 7):
                        print("Please choose from the suggested values(1 to 8).")
                        continue
                    break
                except ValueError:
                    print("Please enter a number.")
        df = len(self.data) - s - 1
        try:
            return float(self.chi_square_crit[df][alpha_index])
        except ValueError:
            print("Provided invalid alpha or number of intervals. Returning default value...")
            return 0.0
        except IndexError:
            print("Provided invalid alpha or number of intervals. Returning default value...")
            return 0.0


class CheckHypothesis(Hypothesis):
    def __init__(self, file: str, default: int = 1):
    	super().__init__(file, default)
    	
    # prints itself as a list of calculated attributes and a conclusion
    def check(self):
        d = self.choose_hypothesis()
        s = self.p(d)
        self.npi()
        self.represent_as_a_table()
        self.fix_intervals()
        self.represent_as_a_table()
        chi_emp = self.x_emp()
        chi_crit = self.x_crit(s)
        print(f"Chi squared empirical: {chi_emp}")
        print(f"Chi squared critical: {chi_crit}")
        if chi_emp > chi_crit:
            print("Hypothesis is wrong.")
        else:
            print("Hypothesis is correct.")
