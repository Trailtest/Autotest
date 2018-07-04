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


class rf_current_sensor(test.test):

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
        logging.info('TEST CASE XX - AP Test - Manufacturing - RF current Sensor Test')   

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
        logging.info('Navigating....')
        s.sendline('/home/oc/host/ocmw')
        time.sleep(5)


        logging.info('COLLECTING RF current sensor details ....')
        rf_crnt = subprocess.check_output('/home/oc/host/ocmw/occmd get status rf.ch1_sensor.current', shell=True) 
        time.sleep(5)
        logging.info('bms tiva current is : %s',rf_crnt)

        rf1_crnt = 0

        if 'rf.ch1_sensor.current' in rf_crnt:
            if isinstance(rf_crnt.split(' = ')[1], int):
                rf1_crnt = int(rf_crnt.split(' = ')[1])
            logging.info('RF CURRENT IS %s',rf1_crnt)  

        logging.info('COLLECTING RF Voltage  ....')
        rf_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status rf.ch1_sensor.busvoltage', shell=True)
        time.sleep(5)
        logging.info('rf bus voltage is : %s',rf_volt)
     
        rf_busvolt = 0

        if 'rf.ch1_sensor.busvoltage' in rf_volt:
            if isinstance(rf_volt.split(' = ')[1], int):
                rf_busvolt = int(rf_volt.split(' = ')[1])
            logging.info('RF TEMPERATURE1 IS %s',rf_busvolt)

        logging.info('COLLECTING shunt voltage ....')
        shunt_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status rf.ch1_sensor.shuntvoltage', shell=True)
        time.sleep(5)
        logging.info('rf shuntvoltage is : %s',shunt_volt)

        rf_shuntvolt = 0

        if 'rf.ch1_sensor.shuntvoltage' in shunt_volt:
            if isinstance(shunt_volt.split(' = ')[1], int):
                rf_shuntvolt = int(shunt_volt.split(' = ')[1])
            logging.info('RF SHUNT VOLTAGE IS %s',rf_shuntvolt)

        logging.info('COLLECTING rf sensor current ....')
        rf_crnt = subprocess.check_output('/home/oc/host/ocmw/occmd get status rf.ch1_sensor.current', shell=True)
        time.sleep(5)
        logging.info('rf sensor current is : %s',rf_crnt)

        rf1_crnt = 0

        if 'rf.ch1_sensor.current' in rf_crnt:
            if isinstance(rf_crnt.split(' = ')[1], int):
                rf1_crnt = int(rf_crnt.split(' = ')[1])
            logging.info('RF CURRENT IS %s',rf1_crnt)

        logging.info('COLLECTING rf bus voltage ....')
        rf_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status rf.ch1_sensor.busvoltage', shell=True)
        time.sleep(5)
        logging.info('rf voltage is : %s',rf_volt)

        rf_busvolt = 0

        if 'rf.ch1_sensor.busvoltage' in rf_volt:
            if isinstance(rf_volt.split(' = ')[1], int):
                rf_busvolt = int(rf_volt.split(' = ')[1])
            logging.info('RF BUS VOLTAGE IS %s',rf_busvolt)

        logging.info('COLLECTING rf shunt voltage ....')
        rf_shunt_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status rf.ch1_sensor.shuntvoltage', shell=True)
        time.sleep(5)
        logging.info('rf shuntvoltage is : %s',rf_shunt_volt)

        rf_shuntvolt = 0

        if 'rf.ch1_sensor.shuntvoltage' in rf_shunt_volt:
            if isinstance(rf_shunt_volt.split(' = ')[1], int):
                rf_shuntvolt = int(rf_shunt_volt.split(' = ')[1])
            logging.info('RF SHUNT VOLTAGE IS %s',rf_shuntvolt)

        logging.info('COLLECTING rf intel power ....')
        rf_pwr = subprocess.check_output('/home/oc/host/ocmw/occmd get status rf.ch1_sensor.power', shell=True)
        time.sleep(5)
        logging.info('rf power is : %s',rf_pwr)

        rf_power = 0

        if 'rf.ch1_sensor.power' in rf_pwr:
            if isinstance(rf_pwr.split(' = ')[1], int):
                rf_power = int(rf_pwr.split(' = ')[1])
            logging.info('RF POWER IS %s',rf_power)

        if rf1_crnt and rf_busvolt and rf_shuntvolt and rf_power > 0:
            logging.info('CURRENT SENSOR ON RF CHANNEL IS WORKING FINE')
        else:
            logging.info('CURRENT SENSOR ON RF CHANNEL IS NOT WORKING FINE')
            raise ValueError('WRONG DATA') 

        s.close()


