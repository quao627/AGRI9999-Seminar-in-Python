from Student import Student

dorm_ranking = ['zeppos', 'ebi', 'kissam', 'tolman', 'highland', 'blakemore', 'branscomb']

class VandyStudent(Student):
    def __init__(self, fname, lname, dorm, advisor, major='Undecided', GPA=4.0):
        super().__init__(fname, lname, major=major, GPA=GPA)
        self.dorm = dorm.lower()
        self.advisor = advisor

    # Override the previously defined method
    def __repr__(self):
        return self.fname + " " + self.lname + " from " + self.dorm

    def __gt__(self, other):
        first_ranking = dorm_ranking.index(self.dorm) if self.dorm in dorm_ranking else float('inf')
        second_ranking = dorm_ranking.index(other.dorm) if other.dorm in dorm_ranking else float('inf')
        return first_ranking < second_ranking