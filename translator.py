import opcodes
from opcodes import op

class Node :
	def __init__(self,address=None,var=None,inst_code=None,instruction=None,profile = None,label = None) :
		
		self.profile = profile
		self.inst_code = inst_code
		self.var=var
		self.inst_code=inst_code
		self.instruction=instruction
		self.label = label
		self.next=None

class listing :

	def __init__(self) :
		self.head=None

	def insert(self,Node) :

		if self.head==None :
			self.head=Node

		else :
			ptr=self.head 
			while ptr.next != None :
				ptr=ptr.next

			ptr.next=Node

	def display(self) :
		global count
		if self.head==None :
			return

		ptr=self.head
		while ptr != None  :

			if self == bss_sec :
			 inst_code = '<resd ' + ptr.inst_code.upper() + '>' 

			else  :
				inst_code = ptr.inst_code.upper()

			print( count , ' '*(4-len(str(count))),ptr.address.upper() + ' '* (15-len(ptr.address)) + inst_code + ' '*(40-len(ptr.inst_code)) + ptr.instruction  + ' '*(40	-len(ptr.instruction)))
			count = count +1
			ptr=ptr.next
	

#=========================CLASS ENDS============================================

#UTILITIES
count = 1

#dictionary o, registers along with their number in modrm
registers = [("eax", "000"),("ecx", "001"), ("edx", "010"), ("ebx", "011"), ("esp", "100"), ("ebp", "101"), ("esi", "110"), ("edi", "111")]
scales = {'1':'00' , '2' : '01' , '4' : '10' , '8' : '11'}
jumping = {'jmp' : 'EB' , 'jz' : '74' , 'jnz' : '75'}

def get_addr_of_var (var) :

	ptr = data_sec.head
	while ptr != None :
		if ptr.var == var :
			return ptr.address
		ptr = ptr.next

	ptr = bss_sec.head
	while ptr != None :
		if ptr.var == var :
			return ptr.address
		ptr = ptr.next

	return ''

def get_var_disp_addr(value_set) :
	
	var_disp_addr = little_endian(get_addr_of_var(value_set['var'][0][0]))
	var_disp_addr = int('0x'+var_disp_addr,16)  + value_set['disp']
	var_disp_addr = hex(var_disp_addr)[2:].upper()

	var_disp_addr = '['  + little_endian ('0'*(8-len(var_disp_addr)) + var_disp_addr) + ']'

	return var_disp_addr	



def set_addr_dataText_sec(data_sec) :
	
	ptr = data_sec.head
	if ptr == None :
		return 

	addr = 0
	while ptr != None :
		hex_val = hex(addr)[2:]
		ptr.address = '0'* (8-len(hex_val)) + hex_val 
		addr = addr + (len(ptr.inst_code) - ptr.inst_code.count('[') - ptr.inst_code.count(']')) //2
		ptr = ptr.next

def set_addr_bss_sec(bss_sec) :
	
	ptr = bss_sec.head
	if ptr == None :
		return

	addr = 0
	while ptr != None :
		hex_val = hex(addr)[2:]
		ptr.address = '0'* (8-len(hex_val)) + hex_val 
		addr = addr + int('0x' + ptr.inst_code, 16) 
		ptr = ptr.next
	

def get_reg_from_list(s) :
	for reg in registers :
		if reg[0] == s   :
			return reg[1]

def little_endian(addr_bits) :
	separate_2bits_wise=[]
	for i in range(0,len(addr_bits),2) :
		separate_2bits_wise.insert(0,addr_bits[i:i+2])
	return ''.join(separate_2bits_wise)

def div_bin_hex(bin_str_8bit): #breaking 8bits into 4 and then calculating their hex counterpart
	return (hex(int(bin_str_8bit[0:4],2))[2:]+hex(int(bin_str_8bit[4:],2))[2:]).upper()

def get_imm_hex_val(value_set) :
	#to resolve immediate value being written in hex little endian format
	hex_val = hex(value_set['imm'])[2:]

	if value_set['inst'] != 'mov' :

		if value_set['imm'] > 127 :
			imm_conv = little_endian('0'*(8-len(hex_val)) + hex_val)		
		
		else :
			imm_conv = hex_val
	
	else :
			imm_conv = little_endian('0'*(8-len(hex_val)) + hex_val)

	return imm_conv

