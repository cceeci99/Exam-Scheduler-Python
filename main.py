import csp
import time

# variables: (semester, course, teacher, difficulty, with_lab)
semester = 0
course = 1
teacher = 2
difficulty = 3
with_lab = 4

# values: (day, slot)
day = 0
slot = 1


class SchedulingExams(csp.CSP):

    def __init__(self, exams):
        self.variables = []
        self.domains = dict()
        self.neighbors = dict()

        self.readExams(exams)

        for var in self.variables:
            self.domains[var] = [(day, slot) for day in range(1, 22) for slot in range(1, 4)]  # 21 days, 3 slots

        for var in self.variables:
            self.neighbors[var] = [v for v in self.variables if v[course] != var[course]]

        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.var_constraints)

    def readExams(self, file):
        fd = open(file, "r")

        lines = fd.readlines()
        count = 0
        seperator = ','
        for line in lines:
            count += 1
            if count == 1:  # ignore first line
                continue

            tokens = line.split(seperator)

            for i in range(len(tokens)):
                tokens[i] = tokens[i].strip()

            semester_ = tokens[0]
            course_ = tokens[1]
            teacher_ = tokens[2]

            difficulty_ = tokens[3]
            if difficulty_ == "TRUE":
                is_diff = True
            elif difficulty_ == "FALSE":
                is_diff = False
            else:
                return -1

            lab = tokens[4]
            if lab == "TRUE":
                has_lab = True
            elif lab == "FALSE":
                has_lab = False
            else:
                return -1

            self.variables.append((semester_, course_, teacher_, is_diff, has_lab))

        fd.close()

    def var_constraints(self, A, a, B, b):

        # 1. Not 2 exams at same slot on same day
        if a[day] == b[day] and a[slot] == b[slot]:
            return False

        # constraints for courses with lab
        if A[with_lab] and a[slot] == 3:
            return False

        if B[with_lab] and b[slot] == 3:
            return False

        if A[with_lab] or B[with_lab]:
            if a[day] == b[day]:
                if abs(a[slot] - b[slot]) == 1:
                    return False

        # 2. Not 2 exams of same year on same day
        if A[semester] == B[semester]:
            if a[day] == b[day]:
                return False

        # 3. Not 2 exams with same Teacher on same day
        if A[teacher] == B[teacher]:
            if a[day] == b[day]:
                return False

        # # 4. 2 difficult exams must have a space of 2 days between
        if A[difficulty] and B[difficulty]:
            if abs(a[day] - b[day]) <= 2:
                return False

        return True

    def display(self, assignment):
        for var in self.variables:
            print(var, "-->", assignment[var])
            if var[with_lab]:
                print("(", var[0], ",", var[1] + "_lab,", var[2], ") -->", "(", assignment[var][0], ",",
                      assignment[var][1] + 1, ")")


if __name__ == '__main__':
    schedule_exam = SchedulingExams("table.csv")
    #
    print("Start simple BackTracking:")
    begin = time.time()
    res_bt, bt_assign_num = csp.backtracking_search(schedule_exam)
    end = time.time()
    print("Result Exam Scheduling:")
    schedule_exam.display(res_bt)
    bt_time = end - begin
    #
    # print("Start MAC:")
    # begin = time.time()
    # res_mac, mac_assign_num = csp.backtracking_search(schedule_exam, csp.mrv, csp.lcv, csp.mac)
    # end = time.time()
    # print("Result Exam Scheduling:")
    # schedule_exam.display(res_mac)
    # mac_time = end - begin

    # print("Start FC:")
    # begin = time.time()
    # res_fc, fc_assign_num = csp.backtracking_search(schedule_exam, csp.mrv, csp.lcv, csp.forward_checking)
    # end = time.time()
    # print("Result Exam Scheduling:")
    # schedule_exam.display(res_fc)
    # fc_time = end - begin

    # print("Start Min_Conflicts")
    # begin = time.time()
    # res_min, min_assign_num = csp.min_conflicts(schedule_exam)
    # end = time.time()
    # print("Result Exam Scheduling:")
    # schedule_exam.display(res_min)
    # min-cf_time = end - begin

    print("Total time of simple backtracking is {} with {} assignments".format(bt_time, bt_assign_num))
    # print("Total time of MAC is {} with {} assignments".format(mac_time, mac_assign_num))
    # print("Total time of FC is {} with {} assignments".format(fc_time, fc_assign_num))
    # print("Total time of Min_Conflicts is {} with {} assignments".format(min-cf_time, min_assign_num))
