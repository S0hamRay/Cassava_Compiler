section .text
global _start
_start:
mov eax, 10
mov [a], eax
mov eax, 5
mov [b], eax
mov eax, 0
mov [sum], eax
mov eax, 2
push eax
mov eax, [a]
pop ebx
add eax, ebx
mov [a], eax
mov eax, 3
push eax
mov eax, [b]
pop ebx
imul eax, ebx
mov [b], eax
mov eax, [b]
push eax
mov eax, [a]
pop ebx
cmp eax, 0
je else_0
mov eax, [b]
push eax
mov eax, [a]
pop ebx
add eax, ebx
mov [sum], eax
jmp end_if_0
else_0:
mov eax, [b]
push eax
mov eax, [a]
pop ebx
sub eax, ebx
mov [sum], eax
end_if_0:
mov eax, 0
mov [count], eax
start_while_1:
mov eax, 4
push eax
mov eax, [count]
pop ebx
cmp eax, 0
je end_while_1
mov eax, [count]
push eax
mov eax, [sum]
pop ebx
add eax, ebx
mov [sum], eax
jmp start_while_1
end_while_1:
mov eax, [sum]
; TODO: Add integer printing
mov eax, [sum]
mov ebx, eax  ; exit status

; System exit
mov eax, 1    ; sys_exit
int 0x80

section .data
a: dd 10
b: dd 5
sum: dd 0
count: dd 0