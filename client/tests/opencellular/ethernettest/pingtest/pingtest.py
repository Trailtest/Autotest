import logging
import time
import pxssh
import configparser

from autotest.client import test


class pingtest(test.test):

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
        logging.info('TEST CASE XX - Ethernet Test - ping Test')

        # reading test inputs from config file
        oc_config = configparser.ConfigParser()
        oc_config.read(test_path.split('autotest')[
                       0] + 'autotest/config/oc_config.ini')
        iperfsrv_user = oc_config.get('iperfsrv', 'user')
        iperfsrv_passwd = oc_config.get('iperfsrv', 'passwd')
        iperfsrv_ip = oc_config.get('iperfsrv', 'ip')
        oc_ip = oc_config.get('oc', 'ip')

        s = pxssh.pxssh(timeout=60, maxread=2000000)
        s.login(iperfsrv_ip, iperfsrv_user,
                iperfsrv_passwd, auto_prompt_reset=False)
        s.sendline('ping -c 10 ' + oc_ip)
        time.sleep(5)
        s.prompt()
        data = s.before
        logging.info(data)
        s.logout()

        # ping stats are processing for status
        o_data = data.split('ping statistics ---')[1]
        logging.info('O_DATA IS :%s', o_data)
        o_stats = o_data.split(', ')
        logging.info('O_STATS IS :%s', o_stats)

        if int(o_stats[1].split(' ')[0]) == 10:
            logging.info('PING SUCCESS')
        else:
            logging.info('PING FAILURE')