def get_disp_hex (value_set) :
	
	hex_val = hex(value_set['disp'])[2:]

	if value_set['disp'] > 127 :
		disp_conv = little_endian('0'*(8-len(hex_val)) + hex_val)		
	
	else :
		disp_conv = hex_val

	return disp_conv	

def get_imm_index_for_resolving(value_set) :
	# to resolve opcodes 
	if value_set['imm'] < 128 :
		imm = '127'

	else :
		imm = '128'

	return imm

def get_displacement_index(value_set) :
	if value_set['disp'] <128 :
		return '127'
	else :
		return '128'

def change_bits(string) :
	s = ''
	for c in string :
		if c == '0' :
			s = s+ '1'
		else :
			s = s+'0'

	return s

def get_label(text_sec,label_name,upto) :
	len_bytes = 0
	ptr = text_sec.head
	while ptr != upto :
		if ptr.label == ''.join(label_name) :

			temp_ptr = ptr
			while temp_ptr != upto :

				if '[' in temp_ptr.inst_code :
					len_bytes = len_bytes + len(temp_ptr.inst_code) - 2 * temp_ptr.inst_code.count('[')
				else :
					len_bytes = len_bytes + len(temp_ptr.inst_code) 
				
				temp_ptr = temp_ptr.next
			
			len_bytes = len_bytes//2 + 1
			len_bytes = bin(len_bytes)[2:]
			
			len_bytes  = '0'*(8-len(len_bytes)) + len_bytes
			len_bytes = change_bits (len_bytes)
			return div_bin_hex(len_bytes)
				
		ptr = ptr.next

def evaluate_jump_calls(text_sec) :

	ptr = text_sec.head 

	labels = []
	while ptr != None :
		for x in ['jmp','jz','jnz'] :
			if x  in ptr.instruction :
				label_name = ptr.instruction.split(' ')
				label_name = label_name[1:]
				addon = get_label(text_sec,label_name,ptr)
				ptr.inst_code  = ptr.inst_code + addon
		
		ptr = ptr.next 


