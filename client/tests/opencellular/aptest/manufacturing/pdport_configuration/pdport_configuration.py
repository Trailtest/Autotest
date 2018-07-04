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


class pdport_configuration(test.test):

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
        logging.info('TEST CASE XX - AP Test - Manufacturing - PD Port configuration Test')   

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
        s.sendline('/home/oc/host/ocmw/ocmw_usb')
        time.sleep(5)


        logging.info('COLLECTING MSATA Configuration ....')
        port_speed = subprocess.check_output('/home/oc/host/ocmw/occmd get status ethernet.port1.speed', shell=True) 
        time.sleep(5)
        logging.info('PORT SPEED is : %s',port_speed)

        speed = 0
        link = 0
        duplex = 0

        if 'speed' in port_speed:
            speed = int(port_speed.split(' = ')[1])
            logging.info('PORT SPEED IS %s',speed)  

        logging.info('COLLECTING MSATA Configuration ....')
        port_link = subprocess.check_output('/home/oc/host/ocmw/occmd get status ethernet.port1.link', shell=True)
        time.sleep(5)
        logging.info('PORT LINK is : %s',port_link)

        if 'link' in port_link:
            link = int(port_link.split(' = ')[1])
            logging.info('PORT LINK IS %s',link)

        logging.info('COLLECTING MSATA Configuration ....')
        port_duplex = subprocess.check_output('/home/oc/host/ocmw/occmd get status ethernet.port1.duplex', shell=True)
        time.sleep(5)
        logging.info('PORT DUPLEX is : %s',port_duplex)

        if 'duplex' in port_duplex:
            duplex = int(port_duplex.split(' = ')[1])
            logging.info('PORT DUPLEX IS %s',duplex)

        if (speed and link and duplex > 0):
            logging.info('ALL PSE PORT CONFIGURATIONS ARE FINE')
        else:
            logging.info('ALL PSE PORT CONFIGURATIONS ARE NOT FINE')
            raise ValueError('WRONG POWER') 

        s.close()


