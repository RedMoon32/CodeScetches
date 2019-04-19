from schedule.config import *


class DataProcessor:
    denumeration_data = {'courses': [], 'lesson_types': [], 'faculties': [], 'student_groups': [], 'days': [],
                         'time_slots': [],
                         'auditoriums': []}

    @staticmethod
    def get_uniconf(data: dict) -> dict:
        uni_conf = {}
        uni_conf["auditorium_size"] = []
        uni_conf["group_size"] = []

        for ind, audit in enumerate(data["auditoriums"]):
            uni_conf["auditorium_size"].append(int(audit[1]))
        for ind, group in enumerate(data["student_groups"]):
            uni_conf["group_size"].append(int(group[1]))

        uni_conf['number_of_days'] = len(data['days']) - 1
        uni_conf['number_of_auditoriums'] = len(data['auditoriums']) - 1
        uni_conf['number_of_timeslots'] = len(data['time_slots']) - 1
        return uni_conf

    @staticmethod
    def enumerate_data(data: dict) -> (dict, dict):
        """ Transform strings in data to enumerations. It makes algorithm work faster since string comparison is slower. """
        enumerated_data = {'lessons': [], 'days': [], 'time_slots': [], 'auditoriums': [], 'student_groups': []}
        uni_conf = DataProcessor.get_uniconf(data)
        courses = {}
        lesson_types = {'Lecture': LECTURE, 'Tutorial': TUTORIAL, 'Lab': LAB}
        DataProcessor.denumeration_data['lesson_types'] = ['Lecture', 'Tutorial', 'Lab']
        faculties = {}
        groups = {}

        i = 0
        for lesson in data['lessons']:
            if courses.get(lesson[0]) is None:
                courses[lesson[0]] = i
                DataProcessor.denumeration_data['courses'].append(lesson[0])
                i += 1

        i = 0
        for lesson in data['lessons']:
            if faculties.get(lesson[3]) is None:
                faculties[lesson[3]] = i
                DataProcessor.denumeration_data['faculties'].append(lesson[3])
                i += 1

        i = 0
        for group in data['student_groups']:
            if groups.get(group[0]) is None:
                groups[group[0]] = i
                DataProcessor.denumeration_data['student_groups'].append(group[0])
                i += 1

        for data_type in data:
            entry_number = 0
            for entry in data[data_type]:
                enumerated_data[data_type].append([])
                for i in range(len(entry)):
                    if data_type != 'lessons':
                        enumerated_data[data_type][entry_number] = entry_number
                        DataProcessor.denumeration_data[data_type].append(data[data_type][entry_number][0])
                    else:
                        if i == 0:
                            enumerated_data[data_type][entry_number].append(courses[entry[i]])
                        elif i == 1:
                            enumerated_data[data_type][entry_number].append(lesson_types[entry[i]])
                        elif i == 2:
                            enumerated_data[data_type][entry_number].append(groups[entry[i]])
                        else:
                            enumerated_data[data_type][entry_number].append(faculties[entry[i]])
                entry_number += 1
        return enumerated_data, uni_conf

    @staticmethod
    def denumerate_data(enumerated_data: 'Schedule') -> list:
        """ Transform enumerations in data to strings. It makes resultant schedule human readable again. """
        denumerated_data = []
        for row in enumerated_data:
            denumerated_data.append({
                'Course_name': DataProcessor.denumeration_data['courses'][row.lecture_name[0]],
                'Lesson_type': DataProcessor.denumeration_data['lesson_types'][row.lecture_name[1]],
                'Faculty': DataProcessor.denumeration_data['faculties'][row.faculty],
                'Group': DataProcessor.denumeration_data['student_groups'][row.group],
                'Day': DataProcessor.denumeration_data['days'][row.day],
                'Time': DataProcessor.denumeration_data['time_slots'][row.time],
                'Auditorium': DataProcessor.denumeration_data['auditoriums'][row.auditorium],
            })
        return denumerated_data
