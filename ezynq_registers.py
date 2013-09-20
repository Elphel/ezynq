#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# Registers/bit fields manipulation
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
__author__ = "Andrey Filippov"
__copyright__ = "Copyright 2013, Elphel, Inc."
__license__ = "GPL"
__version__ = "3.0+"
__maintainer__ = "Andrey Filippov"
__email__ = "andrey@elphel.com"
__status__ = "Development"
# new_sets.append((addr,data,mask,self.module_name,register_name,self.registers[register_name]))

def print_html_reg_header(html_file, title='',show_bit_fields=True, show_comments=True,filter_fields=True):
    if not html_file:
        return
    if title:
        html_file.write('<h2>'+title+'</h2>\n')
    html_file.write('<table border="1">\n')
    if show_bit_fields:
        html_file.write('<tr><th>Address/<br/>bit field</th><th>Register name/<br>Bit field name</th><th>R/W</th><th>Value</th><th>Previous<br/>Value</th><th>Default</th>\n')
    else:
        html_file.write('<tr><th>Address</th><th>Register name</th><th>R/W</th><th>Value</th><th>Default</th>\n')
    if show_comments:
        html_file.write('<th>Comments</th>')
    html_file.write('</tr>')
def print_html_reg_footer(html_file):
    if not html_file:
        return
    html_file.write('</table>\n')

def print_html_registers(html_file, reg_sets, from_index, show_bit_fields=True, show_comments=True,filter_fields=True,all_used_fields=False):
    def opt_hex(d):
        if d <10:
            return str(d)
        else:
            return hex(d)
    if not html_file:
        return

#            new_sets.append((addr,data,mask,self.module_name,register_name,self.registers[register_name]))
    current_reg_state={} #address: (data,mask)
    for index, (op,addr, data, mask, module_name, register_name, r_def) in enumerate (reg_sets):
#        if (op != 's'):
#            continue # TODO: add handling of test conditions later  
        
