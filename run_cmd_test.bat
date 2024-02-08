@echo off
REM To run this file, naviagte to the current directory and type '.\run_cmd_test.bat'
REM This is a Windows 10 "batch" file that performs the setup for command line testing and runs the command line testing file.
REM First it deleted the database used by the application
REM Second it recreates the database with only demo-data for testing
REM Third it runs the command_line_testing python file. This type of testing can ony work with the demo data we entered earlier.
del /q activity.log
del /q database.db
python create_database_for_testing.py
python command_line_testing.py