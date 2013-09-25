#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# pre-u-boot configuration of the Xilinx Zynq(R) SoC
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
import struct
import argparse # http://docs.python.org/2/howto/argparse.html

import ezynq_ddr
import ezynq_registers
import ezynq_mio
import ezynq_clk
import ezynq_uboot
import ezynq_uart
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbosity', action='count', help='increase output verbosity')
parser.add_argument('-c', '--configs',   help='Configuration file (such as autoconf.mk)')
parser.add_argument('-w', '--warn',      help='Warn when the pin function is overwritten and continue', action='store_true')
parser.add_argument('-o', '--outfile',   help='Path to save the generated boot file')
parser.add_argument('--html', help='Generate HTML map of MIO, save to the specified file')
parser.add_argument('--html-mask', help='Bit mask of what data to include in the HTML MIO map')
#parser.add_argument('-i', '--include',   help='Generate include file for u-boot')
parser.add_argument('-l', '--lowlevel',   help='path to the lowlevel.c file to be generated for u-boot')
parser.add_argument('-u', '--uboot',      help='path to the u-boot.bin to get it\'s length (second pass, when u-boot.bin is already generated)')

args = parser.parse_args()
#print args
#print args.configs

ERROR_DEFS={
    'WRONG_USAGE':1,    
    'MISSING_CONFIG': 2,    
    'INVALID': 3,
    'NOSUCHPIN': 4,
    'NOSUCHSIGNAL': 5,
    'MIOCONFLICT':6,
    'INOUT': 7,
    'HEAD': 8,
    'NONACCESSIBLE_REGISTER': 9,
    'NOT_IMPLEMENTED':10}

COMMENT_CHAR = '#'
OPTION_CHAR = '='
QUALIFIER_CHAR = '__'

if not args.configs:
    parser.print_help()
    exit (ERROR_DEFS['WRONG_USAGE'])
WARN=args.warn
MIO_HTML=args.html
try:
    MIO_HTML_MASK=int(args.html_mask,0)
except:
    MIO_HTML_MASK=0

GPIO_MASKDATA=[
               {'NAME':'MASK_DATA_0_LSW','ADDRESS':0xE000A000,'DATA':0},
               {'NAME':'MASK_DATA_0_MSW','ADDRESS':0xE000A004,'DATA':0},
               {'NAME':'MASK_DATA_1_LSW','ADDRESS':0xE000A008,'DATA':0},
               {'NAME':'MASK_DATA_1_MSW','ADDRESS':0xE000A00C,'DATA':0}]
SLCR_LOCK=[
           {'NAME':'UNLOCK','ADDRESS':0xf8000008,'DATA':0xDF0D},
           {'NAME':'LOCK',  'ADDRESS':0xf8000004,'DATA':0x767B}]

ACCESSIBLE_REGISTERS=((0xe0001000,0xe0001fff), # UART1 controller registers
                      (0xe000d000,0xe000efff), # QUAD SPI controller registers
                      (0xe0100004,0xe0100057), # SDIO 0 controller registers
                      (0xe0100059,0xe0100fff), # SDIO 0 controller registers
                      (0xe000e000,0xe000efff), # SMC controller
                      (0xf8006000,0xf8006fff), # DDR controller
                      # SLCR_LOCK disables all (0xf8000000,0xf8000b74), but it is locked at reset seems to be unlocked, http://www.xilinx.com/support/answers/47570.html
                      #prohibited: SLCR_SCL, SLCR_LOCK, SLCR_UNLOCK, SLCR_STA
                      (0xf8000100,0xf80001b0), # SLCR registers
                      #DOes not seem to be any gap between 0xf80001b0 and 0xf80001b4 
                      (0xf80001b4,0xf80001ff), # SLCR registers
                      #prohibited SLCR_PSS_RST_CTRL 0xf8000200 
                      (0xf8000204,0xf8000234), # SLCR registers - is  SLCR_SMC_RST_CTRL 0xf8000234 also prohibited? 
                      #prohibited? SLCR_OCM_RST_CTRL 0xf8000238 SLCR_FPGA_RST_CTRL 0xf8000240
                      (0xf800024c,0xf800024c), # SLCR registers SLCR_AWDT_CTRL - watchdog timer reset control
                      #prohibited SLSR_REBOOT_STATUS 0xf8000258, SLCR_BOOT_MODE 0xf800025c, SLCR_APU_CTRL 0xf8000300, 
                      (0xf8000304,0xf8000834), # SLCR registers SLCR_AWDT_CLK_SEL,  DDR, MIO
                      #prohibited SLCR_LVL_SHFTR_ON 0xf8000900, SLCR_OCM_CFG 0xf8000910, 
                      (0xf8000a00,0xf8000a8c), # SLCR registers All shown "reserved" ???
                      (0xf8000ab0,0xf8000b74)) # SLCR registers iostd, voltages,  - more DDR stuff
           


  
