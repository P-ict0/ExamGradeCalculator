import json
from pathlib import Path


class PassingGradeCalculator:
    """
    Calculates passing grade for a course.

    Edit the already known grades to ../grades.json
    """

    def __init__(self, filepath: str = Path(__file__).parent / "../grades.json") -> None:
        self.filepath = filepath


    def read_data(self) -> dict:
        """
        Reads all grades from the json file
        """

        jsonDecoder = json.JSONDecoder()

        with open(self.filepath, "r") as f:
            raw_data = f.read()
        
        return jsonDecoder.decode(raw_data)

    @staticmethod
    def validate_data(grades: dict) -> bool:
        """
        Checks if the data is valid
        """

        if not grades["assignments"] or not grades["exam"] or not grades["course"]:
            print("Invalid data!")
            return False
        
        if "assignments" not in grades or "exam" not in grades or "course" not in grades:
            print("Invalid data!")
            return False
        
        if "grades" not in grades["assignments"] or "passing_grade" not in grades["assignments"] or "weight" not in grades["assignments"]:
            print("Invalid assignments data!")
            return False
        
        if "weight" not in grades["exam"] or "passing_grade" not in grades["course"]:
            print("Invalid exam or course data!")
            return False
        
        if grades["assignments"]["weight"] + grades["exam"]["weight"] != 1:
            print("Invalid weights, do not add to 1!")
            return False

        return True

    @staticmethod
    def check_assignments(grades: dict) -> float:
        """
        Calculates assignments passing grade and checks if they meet requirements

        Arguments:
            :param grades: Dictionary containing all the data from the JSON file

        Returns:
            The final assignments grade
        """

        assignment_grades = grades["assignments"]["grades"]
        final_grade = round(sum(assignment_grades) / len(assignment_grades), 2)
        passing_grade = grades["assignments"]["passing_grade"]

        if final_grade < passing_grade:
            print("Assignments not passed!")
            print(f"Your grade: {final_grade}")
            print(f"Passing grade: {passing_grade}")
            exit()
        
        else:
            print("Assignments passed!")
            print(f"Your grade: {final_grade}")
            print()
        
        return final_grade
    

    @staticmethod
    def calculate_course_passing_grade(grades: dict, assignments_final_grade: float):
        """
        Calculates the exam grade needed to pass the course
        """

        total_assignments_grade = assignments_final_grade * grades["assignments"]["weight"]
        course_passing_grade = grades["course"]["passing_grade"]
        exam_weight = grades["exam"]["weight"]
        exam_passing_grade = grades["exam"]["passing_grade"]

        # (final_grade - assignments_grade_with_weight) / exam_weight = exam_grade
        needed_exam_grade = round(max((course_passing_grade - total_assignments_grade) / exam_weight, exam_passing_grade) ,2)

        print(f"To pass the course (grade >= {course_passing_grade}):")
        print(f"You need >= {needed_exam_grade} on the exam")

def main() -> None:
    calculator = PassingGradeCalculator()
    data = calculator.read_data()
    valid = calculator.validate_data(data)
    if not valid:
        print(f"Edit the grades.json file! ({calculator.filepath})")
        exit()
    else:
        assignments_final_grade = calculator.check_assignments(data)
        calculator.calculate_course_passing_grade(data, assignments_final_grade)


if __name__ == "__main__":
    main()
