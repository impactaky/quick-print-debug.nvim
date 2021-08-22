# -*- coding: utf-8 -*-
import pynvim as vim
import tempfile
import re

@vim.plugin
class QuickPrintDebugNvim(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.script_file = tempfile.NamedTemporaryFile('w+', suffix='.py')
        self.value_regex = re.compile(r'\$[a-zA-Z0-9_]+')

    @vim.function('_quick_print_debug_init', sync=True)
    def _quick_print_debug_init(self, args):
        self.ns = args[0]

    def _impl_gen_breakpoint(self, file_name, line, message):
        commands = ''
        m = re.search(self.value_regex, message)
        while m:
            if len(message[:m.start()]):
                msg = message[:m.start()]
                if msg[-1] == " ":
                    msg += "\ "
                commands += 'echo {}\n'.format(msg)
            commands += 'output {}\n'.format(m.group()[1:])
            message = message[m.end():]
            m = re.search(self.value_regex, message)
        if message:
            commands += 'echo {}\n'.format(message)
        commands += 'echo \\\\n\ncontinue'
        self.script_file.write('''bp = gdb.Breakpoint('{}:{}', internal=True)
bp.silent = True
bp.commands = \'''{}\'''
'''.format(file_name, line, commands))

    @vim.function('_quick_print_debug_generate_script', sync=True)
    def _gen_script(self, args) -> str:
        self.script_file.truncate(0)
        self.script_file.seek(0)
        bufs = self.nvim.request('nvim_list_bufs')
        for buf in bufs:
            extmarks = self.nvim.request('nvim_buf_get_extmarks', buf, self.ns, [0, 0], [-1, -1], {'details': True})
            for extmark in extmarks:
                self._impl_gen_breakpoint(buf.name, extmark[1]+1, extmark[3]['virt_text'][0][0])
        self.script_file.write("gdb.execute('run', to_string=True)\n")
        self.script_file.write("gdb.execute('quit', to_string=True)\n")
        self.script_file.flush()
        return self.script_file.name
