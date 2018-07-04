import subprocess
import logging
import pxssh
import configparser

from autotest.client import test


class displaytest(test.test):

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
        logging.info('TEST CASE XX - Display Test - Led verification')

        # reading test inputs from config file
        oc_config = configparser.ConfigParser()
        oc_config.read(test_path.split('autotest')[
                       0] + 'autotest/config/oc_config.ini')
        rasbpi_user = oc_config.get('rasbpi', 'user')
        rasbpi_ip = oc_config.get('rasbpi', 'ip')
        test_path = test_path + '/displaytest'

        # placing ledPositions definition file to raspberry pi
        proc = subprocess.Popen(['scp ledPositions ' + rasbpi_user + '@' + rasbpi_ip + ':/root'],
                                shell=True, stdout=subprocess.PIPE, cwd="%s/displaytest" % (test_path))
        (out, err) = proc.communicate()
        s = pxssh.pxssh(timeout=60, maxread=2000000)
        s.login('192.168.41.19', 'root', 'root123', auto_prompt_reset=False)
        s.sendline('raspistill -ex spotlight -o ledboard.jpg')
        s.logout()

        # capturing led light image and processing light status 
        process = subprocess.Popen(['cat led_detection_g.py | ssh ' + rasbpi_user + '@' + rasbpi_ip +
                                    ' python - ledboard.jpg'], shell=True, stdout=subprocess.PIPE, cwd="%s/displaytest" % (test_path))
        # Poll process for new output until finished
        nextline = {}

        logging.info('READING LED LIGHT STATUS')
        total_green = 0

        # verifying led light status
        while True:
            nextline = process.stdout.readline()
            if 'Number of green LED' in nextline:
                total_green = int(nextline.split(': ')[1])
                logging.info('Total Green Lights :%d', total_green)
            logging.info(nextline)

            if nextline == '' and process.poll() is not None:
                break
        (out, err) = process.communicate()
        if total_green == 14:
            logging.info('DEVICE IS UP AND RUNNING WITHOUT ISSUES')
        else:
            logging.info('DEVICE IS RUNNING WITH ISSUES')
