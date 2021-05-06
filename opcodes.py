op={

	'mov' : {
				'reg,reg' : { 'op': '89' , 'rest' : '11{reg2}{reg1}'},
				'reg,dword[reg]' : { 'op' : '8B', 'rest' : '00{reg1}{reg2}'},
				'dword[reg],reg' : { 'op' : '89', 'rest' : '00{reg2}{reg1}'},
				
				'reg,dword[var]' :{ 'op' : '8B' , 'rest' : '00{reg1}101'},
				'dword[var],reg' :{ 'op' : '89' , 'rest' : '00{reg1}101'},
				'dword[var],imm' :{ 'op' : {'127' : 'C7', '128' : 'C7' } , 'rest' : '00000101'},
				'dword[var],var' :{ 'op' : '89' , 'rest' : '00000101'},
				'reg,var' : '0xb8',

				
				'reg,imm' : '0xb8',
				'dword[reg],imm' : { 'op' : {'127' : 'C7', '128' : 'C7'}, 'rest' : {'127' : '00000{reg1}' ,'128' : '00000{reg1}'} },

				'dword[reg+reg*s],imm' : { 'op' : { '127' : 'C7' , '128' : 'C7' } , 'rest' : '00000100{s}{reg2}{reg1}'},
				'dword[reg+reg*s],reg' : { 'op' : '89' , 'rest' : '00{reg3}100{s}{reg2}{reg1}'},
				'reg,dword[reg+reg*s]' : { 'op' : '8B' , 'rest' : '00{reg1}100{s}{reg3}{reg2}'},

				'reg,dword[reg+disp]' : {'op' : '8B' , 'rest' : {'127' : '01{reg1}{reg2}' , '128' : '10{reg1}{reg2}'}},
				'dword[reg+disp],reg' : {'op' : '89' , 'rest' : {'127' : '01{reg2}{reg1}' , '128' : '10{reg2}{reg1}'}}
			},

	'add' : {
				'reg,reg' : {'op': '01','rest' : '11{reg2}{reg1}' },
				'dword[reg],reg' : { 'op' : '01', 'rest' : '00{reg2}{reg1}'},
				'reg,dword[reg]' : { 'op' : '03', 'rest' : '00{reg1}{reg2}'},
				
				'reg,dword[var]' : {'op': '03','rest' : '00{reg1}101' },
				'dword[var],var' :{ 'op' : '81' , 'rest' : '00000101'},
				'dword[var],imm' :{ 'op' : {'127' : '83', '128' : '81' } , 'rest' : '00000101'},
				'dword[var],reg' : {'op': '01','rest' : '00{reg1}101' },
				
				'dword[reg],imm' : { 'op' : {'127' : '83', '128' : '81'}, 'rest' : {'127' : '00000{reg1}' ,'128' : '00000{reg1}'} },
				'reg,imm' : {'op': {'127' : '83', '128' : '81'}, 'rest' : { '127' : '11000{reg1}', '128' : '11000{reg1}'} } ,

				'dword[reg+reg*s],imm' : { 'op' :{ '127' : '83' , '128' : '81' }, 'rest' : '00000100{s}{reg2}{reg1}'},
				'dword[reg+reg*s],reg' : { 'op' : '01' , 'rest' : '00{reg3}100{s}{reg2}{reg1}'},
				'reg,dword[reg+reg*s]' : { 'op' : '03' , 'rest' : '00{reg1}100{s}{reg3}{reg2}'},

				'reg,dword[reg+disp]' : {'op' : '03' , 'rest' : {'127' : '01{reg1}{reg2}' , '128' : '10{reg1}{reg2}'}},
				'dword[reg+disp],reg' : {'op' : '01' , 'rest' : {'127' : '01{reg2}{reg1}' , '128' : '10{reg2}{reg1}'}}
			},

	'sub' : {
				'reg,reg' : {'op': '29', 'rest' : '11{reg2}{reg1}' },
				'dword[reg],reg' : { 'op' : '29', 'rest' : '00{reg2}{reg1}'},
				'reg,dword[reg]' : { 'op' : '2B', 'rest' : '00{reg1}{reg2}'},

				'reg,dword[var]' : {'op': '2B', 'rest' : '11{reg1}101' },
				'dword[var],reg' : {'op': '29', 'rest' : '00{reg1}101' },
				'dword[var],var' :{ 'op' : '81' , 'rest' : '00101101'},
				'dword[var],imm' :{ 'op' : {'127' : '83', '128' : '81' } , 'rest' : '00101101'},

				'dword[reg],imm' : { 'op' : {'127' : '83', '128' : '81'}, 'rest' : {'127' : '00101{reg1}' ,'128' : '00101{reg1}'} },
				'reg,imm' : {'op': {'127' : '83', '128' : '81'}, 'rest' : { '127' : '11101{reg1}', '128' : '11101{reg1}'} },
				
				'dword[reg+reg*s],imm' : { 'op' : { '127' : '83' , '128' : '81' } , 'rest' : '00101100{s}{reg2}{reg1}'},
				'dword[reg+reg*s],reg' : { 'op' : '29' , 'rest' : '00{reg3}100{s}{reg2}{reg1}'},
				'reg,dword[reg+reg*s]' : { 'op' : '2B' , 'rest' : '00{reg1}100{s}{reg3}{reg2}'},

				'reg,dword[reg+disp]' : {'op' : '2B' , 'rest' : {'127' : '01{reg1}{reg2}' , '128' : '10{reg1}{reg2}'}},
				'dword[reg+disp],reg' : {'op' : '29' , 'rest' : {'127' : '01{reg2}{reg1}' , '128' : '10{reg2}{reg1}'}}
			},

	'cmp' : {
				'reg,reg' : {'op': '39', 'rest' : '11{reg2}{reg1}' },
				'dword[reg],reg' : { 'op' : '39', 'rest' : '00{reg2}{reg1}'},
				'reg,dword[reg]' : { 'op' : '3B', 'rest' : '00{reg1}{reg2}'},

				'reg,dword[var]' : {'op': '3B', 'rest' : '11{reg1}101' },
				'dword[var],reg' : {'op': '39', 'rest' : '11{reg1}101' },
				'dword[var],var' :{ 'op' : '81' , 'rest' : '00111101'},
				'dword[var],imm' :{ 'op' : {'127' : '83', '128' : '81' } , 'rest' : '00111101'},

				'dword[reg],imm' : { 'op' : {'127' : '83', '128' : '81'}, 'rest' : {'127' : '00111{reg1}' ,'128' : '00111{reg1}'} },
				'reg,imm' : {'op': {'127' : '83', '128' : ''}, 'rest' : { '127' : '11111{reg1}', '128' : '00011101'} },

				'dword[reg+reg*s],imm' : { 'op' : { '127' : '83' , '128' : '81' } , 'rest' : '00111100{s}{reg2}{reg1}'},
				'dword[reg+reg*s],reg' : { 'op' : '39' , 'rest' : '00{reg3}100{s}{reg2}{reg1}'},
				'reg,dword[reg+reg*s]' : { 'op' : '3B' , 'rest' : '00{reg1}100{s}{reg3}{reg2}'},


				'reg,dword[reg+disp]' : {'op' : '3B' , 'rest' : {'127' : '01{reg1}{reg2}' , '128' : '10{reg1}{reg2}'}},
				'dword[reg+disp],reg' : {'op' : '39' , 'rest' : {'127' : '01{reg2}{reg1}' , '128' : '10{reg2}{reg1}'}}
			},

	'or' : {
				'reg,reg' : {'op': '09', 'rest' : '11{reg2}{reg1}' },
				'dword[reg],reg' : { 'op' : '09', 'rest' : '00{reg2}{reg1}'},
				'reg,dword[reg]' : { 'op' : '0B', 'rest' : '00{reg1}{reg2}'},
				
				'reg,dword[var]' : {'op': '0B', 'rest' : '11{reg1}101' },
				'dword[var],reg' : {'op': '09', 'rest' : '11{reg1}101' },
				'dword[var],var' :{ 'op' : '81' , 'rest' : '00001101'},
				'dword[var],imm' :{ 'op' : {'127' : '83', '128' : '81' } , 'rest' : '00001101'},
				
				'dword[reg],imm' : { 'op' : {'127' : '83', '128' : '81'}, 'rest' : {'127' : '00001{reg1}' ,'128' : '00001{reg1}'} },
				'reg,imm' : {'op': {'127' : '83', '128' : ''}, 'rest' : { '127' : '11001{reg1}', '128' : '00001101'} },

				'dword[reg+reg*s],imm' : { 'op' : { '127' : '83' , '128' : '81' } , 'rest' : '00001100{s}{reg2}{reg1}'},
				'dword[reg+reg*s],reg' : { 'op' : '09' , 'rest' : '00{reg3}100{s}{reg2}{reg1}'},
				'reg,dword[reg+reg*s]' : { 'op' : '0B' , 'rest' : '00{reg1}100{s}{reg3}{reg2}'},


				'reg,dword[reg+disp]' : {'op' : '0B' , 'rest' : {'127' : '01{reg1}{reg2}' , '128' : '10{reg1}{reg2}'}},
				'dword[reg+disp],reg' : {'op' : '09' , 'rest' : {'127' : '01{reg2}{reg1}' , '128' : '10{reg2}{reg1}'}}
			},

	'xor' : {
				'reg,reg' : {'op': '31', 'rest' : '11{reg2}{reg1}' },
				'dword[reg],reg' : { 'op' : '31', 'rest' : '00{reg2}{reg1}'},
				'reg,dword[reg]' : { 'op' : '33', 'rest' : '00{reg1}{reg2}'},
				
				'reg,dword[var]' : {'op': '33', 'rest' : '11{reg1}101' },
				'dword[var],reg' : {'op': '31', 'rest' : '11{reg1}101' },
				'dword[var],var' :{ 'op' : '81' , 'rest' : '00110101'},
				'dword[var],imm' :{ 'op' : {'127' : '83', '128' : '81' } , 'rest' : '00110101'},
				
				'dword[reg],imm' : { 'op' : {'127' : '83', '128' : '81'}, 'rest' : {'127' : '00110{reg1}' ,'128' : '00110{reg1}'}},
				'reg,imm' : {'op': {'127' : '83', '128' : '81'},'rest' : { '127' : '11110{reg1}', '128' : '11110{reg1}'} },

				'dword[reg+reg*s],imm' : { 'op' : { '127' : '83' , '128' : '81' } , 'rest' : '00110100{s}{reg2}{reg1}'},
				'dword[reg+reg*s],reg' : { 'op' : '31' , 'rest' : '00{reg3}100{s}{reg2}{reg1}'},
				'reg,dword[reg+reg*s]' : { 'op' : '33' , 'rest' : '00{reg1}100{s}{reg3}{reg2}'},
	

				'reg,dword[reg+disp]' : {'op' : '33' , 'rest' : {'127' : '01{reg1}{reg2}' , '128' : '10{reg1}{reg2}'}},
				'dword[reg+disp],reg' : {'op' : '31' , 'rest' : {'127' : '01{reg2}{reg1}' , '128' : '10{reg2}{reg1}'}}
				},

	'inc' : {
				'reg' : '0x40', 
				'dword[reg]' : {'op' : 'FF' , 'rest' : '00000{reg1}'},
				'dword[var]' : {'op' : 'FF' , 'rest' : '00000101'},
				'dword[reg+disp]' : {'op' : 'FF' , 'rest' : {'127' : '01000{reg1}' , '128' : '10000{reg1}'}},
				'dword[var+disp]' : {'op' : 'FF' , 'rest' : {'127' : '00000101' , '128' : '00000101'}},
				'dword[reg+reg*s]' : {'op' : 'FF' , 'rest' : '00000100{s}{reg2}{reg1}'}

			},

	'dec' : {
				'reg' : '0x48' , 
				'dword[reg]' : {'op' : 'FF' , 'rest' : '00001{reg1}'},
				'dword[var]' : {'op' : 'FF' , 'rest' : '00000101'},
				'dword[reg+disp]' : {'op' : 'FF' , 'rest' : {'127' : '01001{reg1}' , '128' : '10001{reg1}'}},
				'dword[var+disp]' : {'op' : 'FF' , 'rest' : {'127' : '00001101' , '128' : '00001101'}},
				'dword[reg+reg*s]' : {'op' : 'FF' , 'rest' : '00001100{s}{reg2}{reg1}'}

			},

	'push' : {	'reg' : '0x50',
				'var' : {'op' : '68'},	
				'imm' : {'op' : {'127' : '6A' ,'128' : '68'} },
				'dword[reg]' : {'op' : 'FF' , 'rest' : '00110{reg1}'},
				'dword[var]' : {'op' : 'FF' , 'rest' : '00110101'},
				'dword[reg+disp]' : {'op' : 'FF' , 'rest' : {'127' : '01110{reg1}' , '128' : '10110{reg1}'}},
				'dword[var+disp]' : {'op' : 'FF' , 'rest' : {'127' : '00110101' , '128' : '00110101'}},
				'dword[reg+reg*s]' : {'op' : 'FF' , 'rest' : '00110100{s}{reg2}{reg1}'}

			},

	'pop' : {
				'reg' : '0x58',
				'dword[reg]' : {'op' : '8F' , 'rest' : '00000{reg1}'},
				'dword[var]' : {'op' : 'FF' , 'rest' : '00000101'},
				'dword[reg+disp]' : {'op' : '8F' , 'rest' : {'127' : '01000{reg1}' , '128' : '10000{reg1}'}},
				'dword[var+disp]' : {'op' : '8F' , 'rest' : {'127' : '00000101' , '128' : '00000101'}},
				'dword[reg+reg*s]' : {'op' : '8F' , 'rest' : '00000100{s}{reg2}{reg1}'}

			},
	'call' : {
				'reg' : '0xFFD0',
				'var' : {'op' : 'E8'},
				'imm' : {'op' : {'127' : 'E8' ,'128' : 'E8'} },
				'dword[reg]' : {'op' : 'FF' , 'rest' : '00010{reg1}'},
				'dword[var]' : {'op' : 'FF' , 'rest' : '00010101'},
				'dword[reg+disp]' : {'op' : 'FF' , 'rest' : {'127' : '01010{reg1}' , '128' : '10010{reg1}'}},
				'dword[var+disp]' : {'op' : 'FF' , 'rest' : {'127' : '00010101' , '128' : '00010101'}},
				'dword[reg+reg*s]' : {'op' : 'FF' , 'rest' : '00010100{s}{reg2}{reg1}'}
			},
	'mul' : {
				'reg' : {'op' : 'F7' , 'rest' : '11100{reg1}'},
				'dword[reg]' : {'op' : 'F7' , 'rest' : '00100{reg1}'},
				'dword[var]' : {'op' : 'F7' , 'rest' : '00100101'},
				'dword[reg+disp]' : {'op' : 'F7' , 'rest' : {'127' : '01100{reg1}' , '128' : '10100{reg1}'}},
				'dword[var+disp]' : {'op' : 'F7' , 'rest' : {'127' : '00100101' , '128' : '00100101'}},
				'dword[reg+reg*s]' : {'op' : 'F7' , 'rest' : '00100100{s}{reg2}{reg1}'}
			}

	}