if args.verbosity >= 2:
    print ezynq_mio.MIO_TEMPLATES
def read_config(filename):
    raw_configs = []
    f = open(filename)
    for line in f:
        # First, remove comments:
        if COMMENT_CHAR in line:
            # split on comment char, keep only the part before
            line,_  = line.split(COMMENT_CHAR, 1)
        # Second, find lines with an option=value:
        if OPTION_CHAR in line:
            # split on option char:
            option, value = line.split(OPTION_CHAR, 1)
            # strip spaces:
            option = option.strip()
            value = value.strip().upper()
            # strip quotes:
            value = value.strip('"')
            raw_configs.append({'KEY':option,'VALUE':value})
    f.close()
    return raw_configs
  
def verify_register_accessible(address):
    for interval in ACCESSIBLE_REGISTERS:
        if (address >= interval[0]) and (address <= interval[1]):
            if args.verbosity >= 1:  print 'Register accessible:' , hex(interval[0]),'<=', hex(address), '<=', hex(interval[1])
            return True
    else:
        return False    

#### Need to be modified for new format of register setup
# def uart_remote_loopback(registers,f,uart_num,MIO_HTML_MASK):
#     if f:
#         f.write ('<H2>UART'+str(uart_num)+' remote loopback</H2>\n')
#         f.write('<table border="1">\n')
#         f.write('  <tr><th>Register name</th><th>Address</th><th>Data</th></tr>\n')
#     word={'NAME':'UART'+str(uart_num)+"_mode_reg0",'ADDRESS':(0xe0000004,0xe0001004)[uart_num!=0],'DATA':0x320}
# #    print word       
#     registers.append({'ADDRESS':word['ADDRESS'],'DATA':word['DATA']})
#     if f:
#         f.write('  <tr><td>'+word['NAME']+'</td><td>'+hex(word['ADDRESS'])+'</td><td>'+hex(word['DATA'])+'</td></tr>\n')
#     if f:
#         f.write('  </table>\n')

        
class Image(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(*args, **kwargs)
        self.waddr = 0
    def __iadd__(self, value):
        self[self.waddr] = value
        self.waddr += 1
class Limage(list):
    def __init__(self, *args, **kwargs):
        list.__init__(*args, **kwargs)
        self.waddr = 0
    def __iadd__(self, value):
        self[self.waddr] = value
        self.waddr += 1

 
def image_generator (image,
                       reg_sets, # registers,
                       options,
                       user_def,
                       ocm_offset,
                       ocm_len,
                       start_exec):
    reserved0044=0;
    if 'CONFIG_EZYNQ_RESERVED44' in options: reserved0044= int(options['CONFIG_EZYNQ_RESERVED44'],0)

    rfi_word=0xeafffffe #from actual image
    waddr=0
    for _ in range (0x20/4):
        image[waddr]=rfi_word # fill reserved for interrupts fields
        waddr+=1
    #width detection
    image[waddr]=0xaa995566 # offset 0x20
    waddr+=1
    
    #image identification
    image[waddr]=0x584c4e58 # offset 0x24, XLNX
    waddr+=1
    
    #encryption status
    image[waddr]=0x0 # offset 0x28, no encryption
    waddr+=1
    
    #User defined word
    image[waddr]=user_def # offset 0x2c
    waddr+=1
    
    #ocm_offset
    if ocm_offset<0x8c0:
        print 'Start offset should be >= 0x8c0, specified', hex(ocm_offset)
        exit (ERROR_DEFS['HEAD'])
    elif (ocm_offset & 0x3f) != 0:
        print 'Start offset should be 64-bytes aligned, specified', hex(ocm_offset)
        exit (ERROR_DEFS['HEAD'])
    image[waddr]=ocm_offset # offset 0x30
    waddr+=1
       
    #ocm_len    
    if ocm_len>0x30000:
        print 'Loaded to the OCM image should fit into 3 mapped pages of OCM - 192K (0x30000), specified ',hex(ocm_len)
        exit (ERROR_DEFS['HEAD'])
    image[waddr]=ocm_len # offset 0x34
    waddr+=1

    #reserved 0
    image[waddr]=0 # offset 0x38
    waddr+=1
    
    #start_exec    
    if (start_exec>0x30000) or (start_exec<0):
        print 'Start address is relative to  OCM and should fit there - in 192K (0x30000), specified ',hex(start_exec)
        exit (ERROR_DEFS['HEAD'])
    image[waddr]=start_exec # offset 0x3c
    waddr+=1
    
    #img_len == ocm_len for unsecure images
    img_len = ocm_len
    image[waddr]=img_len # offset 0x40
    waddr+=1

    #reserved 0
    image[waddr]=reserved0044 #0  # offset 0x44
    waddr+=1
    
    #calculate image checksum
    def add (x,y): return x+y
    checksum=(reduce(add,image[0x20/4:0x48/4]) ^ 0xffffffff) & 0xffffffff 
    image[waddr]=checksum # offset 0x48
    waddr+=1
    if args.verbosity >= 1:  print 'After checksum waddr=',hex(waddr),' byte addr=',hex(4*waddr)
    
    
    #initialize registers
    if args.verbosity >= 1:  print 'Number of registers to initialize',len(reg_sets)
    if len (reg_sets)>256:
        print 'Too many registers to initialize, only 256 allowed,',len(reg_sets),'> 256'
    waddr=0xa0/4
    # new_sets.append((addr,data,mask,self.module_name,register_name,self.defs[register_name]))

    for register in reg_sets:
        op=register[0]
        addr=register[1]
        data=register[2]
        if (op != 's'):
            raise Exception ('Can not test registers (0x%08x) in RBL, it should be done in user code'%addr)
        if not verify_register_accessible (addr):
            print 'Tried to set non-accessible register', hex(addr),' with data ', hex(data)
            exit (ERROR_DEFS['NONACCESSIBLE_REGISTER'])
        image[waddr]=addr
        waddr+=1
        image[waddr]=data
        waddr+=1
    #Fill in FFs for unused registers
    while waddr < (0x8c0/4):
        image[waddr]=0xffffffff
        waddr+=1
        image[waddr]=0
        waddr+=1
           
def write_image(image,name):
    bf=open(name,'wb')
    data=struct.pack('I' * len(image), *image)
    bf.write(data)
    bf.close()

def raw_config_value(key, raw_config):
    for kv in raw_config:
        if kv['KEY']== key:
            return kv['VALUE']
    return None     

#=========================
if not args.verbosity:
    args.verbosity=0
raw_configs=read_config(args.configs)
raw_options={n['KEY']:n['VALUE'] for n in raw_configs}
permit_undefined_bits=False
force=True #False
warn_notfit=True # False
regs_masked=[]
u_boot=ezynq_uboot.EzynqUBoot(raw_configs,args.verbosity)

mio_regs=ezynq_mio.EzynqMIO(args.verbosity,QUALIFIER_CHAR,[],permit_undefined_bits) # does not use regs_masked
mio_regs.process_mio(raw_configs,WARN)      # does not use regs_masked

ddr=ezynq_ddr.EzynqDDR([],permit_undefined_bits, force, warn_notfit) #regs_masked are  just []
ddr.parse_parameters(raw_configs)
ddr_type=ddr.get_ddr_type()

used_mio_interfaces=mio_regs.get_used_interfaces()
#for iface in used_mio_interfaces:
#    print iface
#clk=ezynq_clk.EzynqClk(regs_masked,ddr_type,permit_undefined_bits=False,force=False,warn=False)
clk=ezynq_clk.EzynqClk(args.verbosity,[],ddr_type,used_mio_interfaces,permit_undefined_bits,force,warn_notfit) # will it verify memory type is set?
clk.parse_parameters(raw_configs)

clk.calculate_dependent_pars() # will calculate DDR clock, needed for ddr.calculate_dependent_pars()
clk.check_missing_features() #and apply default values
clk.check_ds_compliance()
clk.setup_clocks()

ddr_mhz=clk.get_ddr_mhz()
    
        
if MIO_HTML:
    html_file=open(MIO_HTML,'w')
    print 'Generating HTML output',os.path.abspath(MIO_HTML)
else:
    html_file=False
u_boot.html_list_features(html_file)
#output_slcr_lock(registers,f,False,MIO_HTML_MASK) #prohibited by RBL
mio_regs.output_mio(html_file,MIO_HTML_MASK)
#  def process_mio(self,raw_configs,warn):
#  def output_mio(self,f,MIO_HTML_MASK)
#  setregs_mio(self,current_reg_sets,force=True):
clk.html_list_clocks(html_file)

ddr.calculate_dependent_pars(ddr_mhz)
ddr.pre_validate() # before applying default values (some timings should be undefined, not defaults)
ddr.check_missing_features() #and apply default values

ddr.html_list_features(html_file) #verify /fix values after defaults are applied

#clk.calculate_dependent_pars()
clk.html_list_features(html_file)

reg_sets=[]
segments=[]
reg_sets=mio_regs.setregs_mio(reg_sets,force) # reg Sets include now MIO
segments.append({'TO':len(reg_sets),'RBL':True,'NAME':'MIO','TITLE':'MIO registers configuration'})
led_debug_mio_pin= u_boot.features.get_par_value_or_none('LED_DEBUG')
if not led_debug_mio_pin is None:
    led_cp_1=u_boot.features.get_par_value_or_none('LED_CHECKPOINT_1')
    if not led_cp_1 is None:
        reg_sets=mio_regs.rbl_led_on_off(led_debug_mio_pin, led_cp_1, reg_sets)
        segments.append({'TO':len(reg_sets),'RBL':True,'NAME':'RBL_LED','TITLE':'Setting debug LED during RBL to '+('OFF','ON')[led_cp_1]})
#adding ddr registers
if raw_config_value('CONFIG_EZYNQ_SKIP_DDR', raw_configs) is None:        
    ddr.ddr_init_memory(reg_sets,False,False)
    reg_sets=ddr.get_new_register_sets() # mio, ddr
    segments.append({'TO':len(reg_sets),'RBL':True,'NAME':'DDR0','TITLE':'DDR registers configuration'})
else:
    print 'Debug mode: skipping DDR-related configuration'
#initialize clocks
# unlock slcr - it is locked by RBL, but attempt to unlock in RBL will fail (and hang the system)
reg_sets=clk.clocks_regs_setup(reg_sets,force)
segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'CLK','TITLE':'Clock registers configuration'})
#print 'Debug mode: CLK/PLL configuration by u-boot'
reg_sets=clk.clocks_pll_bypass_off(reg_sets,force)
segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'PLL','TITLE':'Registers to switch to PLL'})

