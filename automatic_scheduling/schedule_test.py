import unittest
from time import sleep
import os
import time
from schedule.data_process import DataProcessor
from schedule.ga import Schedule, Lesson, GeneticSchedule, set_uniconf
from schedule.config import set_run_info, config
from schedule.data_exchange import Exchanger, ExchangeFormat

LECTURE = 0
TUTORIAL = 1
LAB = 2

test_data2 = {
    "lessons": [
        [
            "Discrete Math and Logic",
            "Lecture",
            "B18",
            "Nikolay Shilov"
        ],
        [
            "Data Mining",
            "Lab",
            "B16-DS-01",
            "Ivan Grebenkin"
        ],
        [
            "Advanced Statistics for DS",
            "Lecture",
            "M18-DS",
            "Giancarlo Succi"
        ],
        [
            "Advanced robotic manipulation",
            "Lab",
            "M18-RO-01",
            "Dmitry Popov"
        ],
        [
            "Introduction to Programming 2",
            "Lab",
            "B18-02",
            "Marat Mingazov"
        ],
        [
            "Introduction to Programming 2",
            "Lab",
            "B18-04",
            "Munir Makhmutov"
        ],
        [
            "Introduction to Programming 2",
            "Lab",
            "B18-06",
            "Daniel De Carvalho"
        ],
        [
            "Probability and Statistics",
            "Lecture",
            "B17",
            "Sergey Gorodetskiy"
        ],
        [
            "Digital Signal Processing",
            "Lab",
            "B16-RO-01",
            "Alex Boyko"
        ],
        [
            "Advanced Statistics for DS",
            "Lab",
            "M18-DS-01",
            "Vladimir Ivanov"
        ],
        [
            "Advanced robotic manipulation",
            "Lab",
            "M18-RO-02",
            "Dmitry Popov"
        ],
        [
            "Mathematical Analysis 2",
            "Lecture",
            "B18",
            "Sergey Gorodetskiy"
        ],
        [
            "Probability and Statistics (tutorial)",
            "Tutorial",
            "B17",
            "Rustam Gafarov"
        ],
        [
            "Digital Signal Processing",
            "Lab",
            "B16-SE-01",
            "Alex Boyko"
        ],
        [
            "Software Project",
            "Lab",
            "B17-01",
            "Evgenii Bobrov"
        ],
        [
            "Software Project",
            "Lab",
            "B17-07",
            "Vladislav Dmitriyev"
        ],
        [
            "Data Structure and Algorithms ",
            "Lab",
            "B18-02",
            "Vladislav Ostankovich"
        ],
        [
            "Data Structure and Algorithms ",
            "Lab",
            "B18-04",
            "Mikhail Ostanin"
        ],
        [
            "Mathematical Analysis 2",
            "Lab",
            "B18-05",
            "Ivan Konyukhov"
        ],
        [
            "Data Structure and Algorithms",
            "Lab",
            "B18-06",
            "Nikolay Kudasov"
        ],
        [
            "Software Project",
            "Lab",
            "B17-02",
            "Ivan Dmitriev"
        ],
        [
            "Software Project",
            "Lecture",
            "B17",
            "Alexandr Borisov"
        ],
        [
            "Software Project",
            "Lab",
            "B17-08",
            "Vladislav Dmitriyev"
        ],
        [
            "Data Structure and Algorithms",
            "Lab",
            "B18-05",
            "Nikolay Kudasov"
        ],
        [
            "Mathematical Analysis 2",
            "Lab",
            "B18-06",
            "Ivan Konyukhov"
        ],
        [
            "Software Project",
            "Lab",
            "B17-03",
            "Ivan Dmitriev"
        ],
        [
            "Software Project",
            "Lab",
            "B17-06",
            "Alexandr Borisov"
        ]
    ],
    "days": [
        [
            "Monday"
        ],
        [
            "Tuesday"
        ],
        [
            "Wednesday"
        ],
        [
            "Thursday"
        ],
        [
            "Friday"
        ]
    ],
    "time_slots": [
        [
            "09:00-10:30"
        ],
        [
            "10:35-12:05"
        ],
        [
            "12:10-13:40"
        ],
        [
            "14:10-15:40"
        ],
        [
            "15:45-17:15"
        ],
        [
            "17:20-18:50"
        ],
        [
            "18:55-20:25"
        ]
    ],
    "auditoriums": [
        [
            "101",
            "20"
        ],
        [
            "102",
            "20"
        ],
        [
            "103",
            "20"
        ],
        [
            "104",
            "20"
        ],
        [
            "105",
            "150"
        ],
        [
            "106",
            "100"
        ],
        [
            "107",
            "100"
        ],
        [
            "108",
            "250"
        ],
        [
            "109",
            "20"
        ],
        [
            "301",
            "60"
        ],
        [
            "302",
            "25"
        ],
        [
            "303",
            "25"
        ],
        [
            "304",
            "25"
        ],
        [
            "305",
            "25"
        ],
        [
            "306",
            "25"
        ],
        [
            "307",
            "30"
        ],
        [
            "308",
            "20"
        ],
        [
            "309",
            "30"
        ],
        [
            "310",
            "40"
        ],
        [
            "311",
            "30"
        ],
        [
            "312",
            "40"
        ],
        [
            "313",
            "50"
        ],
        [
            "314",
            "30"
        ],
        [
            "316",
            "20"
        ],
        [
            "317",
            "20"
        ],
        [
            "318",
            "20"
        ],
        [
            "320",
            "20"
        ],
        [
            "321",
            "20"
        ],
        [
            "421",
            "20"
        ]
    ],
    "student_groups": [
        [
            "B18-01",
            "17"
        ],
        [
            "B18-02",
            "29"
        ],
        [
            "B18-03",
            "28"
        ],
        [
            "B18-04",
            "18"
        ],
        [
            "B18-05",
            "28"
        ],
        [
            "B18-06",
            "10"
        ],
        [
            "B17-01",
            "19"
        ],
        [
            "B17-02",
            "28"
        ],
        [
            "B17-03",
            "22"
        ],
        [
            "B17-05",
            "28"
        ],
        [
            "B17-06",
            "28"
        ],
        [
            "B17-07",
            "15"
        ],
        [
            "B17-08",
            "17"
        ],
        [
            "B16-DS-01",
            "23"
        ],
        [
            "B16-DS-02",
            "15"
        ],
        [
            "B16-RO-01",
            "16"
        ],
        [
            "B16-SE-01",
            "23"
        ],
        [
            "B15-01 (SE)",
            "13"
        ],
        [
            "B15-02 (DS)",
            "26"
        ],
        [
            "B15-03 (RO)",
            "11"
        ],
        [
            "M18-DS-01",
            "23"
        ],
        [
            "M18-DS-02",
            "14"
        ],
        [
            "M18-RO-01",
            "15"
        ],
        [
            "M18-RO-02",
            "23"
        ],
        [
            "M18-SE-01",
            "25"
        ],
        [
            "M18-SE-02",
            "27"
        ],
        [
            "B18",
            "130"
        ],
        [
            "B17",
            "157"
        ],
        [
            "M18-RO",
            "38"
        ],
        [
            "M18-SE",
            "52"
        ],
        [
            "M18-DS",
            "37"
        ],
        [
            "B16",
            "77"
        ],
        [
            "B16-DS",
            "38"
        ]
    ]
}
test_data1 = [{'Course_name': 'DSA', 'Lesson_type': 'Lecture', 'Faculty': 'Adil', 'Group': 'BS17', 'Day': 'Monday',
               'Time': '17:20-18:50', 'Auditorium': '103'},
              {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-01',
               'Day': 'Wednesday', 'Time': '10:35-12:05', 'Auditorium': '106'},
              {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-02',
               'Day': 'Wednesday', 'Time': '09:00-10:30', 'Auditorium': '108'},
              {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-03', 'Day': 'Monday',
               'Time': '15:45-17:15', 'Auditorium': '106'},
              {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-05',
               'Day': 'Saturday', 'Time': '17:20-18:50', 'Auditorium': '103'},
              {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-06', 'Day': 'Tuesday',
               'Time': '17:20-18:50', 'Auditorium': '101'},
              {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-07',
               'Day': 'Wednesday', 'Time': '17:20-18:50', 'Auditorium': '104'},
              {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-08', 'Day': 'Friday',
               'Time': '15:45-17:15', 'Auditorium': '105'}, {'Course_name': 'Intro to AI', 'Lesson_type': 'Lecture',
                                                             'Faculty': 'Professor Professor Doctor Joseph Alexander Brown IEEE Senior Member Fallout 76 and Neural Networks Hater',
                                                             'Group': 'BS17', 'Day': 'Saturday',
                                                             'Time': '18:55-20:25', 'Auditorium': '108'},
              {'Course_name': 'Intro to AI', 'Lesson_type': 'Tutorial', 'Faculty': 'Hamna', 'Group': 'BS17',
               'Day': 'Friday', 'Time': '10:35-12:05', 'Auditorium': '102'},
              {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-01',
               'Day': 'Wednesday', 'Time': '09:00-10:30', 'Auditorium': '105'},
              {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-02',
               'Day': 'Tuesday', 'Time': '17:20-18:50', 'Auditorium': '105'},
              {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-03',
               'Day': 'Saturday', 'Time': '15:45-17:15', 'Auditorium': '103'},
              {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-05',
               'Day': 'Saturday', 'Time': '12:10-13:40', 'Auditorium': '106'},
              {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-06',
               'Day': 'Friday', 'Time': '17:20-18:50', 'Auditorium': '108'},
              {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-07',
               'Day': 'Wednesday', 'Time': '10:35-12:05', 'Auditorium': '105'},
              {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-08',
               'Day': 'Thursday', 'Time': '14:10-15:40', 'Auditorium': '108'},
              {'Course_name': 'Calculus', 'Lesson_type': 'Lecture', 'Faculty': 'Gorodetskiy', 'Group': 'BS18',
               'Day': 'Monday', 'Time': '18:55-20:25', 'Auditorium': '108'},
              {'Course_name': 'Calculus', 'Lesson_type': 'Tutorial', 'Faculty': 'Gorodetskiy', 'Group': 'BS18',
               'Day': 'Wednesday', 'Time': '15:45-17:15', 'Auditorium': '104'},
              {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-01',
               'Day': 'Saturday', 'Time': '09:00-10:30', 'Auditorium': '106'},
              {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-02',
               'Day': 'Tuesday', 'Time': '09:00-10:30', 'Auditorium': '101'},
              {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-03',
               'Day': 'Friday', 'Time': '14:10-15:40', 'Auditorium': '104'},
              {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-04',
               'Day': 'Tuesday', 'Time': '14:10-15:40', 'Auditorium': '106'},
              {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Rustam', 'Group': 'BS18-05',
               'Day': 'Monday', 'Time': '18:55-20:25', 'Auditorium': '103'},
              {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Rustam', 'Group': 'BS18-06',
               'Day': 'Friday', 'Time': '09:00-10:30', 'Auditorium': '301'},
              {'Course_name': 'DML', 'Lesson_type': 'Lecture', 'Faculty': 'Nikolay', 'Group': 'BS18', 'Day': 'Friday',
               'Time': '09:00-10:30', 'Auditorium': '108'},
              {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-01', 'Day': 'Friday',
               'Time': '09:00-10:30', 'Auditorium': '105'},
              {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-02', 'Day': 'Saturday',
               'Time': '18:55-20:25', 'Auditorium': '109'},
              {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-03', 'Day': 'Tuesday',
               'Time': '14:10-15:40', 'Auditorium': '301'},
              {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-04', 'Day': 'Monday',
               'Time': '10:35-12:05', 'Auditorium': '107'},
              {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-05', 'Day': 'Monday',
               'Time': '12:10-13:40', 'Auditorium': '105'},
              {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-06', 'Day': 'Monday',
               'Time': '15:45-17:15', 'Auditorium': '107'},
              {'Course_name': 'DSP', 'Lesson_type': 'Lecture', 'Faculty': 'Nikolay', 'Group': 'B16-DS',
               'Day': 'Saturday', 'Time': '10:35-12:05', 'Auditorium': '302'},
              {'Course_name': 'Information Retrieval', 'Lesson_type': 'Lecture', 'Faculty': 'Joo Lee',
               'Group': 'B16-DS-01', 'Day': 'Monday', 'Time': '17:20-18:50', 'Auditorium': '302'}]


