import os
import sys
import subprocess
import logging
import time
import paramiko
import pxssh
import configparser

from autotest.client import test, utils
from autotest.client.shared import error, utils_memory


class i2cbus_configuration(test.test):

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
        logging.info('TEST CASE XX - AP Test - Manufacturing - I2C BUS  configuration Test')   

        oc_config = configparser.ConfigParser()
        oc_config.read(test_path.split('autotest')[0] + 'autotest/config/oc_config.ini')
        iperfsrv_user = oc_config.get('iperfsrv', 'user')
        iperfsrv_passwd = oc_config.get('iperfsrv', 'passwd')
        iperfsrv_ip = oc_config.get('iperfsrv', 'ip')
        oc_user = oc_config.get('oc', 'user')
        oc_passwd = oc_config.get('oc', 'passwd')
        oc_ip = oc_config.get('oc', 'ip')

        # Poll process for new output until finished
        s = pxssh.pxssh(timeout=500, maxread=2000000)
        s.login(oc_ip,oc_user,oc_passwd,auto_prompt_reset=False)
        logging.info('CONFIGURING UART LINK....')
        s.sendline('cd /home/oc/host/ocmw')
        s.sendline('modprobe i2c-i801')
        time.sleep(5)


        logging.info('COLLECTING I2C BUS Configuration ....')
        output = subprocess.check_output('i2cdetect -y 9', shell=True, cwd='/home/oc/host/ocmw')
        time.sleep(5)
        logging.info('I2C BUS Configuration is : %s',output)
        if '08' and '1f' and '30' and '50' in output:
            logging.info('Temperature sensors detected on device')
        else:
            logging.info('Temperature sensors not detected on device')
            raise ValueError('Failed to detect temperature sensors')


        logging.info('COLLECTING I2C BUS Configuration ....')
        output_2 = subprocess.check_output('i2cdetect -y -r 0', shell=True, cwd='/home/oc/host/ocmw')
        time.sleep(5)
        logging.info('I2C BUS Configuration is : %s',output_2)
        if '5e' in output_2:
            logging.info('Temperature sensors detected on device')
        else:
            logging.info('Temperature sensors not detected on device')
            raise ValueError('Failed to detect temperature sensors') 


        s.close()


