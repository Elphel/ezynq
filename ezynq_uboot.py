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
    {'NAME':'DUMP_SLCR_LATE',    'CONF_NAME':'CONFIG_EZYNQ_DUMP_SLCR_LATE','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump SLCR registers after DDR memory is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG)'},              
    {'NAME':'DUMP_DDRC_LATE',    'CONF_NAME':'CONFIG_EZYNQ_DUMP_DDRC_LATE','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Dump DDRC registers after DDR memory is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG)'},              

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
                self.cfile+='\tdebug_led_on(); /* Turn debug LED ON */\n'
            else:
                self.cfile+='\tdebug_led_off(); /* Turn debug LED OFF */\n'    
    
    def make_arch_cpu_init (self):
            

        self.cfile+='''/* Initialize clocks, DDR memory, copy OCM to DDR */        
int arch_cpu_init(void)
{
/* Unlock SLCR */
\tunlock_slcr();

'''
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
        self._cp_led('LED_CHECKPOINT_5') # After UART is programmed
        if self.features.get_par_value_or_none('DUMP_SLCR_EARLY'):
            self.cfile+='\tuart_puts("SLCR registers before DCI/DDR initialization\\r\\n");\n'
            self.cfile+='\tdump_slcr_regs();    /* Dump all SLCR registers before DCI/DDR initialization */\n'
        if self.features.get_par_value_or_none('DUMP_DDRC_EARLY'):
            self.cfile+='\tuart_puts("DDRC registers before DCI/DDR initialization\\r\\n");\n'
            self.cfile+='\tdump_ddrc_regs();    /* Dump all DDRC registers before DCI/DDR initialization */\n'
        self.cfile+='\tdci_calibration();   /* Calibrate DDR DCI impedance and wait for completion */\n'  
        self._cp_led('LED_CHECKPOINT_6') # After DCI is calibrated
        self.cfile+='\tddr_start();         /* Remove soft reset from DDR controller - this will start initialization. Wait for completion */\n'  
        self._cp_led('LED_CHECKPOINT_7') # After DDR is initialized
        if self.features.get_par_value_or_none('DUMP_SLCR_LATE'):
            self.cfile+='\tuart_puts("SLCR registers after DCI/DDR initialization\\r\\n");\n'
            self.cfile+='\tdump_slcr_regs();    /* Dump all SLCR registers after DCI/DDR initialization */\n'
        if self.features.get_par_value_or_none('DUMP_DDRC_LATE'):
            self.cfile+='\tuart_puts("DDRC registers after DCI/DDR initialization\\r\\n");\n'
            self.cfile+='\tdump_ddrc_regs();    /* Dump all DDRC registers after DCI/DDR initialization */\n'
        self.cfile+='''/* Copy 3 pages of OCM from 0x00000.0x2ffff to DDR 0x4000000.0x402ffff*/  
\tint * s= (int *) 0;
\tint * d= (int *) 0x4000000;
\twhile (s< ((int *)0x30000)) *d++=*s++;
'''
        self.cfile+='\tddrc_wait_queue_empty(); /* Wait no commands are pending in DDRC queue */\n'            

        self._cp_led('LED_CHECKPOINT_8') # Before relocation to DDR (to 0x4000000+ )
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
        if 'uart_xmit' in self.sections:
            self.cfile+='\tuart_wait_tx_fifo_empty(); /* u-boot may re-program UART differently, wait all is sent before getting there */\n'
#uart_wait_tx_fifo_empty() - add if u-boot debug is on
        self._cp_led('LED_CHECKPOINT_12') # Before leaving lowlevel_init()

#Setup GPIO outputs (after LED debug is over)        
        if 'gpio_out' in self.sections:
            self.cfile+='\tsetup_gpio_outputs(); /* Setup GPIO outputs */\n'
        
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
    