class TestInvididual(unittest.TestCase):

    def test_fitness1(self):
        # One auditorium is small

        set_uniconf({"auditorium_size": [10, 20, 15], "group_size": [100, 20, 15]})
        data = [Lesson(time=1, lecture_name=(2, 0), group=2, day=2, auditorium=2, faculty=1),
                Lesson(time=1, lecture_name=(3, 0), group=1, day=2, auditorium=1, faculty=2),
                Lesson(time=1, lecture_name=(4, 0), group=0, day=2, auditorium=0, faculty=3),
                ]

        s = Schedule(lessons=data).fitness
        self.assertEqual(s, config["penalty"])

    def test_fitness2(self):
        # Tutorial before Lecture

        set_uniconf({"auditorium_size": [30, 30, 30], "group_size": [10, 20, 15]})
        data = [Lesson(time=1, lecture_name=(2, TUTORIAL), group=1, day=2, auditorium=2, faculty=1),
                Lesson(time=2, lecture_name=(2, LECTURE), group=1, day=2, auditorium=1, faculty=2),
                Lesson(time=3, lecture_name=(4, LAB), group=1, day=2, auditorium=0, faculty=3),
                ]

        s = Schedule(lessons=data).fitness
        self.assertEqual(s, config["penalty"])

    def test_fitness3(self):
        # Two intersections - one extra lecture for professor & one extra
        # lecture for same group per time slot
        set_uniconf({"auditorium_size": [30, 30, 30], "group_size": [10, 20, 15]})
        data = [Lesson(time=2, lecture_name=(2, TUTORIAL), group=2, day=2, auditorium=2, faculty=2),
                Lesson(time=2, lecture_name=(3, LECTURE), group=1, day=2, auditorium=1, faculty=2),
                Lesson(time=2, lecture_name=(4, LAB), group=1, day=2, auditorium=0, faculty=1),
                ]
        s = Schedule(lessons=data).fitness
        self.assertEqual(s, config['penalty'] * 2)

    def test_fitness4(self):
        # Good Schedule
        set_uniconf({"auditorium_size": [30, 30, 30], "group_size": [10, 20, 15]})
        data = [Lesson(time=0, lecture_name=(2, LECTURE), group=2, day=2, auditorium=2, faculty=2),
                Lesson(time=1, lecture_name=(2, TUTORIAL), group=2, day=2, auditorium=1, faculty=1),
                Lesson(time=2, lecture_name=(2, LAB), group=2, day=2, auditorium=0, faculty=1),
                ]
        s = Schedule(lessons=data).fitness
        self.assertEqual(s, 0)

    def test_csv_import(self):
        # Check that data imported from CSV file has correct structure
        set_run_info(import_csv_path='csv/')
        data = Exchanger.import_data(ExchangeFormat.CSV)
        self.assertGreater(len(data), 0)
        self.assertGreater(len(data['lessons']), 0)
        self.assertGreater(len(data['days']), 0)
        self.assertGreater(len(data['time_slots']), 0)
        self.assertGreater(len(data['auditoriums']), 0)
        self.assertGreater(len(data['student_groups']), 0)

    def test_json_import(self):
        # Check that data imported from JSON file has correct structure
        set_run_info(import_json_path='json/schedule_data.json')
        data = Exchanger.import_data(ExchangeFormat.JSON)
        self.assertGreater(len(data), 0)
        self.assertGreater(len(data['lessons']), 0)
        self.assertGreater(len(data['days']), 0)
        self.assertGreater(len(data['time_slots']), 0)
        self.assertGreater(len(data['auditoriums']), 0)
        self.assertGreater(len(data['student_groups']), 0)

    def test_csv_export(self):
        set_run_info(export_json_path='json/test.json')
        data = test_data1
        Exchanger.export_data(data, ExchangeFormat.CSV)
        os.stat(config['export_csv_path'])

    def test_json_export(self):
        # Check that file with JSON data exists after export
        # ToDO validate correctness of data in output file
        set_run_info(export_json_path='json/test.json')
        data = test_data1
        Exchanger.export_data(data, ExchangeFormat.JSON)
        os.stat(config['export_json_path'])

    def test_csv_to_json(self):
        # Check that file with JSON data exists after transformation
        set_run_info(import_json_path='json/imported_schedule_data.json')
        Exchanger.csv_to_json()
        os.stat(config['import_json_path'])

    def test_initial_population1(self):
        # Test that created population has given size
        set_run_info(size_of_population=10, exchange_format=ExchangeFormat.CSV)
        population, uni_conf = GeneticSchedule.get_initial_population()
        self.assertEqual(10, len(population))

    def test_denumerate_schedule(self):
        # Test that data denumeration do not crash
        pop, uni_conf = GeneticSchedule.get_initial_population(data={
            "lessons": [["DSA", "Lecture", "BS17", "Adil"], ["DML", "Lecture", "BS17", "Nikolay"]],
            "days": [["Monday"], ["Tuesday"], ["Wednesday"]],
            "time_slots": [["09:00-10:30"], ["10:35-12:05"], ["12:10-13:40"], ["14:10-15:40"]],
            "auditoriums": [["101", "20"], ["102", "20"], ["103", "20"], ["104", "20"], ["105", "150"], ["106", "100"]],
            "student_groups": [["BS18", "150"], ["BS17", "150"], ["B16", "60"], ["B16-DS", "25"]]
        }
        )
        best = GeneticSchedule.run(pop, uni_conf)
        schedule = DataProcessor.denumerate_data(best)
        self.assertEqual(len(best), len(schedule))

    def test_system1(self):
        # Test that correct schedule is built

        data = [Lesson(time=1, lecture_name=(2, TUTORIAL), group=2, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=(2, LAB), group=2, day=2, auditorium=1, faculty=2),
                Lesson(time=1, lecture_name=(2, LECTURE), group=2, day=2, auditorium=1, faculty=1),
                Lesson(time=1, lecture_name=(3, TUTORIAL), group=1, day=2, auditorium=1, faculty=4),
                Lesson(time=1, lecture_name=(3, LECTURE), group=1, day=2, auditorium=1, faculty=1),
                Lesson(time=1, lecture_name=(3, LAB), group=1, day=2, auditorium=1, faculty=4),
                ]
        uniconf = {"auditorium_size": [30, 30, 30, 30, 30, 30],
                   "group_size": [10, 20, 15],
                   "number_of_auditoriums": 5,
                   "number_of_timeslots": 5,
                   "number_of_days": 5,
                   }
        set_uniconf(uniconf)
        pop = GeneticSchedule.create_initial(lessons=data)

        best = GeneticSchedule.run(pop, uniconf)
        self.assertEqual(best.fitness, 0)
        self.assert_no_intersections(best)

    def test_system2(self):
        # Test building correct schedule
        t1 = time.time()
        data = [Lesson(time=1, lecture_name=(1, TUTORIAL), group=3, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=(1, LAB), group=3, day=2, auditorium=1, faculty=2),
                Lesson(time=1, lecture_name=(1, LECTURE), group=3, day=2, auditorium=1, faculty=1),
                Lesson(time=1, lecture_name=(4, TUTORIAL), group=3, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=(4, LAB), group=3, day=2, auditorium=1, faculty=2),
                Lesson(time=1, lecture_name=(4, LECTURE), group=3, day=2, auditorium=1, faculty=1),
                Lesson(time=1, lecture_name=(2, TUTORIAL), group=2, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=(2, LAB), group=2, day=2, auditorium=1, faculty=2),
                Lesson(time=1, lecture_name=(2, LECTURE), group=2, day=2, auditorium=1, faculty=1),
                Lesson(time=1, lecture_name=(3, TUTORIAL), group=1, day=2, auditorium=1, faculty=4),
                Lesson(time=1, lecture_name=(3, LECTURE), group=1, day=2, auditorium=1, faculty=1),
                Lesson(time=1, lecture_name=(3, LAB), group=1, day=2, auditorium=1, faculty=4),
                ]
        uniconf = {"auditorium_size": [30, 30, 30, 30, 30, 30],
                   "group_size": [10, 20, 15, 20],
                   "number_of_auditoriums": 5,
                   "number_of_timeslots": 5,
                   "number_of_days": 2,
                   }
        set_uniconf(uniconf)
        pop = GeneticSchedule.create_initial(lessons=data)

        best = GeneticSchedule.run(pop, uniconf)
        self.assertEqual(best.fitness, 0)
        self.assert_no_intersections(best)

    def assert_no_intersections(self, best):
        for l1 in best.lessons:
            for l2 in best.lessons:
                if l1 != l2 and l1.time == l2.time and l1.day == l2.day:
                    self.assertTrue(l1.auditorium != l2.auditorium)
                    self.assertTrue(l1.group != l2.group)
                    self.assertTrue(l1.faculty != l2.faculty)

    def test_dict_import2(self):
        # Check import from dictionary
        pop, uniconf = GeneticSchedule.get_initial_population({
            "lessons": [["DSA", "Lecture", "BS17", "Adil"], ["DML", "Lecture", "BS17", "Nikolay"]],
            "days": [["Monday"], ["Tuesday"], ["Wednesday"]],
            "time_slots": [["09:00-10:30"], ["10:35-12:05"], ["12:10-13:40"], ["14:10-15:40"]],
            "auditoriums": [["101", "20"], ["102", "20"], ["103", "20"], ["104", "20"], ["105", "150"], ["106", "100"]],
            "student_groups": [["BS18", "150"], ["BS17", "150"], ["B16", "60"], ["B16-DS", "25"]]
        }
        )

        sch = GeneticSchedule.run(pop, uniconf)
        self.assert_no_intersections(sch)

    def test_benchmark(self):
        init, uniconf = GeneticSchedule.get_initial_population(test_data2)
        t1 = time.time()
        sch = DataProcessor.denumerate_data(GeneticSchedule.run(init, uniconf))
        print('Running time:', time.time() - t1)


if __name__ == '__main__':
    unittest.main()
