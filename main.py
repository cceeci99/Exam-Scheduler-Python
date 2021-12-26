import csp
import time
import sys

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

        # 2.Constraints for courses with lab
        if (A[with_lab] and a[slot] == 3) or (B[with_lab] and b[slot] == 3):
            return False

        if A[with_lab] or B[with_lab]:
            if a[day] == b[day]:
                if abs(a[slot] - b[slot]) == 1:
                    return False

        # 3. Not 2 exams of same year on same day
        if A[semester] == B[semester]:
            if a[day] == b[day]:
                return False

        # 4. Not 2 exams with same Teacher on same day
        if A[teacher] == B[teacher]:
            if a[day] == b[day]:
                return False

        # # 5. Difficult exams must have a free space of 2 days between
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

    # --- SIMPLE BackTracking ---

    print("Start simple BackTracking:")
    begin = time.time()
    res_bt, bt_nassigns = csp.backtracking_search(schedule_exam)
    end = time.time()
    print("Result Exam Scheduling:")
    schedule_exam.display(res_bt)
    bt_time = end - begin

    # --- MAC + MRV ---

    schedule_exam = SchedulingExams("table.csv")

    print("Start MAC+mrv:")
    begin = time.time()
    res_mac_mrv, mac_mrv_nassigns = csp.backtracking_search(schedule_exam, csp.mrv, csp.lcv, csp.mac)
    end = time.time()
    print("Result Exam Scheduling:")
    schedule_exam.display(res_mac_mrv)
    mac_mrv_time = end - begin

    # --- MAC + dom/wdeg ---

    schedule_exam = SchedulingExams("table.csv")

    print("Start MAC+dom/wdeg:")
    begin = time.time()
    res_mac_dom, mac_dom_nassigns = csp.backtracking_search(schedule_exam, csp.dom_wdeg, csp.lcv, csp.mac)
    end = time.time()
    print("Result Exam Scheduling:")
    schedule_exam.display(res_mac_dom)
    mac_dom_time = end - begin

    # --- FC + MRV ---

    schedule_exam = SchedulingExams("table.csv")

    print("Start FC+mrv:")
    begin = time.time()
    res_fc_mrv, fc_mrv_nassigns = csp.backtracking_search(schedule_exam, csp.mrv, csp.lcv, csp.forward_checking)
    end = time.time()
    print("Result Exam Scheduling:")
    schedule_exam.display(res_fc_mrv)
    fc_mrv_time = end - begin

    # --- FC + dom/wdeg ---

    schedule_exam = SchedulingExams("table.csv")

    print("Start FC+dom/wdeg:")
    begin = time.time()
    res_fc_dom, fc_dom_nassigns = csp.backtracking_search(schedule_exam, csp.dom_wdeg, csp.lcv, csp.forward_checking)
    end = time.time()
    print("Result Exam Scheduling:")
    schedule_exam.display(res_fc_dom)
    fc_dom_time = end - begin

    # --- MIN CONFLICTS ---

    schedule_exam = SchedulingExams("table.csv")

    print("Start Min_Conflicts")
    begin = time.time()
    res_min, min_nassigns = csp.min_conflicts(schedule_exam)
    end = time.time()
    print("Result Exam Scheduling:")
    schedule_exam.display(res_min)
    min_cf_time = end - begin

    print("Total time of simple backtracking is {} with {} assignments".format(bt_time, bt_nassigns))
    print("Total time of MAC+mrv is {} with {} assignments".format(mac_mrv_time, mac_mrv_nassigns))
    print("Total time of MAC+dom/wdeg is {} with {} assignments".format(mac_dom_time, mac_dom_nassigns))
    print("Total time of FC+mrv is {} with {} assignments".format(fc_mrv_time, fc_mrv_nassigns))
    print("Total time of FC+dom/wdeg is {} with {} assignments".format(fc_dom_time, fc_dom_nassigns))
    print("Total time of Min_Conflicts is {} with {} assignments".format(min_cf_time, min_nassigns))