#        if addr==0xf8000100:
#            print 'index=',index,' addr=',hex(addr),' data=',hex(data),' mask=',hex(mask)
        if mask!=0:
            if (op == 's'):
                try:
                    dflt_data=r_def['DFLT']
                except:
                    dflt_data=0
                try:
                    rw=r_def['RW']
                except:
                    rw='RW'
                try:
                    old_data,old_mask=current_reg_state[addr]
                    if not all_used_fields:
                        old_mask=0
                    prev_sdata=opt_hex(old_data)
                except:
                    old_data=dflt_data
                    old_mask=0        
                    prev_sdata='-'
                new_data=((old_data ^ data) & mask) ^ old_data
                new_mask= old_mask | mask
                current_reg_state[addr]=(new_data,new_mask)
            else:
                new_data= data
                new_mask= mask
            
            if index<from_index: # just accumulate previous history of the register mask/values, no output
                continue

            html_file.write('<tr>\n')
            try:
                comments=r_def['COMMENTS']
            except:
                comments=''    

            if show_bit_fields:
                if op == 's':
                    html_file.write('  <th>0x%8x</th><th>%s.%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th>'%
                                         (addr, module_name,register_name,rw,   opt_hex(new_data), prev_sdata,    opt_hex(dflt_data)))
                elif op == '=':
                    html_file.write('  <th>0x%8x</th><th>%s.%s</th><th colspan="4">Wait for (reg & %s) == %s</th>'%
                                         (addr, module_name,register_name, opt_hex(mask), opt_hex(data)))
                elif op == '!':
                    html_file.write('  <th>0x%8x</th><th>%s.%s</th><th colspan="4">Wait for (reg & %s) != %s</th>'%
                                         (addr, module_name,register_name,  opt_hex(mask), opt_hex(data)))
                else:
                    raise Exception ('Invalid register operation: %s for register 0x%08x'%(op,addr))    
                if show_comments:
                    html_file.write('<th>%s</th>'%comments)
                html_file.write('\n</tr>\n')
                if 'FIELDS' in r_def:
                    #sort bit fields
                    for f_name in [pair[0] for pair in sorted([(nam,r_def['FIELDS'][nam]['r'][0]) for nam in r_def['FIELDS']], key = lambda rr: -rr[1])]:
                        field=r_def['FIELDS'][f_name]
                        try:
                            f_rw=('R','RW')[field['m']!='R']
                        except:
                            f_rw='RW'
                        f_mask=0
                        r=(min(field['r'][0],field['r'][1]),max(field['r'][0],field['r'][1]))
                        for i in range(r[0],r[1]+1):
                            f_mask|=(1<<i)
                        if (not filter_fields) or (f_mask & mask):
                            f_data=(new_data & f_mask) >> r[0]
                            if op == 's':
                                f_dflt=(dflt_data & f_mask) >> r[0]
                                f_prev=(old_data & f_mask) >> r[0]
                                field_prev=('-', opt_hex(f_prev))[prev_sdata!='-']
                                modified=f_data != f_prev
                                html_file.write('  <tr><td>%i:%i</td><td>%s</td><td>%s</td><td>%s%s%s</td><td>%s</td><td>%s</td>'%
                                                        (r[0],r[1],   f_name,     f_rw,('','<b>')[modified],opt_hex(f_data),('','</b>')[modified],field_prev,opt_hex(f_dflt)))
                            elif op == '=':
                                html_file.write('  <tr><td>%i:%i</td><td>%s</td><td colspan="4">Wait for bit(s) == %s</th>'%
                                                        (r[0],r[1],  f_name,                                   opt_hex(f_data)))
                            elif op == '!':
                                html_file.write('  <tr><td>%i:%i</td><td>%s</td><td colspan="4">Wait for bit(s) != %s</th>'%
                                                        (r[0],r[1],  f_name,                                   opt_hex(f_data)))
    
                            else:
                                raise Exception ('Invalid register operation: %s for register 0x%08x'%(op,addr))    
                            
                            if show_comments:
                                try:
                                    f_comments=field['c']
                                except:
                                    f_comments=''    
                                html_file.write('<td>%s</td>'%f_comments)
                            html_file.write('\n</tr>\n')
            else:
                if op == 's':
                    html_file.write('  <th>0x%8x</th><td>%s.%s</td><td>%s</td><td><b>%s</b></td><td>%s</td><td>%s</td>'%
                                         (addr, module_name,register_name,rw,opt_hex(new_data),    prev_sdata, opt_hex(dflt_data)))
                elif op == '=':
                    html_file.write('  <th>0x%8x</th><td>%s.%s</td><tdcolspan="4"><b>Wait for (reg & %s) == %s</b></td>'%
                                          (addr, module_name,register_name,opt_hex(mask),opt_hex(data)))
                elif op == '!':
                    html_file.write('  <th>0x%8x</th><td>%s.%s</td><tdcolspan="4"><b>Wait for (reg & %s) != %s</b></td>'%
                                          (addr, module_name,register_name,opt_hex(mask),opt_hex(data)))
                else:
                    raise Exception ('Invalid register operation: %s for register 0x%08x'%(op,addr))    
                if show_comments:
                    html_file.write('<td>%s</td>'%comments)
                html_file.write('\n</tr>\n')


def accumulate_reg_data(reg_sets,accumulate_mask=False):
    initial_state={}
    cumulative_regs=[() for _ in reg_sets]
    for index, (op, addr, data, mask, module_name, register_name, r_def) in enumerate (reg_sets):
        if (op == 's') and (addr in initial_state): # only accumulate register set operations, not wait for equal ('=') or wait for not-equal ('!')
            old_data,old_mask=initial_state[addr]
            data=((old_data ^ data) & mask) ^ old_data
            if accumulate_mask:
                mask |= old_mask
        initial_state[addr]=(data,mask)
        cumulative_regs[index]=(op, addr, data, mask, module_name, register_name, r_def)
    return cumulative_regs     
        
   
 

