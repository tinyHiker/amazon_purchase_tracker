from playground.demo_exception_raiser import *

try:
    example_function()
except RatingOutOfBounds:
    print("Caught it")