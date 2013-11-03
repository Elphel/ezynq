#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# Generation of the C source file for u-boot lowlevel init
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
import os
import ezynq_ddrc_defs
#import ezynq_clk
import ezynq_feature_config
#Use 'TYPE':'I' for decimal output, 'H' - for hex. On input both are accepted
UBOOT_CFG_DEFS=[
    {'NAME':'LOCK_SLCR',          'CONF_NAME':'CONFIG_EZYNQ_LOCK_SLCR','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':True,
                'DESCRIPTION':'Lock SLCR after boot'},              
    {'NAME':'BOOT_DEBUG',         'CONF_NAME':'CONFIG_EZYNQ_BOOT_DEBUG','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Enable debug features during boot'},              
    {'NAME':'LED_DEBUG',          'CONF_NAME':'CONFIG_EZYNQ_LED_DEBUG','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'Specify MIO pin to use for debug purposed during boot process'},
    {'NAME':'UART_DEBUG_USE_LED', 'CONF_NAME':'CONFIG_EZYNQ_UART_DEBUG_USE_LED','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Turn debug LED off/on while waiting for UART FIFO not full'},              
    {'NAME':'DUMP_SLCR_EARLY',    'CONF_NAME':'CONFIG_EZYNQ_DUMP_SLCR_EARLY','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump SLCR registers as soon as UART is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG)'},              
    {'NAME':'DUMP_DDRC_EARLY',    'CONF_NAME':'CONFIG_EZYNQ_DUMP_DDRC_EARLY','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump DDRC registers as soon as UART is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG)'},              
    {'NAME':'DUMP_SLCR_LATE',     'CONF_NAME':'CONFIG_EZYNQ_DUMP_SLCR_LATE','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump SLCR registers after DDR memory is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG)'},              
    {'NAME':'DUMP_DDRC_LATE',     'CONF_NAME':'CONFIG_EZYNQ_DUMP_DDRC_LATE','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump DDRC registers after DDR memory is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG)'},

    {'NAME':'DUMP_TRAINING_EARLY','CONF_NAME':'CONFIG_EZYNQ_DUMP_TRAINING_EARLY','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump Training results before DDRC initialization (depends on CONFIG_EZYNQ_BOOT_DEBUG)'},              
    {'NAME':'DUMP_TRAINING_LATE', 'CONF_NAME':'CONFIG_EZYNQ_DUMP_TRAINING_LATE','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':True,
                'DESCRIPTION':'Dump Training results after DDRC initialization (depends on CONFIG_EZYNQ_BOOT_DEBUG)'},              
                              
    {'NAME':'DUMP_OCM',           'CONF_NAME':'CONFIG_EZYNQ_DUMP_OCM','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump OCM memory range'},              
    {'NAME':'DUMP_DDR',           'CONF_NAME':'CONFIG_EZYNQ_DUMP_DDR','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump DDER memory range'},              

    {'NAME':'DUMP_OCM_LOW',       'CONF_NAME':'CONFIG_EZYNQ_DUMP_OCM_LOW','TYPE':'H','MANDATORY':False,'DERIVED':False,'DEFAULT':0,
                'DESCRIPTION':'Dump OCM memory range start address'},              
    {'NAME':'DUMP_OCM_HIGH',      'CONF_NAME':'CONFIG_EZYNQ_DUMP_OCM_HIGH','TYPE':'H','MANDATORY':False,'DERIVED':False,'DEFAULT':0x2ff,
                'DESCRIPTION':'Dump OCM memory range end address'},              
    {'NAME':'DUMP_DDR_LOW',       'CONF_NAME':'CONFIG_EZYNQ_DUMP_DDR_LOW','TYPE':'H','MANDATORY':False,'DERIVED':False,'DEFAULT':0x4000000,
                'DESCRIPTION':'Dump DDR memory range start address'},              
    {'NAME':'DUMP_DDR_HIGH',      'CONF_NAME':'CONFIG_EZYNQ_DUMP_DDR_HIGH','TYPE':'H','MANDATORY':False,'DERIVED':False,'DEFAULT':0x40002ff,
                'DESCRIPTION':'Dump DDR memory range end address'},              


    {'NAME':'LED_CHECKPOINT_1',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_1', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF in RBL (just after MIO is set up)'},              
    {'NAME':'LED_CHECKPOINT_2',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_2', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF first after getting to user code'},              
    {'NAME':'LED_CHECKPOINT_3',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_3', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF first after getting to user code'},              
    {'NAME':'LED_CHECKPOINT_4',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_4', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF after PLL bypass is OFF'},              
    {'NAME':'LED_CHECKPOINT_5',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_5', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF after UART is programmed'},              
    {'NAME':'LED_CHECKPOINT_6',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_6', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF after DCI is calibrated'},              
    {'NAME':'LED_CHECKPOINT_7',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_7', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF after DDR is initialized'},              
    {'NAME':'LED_CHECKPOINT_8',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_8', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF before relocation to DDR (to 0x4000000+ )'},              
    {'NAME':'LED_CHECKPOINT_9',    'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_9', 'TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF after  relocation to DDR (to 0x4000000+ )'},              
    {'NAME':'LED_CHECKPOINT_10',   'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_10','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF before remapping OCM0-OCM2 high'},              
    {'NAME':'LED_CHECKPOINT_11',   'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_11','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF after remapping OCM0-OCM2 high'},              
    {'NAME':'LED_CHECKPOINT_12',   'CONF_NAME':'CONFIG_EZYNQ_LED_CHECKPOINT_12','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'LED ON/OFF before leaving lowlevel_init()'},              
    {'NAME':'LAST_PRINT_DEBUG',   'CONF_NAME':'CONFIG_EZYNQ_LAST_PRINT_DEBUG','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':None,
                'DESCRIPTION':'Output to UART before exiting arch_cpu_init()'},              
]
# 
# CONFIG_EZYNQ_BOOT_DEBUG = y # configure UARTx and send register dumps there
# CONFIG_EZYNQ_LED_DEBUG = 47 # toggle LED during boot
# CONFIG_EZYNQ_UART_DEBUG_USE_LED = y # turn on/off LED while waiting for transmit FIFO not full
# 
# CONFIG_EZYNQ_DUMP_SLCR_EARLY = y # Dump SLCR registers as soon as UART is initilaized (depends on CONFIG_EZYNQ_BOOT_DEBUG)
# CONFIG_EZYNQ_DUMP_DDRC_EARLY = y # Dump DDRC registers as soon as UART is initilaized (depends on CONFIG_EZYNQ_BOOT_DEBUG)
# CONFIG_EZYNQ_DUMP_SLCR_LATE = y # Dump SLCR registers after DDR memory is initilaized (depends on CONFIG_EZYNQ_BOOT_DEBUG)
# CONFIG_EZYNQ_DUMP_DDRC_LATE = y # Dump DDRC registers after DDR memory is initilaized (depends on CONFIG_EZYNQ_BOOT_DEBUG)
# 
# #Turning LED on/off at different stages of the boot process. Requires CONFIG_EZYNQ_LED_DEBUG to be set
# #If defined, each can be 0,1, ON or OFF
# CONFIG_EZYNQ_LED_CHECKPOINT_1  = ON  # in RBL setup, as soon as MIO is programmed 
# CONFIG_EZYNQ_LED_CHECKPOINT_2  = OFF # First after getting to user code 
# CONFIG_EZYNQ_LED_CHECKPOINT_3  = OFF # After setting clock registers 
# CONFIG_EZYNQ_LED_CHECKPOINT_4  = ON  # After PLL bypass is OFF
# CONFIG_EZYNQ_LED_CHECKPOINT_5  = ON  # After UART is programmed
# CONFIG_EZYNQ_LED_CHECKPOINT_6  = OFF # After DCI is calibrated
# CONFIG_EZYNQ_LED_CHECKPOINT_7  = ON  # After DDR is initialized
# CONFIG_EZYNQ_LED_CHECKPOINT_8  = OFF # Before relocation to DDR (to 0x4000000+ )
# CONFIG_EZYNQ_LED_CHECKPOINT_9  = ON  # After  relocation to DDR (to 0x4000000+ )
# CONFIG_EZYNQ_LED_CHECKPOINT_10 = OFF # Before remapping OCM0-OCM2 high
# CONFIG_EZYNQ_LED_CHECKPOINT_11 = ON  # After remapping OCM0-OCM2 high
# CONFIG_EZYNQ_LED_CHECKPOINT_12 = OFF # Before leaving lowlevel_init()

class EzynqUBoot:
    license="""/*
 * This file is automatically generated by the Free Software program using open information from the
 * components datasheets, reference manuals and user data.
 * No license is required to distribute this file. User may select his/her own license to replace
 * this header text.
 */
 
"""
    # remove unneeded 
    include_section="""
#include <common.h>
#include <asm/io.h>
#include <asm/arch/sys_proto.h>
#include <asm/arch/hardware.h>

"""
    
    def __init__(self, raw_configs, verbosity):
        self.cfile=self.license + self.include_section
        self.verbosity=verbosity
        self.sections=['license','include']
        self.features=ezynq_feature_config.EzynqFeatures(UBOOT_CFG_DEFS)
        self.features.parse_features(raw_configs)
        self.features.check_missing_features()
# undefine all if debug is disabled
        if not self.features.get_par_value_or_none('BOOT_DEBUG'):
            for name in self.features.get_par_names():
                self.features.undefine_parameter(name)
        elif self.features.get_par_value_or_none('LED_DEBUG') is None:
            for name in self.features.get_par_names():
                if 'LED' in name:
                    self.features.undefine_parameter(name)
            
    def html_list_features(self,html_file):
        if not html_file:
            return
        html_file.write('<h2>Boot process debug features setup</h2>\n')
        self.features.html_list_features(html_file)
#       print self.features.get_par_names()
      
        
         
    def get_c_file(self):
        return self.cfile
    def _opt_hex(self,d):
        if d <10:
            return str(d)
        else:
            return hex(d)
   
    def _add_reg_writes(self,reg_sets):
        for op, addr, data, mask, module_name, register_name, r_def in reg_sets:
            try:
                comments=r_def['COMMENTS']
            except:
                comments=''
            if op == 's':    
                self.cfile+='\twritel(0x%08x, 0x%08x); /* %s.%s  %s */\n'%(data,addr,module_name,register_name,comments)
            elif op == '=':
                self.cfile+='\twhile((readl(0x%08x) & %s) != %s); /* %s.%s  %s */\n'%(addr,self._opt_hex(mask),self._opt_hex(data),module_name,register_name,comments)
            elif op == '!':
                self.cfile+='\twhile((readl(0x%08x) & %s) == %s); /* %s.%s  %s */\n'%(addr,self._opt_hex(mask),self._opt_hex(data),module_name,register_name,comments)
            else:
                raise Exception('Invalid register operation "%s" specified for register 0x%08x, data=0x%08x, mask=0x%08x'%(op,addr,data,mask))        
    def make_slcr_lock_unlock(self, reg_sets):
        self.sections.append('slcr_lock_unlock_setup')
        self.cfile+="""
/* Lock SLCR registers - may be called after everything is done. */        
inline void lock_slcr(void)
{
"""
        self._add_reg_writes(reg_sets[:1])        
        self.cfile+="""}
        
/* Unlock SLCR registers - SHOULD be called first before writing any SLCR registers. */        
inline void unlock_slcr(void)
{
"""
        self._add_reg_writes(reg_sets[1:])        
        self.cfile+='}\n'

    def make_led_on_off(self, reg_sets):
        self.sections.append('led_on_off')
        self.cfile+="""
/* Turn LED ON for debugging of the early stages of boot process. */        
inline void debug_led_on(void)
{
"""
        self._add_reg_writes([reg_sets[1]])
        self.cfile+="""}
        
/* Turn LED OFF for debugging of the early stages of boot process. */        
inline void debug_led_off(void)
{
"""
        self._add_reg_writes(reg_sets[:1])
        self.cfile+='}\n'
                
    def registers_setup(self, reg_sets,clk,num_rbl_regs): #clk is an instance of ezynq_clk.EzynqClk
        self.sections.append('registers_setup')
        self.cfile+="""
/*
   Setup registers after control is passed from the ROM boot loader to the user code.
   %i registers are already set up using RBL register initialization feature
 */        
inline void register_setup(void)
{
"""%num_rbl_regs
        self._add_reg_writes(reg_sets)        
        self.cfile+='}\n\n'

    def pll_setup (self, reg_sets):
        self.sections.append('pll_setup')
        self.cfile+='''/* Wait for PLLs locked */        
inline void pll_setup(void)
{
\t/* Wait for all used PLLs locked, then  release PLL bypass on each PLL */
'''
        self._add_reg_writes(reg_sets)            
        self.cfile+='}\n\n'

    def make_resets (self, reg_sets):
        self.sections.append('resets')
        self.cfile+='''/* Reset defined peripherals */        
inline void reset_peripherals(void)
{
'''
        self._add_reg_writes(reg_sets)            
        self.cfile+='}\n\n'

    def gpio_out (self, reg_sets):
        self.sections.append('gpio_out')
        self.cfile+='''/* Setup GPIO outputs */        
inline void setup_gpio_outputs(void)
{
'''
        self._add_reg_writes(reg_sets)            
        self.cfile+='}\n\n'

    def uart_init (self, reg_sets):
        self.sections.append('uart_init')
        self.cfile+='''/* Initilize UART to output debug info during boot */        
inline void uart_init(void)
{
\t/* Wait for all used PLLs locked, then  release PLL bypass on each PLL */
'''
        self._add_reg_writes(reg_sets)            
        self.cfile+='}\n\n'

#uart_transmit (should be called after LED control is set)
    def uart_transmit (self, reg_sets):
        use_led=self.features.get_par_value_or_none('UART_DEBUG_USE_LED')
        self.sections.append('uart_xmit')
#        op, addr, data, mask, module_name, register_name, r_def=reg_sets[2]
        _, addr, _, _, module_name, register_name, r_def=reg_sets[2]
        try:
            comments=r_def['COMMENTS']
        except:
            comments=''
        self.cfile+='''/* Wait FIFO is empty (call before getting to risky for reboot code
   to make sure all output has been actually sent  */        
inline void uart_wait_tx_fifo_empty(void)
{
'''
        self._add_reg_writes([reg_sets[0]])
        self.cfile+='''}

/* Wait FIFO is not full, send one character
   to make sure all output has been actually sent  */        
void uart_putc(int c)
{
'''
        if use_led:
            self.cfile+='\tdebug_led_off(); /* turn LED off */\n'
        self._add_reg_writes([reg_sets[1]]) # wait FIFO not full
        if use_led:
            self.cfile+='\tdebug_led_on(); /* turn LED on */\n'
        self.cfile+='\twritel(c, 0x%08x); /* %s.%s  %s */\n'%(addr,module_name,register_name,comments)
        self.cfile+='''}

void uart_puts(char * line){
\tint i=0;
\twhile (line[i]!=0) uart_putc(line[i++]);
}

inline void uart_put_hex_digit(int c)
{
\tuart_putc(c+ ((c>9)? ('a'-10):'0'));
}

void uart_put_hex(int d)
{
\tint i;
\tfor (i=28;i>=0;i-=4) uart_put_hex_digit((d>>i) & 0xf);
}

void uart_dump_regs(int addr_from, int addr_to, int num_per_line )
{
\tint a;
\taddr_from &= ~3;
\tint addr_display= (num_per_line * (((addr_from>>2) & 0x3fffffff)/num_per_line))<<2;
\tfor (a=addr_display; a<=addr_to; a+=4){
\t\tint r= (((a-addr_display)>>2) & 0x3fffffff) % num_per_line;
\t\tif (r==0) {
\t\t\tuart_put_hex(a);
\t\t\tuart_putc(':');
\t\t}
\t\tuart_putc(' ');
\t\tif (a<addr_from){
\t\t\tint j;
\t\t\tfor (j=0;j<8;j++) uart_putc('-');
\t\t} else {
\t\t\tuart_put_hex(readl(a));
\t\t}
\t\tif (r==(num_per_line-1)) {
\t\t\tuart_puts("\\r\\n");
\t\t}
\t}
\tuart_puts("\\r\\n");
}

'''

    def make_ddrc_register_dump(self):
        self.sections.append('ddrc_dump')
        self.cfile+='''/* Dump all DDR Controller registers that do not hang the system */        
void dump_ddrc_regs(void)
{
\tuart_puts("DDRC registers\\r\\n");

\tuart_dump_regs(0xf8006000,0xf800607c, 16); /* access to 0xf8006080 hangs */
\tuart_puts("\\r\\n");

\tuart_dump_regs(0xf80060a0, 0xf80060b8, 16);
\tuart_puts("\\r\\n");

\tuart_dump_regs(0xf80060c4, 0xf80060fc, 16);
\tuart_puts("\\r\\n");

\tuart_dump_regs(0xf8006114, 0xf8006194, 16); /* 0xf8006198 hangs */
\tuart_puts("\\r\\n");

\tuart_dump_regs(0xf80061a4, 0xf80061e8, 16); /* 0xf80061f0 hangs */
\tuart_puts("\\r\\n");

\tuart_dump_regs(0xf8006200, 0xf8006224, 16); /* 0xf8006228 hangs */
\tuart_puts("\\r\\n");

\tuart_dump_regs(0xf8006294, 0xf80062b4, 16);
\tuart_puts("\\r\\n");
}

'''
    def make_slcr_register_dump(self):
        self.sections.append('slcr_dump')
        self.cfile+='''/* Dump all SLCR */        
void dump_slcr_regs(void)
{
\tuart_dump_regs(0xf8000000, 0xf8000b74, 16);
\tuart_puts("\\r\\n");
}

'''
        
    def dci_calibration (self, reg_sets):
        if len(reg_sets)==0:
            print 'No DCI calibration register data is provided, skipping generating dci_calibration()'
            return
        self.cfile+='''/* Calibrate DDR DCI, wait for completion */        
inline void dci_calibration(void)
{
\t/* Toggle active-low DCI reset, initialize DCI calibration, wait for DONE */
'''
        self._add_reg_writes(reg_sets)
        self.cfile+='}\n\n'
        self.sections.append('dci_calibration')


    def ddr_start (self, reg_sets):
        if len(reg_sets)==0:
            print 'No DDR start data is provided, skipping generating ddr_start()'
            return
        self.cfile+='''/* Start DDRC, wait for initialization complete */        
inline void ddr_start(void)
{
'''
        self._add_reg_writes(reg_sets)
        self.cfile+='}\n\n'
        self.sections.append('ddr_start')

    def ddrc_wait_empty_queue (self,reg_sets):
        if len(reg_sets)==0:
            print 'No DDR start data is provided, skipping generating ddrc_status()'
            return
        self.cfile+='''/* Verify there are no commands in DDRC queue pending */        
inline void ddrc_wait_queue_empty(void)
{
'''
        self._add_reg_writes(reg_sets)
        self.cfile+='}\n\n'
        self.sections.append('ddrc_status')

    def _cp_led(self,name):
        led_cp=self.features.get_par_value_or_none(name)
#        print name, led_cp
        if not led_cp is None:
            if led_cp:
                self.cfile+='\tdebug_led_on(); /* Turn debug LED ON: %s */\n'%name
            else:
                self.cfile+='\tdebug_led_off(); /* Turn debug LED OFF: %s*/\n'%name
    def _read_bit_field(self,reg_set,reg_name,field_name,channel=0): #accepts bit field tuple instead of the field name
        addr=reg_set['BASE_ADDR'][channel]+ reg_set[reg_name]['OFFS']
        if isinstance(field_name,tuple):
            bits = field_name
        else:
            bits=     reg_set[reg_name]['FIELDS'][field_name]['r']
#    self._report_bit_field('BIST errors from reg_6c (1 bit per slice)',DDRC_DEFS,'reg_6c','phy_reg_bist_err')
            
        mask=(1<<(max(bits)-min(bits)+1))-1
        return ('(readl(0x%08x) >> %d) & 0x%x'%(addr,min(bits),mask), max(bits)-min(bits)+1)
    def _report_bit_field(self,name,reg_set,reg_name,field_name,channel=0):
        self.cfile+='\tuart_puts("'+name+' = 0x");\n'
        self.cfile+='\tuart_put_hex('+self._read_bit_field(reg_set,reg_name,field_name,channel)[0]+');\n'
        self.cfile+='\tuart_puts("\\r\\n");\n'

    def _report_multi_bit_fields(self,name,reg_set,fields,channel=0):
        expr=''
        shft=0
        for field in reversed(fields):
            e,w=self._read_bit_field(reg_set,field[0],field[1],channel)
            if shft==0:
                expr+='('+e+')'
            else:
                expr+='+(('+e+') << '+str(shft)+')'
            shft+=w    
        self.cfile+='\tuart_puts("'+name+' = 0x");\n'
        self.cfile+='\tuart_put_hex('+expr+');\n'
        self.cfile+='\tuart_puts("\\r\\n");\n'
        
    def make_report_training(self):
        if not (self.features.get_par_value_or_none('DUMP_TRAINING_EARLY') or self.features.get_par_value_or_none('DUMP_TRAINING_LATE') ):
            return # do not generate any code
        DDRC_DEFS=  ezynq_ddrc_defs.DDRC_DEFS
        self.cfile+='''/* Report DDR training results*/        
void report_training(void)
{
'''
        
# The fifo_we_slave ratios for each slice(0 through 3) must be interpreted by software in the following way:
# Slice 0: fifo_we_ratio_slice_0[10:0] = {Reg_6A[9],Reg_69[18:9]}\

# There is no Reg_B !!!
# Slice1: fifo_we_ratio_slice_1[10:0] = {Reg_6B[10:9],Reg_6A[18:10]}
# Slice2: fifo_we_ratio_slice_2[10:0] = {Reg_6C[11:9],Reg_6B[18:11]}
# Slice3: fifo_we_ratio_slice_3[10:0] = {phy_reg_rdlvl_fifowein_ratio_slice3_msb,Reg_6C[18:12]}

#     'reg_69':                  {'OFFS': 0x1A4,'DFLT':0x000F0000,'RW':'R','COMMENTS':'Training results for data slice 0','FIELDS':{
#                   'phy_reg_status_fifo_we_slave_dll_value': {'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
#                   'phy_reg_rdlvl_fifowein_ratio':           {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
#                   'reserved':                               {'r':( 0, 8),'d':0,    'm':'R','c':'reserved'}}},
#     'reg_6a':                  {'OFFS': 0x1A8,'DFLT':0x000F0000,'RW':'R','COMMENTS':'Training results for data slice 1','FIELDS':{
#                   'phy_reg_status_fifo_we_slave_dll_value': {'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
#                   'phy_reg_rdlvl_fifowein_ratio':           {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
#                   'reserved':                               {'r':( 0, 8),'d':0,    'm':'R','c':'reserved'}}},
# #     u32 reserved8[1];              /* 0x1AC */
#     'reg_6c':                  {'OFFS': 0x1B0,'DFLT':0x000F0000,'RW':'R','COMMENTS':'Training results for data slice 2','FIELDS':{
#                   'phy_reg_status_fifo_we_slave_dll_value':{'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
#                   'phy_reg_rdlvl_fifowein_ratio':          {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
#                   'phy_reg_bist_err':                      {'r':( 0, 8),'d':0,    'm':'R','c':'Mismatch error from BIST checker, 1 bit per data slice'}}},
#     'reg_6d':                  {'OFFS': 0x1B4,'DFLT':0x000F0000,'RW':'R','COMMENTS':'Training results for data slice 3','FIELDS':{
#                   'phy_reg_status_fifo_we_slave_dll_value':{'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
#                   'phy_reg_rdlvl_fifowein_ratio':          {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
#                   'phy_reg_bist_err':                      {'r':( 0, 8),'d':0,    'm':'R','c':'Mismatch error from BIST checker, 1 bit per data slice'}}},


        self._report_bit_field('BIST errors from reg_6c (1 bit per slice)',DDRC_DEFS,'reg_6c','phy_reg_bist_err')
        self._report_bit_field('BIST errors from reg_6d (1 bit per slice)',DDRC_DEFS,'reg_6d','phy_reg_bist_err')
        self.cfile+='\tuart_puts("\\r\\n");\n'
        
        self.cfile+='\tuart_puts("Adjusted always:\\r\\n");\n'
        self._report_bit_field('FIFO WE DLL SLICE 0',DDRC_DEFS,'reg_69','phy_reg_status_fifo_we_slave_dll_value')
        self._report_bit_field('FIFO WE DLL SLICE 1',DDRC_DEFS,'reg_6a','phy_reg_status_fifo_we_slave_dll_value')
        self._report_bit_field('FIFO WE DLL SLICE 2',DDRC_DEFS,'reg_6c','phy_reg_status_fifo_we_slave_dll_value')
        self._report_bit_field('FIFO WE DLL SLICE 3',DDRC_DEFS,'reg_6d','phy_reg_status_fifo_we_slave_dll_value')
        self.cfile+='\tuart_puts("\\r\\n");\n'

        self.cfile+='\tuart_puts("Adjusted when CONFIG_EZYNQ_DDR_TRAIN_READ_GATE is set :\\r\\n");\n'
        self._report_multi_bit_fields('FIFO WE ratio SLICE 0',DDRC_DEFS,(('reg_6a',( 9, 9)),('reg_69',( 9,18))))
        self._report_multi_bit_fields('FIFO WE ratio SLICE 1',DDRC_DEFS,(('reg_6c',( 9,10)),('reg_6a',(10,18))))
        self._report_multi_bit_fields('FIFO WE ratio SLICE 2',DDRC_DEFS,(('reg_6d',( 9,11)),('reg_6c',(11,18))))
        self._report_multi_bit_fields('FIFO WE ratio SLICE 3',DDRC_DEFS,
                                      (('dll_lock_sts','phy_reg_rdlvl_fifowein_ratio_slice3_msb'),
                                       ('reg_6d',(12,18))))
        self.cfile+='\tuart_puts("\\r\\n");\n'

        self.cfile+='\tuart_puts("Adjusted when CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE is set :\\r\\n");\n'
        self._report_bit_field('DQS ratio from Read Data Eye Training SLICE 0',DDRC_DEFS,'reg_6e','phy_reg_rdlvl_dqs_ratio')
        self._report_bit_field('DQS ratio from Read Data Eye Training SLICE 1',DDRC_DEFS,'reg_6f','phy_reg_rdlvl_dqs_ratio')
        self._report_bit_field('DQS ratio from Read Data Eye Training SLICE 2',DDRC_DEFS,'reg_70','phy_reg_rdlvl_dqs_ratio')
        self._report_bit_field('DQS ratio from Read Data Eye Training SLICE 3',DDRC_DEFS,'reg_71','phy_reg_rdlvl_dqs_ratio')
        self.cfile+='\tuart_puts("\\r\\n");\n'
        
        self.cfile+='\tuart_puts("Adjusted when CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL is set :\\r\\n");\n'
        self._report_bit_field('DQ write data ratio from Write Leveling Training SLICE 0',DDRC_DEFS,'reg_6e','phy_reg_wrlvl_dq_ratio')
        self._report_bit_field('DQ write data ratio from Write Leveling Training SLICE 1',DDRC_DEFS,'reg_6f','phy_reg_wrlvl_dq_ratio')
        self._report_bit_field('DQ write data ratio from Write Leveling Training SLICE 2',DDRC_DEFS,'reg_70','phy_reg_wrlvl_dq_ratio')
        self._report_bit_field('DQ write data ratio from Write Leveling Training SLICE 3',DDRC_DEFS,'reg_71','phy_reg_wrlvl_dq_ratio')
        self.cfile+='\tuart_puts("\\r\\n");\n'
        
        self.cfile+='\tuart_puts("Adjusted when CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL is set :\\r\\n");\n'
        self._report_bit_field('DQS write ratio from Write Leveling Training SLICE 0',DDRC_DEFS,'reg_6e','phy_reg_wrlvl_dqs_ratio')
        self._report_bit_field('DQS write ratio from Write Leveling Training SLICE 1',DDRC_DEFS,'reg_6f','phy_reg_wrlvl_dqs_ratio')
        self._report_bit_field('DQS write ratio from Write Leveling Training SLICE 2',DDRC_DEFS,'reg_70','phy_reg_wrlvl_dqs_ratio')
        self._report_bit_field('DQS write ratio from Write Leveling Training SLICE 3',DDRC_DEFS,'reg_71','phy_reg_wrlvl_dqs_ratio')
        self.cfile+='\tuart_puts("\\r\\n");\n'
        
        self.cfile+='\tuart_puts("Adjusted when CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL is set :\\r\\n");\n'
        self._report_bit_field('Delay for write DQS slave DLL SLICE 0',DDRC_DEFS,'phy_dll_sts0','phy_reg_status_wr_dqs_slave_dll_value')
        self._report_bit_field('Delay for write DQS slave DLL SLICE 1',DDRC_DEFS,'phy_dll_sts1','phy_reg_status_wr_dqs_slave_dll_value')
        self._report_bit_field('Delay for write DQS slave DLL SLICE 2',DDRC_DEFS,'phy_dll_sts2','phy_reg_status_wr_dqs_slave_dll_value')
        self._report_bit_field('Delay for write DQS slave DLL SLICE 3',DDRC_DEFS,'phy_dll_sts3','phy_reg_status_wr_dqs_slave_dll_value')
        self.cfile+='\tuart_puts("\\r\\n");\n'
        
        self.cfile+='\tuart_puts("Adjusted when CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL is set :\\r\\n");\n'
        self._report_bit_field('Delay for write DQ slave DLL SLICE 0',DDRC_DEFS,'phy_dll_sts0','phy_reg_status_wr_data_slave_dll_value')
        self._report_bit_field('Delay for write DQ slave DLL SLICE 1',DDRC_DEFS,'phy_dll_sts1','phy_reg_status_wr_data_slave_dll_value')
        self._report_bit_field('Delay for write DQ slave DLL SLICE 2',DDRC_DEFS,'phy_dll_sts2','phy_reg_status_wr_data_slave_dll_value')
        self._report_bit_field('Delay for write DQ slave DLL SLICE 3',DDRC_DEFS,'phy_dll_sts3','phy_reg_status_wr_data_slave_dll_value')
        self.cfile+='\tuart_puts("\\r\\n");\n'
        
        self.cfile+='\tuart_puts("Adjusted always:\\r\\n");\n'
        self._report_bit_field('Delay for read DQ slave DLL SLICE 0',DDRC_DEFS,'phy_dll_sts0','phy_reg_status_rd_dqs_slave_dll_value')
        self._report_bit_field('Delay for read DQ slave DLL SLICE 1',DDRC_DEFS,'phy_dll_sts1','phy_reg_status_rd_dqs_slave_dll_value')
        self._report_bit_field('Delay for read DQ slave DLL SLICE 2',DDRC_DEFS,'phy_dll_sts2','phy_reg_status_rd_dqs_slave_dll_value')
        self._report_bit_field('Delay for read DQ slave DLL SLICE 3',DDRC_DEFS,'phy_dll_sts3','phy_reg_status_rd_dqs_slave_dll_value')
        self.cfile+='\tuart_puts("\\r\\n");\n'


        self._report_bit_field('Delay all Slave DLLs for Master DLL 1',DDRC_DEFS,'dll_lock_sts','phy_reg_status_dll_slave_value_1')
        self._report_bit_field('Delay all Slave DLLs for Master DLL 0',DDRC_DEFS,'dll_lock_sts','phy_reg_status_dll_slave_value_0')
        self._report_bit_field('Master DLL 1 locked',DDRC_DEFS,'dll_lock_sts','phy_reg_status_dll_lock_1')
        self._report_bit_field('Master DLL 0 locked',DDRC_DEFS,'dll_lock_sts','phy_reg_status_dll_lock_0')
        self.cfile+='\tuart_puts("\\r\\n");\n'

        self._report_bit_field('Master DLL Output filter locked (+2 - coarse, +1 - fine',DDRC_DEFS,'phy_ctrl_sts','phy_reg_status_phy_ctrl_of_in_lock_state')
        self._report_bit_field('Values applied to PHY_CTRL Slave DLL',                   DDRC_DEFS,'phy_ctrl_sts','phy_reg_status_phy_ctrl_dll_slave_value')
        self._report_bit_field('PHY Control Master DLL status (locked)',                 DDRC_DEFS,'phy_ctrl_sts','phy_reg_status_phy_ctrl_dll_lock')
        self._report_bit_field('Values from Master DLL Output Filter',                   DDRC_DEFS,'phy_ctrl_sts','phy_reg_status_of_out_delay_value')
        self._report_bit_field('Values applied to Master DLL Output Filter',             DDRC_DEFS,'phy_ctrl_sts','phy_reg_status_of_in_delay_value')
        self.cfile+='\tuart_puts("\\r\\n");\n'

        self._report_bit_field('Delay values applied to read DQS slave DLL',             DDRC_DEFS,'phy_ctrl_sts_reg2','phy_reg_status_phy_ctrl_slave_dll_value')
        self._report_bit_field('Values applied to Master DLL Output Filter',             DDRC_DEFS,'phy_ctrl_sts_reg2','phy_reg_status_phy_ctrl_of_in_delay_value')
        
        self.cfile+='}\n'

        self.sections.append('ddrc_training')
    
    def make_arch_cpu_init(self):
        self.cfile+='''/* Initialize clocks, DDR memory, copy OCM to DDR */        
int arch_cpu_init(void)
{
/* Unlock SLCR */
\tunlock_slcr();

'''
        #Setup GPIO outputs (To be used by LED)        
        if 'gpio_out' in self.sections:
            self.cfile+='\tsetup_gpio_outputs(); /* Setup GPIO outputs */\n'
        self._cp_led('LED_CHECKPOINT_2') # First after getting to user code
        self.cfile+='''/*
   Write PLL and clocks registers as the code is now completely loaded to the OCM and no
   peripherals are needed immediately 
 */
\tregister_setup();

'''
        self._cp_led('LED_CHECKPOINT_3') # After setting clock registers

        self.cfile+='\tpll_setup();         /* Wait PLLs locked and turn off bypass - all clocks should have specified values now */ \n'
        self.cfile+='\treset_peripherals(); /* Reset defined peripherals */\n'
        self._cp_led('LED_CHECKPOINT_4') # After PLL bypass is OFF
        if 'uart_init' in self.sections:
            self.cfile+='\tuart_init();         /* Initialize UART for debug information output */\n'
            self.cfile+='\tuart_puts("devcfg.PS_VERSION=");\n'
            self.cfile+='\tuart_put_hex(readl(0xf8007080));\n'; #TODO:Compare against specified
            self.cfile+='\tuart_puts("\\r\\n");\n'
            self.cfile+='\tuart_puts("slcr.PSS_IDCODE=");\n'
            self.cfile+='\tuart_put_hex(readl(0xf8000530));\n';
            self.cfile+='\tuart_puts("\\r\\n");\n'
            
        self._cp_led('LED_CHECKPOINT_5') # After UART is programmed
        if self.features.get_par_value_or_none('DUMP_SLCR_EARLY'):
            self.cfile+='\tuart_puts("SLCR registers before DCI/DDR initialization\\r\\n");\n'
            self.cfile+='\tdump_slcr_regs();    /* Dump all SLCR registers before DCI/DDR initialization */\n'
        if self.features.get_par_value_or_none('DUMP_DDRC_EARLY'):
            self.cfile+='\tuart_puts("DDRC registers before DCI/DDR initialization\\r\\n");\n'
            self.cfile+='\tdump_ddrc_regs();    /* Dump all DDRC registers before DCI/DDR initialization */\n'
            
        if self.features.get_par_value_or_none('DUMP_TRAINING_EARLY'):
            self.cfile+='\tuart_puts("Training results registers state before DDRC initialization\\r\\n");\n'
            self.cfile+='\treport_training();    /* Print training results */\n'
#         if 'uart_xmit' in self.sections:
#             self.cfile+='\tuart_wait_tx_fifo_empty();\n'
    
        self.cfile+='\tdci_calibration();   /* Calibrate DDR DCI impedance and wait for completion */\n'  
#        self._cp_led('LED_CHECKPOINT_6') # After DCI is calibrated
        self.cfile+='\tddr_start();         /* Remove soft reset from DDR controller - this will start initialization. Wait for completion */\n'  
        self._cp_led('LED_CHECKPOINT_7') # After DDR is initialized
        if self.features.get_par_value_or_none('DUMP_SLCR_LATE'):
            self.cfile+='\tuart_puts("SLCR registers after DCI/DDR initialization\\r\\n");\n'
            self.cfile+='\tdump_slcr_regs();    /* Dump all SLCR registers after DCI/DDR initialization */\n'
        if self.features.get_par_value_or_none('DUMP_DDRC_LATE'):
            self.cfile+='\tuart_puts("DDRC registers after DCI/DDR initialization\\r\\n");\n'
            self.cfile+='\tdump_ddrc_regs();    /* Dump all DDRC registers after DCI/DDR initialization */\n'
        if self.features.get_par_value_or_none('DUMP_TRAINING_LATE'):
            self.cfile+='\tuart_puts("Training results registers state after DDRC initialization\\r\\n");\n'
            self.cfile+='\treport_training();    /* Print training results */\n'
        self.cfile+='''/* Copy 3 pages of OCM from 0x00000.0x2ffff to DDR 0x4000000.0x402ffff*/  
\tint * s= (int *) 0;
\tint * d= (int *) 0x4000000;
\twhile (s< ((int *)0x30000)) *d++=*s++;
'''
        self.cfile+='\tddrc_wait_queue_empty(); /* Wait no commands are pending in DDRC queue */\n'            

        self._cp_led('LED_CHECKPOINT_8') # Before relocation to DDR (to 0x4000000+ )
        
        if self.features.get_par_value_or_none('DUMP_OCM'):
            self.cfile+='\tuart_puts("OCM memory data\\r\\n");\n'
            self.cfile+='\tuart_dump_regs(0x%08x,0x%08x, 16);\n'%(self.features.get_par_value_or_default('DUMP_OCM_LOW'),self.features.get_par_value_or_default('DUMP_OCM_HIGH'))
            self.cfile+='\tuart_puts("\\r\\n");\n'
           
        if self.features.get_par_value_or_none('DUMP_DDR'):
            self.cfile+='\tuart_puts("DDR memory data\\r\\n");\n'
            self.cfile+='\tuart_dump_regs(0x%08x,0x%08x, 16);\n'%(self.features.get_par_value_or_default('DUMP_DDR_LOW'),self.features.get_par_value_or_default('DUMP_DDR_HIGH'))
            self.cfile+='\tuart_puts("\\r\\n");\n'

#         if 'uart_xmit' in self.sections:
#             self.cfile+='\tuart_wait_tx_fifo_empty();\n'
        
        self.cfile+='''/*
   Now jump to the same instruction in the DDR copy of the currently executed code in OCM
   Be careful not to call functions or access data stored in the 3 lower OCM pages.
   writel() is OK as it is just a macro, not a function call 
 */
\tasm("add pc, pc, #0x4000000" );

'''
# seems some delay is needed before remapping DDR memory
        self.cfile+='\tddrc_wait_queue_empty(); /* seems some delay is needed here before remapping DDR memory */\n'            
        self._cp_led('LED_CHECKPOINT_9') # After relocation to DDR (to 0x4000000+ )
        self.cfile+='\twritel(0, &scu_base->filter_start); /* Remap DDR to zero, FILTERSTART */\n'
        self.cfile+='''/* Device config APB, unlock the PCAP */
\twritel(0x757BDF0D, &devcfg_base->unlock);
\twritel(0xFFFFFFFF, &devcfg_base->rom_shadow);
'''
        self._cp_led('LED_CHECKPOINT_10') # Before remapping OCM0-OCM2 high
        self.cfile+='''/*
   Now as the code is executed outside of the OCM it is possible to remap the 3 lower
   OCM pages to high memory. 
   OCM_CFG, Mask out the ROM, map ram into upper addresses
 */
\twritel(0x1F, &slcr_base->ocm_cfg);
'''
        self._cp_led('LED_CHECKPOINT_11') # After remapping OCM0-OCM2 high
        self.cfile+='''/*
   Copy program memory that we are currently executing to low DRAM (0x0.0x2ffff)
   Not possible to call library memcpy() as it will try to access not-yet copied code
 */
\ts= (int *) 0x4000000;
\td= (int *) 0;
\twhile (d < ((int *) 0x30000)) *d++=*s++;

\tddrc_wait_queue_empty(); /* Wait no commands are pending in DDRC queue */   
/*
 * Below is a hack - copying the same data to low SDRAM again - probably just a delay.
 * Waiting for ddrc_wait_queue_empty() alone is not sufficient - some of the
 * generated images work always, some - half times, some - never, dependent on 
 * seemingly unrelated changes. With this extra delay all seems fine.
 * Better understanding of the original problem and a fix is needed.
 */
\ts= (int *) 0x4000000;
\td= (int *) 0;
\twhile (d < ((int *) 0x30000)) *d++=*s++;

\tddrc_wait_queue_empty(); /* Wait no commands are pending in DDRC queue */   

/*
   Continue with the original low-level init, Now we have 2 copies of the code again,
   currently executing somewhere above 0x4000000. But as soon as we will return
   from the call (execute 'bx lr') we'll get back to the low memory.
 */  
\t/* FPGA_RST_CTRL, clear resets on AXI fabric ports */
\twritel(0x0, &slcr_base->fpga_rst_ctrl);
\t/* TZ_DDR_RAM, Set DDR trust zone non-secure */
\twritel(0xFFFFFFFF, &slcr_base->trust_zone);
\t/* Set urgent bits with register */
\twritel(0x0, &slcr_base->ddr_urgent_sel);
\t/* Urgent write, ports S2/S3 */
\twritel(0xC, &slcr_base->ddr_urgent);
'''

        if ('uart_xmit' in self.sections) and self.features.get_par_value_or_none('LAST_PRINT_DEBUG'):
            self.cfile+='\tuart_put_hex(0x12345678);\n'
            self.cfile+='\tuart_putc(0xd);\n'
            self.cfile+='\tuart_putc(0xa);\n'
        if 'uart_xmit' in self.sections:
            self.cfile+='\tuart_wait_tx_fifo_empty(); /* u-boot may re-program UART differently, wait all is sent before getting there */\n'
#uart_wait_tx_fifo_empty() - add if u-boot debug is on
        self._cp_led('LED_CHECKPOINT_12') # Before leaving lowlevel_init()

# #Setup GPIO outputs (after LED debug is over)        
#         if 'gpio_out' in self.sections:
#             self.cfile+='\tsetup_gpio_outputs(); /* Setup GPIO outputs */\n'
        
#LOCK_SLCR        
        if self.features.get_par_value_or_none('LOCK_SLCR') is False:
            self.cfile+='/* Leaving SLCR registers UNLOCKED according to setting of %s */\n'%self.features.get_par_confname('LOCK_SLCR')
        else:            
            self.cfile+='''/* Lock SLCR back after everything with it is done */
\tlock_slcr();
'''
        self.cfile+='''/* This code was called from low OCM, so return should just get back correctly */
\treturn 0;        
}
'''

    def output_c_file(self,cname):
        if not cname:
            return
        print 'Writing generated u-boot arch_cpu_init() function to ',os.path.abspath(cname)
        c_out_file=open(cname,'w')
        c_out_file.write(self.cfile)
        c_out_file.close()
    