class EzynqRegisters:
    ERRORS={
            'ERR_REG':   'Register name is not defined',
            'ERR_FIELD': 'Bit field is not defined',
            'ERR_RO':    'Trying to overwrite read only register/ bit field',
            'ERR_BITS':  'Data exceeds the available bits',
            'ERR_NOTSET':'Register is not set',
            }
    def _mask(self,bits):
        mask=0
        for i in range (min(bits),max(bits)+1):
            mask |= 1<<i
        return mask    
    def _data(self,bits,data,warn=False):
        mask=self._mask(bits)
        smask=mask>>min(bits)
        if (data  & ~smask)!=0 :
            msg ='Data '+hex(data)+' does not fit info the bit field '+str(bits)
            if warn:
                print 'WARNING: '+msg
            else:
                raise Exception (self.ERRORS['ERR_BITS']+' '+msg)
        return ((data & smask) << min(bits),mask)
    def _final_data_mask(self,register_name):
        if not register_name in self.defs:
            raise Exception (self.ERRORS['ERR_REG']+' '+register_name)
        addr=self.base_addr+self.defs[register_name]['OFFS']
        try:
            data,mask=self.registers[register_name] # already in the list of registers?
        except:
            raise Exception (self.ERRORS['ERR_REG']+' '+register_name+" is not set in this series")
        try:
            old_data,old_mask=self.initial_state[addr] 
        except:
            old_data=data
            old_mask=0
        data = ((old_data ^ data) & mask) ^old_data
        mask |= old_mask        
        return (data,mask) 
        
        
    def set_initial_state(self,added_reg_sets, init=True):
        if init:
            self.initial_state={}
            self.previous_reg_sets=[]
            try:
                self.initial_register_count=len(added_reg_sets)
            except:
                self.initial_register_count=0    
        if not added_reg_sets:
            return
        self.previous_reg_sets+=added_reg_sets # appends, not overwrites
        for op,addr,data,mask,_,_,_ in added_reg_sets: # Do not need to care about default values - they will have 0 in the mask bits.
            if (op == 's') and (addr in self.initial_state):
#                old_data,old_mask=self.initial_state[addr]
                old_data,_=self.initial_state[addr]
                data=((old_data ^ data) & mask) ^ old_data
#                mask |= old_mask
#            self.initial_state[addr]=(data,mask)
            self.initial_state[addr]=(data,0) # ignoring old mask - only accumulating newly set bits in this set
            
    def get_reg_names(self):
        return [n[0] for n in sorted([(name,self.defs[name]['OFFS']) for name in self.registers], key = lambda l: l[1])]
    
    def get_register_comments(self,register_name):
        try:
            return self.defs[register_name]['COMMENTS']
        except:
            return ''
            
    def get_bitfield_address_mask_comments(self,register_name,field_name): #channel is implied in self
        try:
            bit_field=self.defs[register_name]['FIELDS'][field_name]
        except:    
            raise Exception (self.ERRORS['ERR_FIELD']+' '+register_name+'.'+field_name)
        mask=self._mask(bit_field['r'])
        try:
            comments=bit_field['c']
        except:
            comments=''    
        addr=self.base_addr+self.defs[register_name]['OFFS']
        return (addr,mask,comments)
                
    #number of registers set before this module (can be removed from the result of get_register_sets(sort_addr=True,apply_new=True))      
    def get_initial_count(self):
        return self.initial_register_count
    
    def flush(self):
        _= self.get_register_sets(sort_addr=True,apply_new=True)
            
    def get_register_sets(self, sort_addr=True,apply_new=True):
        new_sets=[]