def decode_inst(value_set) :
	
	var_addr = ''
	imm_conv = ''

	if value_set['imm'] != None :
		imm_conv = get_imm_hex_val(value_set)
		imm = get_imm_index_for_resolving(value_set)

	if value_set['disp'] is not None :
		disp = get_displacement_index(value_set)
		disp_conv = get_disp_hex(value_set)

	if len(value_set['var']) >= 1 :
		for i in range (value_set['var'][0][1]) :
			var_addr  = var_addr + '[' + little_endian(get_addr_of_var(value_set['var'][0][0])) + ']'

	if value_set['inst'] in ['mov' , 'add' , 'or' , 'sub' , 'cmp' ,'xor'] :
		if value_set['profile'] == 'reg,reg' or value_set['profile'] == 'dword[reg],reg' or value_set['profile'] == 'reg,dword[reg]' or value_set['profile'] == 'dword[var],var' or value_set['profile'] == 'dword[var],reg' or value_set['profile'] == 'reg,dword[var]':
			
			opcode=op[value_set['inst']][value_set['profile']]['op'] 

			if value_set['profile'] == 'dword[var],var' :
				binary = op[value_set['inst']][value_set['profile']]['rest']
			
			elif value_set['profile'] == 'dword[var],reg' or value_set['profile'] == 'reg,dword[var]' :
				if value_set['inst'] == 'mov' :
					if value_set['profile'] == 'reg,dword[var]' :
						binary = '10100001'
			
					else :
						binary = '10100011'
			
					opcode = ''

				else :
					binary = op[value_set['inst']][value_set['profile']]['rest'].format(reg1=get_reg_from_list(value_set['reg'][0]))
					
			else  :
				binary = op[value_set['inst']][value_set['profile']]['rest'].format(reg1=get_reg_from_list(value_set['reg'][0]), reg2=get_reg_from_list(value_set['reg'][1]) )

			inst_code = opcode+div_bin_hex(binary)  + var_addr
			text_sec.insert(Node(None,None,inst_code,value_set['full_inst'], value_set['profile'],value_set['label']))
			
		elif value_set['profile'] ==  'dword[reg],imm' or  value_set['profile'] ==  'reg,imm' or value_set['profile'] == 'dword[var],imm' :
		
			if value_set['inst'] == 'mov' and value_set['profile'] == 'reg,imm' or  value_set['profile'] == 'reg,var' :
				opcode_bin = hex(int('0xB8',16) + int(get_reg_from_list(value_set['reg'][0]) ,2 ) )
				inst_code = opcode_bin[2:].upper()  + var_addr + imm_conv
				text_sec.insert(Node(None,None,inst_code,value_set['full_inst'],value_set['profile'],value_set['label'] ))
		

			else :
				
				opcode = ''
				binary = ''

				if value_set['profile'] == 'reg,imm' and value_set['reg'][0] == 'eax' and imm == '128':
					opcode = ''
					binary = '00{op}101'.format (op = opbin[value_set['inst']])
				elif value_set['profile'] == 'reg,imm' and  imm == '128' :
					opcode = op[value_set['inst']][value_set['profile']]['op'][imm] 
					binary = op[value_set['inst']][value_set['profile']]['rest'][imm].format(reg1 = get_reg_from_list(value_set['reg'][0])) 
				
				elif  value_set['profile'] == 'dword[var],imm' :
					opcode = op[value_set['inst']][value_set['profile']]['op'][imm] 
					binary = op[value_set['inst']][value_set['profile']]['rest']	 

				else :
					opcode = op[value_set['inst']][value_set['profile']]['op'][imm] 
					binary = op[value_set['inst']][value_set['profile']]['rest'][imm].format(
										reg1=get_reg_from_list(value_set['reg'][0]))

				inst_code = opcode + div_bin_hex(binary) + var_addr + imm_conv
				text_sec.insert(Node(None,None,inst_code,value_set['full_inst'] , value_set['profile'] ,value_set['label']))
				
		
		elif value_set['profile'] == 'dword[reg+reg*s],imm' or value_set['profile'] == 'dword[reg+reg*s],reg' or value_set['profile'] == 'reg,dword[reg+reg*s]' :

			#to resolve immediate value being written in hex little endian format
			
			if value_set['imm'] != None:
				hex_val = hex(value_set['imm'])[2:]
				if  value_set['inst'] != 'mov' :

					if value_set['imm'] > 127 :
						imm_conv = little_endian('0'*(8-len(hex_val)) + hex_val)		
					
					else :
						imm_conv = hex_val
				
				else :
					imm_conv = little_endian('0'*(8-len(hex_val)) + hex_val)


			if  value_set['imm'] == None :
				opcode = op[value_set['inst']][value_set['profile']]['op']
			else :
				if value_set['imm'] < 128:
					imm = '127'
				else:
					imm = '128'
				opcode = op[value_set['inst']][value_set['profile']]['op'][imm]


			if len(value_set['reg']) > 2  :
				binary = op[value_set['inst']][value_set['profile']]['rest'].format(
					reg1=get_reg_from_list(value_set['reg'][0]) , reg2=get_reg_from_list(value_set['reg'][1]),
					reg3=get_reg_from_list(value_set['reg'][2]) , s = scales[value_set['scale']] )
			
			else :
				binary = op[value_set['inst']][value_set['profile']]['rest'].format(
					reg1=get_reg_from_list(value_set['reg'][0]), reg2=get_reg_from_list(value_set['reg'][1]),
					s = scales[value_set['scale']] )

			inst_code = opcode + div_bin_hex(binary[:8]) + div_bin_hex(binary[8:]) + var_addr + imm_conv
			text_sec.insert(Node(None,None,inst_code,value_set['full_inst'] , value_set['profile'],value_set['label'] ))

		elif value_set['profile'] == 'reg,var' :

			if value_set['inst'] == 'mov' :
				opcode_bin = hex(int('0xB8',16) + int(get_reg_from_list(value_set['reg'][0]) ,2 ) )
				inst_code = opcode_bin[2:].upper()  + var_addr
				text_sec.insert(Node(None,None,inst_code,value_set['full_inst'],value_set['profile'] ,value_set['label']))
			
			else :
				if value_set['reg'][0] == 'eax' :
					inst_code = div_bin_hex('00{op}101'.format(op = opbin[value_set['inst']]))  + var_addr
				else :
					inst_code = '81' + div_bin_hex('11{op}{reg}'.format(op = opbin[value_set['inst']] , reg = get_reg_from_list(value_set['reg'][0]))) + var_addr

				text_sec.insert(Node(None,None,inst_code,value_set['full_inst'],value_set['profile'],value_set['label'] ))

		elif value_set['profile'] == 'reg,dword[reg+disp]' or value_set['profile'] == 'dword[reg+disp],reg' :

			opcode = op[value_set['inst']][value_set['profile']]['op']
			binary = op[value_set['inst']][value_set['profile']]['rest'][disp].format(reg1 = get_reg_from_list( value_set['reg'][0]) ,reg2 = get_reg_from_list( value_set['reg'][1]))
			inst_code = opcode + div_bin_hex(binary) + disp_conv
			text_sec.insert(Node(None,None,inst_code,value_set['full_inst'],value_set['profile'] ,value_set['label']))

	elif value_set['inst'] in ['inc' ,'dec' ,'push', 'call', 'pop','mul'] :

		opcode = ''
		binary = ''
		inst_code = ''
		if value_set['profile'] == 'reg' :
			if value_set['inst'] == 'mul' :
				inst_code = 'F7' + div_bin_hex('11100{reg}'.format(reg = get_reg_from_list(value_set['reg'][0])))
			else :
				inst_code = hex(int(op[value_set['inst']][value_set['profile']],16) + int(get_reg_from_list(value_set['reg'][0]),2) )[2:].upper()

		else:
			opcode = op[value_set['inst']][value_set['profile']]['op']

			if value_set['profile'] == 'var' :
				inst_code = opcode + var_addr

			if value_set['profile'] == 'dword[var]'  :
				binary = op[value_set['inst']][value_set['profile']]['rest']
				inst_code = opcode + div_bin_hex(binary)	 + var_addr		

			if value_set['profile'] == 'dword[reg]' :
				binary = op[value_set['inst']][value_set['profile']]['rest'].format(reg1 = get_reg_from_list(value_set['reg'][0]))
				inst_code = opcode + div_bin_hex(binary)

			if value_set['profile'] == 'dword[reg+disp]' or value_set['profile'] == 'dword[var+disp]' :
				if value_set['profile'] == 'dword[var+disp]' :
					binary = op[value_set['inst']][value_set['profile']]['rest'][disp]
					inst_code = opcode + div_bin_hex(binary) + get_var_disp_addr(value_set)
				else :
					binary = op[value_set['inst']][value_set['profile']]['rest'][disp].format(reg1 = get_reg_from_list(value_set['reg'][0]))
					inst_code = opcode + div_bin_hex(binary) + disp_conv 
				
				
			if value_set['profile'] == 'dword[reg+reg*s]' :
				binary = op[value_set['inst']][value_set['profile']]['rest'].format(reg1 = get_reg_from_list(value_set['reg'][0]),reg2 = get_reg_from_list(value_set['reg'][1]),s =scales[value_set['scale']])
				inst_code = opcode + div_bin_hex(binary[:8]) +  div_bin_hex(binary[8:])

			if value_set['profile'] == 'imm' :
				if value_set['inst'] == 'call' :
					imm_conv = imm_conv + '0' * (8-len(imm_conv))
				inst_code = op[value_set['inst']][value_set['profile']]['op'][imm] + imm_conv

		text_sec.insert(Node(None,None,inst_code,value_set['full_inst'],value_set['profile'] ,value_set['label']))	
	
	elif value_set['inst'] in ['jmp' , 'jnz' , 'jz'] :
		inst_code = jumping[value_set['inst']]
		
		text_sec.insert(Node(None,None,inst_code,value_set['full_inst'],value_set['profile'] ,value_set['label']))	


