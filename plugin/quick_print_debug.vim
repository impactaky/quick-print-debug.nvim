if exists('g:loaded_quick_print_debug_nvim')
    finish
endif
let g:loaded_quick_print_debug_nvim = 1

let g:quick_print_debug_ns_id = nvim_create_namespace('quick-print-debug')

nnoremap <silent><Plug>(quick_print_debug_line) :call quick_print_debug#add_line_print()<CR>
nnoremap <silent><Plug>(quick_print_debug_value) :call quick_print_debug#add_value_print()<CR>