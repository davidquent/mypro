#!/usr/bin/python3
# -*- coding utf-8 -*-

class Student:
    """
    学生类
    """
    stu_school = 'soochow'

    def tell_stu_info(self):
        print('a')

    def set_info(self):
        pass

print(Student.__dict__['stu_school'])
print(Student.__dict__)