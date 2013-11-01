#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# Definitions of Zynq DDRIOB registers 
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
# DDRIOB Registers
DDRIOB_DEFS={ #not all fields are defined currently
    'BASE_ADDR':(0xF8000000,), # SLCR 
    'MODULE_NAME':('slcr',),
    'ddriob_addr0':               {'OFFS': 0xb40,'DFLT':0x00000800,'RW':'RW', #0x600
                                   'COMMENTS':'DDR IOB config for A[0:14], CKE and DRST_B',
                                   'FIELDS':{
                  'reserved1':                {'r':(12,31),'d':0,  'c':'Reserved'},
                  'pullup_en':                {'r':(11,11),'d':0x1,'c':'Pullup on outputs 1- enabled, 0 - disabled'}, #0
                  'output_en':                {'r':( 9,10),'d':0,  'c':'Output enable tied to 0 - ibuf, 3 - obuf, 1,2 - reserved'}, #3
                  'term_disable_mode':        {'r':( 8, 8),'d':0,  'c':'0 - termination always enabled (should be during init/training), 1 - use dynamic on/off'},
                  'ibuf_disable_mode':        {'r':( 7, 7),'d':0,  'c':'0 - ibuf enabled (should be  during init/training), 1 - dynamic'},
                  'dci_type':                 {'r':( 5, 6),'d':0,  'c':'0 - DCI disabled (DDR2/3L ADDR, CLK), 1 DCI DRIVE LPDDR2, 2 - reserved, 3 - DCI term (DDR2/3/3L DQ, DQS'},
                  'term_en':                  {'r':( 4, 4),'d':0,  'c':'1 - tri-state termination enabled, 0 - disabled'},
                  'dci_update_b':             {'r':( 3, 3),'d':0,  'c':'1 - DCI update enabled, 0 - disabled'},
                  'inp_type':                 {'r':( 1, 2),'d':0,  'c':'Input buffer control: 0 - off, 1 - Vref based (sstl, hstl), 2 - diff rcv, 3 - LVCMOS rcv'},
                  'inp_power':                {'r':( 0, 0),'d':0,  'c':'Reserved'}}},
    'ddriob_addr1':               {'OFFS': 0xb44,'DFLT':0x00000800,'RW':'RW', #0x600
                                   'COMMENTS':'DDR IOB config for BA[0:2], ODT, CS, WE, RAS, CAS',
                                   'FIELDS':{
                  'reserved1':                {'r':(12,31),'d':0,  'c':'Reserved'},
                  'pullup_en':                {'r':(11,11),'d':0x1,'c':'Pullup on outputs 1- enabled, 0 - disabled'}, #0
                  'output_en':                {'r':( 9,10),'d':0,  'c':'Output enable tied to 0 - ibuf, 3 - obuf, 1,2 - reserved'}, #3
                  'term_disable_mode':        {'r':( 8, 8),'d':0,  'c':'0 - termination always enabled (should be during init/training), 1 - use dynamic on/off'},
                  'ibuf_disable_mode':        {'r':( 7, 7),'d':0,  'c':'0 - ibuf enabled (should be  during init/training), 1 - dynamic'},
                  'dci_type':                 {'r':( 5, 6),'d':0,  'c':'0 - DCI disabled (DDR2/3L ADDR, CLK), 1 DCI DRIVE LPDDR2, 2 - reserved, 3 - DCI term (DDR2/3/3L DQ, DQS'},
                  'term_en':                  {'r':( 4, 4),'d':0,  'c':'1 - tri-state termination enabled, 0 - disabled'},
                  'dci_update_b':             {'r':( 3, 3),'d':0,  'c':'1 - DCI update enabled, 0 - disabled'},
                  'inp_type':                 {'r':( 1, 2),'d':0,  'c':'Input buffer control: 0 - off, 1 - Vref based (sstl, hstl), 2 - diff rcv, 3 - LVCMOS rcv'},
                  'inp_power':                {'r':( 0, 0),'d':0,  'c':'Reserved'}}},
    'ddriob_data0':               {'OFFS': 0xb48,'DFLT':0x00000800,'RW':'RW', #0x672
                                   'COMMENTS':'DDR IOB config for data[0:15]',
                                   'FIELDS':{
                  'reserved1':                {'r':(12,31),'d':0,  'c':'Reserved'},
                  'pullup_en':                {'r':(11,11),'d':0x1,'c':'Pullup on outputs 1- enabled, 0 - disabled'}, #0
                  'output_en':                {'r':( 9,10),'d':0,  'c':'Output enable tied to 0 - ibuf, 3 - obuf, 1,2 - reserved'}, #3
                  'term_disable_mode':        {'r':( 8, 8),'d':0,  'c':'0 - termination always enabled (should be during init/training), 1 - use dynamic on/off'},
                  'ibuf_disable_mode':        {'r':( 7, 7),'d':0,  'c':'0 - ibuf enabled (should be  during init/training), 1 - dynamic'},
                  'dci_type':                 {'r':( 5, 6),'d':0,  'c':'0 - DCI disabled (DDR2/3L ADDR, CLK), 1 DCI DRIVE LPDDR2, 2 - reserved, 3 - DCI term (DDR2/3/3L DQ, DQS'}, #3
                  'term_en':                  {'r':( 4, 4),'d':0,  'c':'1 - tri-state termination enabled, 0 - disabled'}, #1
                  'dci_update_b':             {'r':( 3, 3),'d':0,  'c':'1 - DCI update enabled, 0 - disabled'},
                  'inp_type':                 {'r':( 1, 2),'d':0,  'c':'Input buffer control: 0 - off, 1 - Vref based (sstl, hstl), 2 - diff rcv, 3 - LVCMOS rcv'},#1
                  'inp_power':                {'r':( 0, 0),'d':0,  'c':'Reserved'}}},
    'ddriob_data1':               {'OFFS': 0xb4C,'DFLT':0x00000800,'RW':'RW', #0x672
                                   'COMMENTS':'DDR IOB config for data[16:31]',
                                   'FIELDS':{
                  'reserved1':                {'r':(12,31),'d':0,  'c':'Reserved'},
                  'pullup_en':                {'r':(11,11),'d':0x1,'c':'Pullup on outputs 1- enabled, 0 - disabled'}, #0
                  'output_en':                {'r':( 9,10),'d':0,  'c':'Output enable tied to 0 - ibuf, 3 - obuf, 1,2 - reserved'}, #3
                  'term_disable_mode':        {'r':( 8, 8),'d':0,  'c':'0 - termination always enabled (should be during init/training), 1 - use dynamic on/off'}, 
                  'ibuf_disable_mode':        {'r':( 7, 7),'d':0,  'c':'0 - ibuf enabled (should be  during init/training), 1 - dynamic'},
                  'dci_type':                 {'r':( 5, 6),'d':0,  'c':'0 - DCI disabled (DDR2/3L ADDR, CLK), 1 DCI DRIVE LPDDR2, 2 - reserved, 3 - DCI term (DDR2/3/3L DQ, DQS'}, #3
                  'term_en':                  {'r':( 4, 4),'d':0,  'c':'1 - tri-state termination enabled, 0 - disabled'}, #1
                  'dci_update_b':             {'r':( 3, 3),'d':0,  'c':'1 - DCI update enabled, 0 - disabled'},
                  'inp_type':                 {'r':( 1, 2),'d':0,  'c':'Input buffer control: 0 - off, 1 - Vref based (sstl, hstl), 2 - diff rcv, 3 - LVCMOS rcv'}, #1
                  'inp_power':                {'r':( 0, 0),'d':0,  'c':'Reserved'}}},
    'ddriob_diff0':               {'OFFS': 0xb50,'DFLT':0x00000800,'RW':'RW', #0x674
                                   'COMMENTS':'DDR IOB config for DQS[0:1]',
                                   'FIELDS':{
                  'reserved1':                {'r':(12,31),'d':0,  'c':'Reserved'},
                  'pullup_en':                {'r':(11,11),'d':0x1,'c':'Pullup on outputs 1- enabled, 0 - disabled'}, #0
                  'output_en':                {'r':( 9,10),'d':0,  'c':'Output enable tied to 0 - ibuf, 3 - obuf, 1,2 - reserved'}, #3
                  'term_disable_mode':        {'r':( 8, 8),'d':0,  'c':'0 - termination always enabled (should be during init/training), 1 - use dynamic on/off'},
                  'ibuf_disable_mode':        {'r':( 7, 7),'d':0,  'c':'0 - ibuf enabled (should be  during init/training), 1 - dynamic'},
                  'dci_type':                 {'r':( 5, 6),'d':0,  'c':'0 - DCI disabled (DDR2/3L ADDR, CLK), 1 DCI DRIVE LPDDR2, 2 - reserved, 3 - DCI term (DDR2/3/3L DQ, DQS'}, #3
                  'term_en':                  {'r':( 4, 4),'d':0,  'c':'1 - tri-state termination enabled, 0 - disabled'}, #1 
                  'dci_update_b':             {'r':( 3, 3),'d':0,  'c':'1 - DCI update enabled, 0 - disabled'},
                  'inp_type':                 {'r':( 1, 2),'d':0,  'c':'Input buffer control: 0 - off, 1 - Vref based (sstl, hstl), 2 - diff rcv, 3 - LVCMOS rcv'}, #2
                  'inp_power':                {'r':( 0, 0),'d':0,  'c':'Reserved'}}},
    'ddriob_diff1':               {'OFFS': 0xb54,'DFLT':0x00000800,'RW':'RW', #0x674
                                   'COMMENTS':'DDR IOB config for DQS[2:3]',
                                   'FIELDS':{
                  'reserved1':                {'r':(12,31),'d':0,  'c':'Reserved'},
                  'pullup_en':                {'r':(11,11),'d':0x1,'c':'Pullup on outputs 1- enabled, 0 - disabled'}, #0
                  'output_en':                {'r':( 9,10),'d':0,  'c':'Output enable tied to 0 - ibuf, 3 - obuf, 1,2 - reserved'}, #3
                  'term_disable_mode':        {'r':( 8, 8),'d':0,  'c':'0 - termination always enabled (should be during init/training), 1 - use dynamic on/off'},
                  'ibuf_disable_mode':        {'r':( 7, 7),'d':0,  'c':'0 - ibuf enabled (should be  during init/training), 1 - dynamic'},
                  'dci_type':                 {'r':( 5, 6),'d':0,  'c':'0 - DCI disabled (DDR2/3L ADDR, CLK), 1 DCI DRIVE LPDDR2, 2 - reserved, 3 - DCI term (DDR2/3/3L DQ, DQS'}, #3
                  'term_en':                  {'r':( 4, 4),'d':0,  'c':'1 - tri-state termination enabled, 0 - disabled'}, #1
                  'dci_update_b':             {'r':( 3, 3),'d':0,  'c':'1 - DCI update enabled, 0 - disabled'},
                  'inp_type':                 {'r':( 1, 2),'d':0,  'c':'Input buffer control: 0 - off, 1 - Vref based (sstl, hstl), 2 - diff rcv, 3 - LVCMOS rcv'}, #2
                  'inp_power':                {'r':( 0, 0),'d':0,  'c':'Reserved'}}},
    'ddriob_clock':               {'OFFS': 0xb58,'DFLT':0x00000800,'RW':'RW', #use 0x600
                                   'COMMENTS':'DDR IOB config for clock output',
                                   'FIELDS':{
                  'reserved1':                {'r':(12,31),'d':0,  'c':'Reserved'},
                  'pullup_en':                {'r':(11,11),'d':0x1,'c':'Pullup on outputs 1- enabled, 0 - disabled '}, # 0
                  'output_en':                {'r':( 9,10),'d':0,  'c':'Output enable tied to 0 - ibuf, 3 - obuf, 1,2 - reserved'}, #3
                  'term_disable_mode':        {'r':( 8, 8),'d':0,  'c':'0 - termination always enabled (should be during init/training), 1 - use dynamic on/off'},
                  'ibuf_disable_mode':        {'r':( 7, 7),'d':0,  'c':'0 - ibuf enabled (should be  during init/training), 1 - dynamic'},
                  'dci_type':                 {'r':( 5, 6),'d':0,  'c':'0 - DCI disabled (DDR2/3L ADDR, CLK), 1 DCI DRIVE LPDDR2, 2 - reserved, 3 - DCI term (DDR2/3/3L DQ, DQS'},
                  'term_en':                  {'r':( 4, 4),'d':0,  'c':'1 - tri-state termination enabled, 0 - disabled'},
                  'dci_update_b':             {'r':( 3, 3),'d':0,  'c':'1 - DCI update enabled, 0 - disabled'},
                  'inp_type':                 {'r':( 1, 2),'d':0,  'c':'Input buffer control: 0 - off, 1 - Vref based (sstl, hstl), 2 - diff rcv, 3 - LVCMOS rcv'},
                  'inp_power':                {'r':( 0, 0),'d':0,  'c':'Reserved'}}},
    'ddriob_drive_slew_addr':               {'OFFS': 0xb5c,'DFLT':0,'RW':'RW', #0xd6861c
                                   'COMMENTS':'Drive/slew control for address and command pins, computed by a undisclosed Xilinx algorithm using silicon version and DDR standard, should be taken from TCL code',
                                   'FIELDS':{
                  'rterm':                    {'r':(27,31),'d':0,   'c':'Reserved'},
                  'gtl':                      {'r':(24,26),'d':0,   'c':'Reserved'},
                  'slew_n':                   {'r':(19,23),'d':0x1a,'c':'Reserved'},
                  'slew_p':                   {'r':(14,18),'d':0x1a,'c':'Reserved'},
                  'drive_n':                  {'r':( 7,13),'d':0xc, 'c':'Reserved'},
                  'drive_p':                  {'r':( 0, 6),'d':0x1c,'c':'Reserved'}}},
    'ddriob_drive_slew_data':                 {'OFFS': 0xb60,'DFLT':0,'RW':'RW', #0xf9861c
                                   'COMMENTS':'Drive/slew control for data pins, computed by a undisclosed Xilinx algorithm using silicon version and DDR standard, should be taken from TCL code',
                                   'FIELDS':{
                  'rterm':                    {'r':(27,31),'d':0,   'c':'Reserved'},
                  'gtl':                      {'r':(24,26),'d':0,   'c':'Reserved'},
                  'slew_n':                   {'r':(19,23),'d':0x1f,'c':'Reserved'},
                  'slew_p':                   {'r':(14,18),'d':0x6, 'c':'Reserved'},
                  'drive_n':                  {'r':( 7,13),'d':0xc, 'c':'Reserved'},
                  'drive_p':                  {'r':( 0, 6),'d':0x1c,'c':'Reserved'}}},
    'ddriob_drive_slew_diff':               {'OFFS': 0xb64,'DFLT':0,'RW':'RW',  #0xf9861c
                                   'COMMENTS':'Drive/slew control for differential DQS pins, computed by a undisclosed Xilinx algorithm using silicon version and DDR standard, should be taken from TCL code',
                                   'FIELDS':{
                  'rterm':                    {'r':(27,31),'d':0,   'c':'Reserved'},
                  'gtl':                      {'r':(24,26),'d':0,   'c':'Reserved'},
                  'slew_n':                   {'r':(19,23),'d':0x1f,'c':'Reserved'},
                  'slew_p':                   {'r':(14,18),'d':0x6, 'c':'Reserved'},
                  'drive_n':                  {'r':( 7,13),'d':0xc, 'c':'Reserved'},
                  'drive_p':                  {'r':( 0, 6),'d':0x1c,'c':'Reserved'}}},
    'ddriob_drive_slew_clock':               {'OFFS': 0xb68,'DFLT':0,'RW':'RW', #0xd6861c
                                   'COMMENTS':'Drive/slew control for differential DQS pins, computed by a undisclosed Xilinx algorithm using silicon version and DDR standard, should be taken from TCL code',
                                   'FIELDS':{
                  'rterm':                    {'r':(27,31),'d':0,   'c':'Reserved'},
                  'gtl':                      {'r':(24,26),'d':0,   'c':'Reserved'},
                  'slew_n':                   {'r':(19,23),'d':0x1a,'c':'Reserved'},
                  'slew_p':                   {'r':(14,18),'d':0x1a,'c':'Reserved'},
                  'drive_n':                  {'r':( 7,13),'d':0xc, 'c':'Reserved'},
                  'drive_p':                  {'r':( 0, 6),'d':0x1c,'c':'Reserved'}}},
    'ddriob_ddr_ctrl':                       {'OFFS': 0xb6C,'DFLT':0x0,'RW':'RW', #0xe60
                                   'COMMENTS':'DDR IOB buffer control',
                                   'FIELDS':{
                  'reserved1':                {'r':(15,31),'d':0,  'c':'Reserved'},
                  'cke_pullup_en':            {'r':(14,14),'d':0,  'c':'Reserved'},
                  'drst_b_pullup_en':         {'r':(13,13),'d':0,  'c':'Reserved'},
                  'refio_pullup_en':          {'r':(12,12),'d':0,  'c':'Reserved'},
                  'refio_test':               {'r':(10,11),'d':0,  'c':'Reserved'}, #3/0 - changing
                  'refio_en':                 {'r':( 9, 9),'d':0,  'c':'1 - use VRP/VRN, 0 - ignore'}, #1
                  'vref_pullup_en':           {'r':( 7, 8),'d':0,  'c':'Reserved'},
                  'vref_ext_en':              {'r':( 5, 6),'d':0,  'c':'+1 - enable external Vref for dq[0:15], +2 - en Vref for dq[16:31]'}, #3
                  'vref_sel':                 {'r':( 1, 4),'d':0,  'c':'Vref: 0 -off,  1 - 1.2/2V (LPDDR2), 2 - 1.35/2V (DDR3L), 4 - 1.5/2(DDR3), 8 - 1.8/2V(DDR2)'},
                  'vref_int_en':              {'r':( 0, 0),'d':0,  'c':'1 - enable internal Vref'}}},
    'ddriob_dci_ctrl':                       {'OFFS': 0xb70,'DFLT':0x20,'RW':'RW', #0x823
                                   'COMMENTS':'DDR IOB DCI Config',
                                   'FIELDS':{
                  'reserved1':                {'r':(27,31),'d':0,  'c':'Reserved'},
                  'int_dci_en':               {'r':(26,26),'d':0,  'c':'Reserved'},
                  'tst_rst':                  {'r':(25,25),'d':0,  'c':'Reserved'},
                  'tst_hlp':                  {'r':(24,24),'d':0,  'c':'Reserved'},
                  'tst_hln':                  {'r':(23,23),'d':0,  'c':'Reserved'},
                  'tst_clk':                  {'r':(22,22),'d':0,  'c':'Reserved'},
                  'init_complete':            {'r':(21,21),'d':0,  'c':'Reserved'},
                  'update_control':           {'r':(20,20),'d':0,  'c':'DCI update mode - use values in the Calibration Table'},
                  'pref_opt2':                {'r':(17,19),'d':0,  'c':'DCI Calibration mode - use values in the Calibration Table'},
                  'pref_opt1':                {'r':(14,16),'d':0,  'c':'14:15 - DCI Calibration mode - use values in the Calibration Table'},
                  'nref_opt4':                {'r':(11,13),'d':0,  'c':'DCI Calibration mode - use values in the Calibration Table'},   #1
                  'nref_opt2':                {'r':( 8,10),'d':0,  'c':'DCI Calibration mode - use values in the Calibration Table'},
                  'nref_opt1':                {'r':( 6, 7),'d':0,  'c':'DCI Calibration mode - use values in the Calibration Table'},
                  'vrn_out':                  {'r':( 5, 5),'d':1,  'c':'1 for silicon 1,2; unused (0) for silicon 3'},   #1
                  'vrp_out':                  {'r':( 4, 4),'d':0,  'c':'Reserved'},
                  'vrn_tri':                  {'r':( 3, 3),'d':0,  'c':'Reserved'},
                  'vrp_tri':                  {'r':( 2, 2),'d':0,  'c':'Reserved'},
                  'enable':                   {'r':( 1, 1),'d':0,  'c':'DCI System enable. Silicon v2+ require set to 1'},   #1
                  'reset':                    {'r':( 0, 0),'d':0,  'c':'Toggle once to initialize FF-s in DCI system.'}}}, #1
             # reset is mentioned as DDRIOB_DCI_CNTRL_RESET_B , so it is active LOW
    'ddriob_dci_status':                      {'OFFS': 0xb74,'DFLT':0x0,'RW':'RW', #0x823
                                   'COMMENTS':'DDR IOB buffer DCI status',
                                   'FIELDS':{
                  'reserved1':                {'r':(14,31),'d':0,'m':'R',  'c':'Reserved'},
                  'done':                     {'r':(13,13),'d':0,          'c':'DCI done'},
                  'reserved2':                {'r':(12,12),'d':0,          'c':'Reserved'},
                  'reserved3':                {'r':(11,11),'d':0,          'c':'Reserved'},
                  'reserved4':                {'r':(10,10),'d':0,'m':'R',  'c':'Reserved'},
                  'reserved5':                {'r':( 9, 9),'d':0,'m':'R',  'c':'Reserved'},
                  'reserved6':                {'r':( 8, 8),'d':0,'m':'R',  'c':'Reserved'},
                  'reserved7':                {'r':( 7, 7),'d':0,'m':'R',  'c':'Reserved'},
                  'reserved8':                {'r':( 6, 6),'d':0,'m':'R',  'c':'Reserved'},
                  'reserved9':                {'r':( 5, 5),'d':0,'m':'R',  'c':'Reserved'},
                  'reserved10':               {'r':( 3, 4),'d':0,'m':'R',  'c':'Reserved'},
                  'reserved11':               {'r':( 2, 2),'d':0,'m':'R',  'c':'Reserved'},
                  'reserved12':               {'r':( 1, 1),'d':0,'m':'R',  'c':'Reserved'},
                  'lock':                     {'r':( 0, 0),'d':0,'m':'R',  'c':'DCI status input'}}},
    }
