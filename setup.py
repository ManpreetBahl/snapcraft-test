import os
from setuptools import setup

def get_requirements():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')) as f:
        return f.read()

setup(
   name='eight-puzzle-manpreet',
   version='1.0',
   description='A simple Python app that solves pre-defined 8 puzzle problems using misplaced, manhattan, and euclidean heuristics with both BFS and A* search algorithms.',
   author='Manpreet Bahl',
   author_email='manpreetsingh.bahl@gmail.com',
   python_requires='>=3.5.0',
   packages=['source'],
   install_requires=get_requirements(),
   scripts=['bin/eight-puzzle-manpreet']
)