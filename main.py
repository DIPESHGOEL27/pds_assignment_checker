# Main file to check assignments

import random
from pathlib import Path
import os

from lib.pds import BASE,pull,push,def_input


def pds_checker():
    students = pull("students.txt")
    def_assign = [i.name[-1] for i in Path.cwd().glob(f"{BASE}*")][-1]
    if def_assign:
        a = def_input(
            f"Please enter the {BASE} number which you want to Grade [{def_assign}]: ",
            '1',
        ).strip()
    else:
        a = def_input(
            f"Please enter the {BASE} number which you want to Grade [1]: ", "1"
        ).strip()
    q = def_input(
            f"Please enter the Question number which you want to Grade [4]: ",
            '4',
        ).strip()
    base = Path(f"{BASE}_{a}/Question_{q}")
    if base.exists():
        os.chdir(base)
    else:
        from init import init

        init(a)

    try:
        home = next(Path.cwd().glob("PDS*/"))
        try:
            home_inter = next(Path.cwd().glob("PDS*Intermediate*/"))
            inter = True
        except StopIteration as si:
            print("Inter mediate PDS Directory not found,")
            inter = False
    except StopIteration as si:
        print("PDS Directory not found,")
        print(f"Please download from moodle and place in the folder, {BASE}_{a}")
        return

    test_cases = pull("test_cases.txt")
    code_questions = pull("code_questions.txt")
    test_marks_list = [float(i.split(";")[0]) for i in test_cases]
    ## Here there is a change for %age negative markings, keeping the % sign to signify
    code_marks_list = [float(i.split(";")[0]) if '%' not in i else i.split(";")[0] for i in code_questions]
    
    ## Max marks are calculated ignoring the -ve mark conditions
    max_marks = sum((i for i in (test_marks_list + code_marks_list) if '%' not in str(i) and i > 0))
    
    test_marks_header = [
        f'"Test_Case_{i+1} ({test_marks_list[i]:g})"' for i in range(len(test_cases))
    ]

    code_marks_header=[]
    for i in range(len(code_questions)):
        if '%' in str(code_marks_list[i]):
            code_marks_header.append(f'"Code_{i+1} ({code_marks_list[i]})"')
        else:
            code_marks_header.append(f'"Code_{i+1} ({code_marks_list[i]:g})"')

    header = f"\"Student_Name\",{','.join(test_marks_header)},{','.join(code_marks_header)},\"Total_Marks ({max_marks:g})\",\"Comments\""

    report_path = f"{BASE}_{a}_Question_{q}_report.csv"
    if not Path(report_path).exists():
        push(report_path, header)
    try:
        done = set(i.split(",")[0].strip('"') for i in pull(report_path)[1:])
    except:
        done = set()

    print(f"Working for {report_path}".center(100, "*"))

    for student in students:
        if student and (student in done or student.startswith("#")):
            continue
        total_marks = 0
        test_marks = [0] * len(test_cases)
        code_marks = [0] * len(code_questions)
        comments = []  # String list
        print("Working for student - ", student)
        try:
            try:
                file_exists = True
                if inter:
                    try:
                        c_inter = next(home_inter.glob(student + "*"))
                        os.system(f'"{c_inter}"')
                    except StopIteration as si:
                        print(f"Intermediate C File for {student} not found")
                c = next(home.glob(f"*{student}*"))
                os.system(f'START /B "" "{c}"')
            except StopIteration as si:
                print(f"C File for {student} not found")
                comments.append(
                    f"{BASE} was not submitted properly - Mark/s lost: {max_marks:g} out of {max_marks:g}"
                )
                file_exists = False
            # TODO: COMPILE THE C FILE
            if file_exists:
                return_code = os.system(f'gcc "{c}"')
                if return_code == 0:
                    print("Code ran successfully")
                    # test = test_cases[0]  # TODO: TESTING
                    comments.append(" TEST CASES ".center(30,'='))
                    comments.append("")
                    for i, line in enumerate(test_cases):
                        ## RUN C FILE here with the test case
                        ## If test_case_input_file_# exists then copy it to infile.txt
                        if Path(f"test_case_input_{i+1}.txt").exists():
                            Path('infile.txt').write_text(Path(f"test_case_input_{i+1}.txt").read_text())
                        mark, test_comment, test = line.split(";")
                        mark = float(mark)
                        print(f"Test_Case_{i+1}:".center(50, "-"))
                        print(f"Input: {test}")
                        print(f"Desired Output: {test_comment}")
                        print(f"Program Output:")
                        os.system(f"echo {test} | a.exe")
                        ## This is for a case when an external file is being created
                        if Path("outfile.txt").exists(): os.system("outfile.txt") 
                        if mark > 0:
                            test_marks[i] = float(
                                def_input(
                                    f"\n\nTest_Case_{i+1} - [{mark:g}] Mark/s : ", mark
                                )
                            )
                            if test_marks[i] < mark:
                                comments.append(
                                    f"FAILED: Test Case {i+1}: {test_comment} - Mark/s lost: {mark-test_marks[i]:g} out of {mark:g}"
                                )
                            elif test_marks[i] >= mark:  # in case of typing errpr
                                test_marks[i] = mark
                                comments.append(
                                    f"PASSED: Test Case {i+1}: {test_comment} - Mark/s : {mark:g}"
                                )
                        else:  # This case is for -ve marking, defaults to zero, adds a comment if -ve marks given
                            test_marks[i] = float(
                                def_input(
                                    f"\n\nTest_Case_{i+1} - ({mark:g}) Mark/s - Def: [0]: ",
                                    0,
                                )
                            )  # defaults to 0
                            if test_marks[i] == mark:
                                # if -ve marks are given then add comment
                                comments.append(
                                    f"Passed Negative Criteria: {test_comment} - Mark/s lost: {mark:g}"
                                )
                else:
                    print("The code didn't compile")
                    comments.append(
                        f"FAILED: Code didn't compile successfully - Mark/s lost: {sum(test_marks_list):g} out of {sum(test_marks_list):g}"
                    )
                comments.append("")
                comments.append(" CODE CASES ".center(30,'='))
                comments.append("")
                for i, q in enumerate(code_questions):
                    mark, ques = q.split(";")
                    if '%' in mark:  # This case is for % marking, defaults to zero, adds a comment if -ve marks given
                        code_marks[i] =  float(
                            def_input(f"\n\n{ques} - ({mark}) Mark/s - [0] / +ve (full negative) / -ve (partial negative): ", 0)
                        )  # defaults to 0
                        ## This is to deal with the case where code marks entered is less than max negtive marks
                        max_neg_mark = float(mark.strip('%'))
                        code_marks[i] = code_marks[i] if max_neg_mark < code_marks[i] <= 0 else max_neg_mark
                        if code_marks[i] < 0:
                            comments.append(
                                f"FAILED: Negative % Code Case {i+1}:- {ques} - Mark/s lost: {code_marks[i]:g}% out of Total Marks Obtained"
                            )
                            code_marks[i]= f"{code_marks[i]:g}%"
                    else:
                        mark = float(mark)
                        if mark >= 0:
                            code_marks[i] = float(
                                def_input(f"\n\n{ques} - [{mark:g}] Mark/s : ", mark)
                            )
                            if code_marks[i] < mark:
                                comments.append(
                                    f"FAILED: Code Case {i+1}:- {ques} - Mark/s lost: {mark-code_marks[i]:g} out of {mark:g}"
                                )
                            elif code_marks[i] >= mark:  # in case of typing err0r
                                code_marks[i] = mark
                                comments.append(
                                    f"PASSED: Code Case {i+1}:- {ques} - Mark/s : {mark:g}"
                                )
                        elif mark < 0:  # This case is for -ve marking, defaults to zero, adds a comment if -ve marks given
                            code_marks[i] =  float(
                                def_input(f"\n\n{ques} - ({mark:g}) Mark/s - [0] / +ve (full negative) / -ve (partial negative): ", 0)
                            )  # defaults to 0
                            ## This is to deal with the case where code marks entered is less than max negtive marks
                            code_marks[i] = code_marks[i] if mark <= code_marks[i] <= 0 else mark
                            if code_marks[i] < 0:
                                comments.append(
                                    f"FAILED: Negative Code Case {i+1}: {ques} - Mark/s lost: {code_marks[i]:g} out of {mark:g}"
                                )
                total_marks = sum((i for i in (test_marks + code_marks) if '%' not in str(i)))
                ## TODO: Here we will deduct the negative percentage sums and round to nearest b=0.5 using formula n=b*round(a/b)
                rounding_base=0.5
                total_marks = rounding_base*round((total_marks + total_marks*sum(float(i.strip('%')) for i in code_marks if '%' in str(i))/100)/rounding_base)
            comments.append("")
            comments.append("".center(30,'='))
            comments.append("")
            comments.append(f" TOTAL MARKS OBTAINED = {total_marks:g} ".center(50,'#'))

            if def_input("\n\nGive any other comment? [0]/1: ", 0) == "1":
                comments.insert(0,"")  # Hack for extra spacing
                comments.insert(0,
                    def_input(f"\nPlease enter your final comment for {student}:\n")
                )
            elif total_marks == max_marks:
                comments.insert(0,"")  # Hack for extra spacing
                # comments.append("")  # Hack for extra spacing
                comments.insert(0,
                    random.choice(
                        """Good work
                        Keep it up
                        Keep up the good work
                        Great Job
                        Clean Code
                        Perfect
                        Good
                        Nice work""".split(
                            "\n"
                        )
                    ).strip()
                )

        except Exception as e:
            print("Something went wrong: ", str(e))
            raise
            return
        else:
            try:
                comm = ";;".join(comments).strip(";;")
                report = f'{student},{",".join(f"{i:g}" for i in test_marks)},{",".join(f"{i:g}" if type(i)!=str else i for i in code_marks)},{total_marks:g},"{comm}"'
                # HACK TO fix: keep trying to save record
                while 1:
                    try:
                        push(report_path, report)
                        break
                    except PermissionError:
                        print("The report file is open, please close it to proceed")
                        if (
                            def_input("Press 1 to Try again, or 0 to Quit [1]/0: ", "1")
                            != "1"
                        ):
                            print(f"EXITING. {student}'s record not saved")
                            return
                done.add(student)
                print("The comments given for student:")
                print("\n".join(comments))
                print(f" Done for {student} ".center(100, "#"))
            except Exception as e:
                print("Something went wrong: ", e, str(e))
                raise
                return

    print("Report has been generated.")

if __name__ == "__main__":
    pds_checker()