#        for register_name in self.registers:
#        print self.get_reg_names()
        for register_name in self.get_reg_names(): # sorted by increasing offsets
            addr=self.base_addr+self.defs[register_name]['OFFS']
            _,mask=self.registers[register_name] #  added (new only) mask, new data
            if mask == 0:
                continue # no bits set
            data,_= self._final_data_mask(register_name) # combined data
            op='s' # register set
            new_sets.append((op,addr,data,mask,self.module_name,register_name,self.defs[register_name]))
        if apply_new:
            self.set_initial_state(new_sets, False)
            self.registers={} # delete the applied registers
            return self.previous_reg_sets # all register sets - previous with new attached
        else:
            return new_sets # only new register sets, does not change state   
     
    def __init__(self,defines,channel=0,current_reg_sets=[],permit_undefined_bits=False):
        self.set_initial_state(current_reg_sets,True) # 'replay' previous register settings to the initial register state (et
        self.defs=defines
        self.base_addr=self.defs['BASE_ADDR'][channel]
        self.module_name=self.defs['MODULE_NAME'][channel]
        self.registers={} # now for name it will hold (address, data, mask) tuples
        # calculate R/W masks
        self.ro_masks={}
        for reg_name in self.defs:
            reg=self.defs[reg_name]
            if ('RW' in reg) and permit_undefined_bits:
                if 'W' in reg['RW']:
                    self.ro_masks[reg_name]=0 # all enabled
                    break;
                elif 'R' in  reg['RW']: # R, but no W - read only
                    self.ro_masks[reg_name]=0xFFFFFFFF # all read only
                    break;
            else:
                # some bits are writable, some - readonly
                ro_mask=0
                wr_mask=0
                try:
                    fields=reg['FIELDS']
                except:
                    continue
                for field_name in fields:
                    field=fields[field_name]
#                    print field_name,field
                    m= self._mask(field['r'])
                    if ('m' in field) and (field['m']=='R'):
                        ro_mask |= m
                    else:
                        wr_mask |= m
                self.ro_masks[reg_name]=((~wr_mask) & 0xFFFFFFFF, ro_mask)[permit_undefined_bits != 0]
        # Combine bit field defaults into register default?                        
                     
    def set_word(self,register_name,data,force=False):
        if not register_name in self.defs:
            raise Exception (self.ERRORS['ERR_REG']+' '+register_name) 
        # see if that register at this address was previously set
        default_mask=(self.ro_masks[register_name] ^ 0xffffffff) & 0xffffffff # write enabled bits in the register
        #no need to look at self.initial_state - it will be combined later. When handling never-defined-fields will use data from the first use of the address 
        try:
            old_data=self.defs[register_name]['DFLT']
        except:
            old_data=0 # DFLT not defined 
        diff = (data ^ old_data) & self.ro_masks[register_name]
        if diff:
            msg= register_name+" readonly mask="+hex(self.ro_masks[register_name])+" previous data="+hex(old_data)+" new data = "+data+" force="+force
            if  force:
                print 'WARNING: '+msg
            else:    
                raise Exception (self.ERRORS['ERR_RO'] + " " + msg)
        data= ((data ^ old_data) & default_mask) ^ old_data   
        #assuming that writing words overwrites all defined bitfields
        self.registers[register_name]=(data,default_mask) # that does not include old mask, will have to be combined for the next state of the registers
        
    def _combine_bitfields(self,register_name,field_data, warn=False):
        if not register_name in self.defs:
            raise Exception (self.ERRORS['ERR_REG']+' '+register_name) 
        if (len(field_data)==2) and not isinstance(field_data[1],tuple):
            field_data=(field_data,)
        data=0
        mask=0    
        for f_name,f_data in field_data:
            try:
                field=self.defs[register_name]['FIELDS'][f_name]
            except:
                print self.defs[register_name]
                raise Exception (self.ERRORS['ERR_FIELD']+': '+register_name+'.'+f_name) 
            shifted_data,shifted_mask=self._data(field['r'],f_data,warn)
            mask |= shifted_mask
            data ^= (data ^ shifted_data) & shifted_data
        return (data,mask)    

    def wait_reg_value(self,register_name, data, mask, equals):
        if not register_name in self.defs:
            raise Exception (self.ERRORS['ERR_REG']+' '+register_name) 
        addr=self.base_addr+self.defs[register_name]['OFFS']
        op=('!','=')[equals]
        new_entry=(op, addr, data, mask, self.module_name, register_name, self.defs[register_name])
        self.flush() # so self.previous_reg_sets have no all registers set so far
        self.previous_reg_sets.append(new_entry)

    def wait_reg_field_values(self,register_name,field_data, equals, warn=False):
        data,mask=self._combine_bitfields(register_name,field_data, warn)
        self.wait_reg_value(register_name,data,mask, equals) 

    def unset_word(self,register):
        if not register in self.defs:
            raise Exception (self.ERRORS['ERR_REG'])
        try:
            del self.registers[register] 
        except:
            pass # OK if it did not exist
            
