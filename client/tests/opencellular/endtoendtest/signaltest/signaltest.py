import subprocess
import logging
import time
import pxssh
import configparser

from autotest.client import test


class signaltest(test.test):

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

    def run_once(self, test_path='', port=None, baudrate=None, relay_num=None, on_off=None):
        """
        Runs one iteration of disktest.

        :param disks: List of directories (usually mountpoints) to be passed
                to the test.
        :param gigabytes: Disk space that will be used for the test to run.
        :param chunk_mb: Size of the portion of the disk used to run the test.
                Cannot be larger than the total amount of free RAM.
        """
        logging.info('TEST CASE XX - EndToEnd Test')

        # reading test inputs from config file
        oc_config = configparser.ConfigParser()
        oc_config.read(test_path.split('autotest')[
                       0] + 'autotest/config/oc_config.ini')
        auto_user = oc_config.get('autotest', 'user')
        auto_ip = oc_config.get('autotest', 'ip')
        oc_user = oc_config.get('oc', 'user')
        oc_passwd = oc_config.get('oc', 'passwd')
        oc_ip = oc_config.get('oc', 'ip')
        modem_1_port = oc_config.get('general', 'modem_1_port')
        modem_2_port = oc_config.get('general', 'modem_2_port')
        modem_1_baudrate = oc_config.get('general', 'modem_1_baudrate')
        modem_2_baudrate = oc_config.get('general', 'modem_2_baudrate')

        test_path = test_path + '/endtoendtest'

        # Poll process for new output until finished
        s = pxssh.pxssh(timeout=500, maxread=2000000)
        s.login(oc_ip, oc_user, oc_passwd, auto_prompt_reset=False)
        logging.info('CONFIGURING OCMW TRX....')
        s.sendline('/home/oc/osmo_stack/osmo-run-script/startosmoTRX.sh')
        time.sleep(20)

        # Poll process for new output until finished
        s2 = pxssh.pxssh(timeout=500, maxread=2000000)
        s2.login(oc_ip, oc_user, oc_passwd, auto_prompt_reset=False)
        logging.info('CONFIGURING OCMW BSC....')
        s2.sendline('cd /home/oc/osmo_stack/osmo-run-script')
        s2.sendline('./startosmobsc.sh')
        time.sleep(15)

        # Poll process for new output until finished
        s3 = pxssh.pxssh(timeout=500, maxread=2000000)
        s3.login(oc_ip, oc_user, oc_passwd, auto_prompt_reset=False)
        logging.info('CONFIGURING OCMW BTS...')
        s3.sendline('cd /home/oc/osmo_stack/osmo-run-script')
        s3.sendline('./startosmobts.sh')
        time.sleep(200)

        # sending AT commands to verify modem signal
        process = subprocess.Popen(['cat at_input.py | ssh ' + auto_user + '@' + auto_ip + ' python - ' + modem_1_port +
                                    ' ' + modem_1_baudrate], shell=True, stdout=subprocess.PIPE, cwd="%s/signaltest" % (test_path))

        # Poll process for new output until finished

        logging.info('READING AT COMMAND RESPONSE..')
        respcnt = 0
        while True:
            response = process.stdout.readline()
            if 'CSQ: ' in response:
                res = response.split('CSQ: ')
                if len(res) > 1:
                    res2 = res[1].split('\r')[0]
                if ',' in res2:
                    out_1 = res2.split(',')[0]
                logging.info('AT RESPONSE FOR +CSQ IS :%s', out_1)

                break
            if respcnt == 20:
                break
            logging.info(response)
            respcnt += 1

        (out, err) = process.communicate()

        # sending AT commands to verify modem signal
        process_2 = subprocess.Popen(['cat at_input.py | ssh ' + auto_user + '@' + auto_ip + ' python - ' + modem_2_port +
                                      ' ' + modem_2_baudrate], shell=True, stdout=subprocess.PIPE, cwd="%s/signaltest" % (test_path))

        # Poll process for new output until finished

        logging.info('READING AT COMMAND RESPONSE..')
        respcnt_2 = 0

        while True:
            response = process_2.stdout.readline()
            if 'CSQ: ' in response:
                res = response.split('CSQ: ')
                if len(res) > 1:
                    res2 = res[1].split('\r')[0]
                if ',' in res2:
                    out_1 = res2.split(',')[0]
                logging.info('AT RESPONSE FOR +CSQ IS :%s', out_1)

                break
            if respcnt_2 == 20:
                break

            logging.info(response)
            respcnt_2 += 1

        (out, err) = process_2.communicate()

        s.close()
        s2.close()
        s3.close()
