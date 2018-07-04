import subprocess
import logging
import time
import pxssh
import configparser

from autotest.client import test


class sdrtemptest(test.test):

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
        logging.info('TEST CASE XX - AP Test - SDR Temperature')

        # reading test inputs from config file
        oc_config = configparser.ConfigParser()
        oc_config.read(test_path.split('autotest')[
                       0] + 'autotest/config/oc_config.ini')
        oc_user = oc_config.get('oc', 'user')
        oc_passwd = oc_config.get('oc', 'passwd')
        oc_ip = oc_config.get('oc', 'ip')

        # Poll process for new output until finished
        s = pxssh.pxssh(timeout=500, maxread=2000000)
        s.login(oc_ip, oc_user, oc_passwd, auto_prompt_reset=False)
        logging.info('CONFIGURING OCMW USB....')
        s.sendline('/home/oc/host/ocmw/ocmw_usb')
        time.sleep(5)
        logging.info('COLLECTING SDR TEMPERATURE ....')
        # executing temperature command on oc
        output = subprocess.check_output(
            '/home/oc/host/ocmw/occmd get status sdr.fpga.temperature', shell=True)
        time.sleep(5)

        # collecting sdr temperature from output
        logging.info('SDR TEMPERATURE IS :%s', output.split(' = ')[1])
        time.sleep(5)
        # s.logout()
        s.close()
