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


class gbc_temperature_sensor(test.test):

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
        logging.info('TEST CASE XX - AP Test - Manufacturing - GBC Temperature Sensor Test')   

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


        logging.info('COLLECTING tiva temperature ....')
        bms_temp = subprocess.check_output('/home/oc/host/ocmw/occmd get status bms.tiva.temperature', shell=True) 
        time.sleep(5)
        logging.info('bms tiva temperature is : %s',bms_temp)

        bt_temp = 0

        if 'bms.tiva.temperature' in bms_temp:
            if isinstance(bms_temp.split(' = ')[1], int):
                bt_temp = int(bms_temp.split(' = ')[1])
            logging.info('BMS TIVA TEMPERATURE IS %s',bt_temp)  

        logging.info('COLLECTING gpp intel temperature1 ....')
        gppintel_temp1 = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.intel.temperature1', shell=True)
        time.sleep(5)
        logging.info('gpp intel temperature1 is : %s',gppintel_temp1)
     
        gi_temp1 = 0

        if 'gpp.intel.temperature1' in gppintel_temp1:
            if isinstance(gppintel_temp1.split(' = ')[1], int):
                gi_temp1 = int(gppintel_temp1.split(' = ')[1])
            logging.info('GPP INTEL TEMPERATURE1 IS %s',gi_temp1)

        logging.info('COLLECTING gpp intel temperature2 ....')
        gppintel_temp2 = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.intel.temperature2', shell=True)
        time.sleep(5)
        logging.info('gpp intel temperature2 is : %s',gppintel_temp2)

        gi_temp2 = 0

        if 'gpp.intel.temperature2' in gppintel_temp2:
            if isinstance(gppintel_temp2.split(' = ')[1], int):
                gi_temp2 = int(gppintel_temp2.split(' = ')[1])
            logging.info('GPP INTEL TEMPERATURE2 IS %s',gi_temp2)

        logging.info('COLLECTING lead acid temperature ....')
        leadacid_temp = subprocess.check_output('/home/oc/host/ocmw/occmd get status power.leadacid.ts.temperature', shell=True)
        time.sleep(5)
        logging.info('lead acid temperature is : %s',leadacid_temp)

        la_temp = 0

        if 'power.leadacid.ts.temperature' in leadacid_temp:
            if isinstance(leadacid_temp.split(' = ')[1], int):
                la_temp = int(leadacid_temp.split(' = ')[1])
            logging.info('LEAD ACID TEMPERATURE IS %s',la_temp)

        logging.info('COLLECTING lion temperature ....')
        lion_temp = subprocess.check_output('/home/oc/host/ocmw/occmd get status power.lion.ts.temperature', shell=True)
        time.sleep(5)
        logging.info('lion temperature is : %s',lion_temp)

        l_temp = 0

        if 'power.lion.ts.temperature' in lion_temp:
            if isinstance(lion_temp.split(' = ')[1], int):
                l_temp = int(lion_temp.split(' = ')[1])
            logging.info('LION TEMPERATURE IS %s',l_temp)




        if (bt_temp and gi_temp1 and gi_temp2 and la_temp and l_temp > 0):
            logging.info('TEMPERATURE SENSOR ON GBC BOARD IS WORKING FINE')
        else:
            logging.info('TEMPERATURE SENSOR ON GBC BOARD IS NOT WORKING FINE')
            raise ValueError('WRONG DATA') 

        s.close()


