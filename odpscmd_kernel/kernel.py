from IPython.kernel.zmq.kernelbase import Kernel
from pexpect import replwrap, EOF

from subprocess import check_output
from os import unlink

import base64
import imghdr
import re
import signal
import urllib
import tempfile
import os

__version__ = '0.2'

version_pat = re.compile(r'MavenVersion (\d+(\.\d+)+)')

class BashKernel(Kernel):
    implementation = 'odpscmd_kernel'
    implementation_version = __version__

    @property
    def language_version(self):
        m = version_pat.search(self.banner)
        return m.group(1)

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = check_output(['odpscmd', '--version']).decode('utf-8')
        return self._banner

    language_info = {'name': 'odps',
                     'codemirror_mode': 'shell',
                     'mimetype': 'text/x-sh',
                     'file_extension': '.sh'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)

        # prepare keywords for auto-completion
        self.keywords = []
        try:
            keywords_file = open("keywords.txt", "r")
            self.keywords = keywords_file.read().split()
            keywords_file.close()
        except:
            pass

        self._start_bash()

    def _start_bash(self):
        # Signal handlers are inherited by forked processes, and we can't easily
        # reset it from the subprocess. Since kernelapp ignores SIGINT except in
        # message handlers, we need to temporarily reset the SIGINT handler here
        # so that bash and its children are interruptible.
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.bashwrapper = replwrap.bash()
        finally:
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            tmp_fd, tmp_path = tempfile.mkstemp()
            os.write(tmp_fd, code.rstrip().encode('UTF-8'))
            os.close(tmp_fd)
            output = self.bashwrapper.run_command('odpscmd --config=odps_config.ini -f ' + tmp_path, timeout=None)
            os.remove(tmp_path)
        except KeyboardInterrupt:
            self.bashwrapper.child.sendintr()
            interrupted = True
            self.bashwrapper._expect_prompt()
            output = self.bashwrapper.child.before
        except EOF:
            output = self.bashwrapper.child.before + 'Restarting Bash'
            self._start_bash()

        if not silent:
            # Send standard output
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        try:
            exitcode = int(self.bashwrapper.run_command('echo $?').rstrip())
        except Exception:
            exitcode = 1

        if exitcode:
            return {'status': 'error', 'execution_count': self.execution_count,
                    'ename': '', 'evalue': str(exitcode), 'traceback': []}
        else:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

    def do_complete(self, code, cursor_pos):
        code = code[:cursor_pos]
        default = {'matches': [], 'cursor_start': 0,
                   'cursor_end': cursor_pos, 'metadata': dict(),
                   'status': 'ok'}

        if not code or code[-1] == ' ':
            return default

        tokens = code.replace(';', ' ').split()
        if not tokens:
            return default

        matches = []
        token = tokens[-1]
        start = cursor_pos - len(token)

        matches = [m for m in self.keywords if m.startswith(token.upper())]

        return {'matches': sorted(matches), 'cursor_start': start,
                'cursor_end': cursor_pos, 'metadata': dict(),
                'status': 'ok'}