reg_sets=clk.reset_peripherals(reg_sets,force)
segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'RESETS','TITLE':'Resetting defined peripherals after clocks changed'})

if u_boot.features.get_par_value_or_none('BOOT_DEBUG'):
    uart=ezynq_uart.EzynqUART()
    uart.parse_parameters(raw_configs,used_mio_interfaces,False)
    uart.check_missing_features()
    uart_channel=uart.channel
    if not uart_channel is None:
        try:
            uart_mhz=clk.get_uart_mhz()
        except:
            print 'UART reference clock is not defined, can not generate boot debug code'
            uart_channel=None   
        uart.set_refclk_mhz(uart_mhz)
#    print 'uart_channel=',uart_channel,' uart_mhz=',uart_mhz
     
else:
    uart_channel=None

if not uart_channel is None:
    uart.html_list_features(html_file)

    reg_sets=uart.setup_uart(reg_sets,force=False,warn=False)
    segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'UART_INIT','TITLE':'Registers to initialize UART'})
    
    reg_sets_uart_extra=uart.set_uart_codes()
    reg_sets.extend (reg_sets_uart_extra) # just to be listed, not to be loaded
    segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'UART_XMIT','TITLE':'UART register tests sets to output debug data'})
    
if raw_config_value('CONFIG_EZYNQ_SKIP_DDR', raw_configs) is None:
    reg_sets=ddr.ddr_dci_calibrate(reg_sets,False,False)
    segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'DCI','TITLE':'DDR DCI Calibration'})
    reg_sets=ddr.ddr_start(reg_sets,False,False)
    segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'DDR_START','TITLE':'DDR initialization start'})

