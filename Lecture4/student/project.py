from VandyStudent import VandyStudent
from Student import add

if __name__ == '__main__':
    print(add(1, 2))
    student1 = VandyStudent('Ao', 'Qu', 'EBI', 'Alex Powell')
    student2 = VandyStudent('Xuhuan', 'Huang', 'Branscomb', 'Lori Rafter')
    print(student1 > student2)
    student1.add_major('Math', 'Econ')
    print(student1.majors)