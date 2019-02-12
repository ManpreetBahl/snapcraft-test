from setuptools import setup

setup(
   name='eight-puzzle-manpreet',
   version='1.0',
   description='A simple Python app that solves pre-defined 8 puzzle problems using misplaced, manhattan, and euclidean heuristics with both BFS and A* search algorithms.',
   author='Manpreet Bahl',
   author_email='manpreetsingh.bahl@gmail.com',
   python_requires='>=3.5.0',
   py_modules=['solver.py'],
   install_requires=['numpy', 'scipy']
)