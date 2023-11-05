mov ax,0xb800
mov es,ax
; 清屏
mov cx,80*25
clean:
	mov di,cx
	add di,di
	mov byte [es:di],''
	add di,1
	mov byte [es:di],0x0F
	loop clean
; 显示上方白条
; 移除(0,0)的S字符
mov byte [es:0x00],''
mov cx,80*2-1
mov di,0
headtitle:
	mov di,cx
	mov byte [es:di],0xF0
	; 写入空字符
	add di,di
	mov byte [es:di],''
	;inc cx
	;sub cx,1
	loop headtitle

mov di,0
mov cx,80*2-1
; 显示下方白条
tailtitle:
	mov di,cx
	add di,80*2*24
	mov byte [es:di],0xF0
	; 写入空字符
	mov di,cx
	add di,di
	add di,80*2*24
	mov byte [es:di],''
	loop tailtitle
; 在第一行写入文本 Hello World!
jmp near showHeadText
headText: db 'Hello World!'
showHeadText:
; 虽然可以简单粗暴的用 movsw，但是会出现问题
	mov cx,showHeadText-headText
	mov ax,0x7c0
	mov ds,ax ; 定位到汇编程序所在的内存地址
	showHeadTextLoop:
		mov dx,cx
		mov di,cx
		add di,di
		mov si,headText
		sub dx,1
		add si,dx
;		inc si
;		mov al,1000
		mov al,[ds:si]
		mov byte [es:di],al
		loop showHeadTextLoop
jmp near showTailText
tailText: db '2020~Now gfdgd xi'
showTailText:
	mov cx,showTailText-tailText
	mov ax,0x7c0
	mov ds,ax
	showTailTextLoop:
		mov dx,cx
		mov di,cx
		add di,di
		add di,80*2*24
		mov si,tailText
		sub dx,1
		add si,dx
		mov al,[ds:si]
		mov byte [es:di],al
		loop showTailTextLoop

poweroff:
	; 跳过关机
	jmp near end
	; 关机
	mov ax,5307H  ; 高级电源管理功能，设置电源状态
	mov bx,0001H  ; 设备ID，1：所有设备
	mov cx,0003H  ; 状态，3：表示关机
	int 15h
end:
	times 510-($-$$) db 0
	db 0x55,0xaa
