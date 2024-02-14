import multiprocessing
import os

def run_script(script_name):
    os.system(f'python {script_name}')

if __name__ == '__main__':
    # Paths to your scripts
    user_interface_script = 'rich_test.py'
    input_gui_script = 'GUI.py'

    # Create process objects for each script
    p1 = multiprocessing.Process(target=run_script, args=(user_interface_script,))
    p2 = multiprocessing.Process(target=run_script, args=(input_gui_script,))

    # Start the processes
    p1.start()
    p2.start()

    # Wait for all processes to finish
    p1.join()
    p2.join()

    print("Both user_interface and input_GUI scripts have completed")