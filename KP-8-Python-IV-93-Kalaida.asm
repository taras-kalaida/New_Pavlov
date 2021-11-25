.386
.model flat, stdcall
option casemap:none
include \masm32\include\masm32rt.inc
includelib \masm32\lib\user32.lib
includelib \masm32\lib\kernel32.lib
.data

a dd ?
b dd ?
.code

func_new proc
    push ebp
    mov ebp, esp
    mov eax, [ebp+12]
    mov a, eax
    mov ebx, [ebp+8]
    mov b, ebx
    @while:
        cmp eax, ebx
        je finish
        cmp eax, ebx
        ja @grater
        mov ebx, b
        sub ebx, eax
        mov b, ebx
        jmp @while
        @grater:
        mov eax, a
        sub eax, ebx
        mov a, eax
    jmp @while
    finish:
    mov a, eax
    fn MessageBox, 0, str$(a), "IV-93, 8, Kalaida", MB_OK
    ret
func_new endp
func_main:
push 25
push 60
invoke func_new
invoke ExitProcess, 0
END func_main