# Generate lock/unlock SLCR to be used in u-boot
reg_sets_lock_unlock=clk.generate_lock_unlock()
#print reg_sets[len(reg_sets)-1]
reg_sets.extend (reg_sets_lock_unlock) # just to be listed, not to be loaded
segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'SLCR_LOCK_UNLOCK','TITLE':'SLCR lock/unlock registers - listed out of sequence'})

if not led_debug_mio_pin is None: 
    reg_sets_led=mio_regs.generate_led_off_on(led_debug_mio_pin)
    reg_sets.extend (reg_sets_led) # just to be listed, not to be loaded
    segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'LED','TITLE':'registers/data to turn on/off debug LED - listed out of sequence'})

#add code to check DDRC status (no commands in queue)    
reg_sets_ddrc_sta=ddr.generate_command_queue_empty()
reg_sets.extend (reg_sets_ddrc_sta) # just to be listed, not to be loaded
segments.append({'TO':len(reg_sets),'RBL':False,'NAME':'DDRC_STA','TITLE':'register to test DDRC comamnd queue status - listed out of sequence'})
    
    
    
#    def generate_led_off_on(self, mio_pin):
#CONFIG_EZYNQ_LED_DEBUG=47 # toggle LED during boot
#CONFIG_EZYNQ_BOOT_DEBUG

