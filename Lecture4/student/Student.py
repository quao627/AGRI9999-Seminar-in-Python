def add(a, b):
    return a+b

class Student:
    def __init__(self, fname, lname, major='Undecided', GPA=4.0):
        self.fname = fname
        self.lname = lname
        self.majors = [major]
        self.__GPA = GPA

    def __len__(self):
        return len(self.majors)

    def __repr__(self):
        return self.fname + " " + self.lname

    def add_major(self, *new_majors):
        if any([major in self.majors for major in new_majors]):
            print("You are not allowed to add repeated majors.")
        else:
            if self.majors == ['Undecided']:
                self.majors = []
            self.majors += new_majors
            print(", ".join(new_majors) + " have been successfully added. ")

    def drop_major(self, major):
        if major not in self.majors:
            print("You haven't declared " + major + " major yet.")
        else:
            self.majors.remove(major)
            print(major + " has been successfully removed.")

    def get_gpa(self):
        return self.__GPA


