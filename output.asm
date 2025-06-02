section .text
global _start
_start:
mov eax, 2
mov [x], eax

; System exit
mov eax, 1    ; sys_exit
int 0x80

section .data
x: dd 0
