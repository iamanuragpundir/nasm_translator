section .data
	msg db "%d",10,0
	w1 dw "abcd",10
	ab dd "abcd"
	d5 dd 100

section .bss
	r1 resb 10
	r2 resw 2
	r3 resd 1

section .text
	global main
	extern printf
	main: xor eax,ecx
	l1: mov eax,dword[ab]
	add dword[ab],eax
	add eax,1000
	or eax,dword[eax]
    mov eax,dword[ecx+1000]
	sib: mov eax,dword[eax+eax*2]
	cmp dword[ab],1000
	mem: mov dword[eax],eax
	add dword[esi+eax*2],1000
	jnz sib
	jz mem
	inc eax
	inc dword[ab]
	dec dword[ab+1000]
	push esi
	push dword[ab+1000]
	push msg
	inc dword[ab+120]
	inc dword[edi+127]
	mul ecx
	mul dword[ecx]
	mul dword[ecx+edx*4]
	mul dword[esi+100]
	mul dword[ab]
	push 1000
	pop dword[ab+127]
	pop dword[ab+128]
	pop edi
	call dword[ecx+eax*4]
	call msg
	call 1000


