#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:08:58 2018

@author: harry
"""

from setuptools import setup

# https://packaging.python.org/tutorials/distributing-packages/

# Assuming you’re in the root of your project directory, then run:
# pip install -e .
# Although somewhat cryptic, -e is short for --editable, and . refers to the current working directory, so together, it means to install the current directory (i.e. your project) in editable mode. This will also install any dependencies declared with “install_requires” and any scripts declared with “console_scripts”. Dependencies will be installed in the usual, non-editable mode.

setup(name='eyepwm',
      version='0.1',
      description='eyepwm_wrapper',
      author='Harry Callahan',
      author_email='harry.callahan@renishaw.com',
      packages=['eyepwm'],
      zip_safe=False)
