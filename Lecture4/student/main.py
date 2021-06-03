from VandyStudent import VandyStudent

if __name__ == '__main__':
    student1 = VandyStudent('Ao', 'Qu', 'EBI', 'Alex Powell')
    student2 = VandyStudent('Xuhuan', 'Huang', 'Branscomb', 'Lori Rafter')
    print(student1 > student2)
    student1.add_major('Math', 'Econ')
    print(student1.majors)