from Start import Start

t = Start(r"KP-8-Python-IV-93-Kalaida.py")
code = t.get_result()
data = t.get_data()

text = fr""".386
.model flat, stdcall
option casemap:none
include \masm32\include\masm32rt.inc
includelib \masm32\lib\user32.lib
includelib \masm32\lib\kernel32.lib
.data
{data}
.code
{code}
"""
print(text)
f = open('KP-8-Python-IV-93-Kalaida.asm', 'w+')
f.write(text)
f.close()
input()