# force - force readonly/undefined, warn - if data does n ot fit into the bit field
    def set_bitfield(self,register_name,field_name,data,force=False,warn=False):
        if not register_name in self.defs:
            print 'register_name=',register_name
            print 'self.defs=',self.defs
            raise Exception (self.ERRORS['ERR_REG']+' '+register_name) 
        try:
            old_data,old_mask=self.registers[register_name] # already in the list of registers?
        except:
            try:
                old_data=self.defs[register_name]['DFLT'] # default provided?
            except:
                old_data=0 # DFLT not defined, use 0
            old_mask=0    
        try:
            field=self.defs[register_name]['FIELDS'][field_name]
        except:
            print self.defs[register_name]
            raise Exception (self.ERRORS['ERR_FIELD']+': '+register_name+'.'+field_name) 
        new_data,new_mask=self._data(field['r'],data,warn)
        combined_data= ((new_data ^ old_data) & new_mask) ^ old_data # new data applied to old data
        combined_mask=old_mask | new_mask
        diff = (combined_data ^ old_data) & self.ro_masks[register_name]
        if diff:
            msg= register_name+" readonly mask="+hex(self.ro_masks[register_name])+" old data="+hex(old_data)+" new data = "+combined_data+" force="+force
            if  force:
                print 'WARNING: '+msg
            else:    
                raise Exception (self.ERRORS['ERR_RO'] + " " + msg)   
        self.registers[register_name]=(combined_data,combined_mask)
        
    def set_bitfields(self,register_name,field_data,force=False,warn=False):
        if (len(field_data)==2) and not isinstance(field_data[1],tuple):
            field_data=(field_data,)
#        print field_data
        for field_name,data in field_data:
            self.set_bitfield(register_name,field_name,data,force,warn)
    # combine multiple bit-fields into (data, mask) pair 


    def unset_bitfield(self,register_name,field_name):
        if not register_name in self.defs:
            raise Exception (self.ERRORS['ERR_REG']+' '+register_name) 
        try:
            old_data,old_mask=self.registers[register_name] # already in the list of registers?
        except:
            return # register is not set    
        try:
            dflt_data=self.defs[register_name]['DFLT'] # default provided?
        except:
            dflt_data=0 # DFLT not defined, use 0
        #new data and mask
        try:
            field=self.defs[register_name]['FIELDS'][field_name]
        except:
            raise Exception (self.ERRORS['ERR_FIELD']+': '+register_name+'.'+field_name) 
        mask=    self._mask(field['r'])
        combined_data= ((dflt_data ^ old_data) & mask) ^ old_data # new data applied to old data
        combined_mask=old_mask & (~mask)
        self.registers[register_name]=(combined_data,combined_mask) # no need to verify readonly - restoring defaults
    

    def _get_register_address_data_mask_default_previous(self,register_name,from_defines=False):
        if not register_name in self.defs:
            raise Exception (self.ERRORS['ERR_REG']+' '+register_name)
        def_reg= self.defs[register_name]
        address=self.base_addr+def_reg['OFFS']
        try:
            dflt_data=self.defs[register_name]['DFLT']
        except:    
            dflt_data=0 #default is not defined for the register
        data=dflt_data
        mask=(self.ro_masks[register_name] ^ 0xffffffff) & 0xffffffff # write enabled bits in the register

        try:
            prev_data,_=self.initial_state[address]
        except:
            prev_data=-1 # never set before    
        #self.initial_state[addr]=(data,mask)

        if not from_defines:
            try:
                _,mask=self.registers[register_name] # keep only this mask fro the register
                data,_=self._final_data_mask(register_name) # return final data, combining mew settings with the previous
            except:
                raise Exception (self.ERRORS['ERR_NOTSET'] + " " + register_name)
        return (address,data,mask,dflt_data,prev_data)

    def get_address_data_pairs_list(self):
        return[{'ADDRESS':self.base_addr+self.defs[name]['OFFS']} for name in self.get_reg_names()]

    def get_register_details(self,register_name,from_defines=False,filter_fields=True):