#print reg_sets_lock_unlock[0]
#print reg_sets_lock_unlock[1]

# make reg_sets data cumulative
reg_sets=ezynq_registers.accumulate_reg_data(reg_sets)
num_rbl_regs=0
for segment in segments:
    if segment['RBL']:
        num_rbl_regs=segment['TO']
segment_dict={}
for index,segment in enumerate(segments):
    if index==0:
        start=0
    else:    
        start=segments[index-1]['TO']
    segment['FROM']=start
    segment_dict[segment['NAME']]=segment
#for index,segment in enumerate(segments):
#    print index,':', segment    
if html_file:
    for segment in segments:
        start=segment['FROM']
        end=segment['TO']    
        show_bit_fields= (MIO_HTML_MASK & 0x100,MIO_HTML_MASK & 0x800)[segment['NAME']=='MIO']
        show_comments=    MIO_HTML_MASK & 0x200
        filter_fields=not MIO_HTML_MASK & 0x400
        all_used_fields= False
        ezynq_registers.print_html_reg_header(html_file,
                                               segment['TITLE']+" (%s)"%(('U-BOOT','RBL')[segment['RBL']]),
                                               show_bit_fields, show_comments, filter_fields)
    #   print segment['TITLE']+" (%s)"%(('U-BOOT','RBL')[segment['RBL']]), start,end
    
        ezynq_registers.print_html_registers(html_file,
                                              reg_sets[:end],
                                              start,
                                              show_bit_fields,
                                              show_comments,
                                              filter_fields,
                                              all_used_fields)
        ezynq_registers.print_html_reg_footer(html_file)
    html_file.write('<h4>Total number of registers set up in the RBL header is <b>'+str(num_rbl_regs)+"</b> of maximal 256</h4>")
    if num_rbl_regs<len(reg_sets):
        html_file.write('<h4>Number of registers set up in u-boot is <b>'+str(len(reg_sets)-num_rbl_regs)+"</b></h4>")
    html_file.close

image =[ 0 for k in range (0x8c0/4)]

