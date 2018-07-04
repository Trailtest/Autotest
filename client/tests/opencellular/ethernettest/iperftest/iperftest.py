import subprocess
import logging
import time
import pxssh
import configparser

from autotest.client import test


class iperftest(test.test):

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
        logging.info('TEST CASE XX - Ethernet Test - iperf throughput test')

        # reading test inputs from config file
        oc_config = configparser.ConfigParser()
        oc_config.read(test_path.split('autotest')[
                       0] + 'autotest/config/oc_config.ini')
        iperfsrv_user = oc_config.get('iperfsrv', 'user')
        iperfsrv_passwd = oc_config.get('iperfsrv', 'passwd')
        iperfsrv_ip = oc_config.get('iperfsrv', 'ip')

        # starting iperf server on local server 
        s = pxssh.pxssh(timeout=500, maxread=2000000)
        s.login(iperfsrv_ip, iperfsrv_user,
                iperfsrv_passwd, auto_prompt_reset=False)
        s.sendline('iperf -s')
        time.sleep(5)
        # starting iperf client on oc board
        output = subprocess.check_output(
            'iperf -c ' + iperfsrv_ip + ' -t 20 -i 2', shell=True)
        time.sleep(5)

        logging.info(output)
        o_data = output.splitlines()
        o_stats = o_data[len(output.splitlines()) - 1].split('  ')
        logging.info(o_stats)
        # calculating banndwidth and throughput
        if o_stats[0] == '[':
            bandwidth = o_stats[3]
            throughput = o_stats[4]
        else:
            bandwidth = o_stats[2]
            throughput = o_stats[3]

        logging.info('BANDWIDTH IS : %s', bandwidth)
        logging.info('THROUGHPUT IS : %s', throughput)
        logging.info('SERVER OUTPUT-----')
        s.sendline('pkill iperf')
        time.sleep(5)
        # s.logout()
        s.close()