#        print '===register_name=',register_name
        address, data, mask, dflt_data, prev_data = self._get_register_address_data_mask_default_previous(register_name,from_defines)
        details={'NAME':register_name,'ADDRESS':address,'DATA':data}
        def_reg= self.defs[register_name]
        for key in def_reg:
            if key=='FIELDS':
                pass
            else:
                details[key]=def_reg[key]
        # fill in needed fields if they were missing
                
        if not 'DFLT' in details:
            details['DFLT']=dflt_data
        if not 'RW' in details:
            details['RW']='RW'
        if not 'COMMENTS' in details:
            details['COMMENTS']=''
        details['PREVIOUS']=prev_data #negative - not previously set    
        field_details=[]
        for field_name in def_reg['FIELDS']:
#            print '+++++ field_name=',field_name
#            print ' details=',details
            field=self.get_bitfield_details(register_name,field_name,from_defines)
            field_mask=self._mask(field['r'])
            if (not filter_fields) or (field_mask & mask):
                field_details.append(field)
#        print '+++++ field_details=',field_details
        details['FIELDS']=sorted(field_details, key = lambda rr: -rr['r'][0]) # from MSB to LSB
        return details    
        

    def get_bitfield_details(self,register_name,field_name,from_defines=False):
#        _, data, dflt_data = self._get_register_address_data_default(register_name,from_defines)
#        address, data, mask, dflt_data, prev_data = self._get_register_address_data_mask_default_previous(register_name,from_defines)
        _, data, _, dflt_data, prev_data = self._get_register_address_data_mask_default_previous(register_name,from_defines)

        if not field_name in self.defs[register_name]['FIELDS']:
            raise Exception (self.ERRORS['ERR_FIELD']+' '+register_name+'.'+field_name)
        bit_field=self.defs[register_name]['FIELDS'][field_name]
        mask=self._mask(bit_field['r'])
        field_data=(data & mask) >> min(bit_field['r'])
        field_dflt=(dflt_data & mask) >> min(bit_field['r'])
        field_prev=((prev_data & mask) >> min(bit_field['r']) & mask) >> min(bit_field['r'])
        field_details={'NAME':field_name,'DATA':field_data,'PREV':field_prev}
        for key in bit_field:
            field_details[key]=bit_field[key]
        field_details['d']=field_dflt
        try:
            field_details['m'] = bit_field['m']
        except:
            field_details['m'] = 'RW'    
        if not 'c' in field_details:
            field_details['c']=''
        return field_details 
        
    def print_html_register(self, register_name, html_file, show_bit_fields=True, show_comments=True,filter_fields=True):
        r=self.get_register_details(register_name,False,filter_fields)
        html_file.write('<tr>\n')
        prev_data_exists=r['PREVIOUS']>=0
        prev_data = ('-', hex(r['PREVIOUS']))[prev_data_exists]
        if show_bit_fields:
            html_file.write('  <th>'+hex(r['ADDRESS'])+'</th><th>'+r['NAME']+'</th><th>'+r['RW']+'</th><th>'+hex(r['DATA'])+'</th><th>'+prev_data+'</th><th>'+hex(r['DFLT'])+'</th>')
            if show_comments:
                html_file.write('<th>'+(r['COMMENTS'])+'</th>')
            html_file.write('\n</tr>\n')
            for field in r['FIELDS']:
                field_prev=('-', hex(field['PREV']))[prev_data_exists]
                html_file.write('  <tr><td>'+str(field['r'][0])+":"+str(field['r'][1])+'</td><td>'+field['NAME']+'</td><td>'+field['m']+'</td>')
                html_file.write('<td>'+hex(field['DATA'])+'</td><td>'+field_prev+'</td><td>'+hex(field['d'])+'</td>')
                if show_comments:
                    html_file.write('<td>'+(field['c'])+'</td>')
                html_file.write('\n</tr>\n')
        else:
            html_file.write('  <th>'+hex(r['ADDRESS'])+'</th><td>'+r['NAME']+'</td><td>'+r['RW']+'</td><td><b>'+hex(r['DATA'])+'</th><th>'+prev_data+'</b></td><td>'+hex(r['DFLT'])+'</td>')
            if show_comments:
                html_file.write('<td>'+r['COMMENTS']+'</td>')
            html_file.write('\n</tr>\n')
        
    def print_html_registers(self, html_file, show_bit_fields=True, show_comments=True,filter_fields=True):
        html_file.write('<table border="1">\n')
        if show_bit_fields:
            html_file.write('<tr><th>Address/<br/>bit field</th><th>Register name/<br>Bit field name</th><th>R/W</th><th>Value</th><th>Previous<br/>Value</th><th>Default</th>\n')
            if show_comments:
                html_file.write('<th>Comments</th>')
            html_file.write('</tr>')
        else:
            html_file.write('<tr><th>Address</th><th>Register name</th><th>R/W</th><th>Value</th><th>Default</th>\n')
            if show_comments:
                html_file.write('<th>Comments</th>')
            html_file.write('</tr>')

        for register in self.get_reg_names():
            self.print_html_register(register[0], html_file, show_bit_fields, show_comments,filter_fields)
        html_file.write('</table>\n')
     
        
    #QULAIFIER_CHAR
    #prefix like CONFIG_EZYNQ_DDR_SET_
    #postfix like '_PRE','_POST' or ''
    #qualifier_char '__'
    #value may be hex/decimal or "FREE" (value convert to upper)
     
    def parse_options_set(self,raw_configs,prefix,postfix,postfixes,qualifier_char,force=True,warn=True): #force - readonly/undefined fields, warn: data does not fit in the bit field
        raw_regs={}
        for line in raw_configs:
            reg =   line['KEY']
            value = line['VALUE']
            value=str(value).upper()
            if (reg[:len(prefix) ]== prefix) and (reg[len(reg)-len(postfix):] == postfix):
                #see if any other postfixes match
                for other_postfix in postfixes:
                    if (other_postfix!=postfix) and (len(other_postfix)> len(postfix)) and  (reg[len(reg)-len(other_postfix):] == other_postfix):
