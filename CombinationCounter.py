import sys
import getopt
import itertools
import os.path


class Combination:

    def __init__(self, name):
        self.name = name
        self.count = 0

    def __str__(self):
        name = ""
        for index, val in enumerate(self.name):
            name += str(val)
            if index != (len(self.name) - 1):
                name += ":"
        name = name.strip()
        return name + " ===> " + str(self.count)

    __repr__ = __str__


def file_reader(file_name):
    try:
        data = open(file_name, "r").readlines()
    except OSError:
        raise OSError
    data_array = []
    for line in data:
        line = line.replace("\n", "")
        data_array.append(line.split(":"))
    return data_array


def file_writer(file_name, result):
    path, name = os.path.split(os.path.abspath(file_name))
    name = os.path.splitext(name)[0] + "_result.txt"
    file = open(os.path.join(path, name), "w")
    for value in result:
        file.write(str(value) + "\n")
    file.close()
    print("file " + name + " with results was created")


def count_combinations(data, t_value):
    final_results = []
    for combination_index in itertools.combinations(range(len(data[0])), t_value):
        combination_array = []
        for combination in data:
            array = []
            for c in combination_index:
                array.append(combination[c])
            combination_array.append(array)
        while len(combination_array) != 0:
            combination = combination_array[0]
            combination_name = [-1] * len(data[0])
            for index, val in enumerate(combination_index):
                combination_name[val] = combination[index]
            comb = Combination(combination_name)
            final_results.append(comb)
            for x in combination_array[:]:
                if combination == x:
                    comb.count += 1
                    combination_array.remove(x)
    final_results.sort(key=lambda x: x.count, reverse=True)
    return final_results


def main(argv):
    input_file = ''
    t_value = ''
    try:
        opts, args = getopt.getopt(argv, "hi:t:")
    except getopt.GetoptError:
        print 'usage: test.py -i <inputfile> -t <t_value>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'usage: test.py -i <inputfile> -t <t_value>'
            sys.exit()
        elif opt == '-i':
            input_file = arg
        elif opt == '-t':
            t_value = arg
    if input_file == '':
        print('option -i is missing')
        print 'usage: test.py -i <inputfile> -t <t_value>'
    elif t_value == '':
        print('option -t is missing')
        print 'usage: test.py -i <inputfile> -t <t_value>'
    else:
        try:
            data = file_reader(input_file)
        except OSError:
            print('cannot open', "filename")
        if len(data) == 0:
            print("file does not contain any data")
        else:
            result = count_combinations(data, int(t_value))
            file_writer(input_file, result)


if __name__ == "__main__":
    main(sys.argv[1:])
