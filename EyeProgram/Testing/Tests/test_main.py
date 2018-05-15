import unittest
import subprocess
import os


class TestMain(unittest.TestCase):

    # Basic test that checks that the program doesn't throw any exceptions.
    # This calls main as an external process.
    def test_basic(self):
        try:
            cwd = os.getcwd()
            path = os.path.join(cwd, '..', '..', 'Main\Main.py')
            subprocess.check_output(['python', path], shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            # Report the error from sub process.
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


if __name__ == '__main__':
    unittest.main()