#                        print '== reg=',reg
#                        print '== postfix=',postfix
#                        print '== other_postfix=',other_postfix
                        break
                else: #no other postfixes match
                    reg=reg[len(prefix):len(reg)-len(postfix)]
#                    print '++++ reg=',reg

                    if qualifier_char in reg:
                        reg,field=reg.split(qualifier_char,1)
                    else:
                        field=''    
                    if not reg in self.defs:
                        raise Exception (self.ERRORS['ERR_REG']+' '+reg)
                    try:
                        value=int(value,0)
                    except:
                        value="FREE" # "Free" - anything but numeric/hex. Or do something else, parse more options?
                    if not reg in raw_regs:
                        raw_regs[reg] = {} 
                    if len(field)>0:
                        if not field in self.defs[reg]['FIELDS']:
                            raise Exception (self.ERRORS['ERR_FIELD']+': '+reg+'.'+field)
                        try:
                            raw_regs[reg]['FIELDS'][field]=value
                        except:
                            raw_regs[reg]['FIELDS']={field:value}     
                    else:     
                        raw_regs[reg]['VALUE']=value
        # apply raw_regs (should be done after normal parameters processed and some registers are populated
#        if len(raw_regs) >0:
#            print raw_regs
        for reg_name in raw_regs:
            reg=raw_regs[reg_name]
            if 'VALUE' in reg:
                if reg['VALUE'] == 'FREE':
                    self.unset_word(reg_name)
                else:
                    self.set_word(reg_name,reg['VALUE'],force)
            try:
                fields=raw_regs[reg_name]['FIELDS']
            except:
                continue        
            for field_name in fields:
                if fields[field_name] == 'FREE': #) or (reg_name in self.registers):
                    self.unset_bitfield(reg_name,field_name) # will do nothing if register is not there
                else:
                    self.set_bitfield(reg_name,field_name,fields[field_name],force,warn)        

     
    
    
    
    
    