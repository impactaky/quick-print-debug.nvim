call _quick_print_debug_init(g:quick_print_debug_ns_id)

function! quick_print_debug#add_value_print()
    let line = line('.')
    let buffer = bufnr('')
    let value_name = expand("<cword>")
    let message = printf(" > %s = $%s", value_name, value_name)
    call nvim_buf_set_virtual_text(buffer, g:quick_print_debug_ns_id, line-1, [[message, 'Comment']], {})
endfunction

function! quick_print_debug#add_line_print()
    let line = line('.')
    let buffer = bufnr('')
    let buffer_name = expand('%:~:.')
    let message = printf(" > %s:%d", buffer_name, line)
    call nvim_buf_set_virtual_text(buffer, g:quick_print_debug_ns_id, line-1, [[message, 'Comment']], {})
endfunction

function! quick_print_debug#delete()
    let line = line('.')
    let buffer = bufnr('')
    call nvim_buf_clear_namespace(buffer, g:quick_print_debug_ns_id, line-1, line)
endfunction

function! quick_print_debug#run()
    let script_file = _quick_print_debug_generate_script()
    execute ':AsyncRun gdb -q -x' script_file '--args' g:quick_print_debug#run_command
endfunction