#image_generator (image, registers, user_def,start_offset,ocm_len,start_exec)
#CONFIG_EZYNQ_BOOT_USERDEF=           0x1234567 # will be saved in the file header
#CONFIG_EZYNQ_BOOT_OCM_OFFSET=        0x8C0   # start of OCM data relative to the flash image start >=0x8C0, 63-bytes aligned
#CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH=  0x30000 # number of bytes to load to the OCM memory, <= 0x30000 
#CONFIG_EZYNQ_START_EXEC=             0x20 # number of bytes to load to the OCM memory, <= 0x30000 
if (args.uboot):
    try:
        uboot_image_len=os.path.getsize(args.uboot)
        print 'Using %s to get image length - it is %i (0x%x) bytes'%(os.path.abspath(args.uboot),uboot_image_len,uboot_image_len)
    except:
        print 'Specified u-boot.bin file: %s (%s) not found'%(args.uboot,os.path.abspath(args.uboot))
else:    
    uboot_image_len=int(raw_options['CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH'],0)
    print 'No u-boot.bin path specified, using provided CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH as image size of %i (0x%x) bytes for the RBL header'%(uboot_image_len,uboot_image_len)
             
image_generator (image,
                 reg_sets[:num_rbl_regs], #
                 #registers,
                 raw_options,
                 int(raw_options['CONFIG_EZYNQ_BOOT_USERDEF'],0), # user_def
                 int(raw_options['CONFIG_EZYNQ_BOOT_OCM_OFFSET'],0), # ocm_offset,
                 uboot_image_len, #ocm_len,
                 int(raw_options['CONFIG_EZYNQ_START_EXEC'],0)) #start_exec)
if args.outfile:
    print 'Generating binary output ',os.path.abspath(args.outfile)
    write_image(image,args.outfile)
if (args.lowlevel):
    if 'SLCR_LOCK_UNLOCK' in segment_dict: 
        u_boot.make_slcr_lock_unlock (reg_sets[segment_dict['SLCR_LOCK_UNLOCK']['FROM']:segment_dict['SLCR_LOCK_UNLOCK']['TO']])
    if 'LED' in segment_dict: 
        u_boot.make_led_on_off(reg_sets[segment_dict['LED']['FROM']:segment_dict['LED']['TO']])
    
    if 'CLK' in segment_dict: 
        u_boot.registers_setup (reg_sets[segment_dict['CLK']['FROM']:segment_dict['CLK']['TO']],clk,num_rbl_regs)
    if 'PLL' in segment_dict: 
        u_boot.pll_setup (reg_sets[segment_dict['PLL']['FROM']:segment_dict['PLL']['TO']])
    if 'RESETS' in segment_dict:
        u_boot.make_resets (reg_sets[segment_dict['RESETS']['FROM']:segment_dict['RESETS']['TO']])

    if 'UART_INIT' in segment_dict: 
        u_boot.uart_init (reg_sets[segment_dict['UART_INIT']['FROM']:segment_dict['UART_INIT']['TO']])
    if 'UART_XMIT' in segment_dict: 
        u_boot.uart_transmit (reg_sets[segment_dict['UART_XMIT']['FROM']:segment_dict['UART_XMIT']['TO']])
        u_boot.make_ddrc_register_dump()
        u_boot.make_slcr_register_dump()
    #if not u_boot.features.get_par_value_or_none('BOOT_DEBUG') is None:
        
    if 'DCI' in segment_dict: 
        u_boot.dci_calibration(reg_sets[segment_dict['DCI']['FROM']:segment_dict['DCI']['TO']])
    if 'DDR_START' in segment_dict: 
        u_boot.ddr_start      (reg_sets[segment_dict['DDR_START']['FROM']:segment_dict['DDR_START']['TO']])
    if 'DDRC_STA' in segment_dict: 
        u_boot.ddrc_wait_empty_queue(reg_sets[segment_dict['DDRC_STA']['FROM']:segment_dict['DDRC_STA']['TO']])
    
    u_boot.make_arch_cpu_init()
    u_boot.output_c_file(args.lowlevel)
#    print u_boot.get_c_file()
