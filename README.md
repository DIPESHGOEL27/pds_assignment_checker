# PDS LAB Assignment Checker Tool

***

## Requirements:

* Python >=3.9 (should exist in path) (This code uses walrus/assignment_operator ( `:=` operator ))
* Gcc >= 8.1 (should exist in path) (best to use code blocks compiler)
* Perl >=5.24 (strawberry) (should exist in path)
* Default editor for `.c` files should be set

## Features:

1. Only reads files of the students from the list in `students.txt`
2. Grading for each Student:
    * Opens the `.c` file in the default text editor (set by user)
    * Automatically Compiles the `.c` file
    * Runs the program with the test cases (read from another file)
    * For each Program:
        * Asks input from TA to grade the test cases (If correct, Press enter to give default: Max Marks)
        * Ask questions to TA according to criteria and takes input the marks for each question (default: Max)
        * Adds comments automatically according to Failed criteria and marks lost
3. At the end, makes a composite `.csv` report file with the results (open with MS Excel or similar application to view)
4. (EXPERIMENTAL) Auto upload the report to moodle (using selenium)

## How to use:

* Download the code anywhere
* Run `init.py` and enter the Assignment number to initialize
* Download all the Assignments from moodle
* Extract and place the "PDSA20S15-\*Assignment\*" folder inside the generated folder
* Edit the `students.txt` file
* For each assignment:
    * Edit the `test_cases.txt` file (located inside the `Assignment_#` folder)
    * Edit the `code_qestions.txt` file (located inside the `Assignment_#` folder)
* Finally run `main.py`

### Editing `students.txt` (NEW):

* Open get_students.py
* Also open any assignment grading page and note the ID
* Edit variable `PAGE_ID` as the noted ID
* Run get_students.py

### Editing `test_cases.txt`:

* This file has to be edited for each Assignment
* Test cases *NEED* to have marks and comments/label for each test case
* Format: `{marks};{label};{test_case}`
* For Example:

```csv
10;Inside Rectangle (should print inside);0 0 7 7 2 3
10;Outside Rectangle (should print Outside);0 0 7 7 9 2
10;On Rectange (should print Outside);0 0 7 7 7 2
```

### Editing `code_questions.txt`:

* This file has to be edited for each Assignment
* Code questions *NEED* to have marks and the question
* Format: `{marks};{code_question}`
* For Example:

```csv
10;Reading in a and b in a single scanf
10;Reading in c and d in a single scanf
20;All four corners computed and printed correctly in correct order
30;If*else statement for checking point is inside or outside
```
## UPDATE
---
### Features added:
* (EXPERIMENTAL) Added support for Auto Upload to moodle, REQUIRED:'
    * Install selenium using `pip install selenium`
    * Download and save the corresponding selenium `chromedirver` in `lib\chromedriver.exe` 
    * Save moodle credentials in `var\creds.txt` as `{USERNAME}:{PASSWORD}`
    * Student ids that moodle uses in `var\mapping.txt`, For Example:
    > {STUDENT_NAME_1},{ID_1}  
    > {STUDENT_NAME_2},{ID_2}  
    * To get ID for student:
        * open any assignment grading page
        * Set to quick grade and display 100 students per page
        * Inspect element using `ctrl+shift+c` and hover in any grade box of the student
        * Note the number you see corresponding to each student in `res\mapping.txt`
* Added support for negative marking in `code_questions.txt`:
    * An entry with negative marks can be given, For Example:
    > -1;Intermediate is missing  
    > -0.5;Missed print statement  
* Added support for assimilating all Assignment and Test results into one csv, use `results_merge.py`
* Added support for negative marking in `test_cases.txt`:
    * An entry with negative marks can be given, For Example:
    > -0.5;Test Case 3: Skips repeated element;5 1 2 3 3 5
* Added support for comemnts in `code_questions.txt` and `test_cases.txt` by starting a line with `#`
* Added support for new line in `code_questions.txt` and `test_cases.txt` by using `!!`
* Added support for predefined comemnts in `code_questions.txt` and `test_cases.txt`


## License:

Copyright <2020-22> (Nishkal Prakash)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
