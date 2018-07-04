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


class rf_band_configuration(test.test):

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
        logging.info('TEST CASE XX - AP Test - Manufacturing - Configure RF Band, power for Ch1 and Ch2 and Activate Ch1 and Ch2')   

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


        logging.info('configuring rf band for ch1 ....')
        ch1_band_config = subprocess.check_output('/home/oc/host/ocmw/occmd set config rf.ch1_fe.band 3', shell=True) 
        time.sleep(5)

        ch1_band_resp = ''

        if 'rf.ch1_fe.band' in ch1_band_config:
            if isinstance(ch1_band_config.split(' = ')[1], str):
                ch1_band_resp = str(ch1_band_config.split(' = ')[1])
            logging.info('CH1 BAND CONFIGURATION: %s',ch1_band_resp)  

        logging.info('configuring rf arfcn ....')
        ch1_arfcn_config = subprocess.check_output('/home/oc/host/ocmw/occmd  set config rf.ch1_fe.arfcn 51', shell=True)
        time.sleep(5)
     
        ch1_arfcn_resp = ''

        if 'rf.ch1_fe.arfcn' in ch1_arfcn_config:
            if isinstance(ch1_arfcn_config.split(' = ')[1], str):
                ch1_arfcn_resp = str(ch1_arfcn_config.split(' = ')[1])
            logging.info('CH1 ARFCN CONFIGURATION: %s',ch1_arfcn_resp)  

        logging.info('configuring rf txattenuation ....')
        ch1_txatn_config = subprocess.check_output('/home/oc/host/ocmw/occmd  set config rf.ch1_fe.txattenuation 20', shell=True)
        time.sleep(5)
     
        ch1_txatn_resp = ''

        if 'rf.ch1_fe.txattenuation' in ch1_txatn_config:
            if isinstance(ch1_txatn_config.split(' = ')[1], str):
                ch1_txatn_resp = str(ch1_txatn_config.split(' = ')[1])
            logging.info('CH1 TX ATTN CONFIGURATION: %s',ch1_txatn_resp)  
			
        logging.info('configuring rf rxattenuation ....')
        ch1_rxatn_config = subprocess.check_output('/home/oc/host/ocmw/occmd  set config rf.ch1_fe.rxattenuation 20', shell=True)
        time.sleep(5)
     
        ch1_rxatn_resp = ''

        if 'rf.ch1_fe.rxattenuation' in ch1_rxatn_config:
            if isinstance(ch1_rxatn_config.split(' = ')[1], str):
                ch1_rxatn_resp = str(ch1_rxatn_config.split(' = ')[1])
            logging.info('CH1 RXATN CONFIGURATION: %s',ch1_rxatn_resp)  

        logging.info('configuring rf rffe ch1 ....')
        ch1_rffe_config = subprocess.check_output('/home/oc/host/ocmw/occmd enable rffe.ch1', shell=True)
        time.sleep(5)
     
        ch1_rffe_resp = ''

        if 'enable.rffe.ch1' in ch1_rffe_config:
            if isinstance(ch1_rffe_config.split(' = ')[1], str):
                ch1_rffe_resp = str(ch1_rffe_config.split(' = ')[1])
            logging.info('CH1 RFFE CH1 CONFIGURATION: %s',ch1_rffe_resp)  

        logging.info('configuring rf band for ch2 ....')
        ch2_band_config = subprocess.check_output('/home/oc/host/ocmw/occmd set config rf.ch2_fe.band 3', shell=True) 
        time.sleep(5)

        ch2_band_resp = ''

        if 'rf.ch2_fe.band' in ch2_band_config:
            if isinstance(ch2_band_config.split(' = ')[1], str):
                ch2_band_resp = str(ch2_band_config.split(' = ')[1])
            logging.info('CH2 BAND CONFIGURATION: %s',ch2_band_resp)  

        logging.info('configuring rf arfcn ....')
        ch2_arfcn_config = subprocess.check_output('/home/oc/host/ocmw/occmd  set config rf.ch2_fe.arfcn 51', shell=True)
        time.sleep(5)
     
        ch2_arfcn_resp = ''

        if 'rf.ch2_fe.arfcn' in ch2_arfcn_config:
            if isinstance(ch2_arfcn_config.split(' = ')[1], str):
                ch2_arfcn_resp = str(ch2_arfcn_config.split(' = ')[1])
            logging.info('CH2 ARFCN CONFIGURATION: %s',ch2_arfcn_resp)  

        logging.info('configuring rf txattenuation ....')
        ch2_txatn_config = subprocess.check_output('/home/oc/host/ocmw/occmd  set config rf.ch2_fe.txattenuation 20', shell=True)
        time.sleep(5)
     
        ch2_txatn_resp = ''

        if 'rf.ch2_fe.txattenuation' in ch2_txatn_config:
            if isinstance(ch2_txatn_config.split(' = ')[1], str):
                ch2_txatn_resp = str(ch2_txatn_config.split(' = ')[1])
            logging.info('CH2 TX ATTN CONFIGURATION: %s',ch2_txatn_resp)  
			
        logging.info('configuring rf rxattenuation ....')
        ch2_rxatn_config = subprocess.check_output('/home/oc/host/ocmw/occmd  set config rf.ch2_fe.rxattenuation 20', shell=True)
        time.sleep(5)
     
        ch2_rxatn_resp = ''

        if 'rf.ch2_fe.rxattenuation' in ch2_rxatn_config:
            if isinstance(ch2_rxatn_config.split(' = ')[1], str):
                ch2_rxatn_resp = str(ch2_rxatn_config.split(' = ')[1])
            logging.info('CH2 RXATN CONFIGURATION: %s',ch2_rxatn_resp)  

        logging.info('configuring rf rffe ch2 ....')
        ch2_rffe_config = subprocess.check_output('/home/oc/host/ocmw/occmd enable rffe.ch2', shell=True)
        time.sleep(5)
     
        ch2_rffe_resp = ''

        if 'enable.rffe.ch2' in ch2_rffe_config:
            if isinstance(ch2_rffe_config.split(' = ')[1], str):
                ch2_rffe_resp = str(ch2_rffe_config.split(' = ')[1])
            logging.info('CH2 RFFE CH1 CONFIGURATION: %s',ch2_rffe_resp)  

        if (bt_temp and gi_temp1 and gi_temp2 and la_temp and l_temp > 0):
            logging.info('TEMPERATURE SENSOR ON GBC BOARD IS WORKING FINE')
        else:
            logging.info('TEMPERATURE SENSOR ON GBC BOARD IS NOT WORKING FINE')
            raise ValueError('WRONG DATA') 

        s.close()


