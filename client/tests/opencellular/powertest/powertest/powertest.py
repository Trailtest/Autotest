import subprocess
import logging
import time
import configparser

from autotest.client import test


class powertest(test.test):

    """
    Autotest module for power test.

    @author: vkancharla@fb.com
    """
    version = 2
    preserve_srcdir = True

    def initialize(self):
        """
        Verifies if we have gcc to compile disktest.
        """
        logging.info('INSIDE INIT FUNCTION')

    def build(self, srcdir):
        """
        Compiles disktest.
        """
        logging.info('INSIDE BUILD')

    def run_once(self, test_path='', rasp_ip=None, user=None, relay_num=None, on_off=None):
        """
        Runs one iteration of disktest.

        :param disks: List of directories (usually mountpoints) to be passed
                to the test.
        :param gigabytes: Disk space that will be used for the test to run.
        :param chunk_mb: Size of the portion of the disk used to run the test.
                Cannot be larger than the total amount of free RAM.
        """
        logging.info('TEST CASE XX - Battery Power Test')
        oc_config = configparser.ConfigParser()
        oc_config.read(test_path.split('autotest')[
                       0] + 'autotest/config/oc_config.ini')
        rasbpi_user = oc_config.get('rasbpi', 'user')
        rasbpi_ip = oc_config.get('rasbpi', 'ip')
        test_path = test_path + '/powertest'

        # reading ina for power parameters

        process = subprocess.Popen(['cat INA219.py | ssh ' + rasbpi_user + '@' + rasbpi_ip +
                                    ' python - 1'], shell=True, stdout=subprocess.PIPE, cwd="%s/powertest" % (test_path))
        # Poll process for new output until finished
        nextline = {}
        power = 0
        current = 0
        voltage = 0
        logging.info('READING BATTAERY POWER PARAMETERS AT IDLE TIME')

        while True:
            nextline = process.stdout.readline()
            if 'Bus Voltage' in nextline:
                voltage = int(nextline.split(': ')[
                              1].split(' ')[0].split('.')[0])
                logging.info('Voltage [Volts] :%d', int(voltage))
            if 'Bus Current' in nextline:
                current = int(nextline.split(': ')[
                              1].split(' ')[0].split('.')[0])
                logging.info('Current [mA]:%d', int(current))
            if 'Power' in nextline:
                power = int(nextline.split(': ')[
                            1].split(' ')[0].split('.')[0])
                logging.info('Power [mW]:%d', int(power))

            if nextline == '' and process.poll() is not None:
                break
        (out, err) = process.communicate()
        if current != 0 or power != 0:
            raise ValueError('WRONG POWER')

        # switch on battary power using relay switch
        proc = subprocess.Popen(['cat relay_control.py | ssh ' + rasbpi_user + '@' + rasbpi_ip +
                                 ' python - 2 1'], shell=True, stdout=subprocess.PIPE, cwd="%s/powertest" % (test_path))

        (out, err) = proc.communicate()
        logging.info("program output: %s", out)

        process = subprocess.Popen(['cat INA219.py | ssh ' + rasbpi_user + '@' + rasbpi_ip +
                                    ' python - 1'], shell=True, stdout=subprocess.PIPE, cwd="%s/powertest" % (test_path))

        nextline = {}
        power = 0
        current = 0
        voltage = 0
        while True:
            nextline = process.stdout.readline()
            if 'Bus Voltage' in nextline:
                voltage = int(nextline.split(': ')[
                              1].split(' ')[0].split('.')[0])
                logging.info('Voltage [Volts] :%d', int(voltage))
            if 'Bus Current' in nextline:
                current = int(nextline.split(': ')[
                              1].split(' ')[0].split('.')[0])
                logging.info('Current [mA]:%d', int(current))
            if 'Power' in nextline:
                power = int(nextline.split(': ')[
                            1].split(' ')[0].split('.')[0])
                logging.info('Power [mW]:%d', int(power))

            if nextline == '' and process.poll() is not None:
                break
        (out, err) = process.communicate()

        logging.info("INTERNAL BATTERY SUPPLYING POWER TO BOARD")
        # verify current and power parameters on battary power
        if current == 0 or power == 0:
            raise ValueError('WRONG POWER')

        # switch off battary power using relay switch
        proc = subprocess.Popen(['cat relay_control.py | ssh ' + rasbpi_user + '@' + rasbpi_ip +
                                 ' python - 2 0'], shell=True, stdout=subprocess.PIPE, cwd="%s/powertest" % (test_path))

        (out, err) = proc.communicate()
        logging.info("program output: %s", out)
        time.sleep(20)
        logging.info('AFTER SLEEP..............................')