def data_bss(line) :

	org_line=line # preserving the original instruction line
	store={'addr':None, 'var':None, 'inst_code':None ,'instruction':line,'size':None}

	# extracting name of the variable
	first_space_index=line.find(' ')
	#print('var = {var}'.format(var=line[:first_space_index]))
	var=line[:first_space_index]
	store['var']=var


	# extracting  datatype of the variable
	line=line[first_space_index+1:]
	second_space_index=line.find(' ')
	store['size']=line[:second_space_index].strip()

	line = line[second_space_index+1:]

	#FOR NON STRING LITERALS
	inst_code = ''
	if '"' not in line :
		array_of_values = line.split(',')
		#print(array_of_values)

		for value in array_of_values :

			# for BSS section literals
			if store['size'] in ['resb','resw','resd','resq'] : # no values separated by commas alowed  in bss section
				if len(array_of_values) >1 :
					print('byte data exceed bounds')
					exit(0)
				else :
					inst_code = hex( datatypes[store['size']]* int(value) )
					inst_code = inst_code[2:]
					inst_code = '0'*(8-len(inst_code)) + inst_code
					store['inst_code'] = inst_code
					bss_sec.insert(Node(None, store['var'], store['inst_code'], store['instruction'], None))
			
			else: # for data section literals	

				temp_inst_code=hex(int(value))
				temp_inst_code=temp_inst_code[2:]
				temp_inst_code= "0"*(datatypes[store['size']] *2 -len(temp_inst_code)) + temp_inst_code
				inst_code = inst_code + little_endian(temp_inst_code)
				inst_code = inst_code.upper()
				store['inst_code'] = inst_code	
				data_sec.insert(Node(None, store['var'], store['inst_code'], store['instruction'], None))
		
	
	# FOR STRING LITERALS
	else :

		array_of_values = line.split(',')
		raw_len = len(array_of_values[0])-2 + len(array_of_values[1:]) * datatypes[store['size']]

		extra_zeros = ''
		if raw_len % datatypes[store['size']] != 0 :
			extra_zeros = '00' * (datatypes[store['size']] - raw_len %  datatypes[store['size']] )

		string_literal = array_of_values[0][1: len( array_of_values[0]) -1 ]
		for char in string_literal :
			inst_code = inst_code + hex(ord(char))[2:]

		inst_code = inst_code + extra_zeros
		
		for value in array_of_values[1:] :
			after_string = hex(int(value))[2:]
			after_string = "0"*(datatypes[store['size']] *2 -len(after_string)) + after_string
			inst_code  = inst_code +  little_endian(after_string)
			inst_code = inst_code.upper()
		store['inst_code'] = inst_code

		data_sec.insert(Node(None, store['var'], store['inst_code'], store['instruction'], None))


	

