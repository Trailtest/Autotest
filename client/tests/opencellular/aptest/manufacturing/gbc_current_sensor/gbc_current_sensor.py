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


class gbc_current_sensor(test.test):

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
        logging.info('TEST CASE XX - AP Test - Manufacturing - GBC current Sensor Test')   

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
        bms_crnt = subprocess.check_output('/home/oc/host/ocmw/occmd get status bms.tiva.current', shell=True) 
        time.sleep(5)
        logging.info('bms tiva current is : %s',bms_crnt)

        bt_crnt = 0

        if 'bms.tiva.current' in bms_crnt:
            if isinstance(bms_crnt.split(' = ')[1], int):
                bt_crnt = int(bms_crnt.split(' = ')[1])
            logging.info('BMS TIVA CURRENT IS %s',bt_crnt)  

        logging.info('COLLECTING BMS Voltage  ....')
        bms_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status bms.tiva.busvoltage', shell=True)
        time.sleep(5)
        logging.info('bms bus voltage is : %s',bms_volt)
     
        bms_busvolt = 0

        if 'bms.tiva.busvoltage' in bms_volt:
            if isinstance(bms_volt.split(' = ')[1], int):
                bms_busvolt = int(bms_volt.split(' = ')[1])
            logging.info('GPP INTEL TEMPERATURE1 IS %s',bms_busvolt)

        logging.info('COLLECTING shunt voltage ....')
        shunt_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status bms.tiva.shuntvoltage', shell=True)
        time.sleep(5)
        logging.info('bms shuntvoltage is : %s',shunt_volt)

        bms_shuntvolt = 0

        if 'bms.tiva.shuntvoltage' in shunt_volt:
            if isinstance(shunt_volt.split(' = ')[1], int):
                bms_shuntvolt = int(shunt_volt.split(' = ')[1])
            logging.info('BMS SHUNT VOLTAGE IS %s',bms_shuntvolt)

        logging.info('COLLECTING gpp intel current ....')
        gpp_crnt = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.intel.current', shell=True)
        time.sleep(5)
        logging.info('gpp intel current is : %s',gpp_crnt)

        gi_crnt = 0

        if 'gpp.intel.current' in gpp_crnt:
            if isinstance(gpp_crnt.split(' = ')[1], int):
                gi_crnt = int(gpp_crnt.split(' = ')[1])
            logging.info('GPP INTEL CURRENT IS %s',gi_crnt)

        logging.info('COLLECTING gpp bus voltage ....')
        gpp_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.intel.busvoltage', shell=True)
        time.sleep(5)
        logging.info('gpp intel bus voltage is : %s',gpp_volt)

        gi_busvolt = 0

        if 'gpp.intel.busvoltage' in gpp_volt:
            if isinstance(gpp_volt.split(' = ')[1], int):
                gi_busvolt = int(gpp_volt.split(' = ')[1])
            logging.info('GPP INTEL BUS VOLTAGE IS %s',gi_busvolt)

        logging.info('COLLECTING shunt voltage ....')
        gi_shunt_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.intel.shuntvoltage', shell=True)
        time.sleep(5)
        logging.info('gpp shuntvoltage is : %s',gi_shunt_volt)

        gpp_shuntvolt = 0

        if 'gpp.intel.shuntvoltage' in gi_shunt_volt:
            if isinstance(gi_shunt_volt.split(' = ')[1], int):
                bms_shuntvolt = int(gi_shunt_volt.split(' = ')[1])
            logging.info('GPP SHUNT VOLTAGE IS %s',gpp_shuntvolt)

        logging.info('COLLECTING gpp intel power ....')
        gi_pwr = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.intel.power', shell=True)
        time.sleep(5)
        logging.info('gpp intel power is : %s',gi_pwr)

        gi_power = 0

        if 'gpp.intel.power' in gi_pwr:
            if isinstance(gi_pwr.split(' = ')[1], int):
                gi_power = int(gi_pwr.split(' = ')[1])
            logging.info('GPP INTEL POWER IS %s',gi_power)



        logging.info('COLLECTING gpp msata current ....')
        msata_crnt = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.msata.current', shell=True)
        time.sleep(5)
        logging.info('gpp msata current is : %s',msata_crnt)

        gm_crnt = 0

        if 'gpp.msata.current' in msata_crnt:
            if isinstance(msata_crnt.split(' = ')[1], int):
                gm_crnt = int(msata_crnt.split(' = ')[1])
            logging.info('GPP MSATA CURRENT IS %s',gm_crnt)

        logging.info('COLLECTING gpp msata bus voltage ....')
        msata_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.msata.busvoltage', shell=True)
        time.sleep(5)
        logging.info('gpp msata bus voltage is : %s',msata_volt)

        gm_busvolt = 0

        if 'gpp.msata.busvoltage' in msata_volt:
            if isinstance(msata_volt.split(' = ')[1], int):
                gm_busvolt = int(msata_volt.split(' = ')[1])
            logging.info('GPP MSATA BUS VOLTAGE IS %s',gm_busvolt)

        logging.info('COLLECTING shunt voltage ....')
        gm_shunt_volt = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.msata.shuntvoltage', shell=True)
        time.sleep(5)
        logging.info('gpp shuntvoltage is : %s',gm_shunt_volt)

        gm_shuntvolt = 0

        if 'gpp.msata.shuntvoltage' in gm_shunt_volt:
            if isinstance(gm_shunt_volt.split(' = ')[1], int):
                gm_shuntvolt = int(gm_shunt_volt.split(' = ')[1])
            logging.info('GPP SHUNT VOLTAGE IS %s',gm_shuntvolt)

        logging.info('COLLECTING gpp msata power ....')
        gm_pwr = subprocess.check_output('/home/oc/host/ocmw/occmd get status gpp.msata.power', shell=True)
        time.sleep(5)
        logging.info('gpp msata power is : %s',gm_pwr)

        gm_power = 0

        if 'gpp.msata.power' in gm_pwr:
            if isinstance(gm_pwr.split(' = ')[1], int):
                gi_power = int(gm_pwr.split(' = ')[1])
            logging.info('GPP MSATA POWER IS %s',gm_power)



        if bt_crnt and bms_busvolt and bms_shuntvolt and gi_crnt and \
           gi_busvolt and gpp_shuntvolt and gi_power and gm_crnt and \
           gm_busvolt and gm_shuntvolt and gm_power > 0:
            logging.info('CURRENT SENSOR ON GBC BOARD IS WORKING FINE')
        else:
            logging.info('CURRENT SENSOR ON GBC BOARD IS NOT WORKING FINE')
            raise ValueError('WRONG DATA') 

        s.close()