#=========================================== TEXT SECTION ===================================================


def  handle_text_section(line):

	line=line.strip()
	
	value_set={'label':None,'imm':None,'reg':[],'var' :[],'inst':None, 'profile' : None, 'disp' : None , 'scale' : None,'full_inst' : line}
	


	instructions=['mov','add','sub','mul','xor','or','cmp','inc','dec','jnz','jmp','jz','push','call']
	org_line=line #line will go under change multiple time in this module, org_line will be used where ever original line 
	line=line.strip()							#would be required
	
	# we will replace all the registers in the instruction with 'reg' to step forward in matching indices from 'op' set
	start_index_of_reg = []
	dup_line = line
	i=0
	while i < len(registers)  :
		if registers[i][0] in line :
			reg_index = line.find(registers[i][0])
			start_index_of_reg.append(reg_index)
			line = line[:reg_index] + 'reg' + line[reg_index + 3:]
			i=0
		else :
			i+=1


	start_index_of_reg.sort()
	for reg_index in start_index_of_reg :
		value_set['reg'].append(dup_line[reg_index : reg_index+3])

	
	start_mem=line.find('[') #check if there is dword involves
	end_mem=line.find(']')   
	plus_index = line.find('+')  #check whether displacment or SIB involved

	if start_mem!=-1 :
		
		if plus_index!=-1:	
			
			#replacing immediate value with imm in the memory part '[reg + imm]'
			if 'reg' not in line[plus_index:end_mem+1] :
				value_set['disp'] = int(line[plus_index+1:end_mem]) 
				
				line=line[0:plus_index] + '+disp' + line[end_mem:]

			#replacing scale by 's'
			if '*' in line :
				index1=line.find('*')
				value_set['scale'] = line[index1+1 : end_mem]
				line=line[0:index1]+'*s'+line[end_mem:]

	
	# finding imm value 
	count=0
	
	#if last char of last word lies in range (48,58) then in must be an immediate value in original instruction  
	for i in range(len(line)-1 , 0 , -1):
		if line[i]==' ' or line[i] == ',' :
			if count>0  :
				value_set['imm'] = int(line[len(line)-count :  ]) 
				line = line[:len(line)-count] + 'imm'
				line=line.strip()
				break		

		elif ord(line[i]) in range (48,58):  
			count+=1
		else :
			break
	
	#checking if there exists a variable in bss or data section
	#if it exists then it would be defined variable and we will reolace the variable name with var
	#replacing if variable is in dword block
	ptr=data_sec.head
	if ptr !=None :
		while(ptr!=None) :

			if ptr.var in line :
				start_var = line.find(ptr.var)
				end_var = line.find(ptr.var) + len(ptr.var)-1

				if end_var == len(line)-1 :
					count = line.count(ptr.var)
					line=line.replace(ptr.var,'var')
					value_set['var'].append((ptr.var, count))
					break

				if ord(line[start_var-1]) not in range(48,58) and ord(line[start_var-1]) not in range(65,91) and ord(line[start_var-1]) not in range(97,123) :
					if ord(line[end_var+1]) not in range(48,58) and ord(line[end_var+1]) not in range(65,91) and ord(line[end_var+1]) not in range(97,123) :
						count = line.count(ptr.var)
						line=line.replace(ptr.var,'var')
						value_set['var'].append((ptr.var, count))
						#print('{var} count is'.format(var =  ptr.var) , count)
						break
			ptr=ptr.next
	
	ptr=bss_sec.head
	if ptr !=None :
		while(ptr!=None) :
			
			if ptr.var in line :
				start_var = line.find(ptr.var)
				end_var = line.find(ptr.var) + len(ptr.var)-1

				if end_var == len(line)-1 :
					count = line.count(ptr.var)
					line=line.replace(ptr.var,'var')
					value_set['var'].append((ptr.var, count))
					break
				
				if ord(line[start_var-1]) not in range(48,58) and ord(line[start_var-1]) not in range(65,91) and ord(line[start_var-1]) not in range(97,123) :
					if ord(line[end_var+1]) not in range(48,58) and ord(line[end_var+1]) not in range(65,91) and ord(line[end_var+1]) not in range(97,123) :
						count = line.count(ptr.var)
						line=line.replace(ptr.var,'var')
						value_set['var'].append((ptr.var, count))
						break
			ptr=ptr.next

	#find if instruction contains a label , ':' specifies tht instruction contains a label
	if ':' in line :
		index=line.find(':')
		value_set['label']=line[0:index]
		#print(value_set['label'])
		line=line[index+1:].strip()
	
	line = line.split(' ')
	value_set['inst'] = line[0].strip()
	#print(line,org_line,value_set['inst'],end='      ')

	line=line[1:]

	line=','.join(line)
	profile=line.strip()
	#print(profile)
	
	value_set['profile'] = profile
	return value_set


#=============================================================================================================
#Program starts  here

data_sec = listing()
bss_sec = listing()
text_sec = listing()

datatypes={'db':1,'dw':2,'dd':4,'dq':8,'resb':1,'resw':2,'resd':4,'resq':8}
opbin = {'add' : '000' , 'or' : '001',  'and' : '100','xor' : '110', 'sub' : '101' , 'cmp' : '111' , }
section=None

fp=open('input.asm')

#------------------------------------------------------------
# reading program line by line
flag = 0
for line in fp :
	line=line.strip()

	if '.' in line :
		index=line.find('.')
		section=line[index+1:]

	else :
		
		if (section == 'data' or section == 'bss') and len(line)!=0 : 
			data_bss(line)

		elif section == 'text':

			if flag == 0 :
				#set addresses of variables of bss and data section to be used in text section
				set_addr_dataText_sec(data_sec)
				set_addr_bss_sec(bss_sec)
				flag = 1

			value_set = handle_text_section(line)
			decode_inst(value_set)

evaluate_jump_calls(text_sec) 
set_addr_dataText_sec(text_sec)
print('                                                      section .data')
data_sec.display() 
print('                                                      section .bss')
bss_sec.display()  
print('                                                      section .text')
text_sec.display() 
