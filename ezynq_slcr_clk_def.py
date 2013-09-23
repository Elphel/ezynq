#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# Definitions of Zynq SLCR clock-related registers 
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
SLCR_CLK_DEFS={ #not all fields are defined currently
    'BASE_ADDR':(0xF8000000,), # SLCR
    'MODULE_NAME':('slcr',),
      'scl':                      {'OFFS': 0x000,'DFLT':0x0,'RW':'RW',
                                   'COMMENTS':'Secure configurqation lock (no way to unlock until POR)',
                                   'FIELDS':{
                  'lock':                     {'r':(0,0),'d':0,  'c':'1 - lock (locker on R) write to scl,pss_rst,apu_ctrl,wdt_clk_sel'}}},
      'slcr_lock':                {'OFFS': 0x004,'DFLT':0x0,'RW':'W',
                                   'COMMENTS':'SLCR write protection lock',
                                   'FIELDS':{
                  'lock_key':                 {'r':( 0,15),'d':0x0,'m':'W',  'c':'Write 0x767b to disable write to 0xf800000...0xf8000b74'}}},
      'slcr_unlock':              {'OFFS': 0x008,'DFLT':0x0,'RW':'W',
                                   'COMMENTS':'SLCR write protection unlock',
                                   'FIELDS':{
                  'unlock_key':               {'r':( 0,15),'d':0x0,'m':'W',  'c':'Write 0xdf0d to enable write to 0xf800000...0xf8000b74'}}},
                  
      'slcr_locksta':             {'OFFS': 0x00c,'DFLT':0x1,'RW':'RO',
                                   'COMMENTS':'SLCR write protection status',
                                   'FIELDS':{
                  'lock_status':              {'r':( 0, 0),'d':0x1,'m':'R',  'c':'0 - registers are write-enabled, 1 - registers are protected from write'}}},
                  
      'arm_pll_ctrl':             {'OFFS': 0x100,'DFLT':0x1a008,'RW':'RW', # 0x28000 (fb only)
                                   'COMMENTS':'ARM PLL Control',
                                   'FIELDS':{
                  'reserved1':                {'r':(19,31),'d':0,   'c':'reserved'},
                  'pll_fdiv':                 {'r':(12,18),'d':0x1a,'c':'Feedback divisor. Before changing, PLL must be bypassed and then reset'}, #0x28
                  'reserved2':                {'r':( 5,11),'d':0,   'c':'reserved'},
                  'pll_bypass_force':         {'r':( 4, 4),'d':0,   'c':'Bypass override control: 1 - bypassed, 0: if pll_bypass_qual==0: enabled, not bypassed else depends on pin strap.'},
                  'pll_bypass_qual':          {'r':( 3, 3),'d':0x1, 'c':'Source of PLL bypass control: 0 - use pll_bypass_force, 1 - use pin strap (read as boot_mode[4])'},
                  'reserved3':                {'r':( 2, 2),'d':0,   'c':'reserved'},
                  'pll_pwrdwn':               {'r':( 1, 1),'d':0,   'c':'PLL power-down control: 0 - run, 1 - power down'},
                  'pll_reset':                {'r':( 0, 0),'d':0,   'c':'PLL reset: 0 - operate, 1 - reset'}}},
                  
      'ddr_pll_ctrl':             {'OFFS': 0x104,'DFLT':0x1a008,'RW':'RW', # 0x20000  (fb only)
                                   'COMMENTS':'DDR PLL Control',
                                   'FIELDS':{
                  'reserved1':                {'r':(19,31),'d':0,   'c':'reserved'},
                  'pll_fdiv':                 {'r':(12,18),'d':0x1a,'c':'Feedback divisor. Before changing, PLL must be bypassed and then reset'}, # 0x20
                  'reserved2':                {'r':( 5,11),'d':0,   'c':'reserved'},
                  'pll_bypass_force':         {'r':( 4, 4),'d':0,   'c':'Bypass override control: 1 - bypassed, 0: if pll_bypass_qual==0: enabled, not bypassed else depends on pin strap.'},
                  'pll_bypass_qual':          {'r':( 3, 3),'d':0x1, 'c':'Source of PLL bypass control: 0 - use pll_bypass_force, 1 - use pin strap (read as boot_mode[4])'},
                  'reserved3':                {'r':( 2, 2),'d':0,   'c':'reserved'},
                  'pll_pwrdwn':               {'r':( 1, 1),'d':0,   'c':'PLL power-down control: 0 - run, 1 - power down'},
                  'pll_reset':                {'r':( 0, 0),'d':0,   'c':'PLL reset: 0 - operate, 1 - reset'}}},
                  
      'io_pll_ctrl':              {'OFFS': 0x108,'DFLT':0x1a008,'RW':'RW', # 0x1e0000  (fb only)
                                   'COMMENTS':'IO PLL Control',
                                   'FIELDS':{
                  'reserved1':                {'r':(19,31),'d':0,   'c':'reserved'},
                  'pll_fdiv':                 {'r':(12,18),'d':0x1a,'c':'Feedback divisor. Before changing, PLL must be bypassed and then reset'}, # 0x1e
                  'reserved2':                {'r':( 5,11),'d':0,   'c':'reserved'},
                  'pll_bypass_force':         {'r':( 4, 4),'d':0,   'c':'Bypass override control: 1 - bypassed, 0: if pll_bypass_qual==0: enabled, not bypassed else depends on pin strap.'},
                  'pll_bypass_qual':          {'r':( 3, 3),'d':0x1, 'c':'Source of PLL bypass control: 0 - use pll_bypass_force, 1 - use pin strap (read as boot_mode[4])'},
                  'reserved3':                {'r':( 2, 2),'d':0,   'c':'reserved'},
                  'pll_pwrdwn':               {'r':( 1, 1),'d':0,   'c':'PLL power-down control: 0 - run, 1 - power down'},
                  'pll_reset':                {'r':( 0, 0),'d':0,   'c':'PLL reset: 0 - operate, 1 - reset'}}},
                  
      'pll_status':               {'OFFS': 0x10c,'DFLT':0x3f,'RW':'RO', # _____________
                                   'COMMENTS':'PLL status',
                                   'FIELDS':{
                  'io_pll_stable':            {'r':( 5, 5),'d':0x1, 'm':'R',  'c':'IO PLL 1 - locked or bypassed, 0 - not locked and not bypassed'},
                  'ddr_pll_stable':           {'r':( 4, 4),'d':0x1, 'm':'R',  'c':'DDR PLL 1 - locked or bypassed, 0 - not locked and not bypassed'},
                  'arm_pll_stable':           {'r':( 3, 3),'d':0x1, 'm':'R',  'c':'ARM PLL 1 - locked or bypassed, 0 - not locked and not bypassed'},
                  'io_pll_lock':              {'r':( 2, 2),'d':0x1, 'm':'R',  'c':'IO PLL 1 - locked , 0 - not locked'},
                  'ddr_pll_lock':             {'r':( 1, 1),'d':0x1, 'm':'R',  'c':'DDR PLL 1 - locked , 0 - not locked'},
                  'arm_pll_lock':             {'r':( 0, 0),'d':0x1, 'm':'R',  'c':'ARM PLL 1 - locked , 0 - not locked'}}},
    
      'arm_pll_cfg':              {'OFFS': 0x110,'DFLT':0x177ea0,'RW':'RW', # 0xfa220
                                   'COMMENTS':'ARM PLL Configuration',
                                   'FIELDS':{
                  'reserved1':                {'r':(22,31),'d':0,     'c':'reserved'},
                  'lock_cnt':                 {'r':(12,21),'d':0x177, 'c':'Lock status bit delay (in clock cycles)'}, # reference or output clock cycles? 0xfa
                  'pll_cp':                   {'r':( 8,11),'d':0xe,   'c':'PLL charge pump control'},          # 0x2
                  'pll_res':                  {'r':( 4, 7),'d':0xa,   'c':'PLL loop filter resistor control'}, # 0x2
                  'reserved2':                {'r':( 0, 3),'d':0,     'c':'reserved'}}},
    
      'ddr_pll_cfg':              {'OFFS': 0x114,'DFLT':0x177ea0,'RW':'RW', # 0x12c220
                                   'COMMENTS':'DDR PLL Configuration',
                                   'FIELDS':{
                  'reserved1':                {'r':(22,31),'d':0,     'c':'reserved'},
                  'lock_cnt':                 {'r':(12,21),'d':0x177, 'c':'Lock status bit delay (in clock cycles)'}, # reference or output clock cycles? 0x12c
                  'pll_cp':                   {'r':( 8,11),'d':0xe,   'c':'PLL charge pump control'},          # 0x2
                  'pll_res':                  {'r':( 4, 7),'d':0xa,   'c':'PLL loop filter resistor control'}, # 0x2
                  'reserved2':                {'r':( 0, 3),'d':0,     'c':'reserved'}}},

      'io_pll_cfg':               {'OFFS': 0x118,'DFLT':0x177ea0,'RW':'RW', # 0x1452c0
                                   'COMMENTS':'IO PLL Configuration',
                                   'FIELDS':{
                  'reserved1':                {'r':(22,31),'d':0,     'c':'reserved'},
                  'lock_cnt':                 {'r':(12,21),'d':0x177, 'c':'Lock status bit delay (in clock cycles)'}, # reference or output clock cycles? 0x145
                  'pll_cp':                   {'r':( 8,11),'d':0xe,   'c':'PLL charge pump control'},                 # 0x2
                  'pll_res':                  {'r':( 4, 7),'d':0xa,   'c':'PLL loop filter resistor control'},        # 0xc
                  'reserved2':                {'r':( 0, 3),'d':0,     'c':'reserved'}}},

      'arm_clk_ctrl':             {'OFFS': 0x120,'DFLT':0x1f000400,'RW':'RW', # 0x1f000200
                                   'COMMENTS':'CPU clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(29,31),'d':0,     'c':'reserved'},
                  'cpu_peri_clkact':          {'r':(28,28),'d':0x1,   'c':'Peripheral clock active (0 - disabled)'},# 1
                  'cpu_1x_clkact':            {'r':(27,27),'d':0x1,   'c':'CPU-1x clock active (0 - disabled)'},    # 1
                  'cpu_2x_clkact':            {'r':(26,26),'d':0x1,   'c':'CPU-2x clock active (0 - disabled)'},    # 1
                  'cpu_3x2x_clkact':          {'r':(25,25),'d':0x1,   'c':'CPU-3x2x clock active (0 - disabled)'},  # 1
                  'cpu_6x4x_clkact':          {'r':(24,24),'d':0x1,   'c':'CPU-6x4x clock active (0 - disabled)'},  # 1
                  'reserved2':                {'r':(14,23),'d':0,     'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x4,   'c':'Frequency divisor for the CPU clock source. If PLL is NOT bypassed values 1 and 3 are invalid'}, #0x2
                  'reserved3':                {'r':( 6, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0x0,   'c':'CPU clock source: 0,1 - ARM PLL, 2 - DDR PLL, 3 - IO PLL, This filed is reset by POR only'},     #0x0
                  'reserved4':                {'r':( 6, 7),'d':0,     'c':'reserved'}}},

      'ddr_clk_ctrl':             {'OFFS': 0x124,'DFLT':0x18400003,'RW':'RW', # 0xc200003
                                   'COMMENTS':'DDR_3x (including PHY) and DDR_2X clock control',
                                   'FIELDS':{
                  'ddr_2x_clk_divisor':       {'r':(26,31),'d':0x6,   'c':'Frequency divisor for ddr_2x clk'},  # 0x3
                  'ddr_3x_clk_divisor':       {'r':(20,25),'d':0x4,   'c':'Frequency divisor for ddr_3x clk'},  # 0x2
                  'reserved1':                {'r':( 2,19),'d':0,     'c':'reserved'},
                  'ddr_2x_clkact':            {'r':( 1, 1),'d':0x1,   'c':'1 - ddr_2x clk enabled (0 - disabled)'},  # 0x1
                  'ddr_3x_clkact':            {'r':( 0, 0),'d':0x1,   'c':'1 - ddr_3x clk enabled (0 - disabled)'}}},# 0x1

      'dci_clk_ctrl':             {'OFFS': 0x128,'DFLT':0x18400003,'RW':'RW', # 0x302301
                                   'COMMENTS':'DDR DCI clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,     'c':'reserved'},
                  'divisor1':                 {'r':(20,25),'d':0x1e,  'c':'Frequency divisor, second stage'},       # 0x3
                  'reserved2':                {'r':(14,19),'d':0,     'c':'reserved'},
                  'divisor0':                 {'r':( 8,13),'d':0x32,  'c':'Frequency divisor, first stage'},        # 0x23
                  'reserved3':                {'r':( 1, 7),'d':0,     'c':'reserved'},
                  'clkact':                   {'r':( 0, 0),'d':0x1,   'c':'1 - dci clock enabled (0 - disabled)'}}},# 0x1

      'aper_clk_ctrl':            {'OFFS': 0x12c,'DFLT':0x01ffcccd, 'RW':'RW', # 0x01ec044d (set after peripherals)
                                   'COMMENTS':'AMBA peripherals clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(25,31),'d':0,     'c':'reserved'},
                  'smc_cpu_1x_clkact':        {'r':(24,24),'d':0x1,   'c':'SMC AMBA clock control (1- enabled, 0- disabled)'},        # 0x1
                  'lqspi_cpu_1x_clkact':      {'r':(23,23),'d':0x1,   'c':'QSPI AMBA clock control (1- enabled, 0- disabled)'},       # 0x1
                  'gpio_cpu_1x_clkact':       {'r':(22,22),'d':0x1,   'c':'GPIO AMBA clock control (1- enabled, 0- disabled)'},       # 0x1
                  'uart1_cpu_1x_clkact':      {'r':(21,21),'d':0x1,   'c':'UART1 AMBA clock control (1- enabled, 0- disabled)'},      # 0x1
                  'uart0_cpu_1x_clkact':      {'r':(20,20),'d':0x1,   'c':'UART0 AMBA clock control (1- enabled, 0- disabled)'},      # 0x0
                  'i2c1_cpu_1x_clkact':       {'r':(19,19),'d':0x1,   'c':'I2C1 AMBA clock control (1- enabled, 0- disabled)'},       # 0x1
                  'i2c0_cpu_1x_clkact':       {'r':(18,18),'d':0x1,   'c':'I2C0 AMBA clock control (1- enabled, 0- disabled)'},       # 0x1
                  'can1_cpu_1x_clkact':       {'r':(17,17),'d':0x1,   'c':'CAN1 AMBA clock control (1- enabled, 0- disabled)'},       # 0x0
                  'can0_cpu_1x_clkact':       {'r':(16,16),'d':0x1,   'c':'CAN0 AMBA clock control (1- enabled, 0- disabled)'},       # 0x0
                  'spi1_cpu_1x_clkact':       {'r':(15,15),'d':0x1,   'c':'SPI1 AMBA clock control (1- enabled, 0- disabled)'},       # 0x0
                  'spi0_cpu_1x_clkact':       {'r':(14,14),'d':0x1,   'c':'SPI0 AMBA clock control (1- enabled, 0- disabled)'},       # 0x0
                  'reserved2':                {'r':(13,13),'d':0,     'c':'reserved'},
                  'reserved3':                {'r':(12,12),'d':0,     'c':'reserved'},
                  'sdi1_cpu_1x_clkact':       {'r':(11,11),'d':0x1,   'c':'SDIO 1 AMBA clock control (1- enabled, 0- disabled)'},       # 0x0
                  'sdi0_cpu_1x_clkact':       {'r':(10,10),'d':0x1,   'c':'SDI0 0 AMBA clock control (1- enabled, 0- disabled)'},       # 0x1
                  'reserved4':                {'r':( 9, 9),'d':0,     'c':'reserved'},
                  'reserved5':                {'r':( 8, 8),'d':0,     'c':'reserved'},
                  'gem1_cpu_1x_clkact':       {'r':( 7, 7),'d':0x1,   'c':'Gigabit Ethernet 1 AMBA clock control (1- enabled, 0- disabled)'}, # 0x0
                  'gem0_cpu_1x_clkact':       {'r':( 6, 6),'d':0x1,   'c':'Gigabit Ethernet 0 AMBA clock control (1- enabled, 0- disabled)'}, # 0x1
                  'reserved6':                {'r':( 5, 5),'d':0,     'c':'reserved'},
                  'reserved7':                {'r':( 4, 4),'d':0,     'c':'reserved'},
                  'usb1_cpu_1x_clkact':       {'r':( 3, 3),'d':0x1,   'c':'USB1 AMBA clock control (1- enabled, 0- disabled)'},       # 0x1
                  'usb0_cpu_1x_clkact':       {'r':( 2, 2),'d':0x1,   'c':'USB0 AMBA clock control (1- enabled, 0- disabled)'},       # 0x1
                  'reserved8':                {'r':( 1, 1),'d':0,     'c':'reserved'},
                  'dma_cpu_2x_clkact':        {'r':( 0, 0),'d':0x1,   'c':'DMA controller AMBA clock control (1- enabled, 0- disabled)'}}},# 0x1
      'usb0_clk_ctrl':            {'OFFS': 0x130,'DFLT':0x00101941,'RW':'RW', # never modified
                                   'COMMENTS':'USB 0 ULPI clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,    'c':'reserved'},
                  'reserved2':                {'r':(20,25),'d':0x1,  'c':'reserved'},
                  'reserved3':                {'r':(14,19),'d':0,    'c':'reserved'},
                  'reserved4':                {'r':( 8,13),'d':0x19, 'c':'reserved'},
                  'reserved5':                {'r':( 7, 7),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 6),'d':0x4,  'c':'Source selection for the USB0 ULPI clock: b1xx: top level MIO USB0 ULPI clock'},
                  'reserved6':                {'r':( 1, 3),'d':0,    'c':'reserved'},
                  'reserved7':                {'r':( 0, 0),'d':0x1,  'c':'reserved'}}},
      'usb1_clk_ctrl':            {'OFFS': 0x134,'DFLT':0x00101941,'RW':'RW', # never modified
                                   'COMMENTS':'USB 1 ULPI clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,    'c':'reserved'},
                  'reserved2':                {'r':(20,25),'d':0x1,  'c':'reserved'},
                  'reserved3':                {'r':(14,19),'d':0,    'c':'reserved'},
                  'reserved4':                {'r':( 8,13),'d':0x19, 'c':'reserved'},
                  'reserved5':                {'r':( 7, 7),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 6),'d':0x4,  'c':'Source selection for the USB1 ULPI clock: b1xx: top level MIO USB1 ULPI clock'},
                  'reserved6':                {'r':( 1, 3),'d':0,    'c':'reserved'},
                  'reserved7':                {'r':( 0, 0),'d':0x1,  'c':'reserved'}}},
                  
      'gem0_rclk_ctrl':           {'OFFS': 0x138,'DFLT':0x1,'RW':'RW', # 0x1
                                   'COMMENTS':'Gigabit Ethernet 0 RX clock and RX signals select',
                                   'FIELDS':{
                  'reserved1':                {'r':( 5,31),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 4),'d':0,    'c':'Source for Rx clock, control and data: 0: MIO, 1 - EMIO'},
                  'reserved2':                {'r':( 1, 3),'d':0,    'c':'reserved'},
                  'clkact':                   {'r':( 0, 0),'d':0x1,  'c':'GigE 0 RX clock control: 0 - disable, 1: enable'}}}, #0x1
                  
      'gem1_rclk_ctrl':           {'OFFS': 0x13c,'DFLT':0x1,'RW':'RW', # never modified
                                   'COMMENTS':'Gigabit Ethernet 1 RX clock and RX signals select',
                                   'FIELDS':{
                  'reserved1':                {'r':( 5,31),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 4),'d':0,    'c':'Source for Rx clock, control and data: 0: MIO, 1 - EMIO'},
                  'reserved2':                {'r':( 1, 3),'d':0,    'c':'reserved'},
                  'clkact':                   {'r':( 0, 0),'d':0x1,  'c':'GigE 1 RX clock control: 0 - disable, 1: enable'}}},
                  
      'gem0_clk_ctrl':            {'OFFS': 0x140,'DFLT':0x3c01,'RW':'RW', # 0x100801
                                   'COMMENTS':'Gigabit Ethernet 0 Reference clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,     'c':'reserved'},
                  'divisor1':                 {'r':(20,25),'d':0x0,   'c':'Frequency divisor, second stage'},       # 0x1
                  'reserved2':                {'r':(14,19),'d':0,     'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x3c,  'c':'Frequency divisor, first stage'},        # 0x8
                  'reserved3':                {'r':( 7, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 6),'d':0,     'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL, 4..7-Ethernet Controller 0 EMIO clock'},        # 0x0
                  'reserved4':                {'r':( 1, 3),'d':0,     'c':'reserved'},
                  'clkact':                   {'r':( 0, 0),'d':0x1,   'c':'GigE controller reference clock 0: 1 -  enabled (0 - disabled)'}}},# 0x1
                  
      'gem1_clk_ctrl':            {'OFFS': 0x144,'DFLT':0x3c01,'RW':'RW', # Never set
                                   'COMMENTS':'Gigabit Ethernet 1  Reference clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,     'c':'reserved'},
                  'divisor1':                 {'r':(20,25),'d':0x0,   'c':'Frequency divisor, second stage'},
                  'reserved2':                {'r':(14,19),'d':0,     'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x3c,  'c':'Frequency divisor, first stage'}, 
                  'reserved3':                {'r':( 7, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 6),'d':0,     'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL, 4..7-Ethernet Controller 1 EMIO clock'}, 
                  'reserved4':                {'r':( 1, 3),'d':0,     'c':'reserved'},
                  'clkact':                   {'r':( 0, 0),'d':0x1,   'c':'GigE controller reference clock 0: 1 -  enabled (0 - disabled)'}}},

      'smc_clk_ctrl':            {'OFFS': 0x148,'DFLT':0x3c21,'RW':'RW', # Never modified
                                   'COMMENTS':'SMC Reference clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(14,31),'d':0,     'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x3c,  'c':'Frequency divisor'},
                  'reserved2':                {'r':( 6, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0x2,   'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'},
                  'reserved3':                {'r':( 1, 3),'d':0,     'c':'reserved'},
                  'clkact':                   {'r':( 0, 0),'d':0x1,   'c':'SMC reference clock: 1 -  enabled (0 - disabled)'}}},

      'lqspi_clk_ctrl':           {'OFFS': 0x14c,'DFLT':0x2821,'RW':'RW', # 0x721
                                   'COMMENTS':'Quad SPI Reference clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(14,31),'d':0,     'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x28,  'c':'Frequency divisor'}, #0x7
                  'reserved2':                {'r':( 6, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0x2,   'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'}, #0x2
                  'reserved3':                {'r':( 1, 3),'d':0,     'c':'reserved'},
                  'clkact':                   {'r':( 0, 0),'d':0x1,   'c':'Quad SPI reference clock: 1 -  enabled (0 - disabled)'}}}, #0x1

      'sdio_clk_ctrl':            {'OFFS': 0x150,'DFLT':0x1e03,'RW':'RW', # 0x801
                                   'COMMENTS':'SDIO 0,1 Reference clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(14,31),'d':0,    'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x1e, 'c':'Frequency divisor'}, #0x8
                  'reserved2':                {'r':( 6, 7),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0x0,  'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'},
                  'reserved3':                {'r':( 2, 3),'d':0,    'c':'reserved'},
                  'clkact1':                  {'r':( 1, 1),'d':0x1,  'c':'SDIO 1 reference clock: 1 -  enabled (0 - disabled)'},   #0
                  'clkact0':                  {'r':( 0, 0),'d':0x1,  'c':'SDIO 0 reference clock: 1 -  enabled (0 - disabled)'}}}, #1

      'uart_clk_ctrl':            {'OFFS': 0x154,'DFLT':0x3f03,'RW':'RW', # 0xa02
                                   'COMMENTS':'UART 0,1 Reference clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(14,31),'d':0,    'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x2f, 'c':'Frequency divisor'}, #0xa
                  'reserved2':                {'r':( 6, 7),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0x0,  'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'},
                  'reserved3':                {'r':( 2, 3),'d':0,    'c':'reserved'},
                  'clkact1':                  {'r':( 1, 1),'d':0x1,  'c':'UART 1 reference clock: 1 -  enabled (0 - disabled)'},   #1
                  'clkact0':                  {'r':( 0, 0),'d':0x1,  'c':'UART 0 reference clock: 1 -  enabled (0 - disabled)'}}}, #0

      'spi_clk_ctrl':             {'OFFS': 0x158,'DFLT':0x3f03,'RW':'RW', # Never set
                                   'COMMENTS':'SPI 0,1 Reference clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(14,31),'d':0,    'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x2f, 'c':'Frequency divisor'},
                  'reserved2':                {'r':( 6, 7),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0x0,  'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'},
                  'reserved3':                {'r':( 2, 3),'d':0,    'c':'reserved'},
                  'clkact1':                  {'r':( 1, 1),'d':0x1,  'c':'SPI 1 reference clock: 1 -  enabled (0 - disabled)'},
                  'clkact0':                  {'r':( 0, 0),'d':0x1,  'c':'SPI 0 reference clock: 1 -  enabled (0 - disabled)'}}},

      'can_clk_ctrl':             {'OFFS': 0x15c,'DFLT':0x501903,'RW':'RW', # Never set
                                   'COMMENTS':'CAN 0,1 Reference clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,    'c':'reserved'},
                  'divisor1':                 {'r':(20,25),'d':0x5,  'c':'Frequency divisor, second stage'},
                  'reserved2':                {'r':(14,19),'d':0,    'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0x19, 'c':'Frequency divisor'},
                  'reserved3':                {'r':( 6, 7),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0x0,  'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'},
                  'reserved4':                {'r':( 2, 3),'d':0,    'c':'reserved'},
                  'clkact1':                  {'r':( 1, 1),'d':0x1,  'c':'CAN 1 reference clock: 1 -  enabled (0 - disabled)'},
                  'clkact0':                  {'r':( 0, 0),'d':0x1,  'c':'CAN 0 reference clock: 1 -  enabled (0 - disabled)'}}},
                  
      'can_mioclk_ctrl':             {'OFFS': 0x160,'DFLT':0x0,'RW':'RW', # Never set
                                   'COMMENTS':'CAN MIO clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(23,31),'d':0,    'c':'reserved'},
                  'can1_ref_sel':             {'r':(22,22),'d':0,    'c':'CAN1 reference clock selection: 0: from internal PLL, 1 - from MIO based on can1_mux selection'},
                  'can1_mux':                 {'r':(16,21),'d':0,    'c':'CAN1 MIO pin selection (valid: 0..53)'},
                  'reserved2':                {'r':( 7,15),'d':0,    'c':'reserved'},
                  'can0_ref_sel':             {'r':( 6, 6),'d':0,    'c':'CAN0 reference clock selection: 0: from internal PLL, 1 - from MIO based on can0_mux selection'},
                  'can0_mux':                 {'r':( 0, 5),'d':0,    'c':'CAN0 MIO pin selection (valid: 0..53)'}}},

      'dbg_clk_ctrl':             {'OFFS': 0x164,'DFLT':0xf03,'RW':'RW', # Never set
                                   'COMMENTS':'SoC debug clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(14,31),'d':0,    'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0xf, 'c':'Frequency divisor'},
                  'reserved2':                {'r':( 7, 7),'d':0,    'c':'reserved'},
                  'srcsel':                   {'r':( 4, 6),'d':0x0,  'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL, 4..7 - EMIO trace clock'},
                  'reserved3':                {'r':( 2, 3),'d':0,    'c':'reserved'},
                  'cpu_1x_clkact':            {'r':( 1, 1),'d':0x1,  'c':'CPU 1x clock: 1 -  enabled (0 - disabled)'},
                  'clkact_trc':               {'r':( 0, 0),'d':0x1,  'c':'Debug trace clock: 1 -  enabled (0 - disabled)'}}},

      'pcap_clk_ctrl':            {'OFFS': 0x168,'DFLT':0xf01,'RW':'RW', # 0x501
                                   'COMMENTS':'PCAP clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':(14,31),'d':0,     'c':'reserved'},
                  'divisor':                  {'r':( 8,13),'d':0xf,   'c':'Frequency divisor'}, # 0x5
                  'reserved2':                {'r':( 6, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0,     'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'},
                  'reserved3':                {'r':( 1, 3),'d':0,     'c':'reserved'},
                  'clkact':                   {'r':( 0, 0),'d':0x1,   'c':'PCAP clock: 1 -  enabled (0 - disabled)'}}}, # 0x1

      'topsw_clk_ctrl':           {'OFFS': 0x16c,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'Central interconnect clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':( 1,31),'d':0,     'c':'reserved'},
                  'clk_dis':                  {'r':( 0, 0),'d':0,     'c':'Central interconnect clock DISABLE: 0 -  enabled (1 - disabled)'}}},

      'fpga0_clk_ctrl':           {'OFFS': 0x170,'DFLT':0x101800,'RW':'RW', # 0x101400
                                   'COMMENTS':'PL clock 0 output control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,     'c':'reserved'},
                  'divisor1':                 {'r':(20,25),'d':0x1,   'c':'Frequency divisor, second stage'}, # 0x1
                  'reserved2':                {'r':(14,19),'d':0,     'c':'reserved'},
                  'divisor0':                 {'r':( 8,13),'d':0x18,  'c':'Frequency divisor, first stage'}, # 0x14
                  'reserved3':                {'r':( 6, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0,     'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'}, #0 
                  'reserved4':                {'r':( 0, 3),'d':0,     'c':'reserved'}}},

      'fpga0_thr_ctrl':           {'OFFS': 0x174,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PL clock 0 throttle control',
                                   'FIELDS':{
                  'reserved1':                {'r':( 4,31),'d':0,     'c':'reserved'},
                  'en_0':                     {'r':( 3, 3),'d':0,     'c':'Set to 0 to use this feature'},
                  'en_1':                     {'r':( 2, 2),'d':0,     'c':'Set to 1 to use this feature'},
                  'cnt_rst':                  {'r':( 1, 1),'d':0,     'c':'1 - reset counter on CPU halt state enter'}, 
                  'cpu_start':                {'r':( 0, 0),'d':0,     'c':'0->1 transition: start/restart count'}}},

      'fpga0_thr_cnt':            {'OFFS': 0x178,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PL clock 0 throttle count control',
                                   'FIELDS':{
                  'reserved1':                {'r':(20,31),'d':0,     'c':'reserved'},
                  'reserved1':                {'r':(16,19),'d':0,     'c':'reserved'},
                  'last_cnt':                 {'r':( 0,15),'d':0,     'c':'Last count value. Specifies total number of clocks output in debug mode by the clock throttle logic'}}},

      'fpga0_thr_sta':            {'OFFS': 0x17c,'DFLT':0,'RW':'RO', # Never set
                                   'COMMENTS':'PL clock 0 throttle count control',
                                   'FIELDS':{
                  'reserved1':                {'r':(17,31),'d':0,'m':'R','c':'reserved'},
                  'running':                  {'r':(16,16),'d':0,'m':'R','c':'0: Clock is stopped or in normal mode - OK to change configuration, 1: clock is running in debug mode (keep configuration)'},
                  'curr_val':                 {'r':( 0,15),'d':0,'m':'R','c':'Clock throttle counter (number of pulses output so far). Only accurate when halted'}}},
      
      'fpga1_clk_ctrl':           {'OFFS': 0x180,'DFLT':0x101800,'RW':'RW', # 0x101400
                                   'COMMENTS':'PL clock 1 output control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,     'c':'reserved'},
                  'divisor1':                 {'r':(20,25),'d':0x1,   'c':'Frequency divisor, second stage'}, # 0x1
                  'reserved2':                {'r':(14,19),'d':0,     'c':'reserved'},
                  'divisor0':                 {'r':( 8,13),'d':0x18,  'c':'Frequency divisor, first stage'}, #0x14
                  'reserved3':                {'r':( 6, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0,     'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'}, # 0x0 
                  'reserved4':                {'r':( 0, 3),'d':0,     'c':'reserved'}}},

      'fpga1_thr_ctrl':           {'OFFS': 0x184,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PL clock 1 throttle control',
                                   'FIELDS':{
                  'reserved1':                {'r':( 4,31),'d':0,     'c':'reserved'},
                  'en_0':                     {'r':( 3, 3),'d':0,     'c':'Set to 0 to use this feature'},
                  'en_1':                     {'r':( 2, 2),'d':0,     'c':'Set to 1 to use this feature'},
                  'cnt_rst':                  {'r':( 1, 1),'d':0,     'c':'1 - reset counter on CPU halt state enter'}, 
                  'cpu_start':                {'r':( 0, 0),'d':0,     'c':'0->1 transition: start/restart count'}}},

      'fpga1_thr_cnt':            {'OFFS': 0x188,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PL clock 1 throttle count control',
                                   'FIELDS':{
                  'reserved1':                {'r':(20,31),'d':0,     'c':'reserved'},
                  'reserved1':                {'r':(16,19),'d':0,     'c':'reserved'},
                  'last_cnt':                 {'r':( 0,15),'d':0,     'c':'Last count value. Specifies total number of clocks output in debug mode by the clock throttle logic'}}},

      'fpga1_thr_sta':            {'OFFS': 0x18c,'DFLT':0,'RW':'RO', # Never set
                                   'COMMENTS':'PL clock 1 throttle count control',
                                   'FIELDS':{
                  'reserved1':                {'r':(17,31),'d':0,'m':'R','c':'reserved'},
                  'running':                  {'r':(16,16),'d':0,'m':'R','c':'0: Clock is stopped or in normal mode - OK to change configuration, 1: clock is running in debug mode (keep configuration)'},
                  'curr_val':                 {'r':( 0,15),'d':0,'m':'R','c':'Clock throttle counter (number of pulses output so far). Only accurate when halted'}}},
      
      'fpga2_clk_ctrl':           {'OFFS': 0x190,'DFLT':0x101800,'RW':'RW', # 0x101400
                                   'COMMENTS':'PL clock 2 output control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,     'c':'reserved'},
                  'divisor1':                 {'r':(20,25),'d':0x1,   'c':'Frequency divisor, second stage'}, # 0x1
                  'reserved2':                {'r':(14,19),'d':0,     'c':'reserved'},
                  'divisor0':                 {'r':( 8,13),'d':0x18,  'c':'Frequency divisor, first stage'}, # 0x14
                  'reserved3':                {'r':( 6, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0,     'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'}, # 0x0 
                  'reserved4':                {'r':( 0, 3),'d':0,     'c':'reserved'}}},

      'fpga2_thr_ctrl':           {'OFFS': 0x194,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PL clock 2 throttle control',
                                   'FIELDS':{
                  'reserved1':                {'r':( 4,31),'d':0,     'c':'reserved'},
                  'en_0':                     {'r':( 3, 3),'d':0,     'c':'Set to 0 to use this feature'},
                  'en_1':                     {'r':( 2, 2),'d':0,     'c':'Set to 1 to use this feature'},
                  'cnt_rst':                  {'r':( 1, 1),'d':0,     'c':'1 - reset counter on CPU halt state enter'}, 
                  'cpu_start':                {'r':( 0, 0),'d':0,     'c':'0->1 transition: start/restart count'}}},

      'fpga2_thr_cnt':            {'OFFS': 0x198,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PL clock 2 throttle count control',
                                   'FIELDS':{
                  'reserved1':                {'r':(20,31),'d':0,     'c':'reserved'},
                  'reserved1':                {'r':(16,19),'d':0,     'c':'reserved'},
                  'last_cnt':                 {'r':( 0,15),'d':0,     'c':'Last count value. Specifies total number of clocks output in debug mode by the clock throttle logic'}}},

      'fpga2_thr_sta':            {'OFFS': 0x19c,'DFLT':0,'RW':'RO', # Never set
                                   'COMMENTS':'PL clock 2 throttle count control',
                                   'FIELDS':{
                  'reserved1':                {'r':(17,31),'d':0,'m':'R','c':'reserved'},
                  'running':                  {'r':(16,16),'d':0,'m':'R','c':'0: Clock is stopped or in normal mode - OK to change configuration, 1: clock is running in debug mode (keep configuration)'},
                  'curr_val':                 {'r':( 0,15),'d':0,'m':'R','c':'Clock throttle counter (number of pulses output so far). Only accurate when halted'}}},
      
      'fpga3_clk_ctrl':           {'OFFS': 0x1a0,'DFLT':0x101800,'RW':'RW', # 0x101400
                                   'COMMENTS':'PL clock 3 output control',
                                   'FIELDS':{
                  'reserved1':                {'r':(26,31),'d':0,     'c':'reserved'},
                  'divisor1':                 {'r':(20,25),'d':0x1,   'c':'Frequency divisor, second stage'}, # 0x1
                  'reserved2':                {'r':(14,19),'d':0,     'c':'reserved'},
                  'divisor0':                 {'r':( 8,13),'d':0x18,  'c':'Frequency divisor, first stage'}, #0x14
                  'reserved3':                {'r':( 6, 7),'d':0,     'c':'reserved'},
                  'srcsel':                   {'r':( 4, 5),'d':0,     'c':'Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL'}, #0x0 
                  'reserved4':                {'r':( 0, 3),'d':0,     'c':'reserved'}}},

      'fpga3_thr_ctrl':           {'OFFS': 0x1a4,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PL clock 3 throttle control',
                                   'FIELDS':{
                  'reserved1':                {'r':( 4,31),'d':0,     'c':'reserved'},
                  'en_0':                     {'r':( 3, 3),'d':0,     'c':'Set to 0 to use this feature'},
                  'en_1':                     {'r':( 2, 2),'d':0,     'c':'Set to 1 to use this feature'},
                  'cnt_rst':                  {'r':( 1, 1),'d':0,     'c':'1 - reset counter on CPU halt state enter'}, 
                  'cpu_start':                {'r':( 0, 0),'d':0,     'c':'0->1 transition: start/restart count'}}},

      'fpga3_thr_cnt':            {'OFFS': 0x1a8,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PL clock 3 throttle count control',
                                   'FIELDS':{
                  'reserved1':                {'r':(20,31),'d':0,     'c':'reserved'},
                  'reserved1':                {'r':(16,19),'d':0,     'c':'reserved'},
                  'last_cnt':                 {'r':( 0,15),'d':0,     'c':'Last count value. Specifies total number of clocks output in debug mode by the clock throttle logic'}}},

      'fpga3_thr_sta':            {'OFFS': 0x1ac,'DFLT':0,'RW':'RO', # Never set
                                   'COMMENTS':'PL clock 3 throttle count control',
                                   'FIELDS':{
                  'reserved1':                {'r':(17,31),'d':0,'m':'R','c':'reserved'},
                  'running':                  {'r':(16,16),'d':0,'m':'R','c':'0: Clock is stopped or in normal mode - OK to change configuration, 1: clock is running in debug mode (keep configuration)'},
                  'curr_val':                 {'r':( 0,15),'d':0,'m':'R','c':'Clock throttle counter (number of pulses output so far). Only accurate when halted'}}},
      
      'clk_621_true':             {'OFFS': 0x1c4,'DFLT':0x1,'RW':'RW', # 0x1
                                   'COMMENTS':'CPU clock ratio mode select',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0,   'c':'reserved'},
                  'clk_621_true':             {'r':( 0, 0),'d':0x1, 'c':'Select the CPU clock ratio: 0- 4:2:1, 1 - 6:2;1. No access to OCM when this value changes'}}}, #0x1

      'pss_rst_ctrl':             {'OFFS': 0x200,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'PS software reset control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'soft_rst':                 {'r':( 0, 0),'d':0, 'c':'1 - assert PS software reset pulse (all but clock generator). Self clearing'}}},

      'ddr_rst_ctrl':             {'OFFS': 0x204,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'DDR software reset control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'ddr_rst':                  {'r':( 0, 0),'d':0, 'c':'DDR software reset: 0 - normal, 1 - reset'}}},

      'topsw_rst_ctrl':           {'OFFS': 0x208,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'Central interconnect software reset control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'ddr_rst':                  {'r':( 0, 0),'d':0, 'c':'Central interconnect reset: 0 - normal, 1 - reset. Make sure AXI does not have outstanding transactions and the bus is idle'}}},

      'dmac_rst_ctrl':            {'OFFS': 0x20c,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'DMA controller software reset control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'ddr_rst':                  {'r':( 0, 0),'d':0, 'c':'DMA controller reset: 0 - normal, 1 - reset (and write enable DMAC trust zone register)'}}},
    
      'usb_rst_ctrl':             {'OFFS': 0x210,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'USB software reset control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 2,31),'d':0, 'c':'reserved'},
                  'usb1_cpu1x_rst':           {'r':( 1, 1),'d':0, 'c':'USB 1 master and slave AMBA interfaces: 0 - normal, 1 - reset'},
                  'usb0_cpu1x_rst':           {'r':( 0, 0),'d':0, 'c':'USB 0 master and slave AMBA interfaces: 0 - normal, 1 - reset'}}},

      'gem_rst_ctrl':             {'OFFS': 0x214,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'GigE software reset control for ref. clock, Rx clock and CPU_1x clock domains',
                                   'FIELDS':{
                  'reserved1':                {'r':( 8,31),'d':0, 'c':'reserved'},
                  'gem1_ref_rst':             {'r':( 7, 7),'d':0, 'c':'GEM 1 reference clock domain reset: 0 - normal, 1 - reset'},
                  'gem0_ref_rst':             {'r':( 6, 6),'d':0, 'c':'GEM 0 reference clock domain reset: 0 - normal, 1 - reset'},
                  'gem1_rx_rst':              {'r':( 5, 5),'d':0, 'c':'GEM 1 RX clock domain reset: 0 - normal, 1 - reset'},
                  'gem0_rx_rst':              {'r':( 4, 4),'d':0, 'c':'GEM 0 RX clock domain reset: 0 - normal, 1 - reset'},
                  'reserved2':                {'r':( 2, 3),'d':0, 'c':'reserved'},
                  'gem1_cpu1x_rst':           {'r':( 1, 1),'d':0, 'c':'GEM 1 CPU_1x clock domain reset: 0 - normal, 1 - reset'},
                  'gem0_cpu1x_rst':           {'r':( 0, 0),'d':0, 'c':'GEM 0 CPU_1x clock domain reset: 0 - normal, 1 - reset'}}},

      'sdio_rst_ctrl':            {'OFFS': 0x218,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'SDIO software reset control for reference clock and CPU_1x clock domains',
                                   'FIELDS':{
                  'reserved1':                {'r':( 6,31),'d':0, 'c':'reserved'},
                  'sdio1_ref_rst':            {'r':( 5, 5),'d':0, 'c':'SDIO 1 reference clock domain reset: 0 - normal, 1 - reset'},
                  'sdio0_ref_rst':            {'r':( 4, 4),'d':0, 'c':'SDIO 0 reference clock domain reset: 0 - normal, 1 - reset'},
                  'reserved2':                {'r':( 2, 3),'d':0, 'c':'reserved'},
                  'sdio1_cpu1x_rst':          {'r':( 1, 1),'d':0, 'c':'SDIO 1 CPU_1x clock domain reset: 0 - normal, 1 - reset'},
                  'sdio0_cpu1x_rst':          {'r':( 0, 0),'d':0, 'c':'SDIO 0 CPU_1x clock domain reset: 0 - normal, 1 - reset'}}},

      'spi_rst_ctrl':             {'OFFS': 0x21c,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'SPI software reset control for reference clock and CPU_1x clock domains',
                                   'FIELDS':{
                  'reserved':                 {'r':( 4,31),'d':0, 'c':'reserved'},
                  'spi1_ref_rst':             {'r':( 3, 3),'d':0, 'c':'SPI 1 reference clock domain reset: 0 - normal, 1 - reset'},
                  'spi0_ref_rst':             {'r':( 2, 2),'d':0, 'c':'SPI 0 reference clock domain reset: 0 - normal, 1 - reset'},
                  'spi1_cpu1x_rst':           {'r':( 1, 1),'d':0, 'c':'SPI 1 CPU_1x clock domain reset: 0 - normal, 1 - reset'},
                  'spi0_cpu1x_rst':           {'r':( 0, 0),'d':0, 'c':'SPI 0 CPU_1x clock domain reset: 0 - normal, 1 - reset'}}},

      'cam_rst_ctrl':             {'OFFS': 0x220,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'CAN software reset control',
                                   'FIELDS':{
                  'reserved1':                {'r':( 4,31),'d':0, 'c':'reserved'},
                  'reserved2':                {'r':( 3, 3),'d':0, 'c':'reserved'},
                  'reserved3':                {'r':( 2, 2),'d':0, 'c':'reserved'},
                  'can1_cpu1x_rst':           {'r':( 1, 1),'d':0, 'c':'CAN 1 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset'},
                  'can0_cpu1x_rst':           {'r':( 0, 0),'d':0, 'c':'CAN 0 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset'}}},

      'i2c_rst_ctrl':             {'OFFS': 0x224,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'I2C software reset control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 2,31),'d':0, 'c':'reserved'},
                  'i2c1_cpu1x_rst':           {'r':( 1, 1),'d':0, 'c':'I2C 1 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset'},
                  'i2c0_cpu1x_rst':           {'r':( 0, 0),'d':0, 'c':'I2C 0 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset'}}},

      'uart_rst_ctrl':            {'OFFS': 0x228,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'UART software reset control for reference clock and CPU_1x (AMBA) clock domains',
                                   'FIELDS':{
                  'reserved':                 {'r':( 4,31),'d':0, 'c':'reserved'},
                  'uart1_ref_rst':            {'r':( 3, 3),'d':0, 'c':'UART 1 reference clock domain reset: 0 - normal, 1 - reset'},
                  'uart0_ref_rst':            {'r':( 2, 2),'d':0, 'c':'UART 0 reference clock domain reset: 0 - normal, 1 - reset'},
                  'uart1_cpu1x_rst':          {'r':( 1, 1),'d':0, 'c':'UART 1 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset'},
                  'uart0_cpu1x_rst':          {'r':( 0, 0),'d':0, 'c':'UART 0 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset'}}},

      'gpio_rst_ctrl':            {'OFFS': 0x22c,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'GPIO software reset control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'gpio_cpu1x_rst':           {'r':( 0, 0),'d':0, 'c':'GPIO 0 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset'}}},

      'lqspi_rst_ctrl':           {'OFFS': 0x230,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'Quad SPI software reset control for reference clock and CPU_1x (AMBA) clock domains',
                                   'FIELDS':{
                  'reserved':                 {'r':( 2,31),'d':0, 'c':'reserved'},
                  'qspi_ref_rst':             {'r':( 1, 1),'d':0, 'c':'QSPI reference clock domain reset: 0 - normal, 1 - reset'},
                  'lqspi_cpu1x_rst':          {'r':( 0, 0),'d':0, 'c':'QSPI CPU_1x clock domain reset: 0 - normal, 1 - reset'}}},

      'smc_rst_ctrl':             {'OFFS': 0x234,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'Quad SPI software reset control for reference clock and CPU_1x (AMBA) clock domains',
                                   'FIELDS':{
                  'reserved':                 {'r':( 2,31),'d':0, 'c':'reserved'},
                  'smc_ref_rst':              {'r':( 1, 1),'d':0, 'c':'SMC reference clock domain reset: 0 - normal, 1 - reset'},
                  'smc_cpu1x_rst':            {'r':( 0, 0),'d':0, 'c':'SMC CPU_1x (AMBA) clock domain reset: 0 - normal, 1 - reset'}}},

      'ocm_rst_ctrl':             {'OFFS': 0x238,'DFLT':0,'RW':'RW', # Never set
                                   'COMMENTS':'OCM software reset control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'OCM_rst':                  {'r':( 0, 0),'d':0, 'c':'OCM subsystem reset: 0 - normal, 1 - reset'}}},
      'fpga_rst_ctrl':            {'OFFS': 0x240,'DFLT':0x01f33f0f,'RW':'RW', #0xffffffff->0x0
                                   'COMMENTS':'FPGA software reset control',
                                   'FIELDS':{
                  'reserved_3':               {'r':(25,31),'d':0,   'c':'reserved'}, #0x7f->0x0
                  'fpga_acp_rst':             {'r':(24,24),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_axds3_rst':           {'r':(23,23),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_axds2_rst':           {'r':(22,22),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_axds1_rst':           {'r':(21,21),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_axds0_rst':           {'r':(20,20),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'reserved_2':               {'r':(18,19),'d':0,   'c':'reserved'}, #0x3 ->0x0
                  'fssw1_fpga_rst':           {'r':(17,17),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fssw0_fpga_rst':           {'r':(16,16),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'reserved_1':               {'r':(14,15),'d':0,   'c':'reserved'}, #0x3 ->0x0
                  'fpga_fmsw1_rst':           {'r':(13,13),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_fmsw0_rst':           {'r':(12,12),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_dma3_rst':            {'r':(11,11),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_dma2_rst':            {'r':(10,10),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_dma1_rst':            {'r':( 9, 9),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'fpga_dma0_rst':            {'r':( 8, 8),'d':0x1, 'c':'reserved'}, #0x1 ->0x0
                  'reserved':                 {'r':( 4, 7),'d':0,   'c':'reserved'}, #0xf ->0x0
                  'fpga3_out_rst':            {'r':( 3, 3),'d':0x1, 'c':'PL reset3 (FCLKRESETN3): 0 - deassert (logic high state), 1 - assert (logic low state)'}, #0x1 ->0x0
                  'fpga2_out_rst':            {'r':( 2, 2),'d':0x1, 'c':'PL reset2 (FCLKRESETN2): 0 - deassert (logic high state), 1 - assert (logic low state)'}, #0x1 ->0x0
                  'fpga1_out_rst':            {'r':( 1, 1),'d':0x1, 'c':'PL reset1 (FCLKRESETN1): 0 - deassert (logic high state), 1 - assert (logic low state)'}, #0x1 ->0x0
                  'fpga0_out_rst':            {'r':( 0, 0),'d':0x1, 'c':'PL reset0 (FCLKRESETN0): 0 - deassert (logic high state), 1 - assert (logic low state)'}}}, #0x1 ->0x0

      'a9_cpu_rst_ctrl':             {'OFFS': 0x244,'DFLT':0,'RW':'RW', #  Never set
                                   'COMMENTS':'CPU reset and clock control',
                                   'FIELDS':{
                  'reserved1':                {'r':( 9,31),'d':0, 'c':'reserved'},
                  'peri_rst':                 {'r':( 8, 8),'d':0, 'c':'CPU peripheral soft reset (0 normal, 1 - hold in reset)'},
                  'reserved2':                {'r':( 6, 7),'d':0, 'c':'reserved'},
                  'a9_clkstop1':              {'r':( 5, 5),'d':0, 'c':'CPU 1 clock stop control: 0 - run, 1 - stop'},
                  'a9_clkstop0':              {'r':( 4, 4),'d':0, 'c':'CPU 0 clock stop control: 0 - run, 1 - stop'},
                  'reserved3':                {'r':( 3, 2),'d':0, 'c':'reserved'},
                  'a9_rst1':                  {'r':( 1, 1),'d':0, 'c':'CPU 1 software reset control: 0 - no reset, 1 - hold in reset'},
                  'a9_rst0':                  {'r':( 0, 0),'d':0, 'c':'CPU 0 software reset control: 0 - no reset, 1 - hold in reset'}}},

      'ps_awdt_ctrl':             {'OFFS': 0x24c,'DFLT':0,'RW':'RW', #  Never set
                                   'COMMENTS':'CPU reset and clock control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 2,31),'d':0, 'c':'reserved'},
                  'ctrl1':                    {'r':( 1, 1),'d':0, 'c':'Select target for APU watchdog timer 1: 0 - same as PS_SRST_B, 1 - CPU associated with this WDT'},
                  'ctrl0':                    {'r':( 0, 0),'d':0, 'c':'Select target for APU watchdog timer 0: 0 - same as PS_SRST_B, 1 - CPU associated with this WDT'}}},
      'reboot_status':            {'OFFS': 0x258,'DFLT':0x00400000,'RW':'RW', #  Never set
                                   'COMMENTS':'Reboot status, persistent through reboots (but POR)',
                                   'FIELDS':{
                  'reboot_state':             {'r':(24,31),'d':0, 'c':'1 byte data that is preserved through all resets but POR. RBL puts last known reset reason here'},
                  'reserved':                 {'r':(23,23),'d':0, 'c':'reserved'},
                  'por':                      {'r':(22,22),'d':0x1, 'c':'Last reset was POR (written by RBL)'}, 
                  'srst_b':                   {'r':(21,21),'d':0, 'c':'Last reset was SRST_B  (written by RBL)'},
                  'dbg_rst':                  {'r':(20,20),'d':0, 'c':'Last reset was by debug system  (written by RBL)'},
                  'slc_rst':                  {'r':(19,19),'d':0, 'c':'Last reset was SLC soft reset (written by RBL)'},
                  'awdt1_rst':                {'r':(18,18),'d':0, 'c':'Last reset was by APU watchdog timer1 (written by RBL)'},
                  'awdt0_rst':                {'r':(17,17),'d':0, 'c':'Last reset was by APU watchdog timer0 (written by RBL)'},
                  'swdt_rst':                 {'r':(16,16),'d':0, 'c':'Last reset was by system watchdog timeout (written by RBL)'},
                  'bootrom_error_code':       {'r':( 0,15),'d':0, 'c':'RBL error code (written by RBL)'}}},
      'boot_mode':                {'OFFS': 0x25c,'RW':'M', #
                                   'COMMENTS':'Boot mode strapping pins state',
                                   'FIELDS':{
                  'reserved':                 {'r':( 5,31),'d':0,          'c':'reserved'},
                  'pll_bypass':               {'r':( 4, 4),'d':0, 'm':'R', 'c':'1 PLL is enabled, outputs routed to clock generators, 0 - PLLs are disabled and bypassed'}, 
                  'boot_mode':                {'r':( 0, 3),       'm':'R', 'c':'boot mode pins as sampled'}}},
      'apu_ctrl':                 {'OFFS': 0x300,'DFLT':0,'RW':'RW', #  Never set
                                   'COMMENTS':'APU control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 3,31),'d':0, 'c':'reserved'},
                  'cfgsdisable':              {'r':( 2, 2),'d':0, 'c':'Disable write to some system control processor registers and some GIC registers. Reset by POR only'},
                  'cp15sdiasble':             {'r':( 0, 1),'d':0, 'c':'Disable write to some system control processor (CP15) registers in each processor. Reset by POR only'}}},

      'wdt_clk_sel':              {'OFFS': 0x304,'DFLT':0,'RW':'RW', #  Never set
                                   'COMMENTS':'SWDT source clock select',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'sel':                      {'r':( 0, 1),'d':0, 'c':'SWDT clock select: 0 - internal CPU_1x, 1 - PL via EMIO or MIO pin'}}},
    
      'ddr_urgent':               {'OFFS': 0x600, 'DFLT':0,'RW':'RW',
                                   'COMMENTS':'DDR Urgent Control',
                                   'FIELDS':{
                  'reserved':                 {'r':( 8,31),'d':0, 'c':'reserved'},
                  's3_arurgent':              {'r':( 7, 7),'d':0, 'c':'Read port 3 - set high priority'},
                  's2_arurgent':              {'r':( 6, 6),'d':0, 'c':'Read port 2 - set high priority'},
                  's3_arurgent':              {'r':( 5, 5),'d':0, 'c':'Read port 1 - set high priority'},
                  's0_arurgent':              {'r':( 4, 4),'d':0, 'c':'Read port 0 - set high priority'},
                  's3_awurgent':              {'r':( 3, 3),'d':0, 'c':'Write port 3 - set high priority'},
                  's2_awurgent':              {'r':( 2, 2),'d':0, 'c':'Write port 2 - set high priority'},
                  's1_awurgent':              {'r':( 1, 1),'d':0, 'c':'Write port 1 - set high priority'},
                  's0_awurgent':              {'r':( 0, 0),'d':0, 'c':'Write port 0 - set high priority'}}},
                  
      'ddr_cal_start':            {'OFFS': 0x60c,'DFLT':0,'RW':'RW',
                                   'COMMENTS':'DDR Calibration start',
                                   'FIELDS':{
                  'reserved':                 {'r':( 2,31),'d':0, 'c':'reserved'},
                  'start_cal_dll':            {'r':( 1, 1),'d':0, 'c':'1 - Start DLL calibration command (self-clearing). Only needed if auto calibration is disabled in reg_ddrc_dis_dll_calib'},
                  'start_cal_short':          {'r':( 0, 0),'d':0, 'c':'1 - Start ZQ calibration short command (self-clearing). Only needed if auto calibration is disabled in reg_ddrc_dis_auto_dq'}}},
                  
      'ddr_ref_start':            {'OFFS': 0x614,'DFLT':0,'RW':'RW',
                                   'COMMENTS':'DDR Refresh start',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'start_ref':                {'r':( 0, 0),'d':0, 'c':'1 - Start Refresh (self-clearing). Only needed if auto refresh is disabled in reg_ddrc_dis_auto_refresh'}}},
      'ddr_cmd_sta':              {'OFFS': 0x618,'DFLT':0,'RW':'RO',
                                   'COMMENTS':'DDR Command queue state',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0, 'c':'reserved'},
                  'cmd_q_empty':              {'r':( 0, 0),'d':0, 'm':'R', 'c':'0 - no commands for DDRC are queued, 1 - commands pending'}}},
      'ddr_urgent_sel':           {'OFFS': 0x61c,'DFLT':0,'RW':'RW',
                                   'COMMENTS':'DDR Urgent select',
                                   'FIELDS':{
                  'reserved':                 {'r':(16,31),'d':0, 'c':'reserved'},
                  's3_ar_qos_mode':           {'r':(14,15),'d':0, 'c':'Select DDRC s3_arurgent source: 0 - ddr_urgent_val reg. bit, 1 - s3_arqos bit, 2 - fabric ddr_arb[3]'},
                  's2_ar_qos_mode':           {'r':(12,13),'d':0, 'c':'Select DDRC s2_arurgent source: 0 - ddr_urgent_val reg. bit, 1 - s2_arqos bit, 2 - fabric ddr_arb[2]'},
                  's1_ar_qos_mode':           {'r':(10,11),'d':0, 'c':'Select DDRC s1_arurgent source: 0 - ddr_urgent_val reg. bit, 1 - s1_arqos bit, 2 - fabric ddr_arb[1]'},
                  's0_ar_qos_mode':           {'r':( 8, 9),'d':0, 'c':'Select DDRC s0_arurgent source: 0 - ddr_urgent_val reg. bit,                   2 - fabric ddr_arb[0]'},
                  's3_aw_qos_mode':           {'r':( 6, 7),'d':0, 'c':'Select DDRC s3_awurgent source: 0 - ddr_urgent_val reg. bit, 1 - s3_awqos bit, 2 - fabric ddr_arb[3]'},
                  's2_aw_qos_mode':           {'r':( 4, 5),'d':0, 'c':'Select DDRC s2_awurgent source: 0 - ddr_urgent_val reg. bit, 1 - s3_awqos bit, 2 - fabric ddr_arb[2]'},
                  's1_aw_qos_mode':           {'r':( 2, 3),'d':0, 'c':'Select DDRC s1_awurgent source: 0 - ddr_urgent_val reg. bit, 1 - s3_awqos bit, 2 - fabric ddr_arb[1]'},
                  's0_aw_qos_mode':           {'r':( 0, 1),'d':0, 'c':'Select DDRC s0_awurgent source: 0 - ddr_urgent_val reg. bit,                   2 - fabric ddr_arb[0]'}}},
      'ddr_dfi_status':           {'OFFS': 0x620,'RW':'M', #
                                   'COMMENTS':'DDR DFI status',
                                   'FIELDS':{
                  'reserved':                 {'r':( 1,31),'d':0,         'c':'reserved'},
                  'dfi_cal_st':               {'r':( 0, 3),'d':0,'m':'R', 'c':'Not clear'}}},

      'sd0_wp_cd_sel':           {'OFFS': 0x830,'RW':'RW', #
                                   'COMMENTS':'SDIO 0 CD and WP source select',
                                   'FIELDS':{
                  'reserved1':                {'r':(22,31),'d':0,         'c':'reserved'},
                  'sdio0_ce_sel':             {'r':(16,21),'d':0,         'c':'Select MIO pin (any but 7,8) as a source for CD (>53 - EMIO)'},
                  'reserved2':                {'r':( 6,15),'d':0,         'c':'reserved'},
                  'sdio0_wp_sel':             {'r':( 0, 5),'d':0,         'c':'Select MIO pin (any but 7,8) as a source for WP (>53 - EMIO)'}}},

      'sd1_wp_cd_sel':           {'OFFS': 0x834,'RW':'RW', #
                                   'COMMENTS':'SDIO 1 CD and WP source select',
                                   'FIELDS':{
                  'reserved1':                {'r':(22,31),'d':0,         'c':'reserved'},
                  'sdio1_ce_sel':             {'r':(16,21),'d':0,         'c':'Select MIO pin (any but 7,8) as a source for CD (>53 - EMIO)'},
                  'reserved2':                {'r':( 6,15),'d':0,         'c':'reserved'},
                  'sdio1_wp_sel':             {'r':( 0, 5),'d':0,         'c':'Select MIO pin (any but 7,8) as a source for WP (>53 - EMIO)'}}},
                  
    }
MIO_PINS_DEFS={'mio_pin_%02i'%i:{'OFFS': 0x700+4*i,
                             'DFLT':0x1601,
                             'RW':'RW',
                             'COMMENTS':'MIO pin %i control'%i,
                             'FIELDS':{
                  'reserved':                 {'r':(14,31),'d':0,   'c':'reserved'},
                  'disable_rcv':              {'r':(13,13),'d':0,   'c':'disable HSTL input buffer'},
                  'pullup':                   {'r':(12,12),'d':0x1, 'c':'1 - enable pullup, 0 - disable'},
                  'io_type':                  {'r':( 9,11),'d':0x3, 'c':'1 - LVCMOS18,2 - LVCMOS25,3 -LVCMOS33, 4 - HSTL'},
                  'fast':                     {'r':( 8, 8),'d':0,   'c':'Output driver edge rate:1 - fast, 0 - slow'},
                  'l3_sel':                   {'r':( 5, 7),'d':0,   'c':'level 3 mux select'},
                  'l2_sel':                   {'r':( 3, 4),'d':0,   'c':'level 2 mux select'},
                  'l1_sel':                   {'r':( 2, 2),'d':0,   'c':'level 1 mux select'},
                  'l0_sel':                   {'r':( 1, 1),'d':0,   'c':'level 0 mux select'},
                  'tri_enable':               {'r':( 0, 0),'d':1,   'c':'1 - enable tri-state, 0 - disable'}}}
                               for i in range (54)}   
MIO_PINS_DEFS['BASE_ADDR']=(0xF8000000,) # SLCR
MIO_PINS_DEFS['MODULE_NAME']=('slcr',)
SLCR_DEFS=    dict(MIO_PINS_DEFS.items()+SLCR_CLK_DEFS.items()) # combine.
    
#UG585: table 25-6: multiplier (PLL_FDIV), PLL_CP, PLL_RES, LOCK_CNT
PLL_PARS=(( 13,    2,6,750),
          ( 14,    2,6,700),
          ( 15,    2,6,650),
          ( 16,    2,10,625),
          ( 17,    2,10,575),
          ( 18,    2,10,550),
          ( 19,    2,10,525),
          ( 20,    2,12,500),
          ( 21,    2,12,475),
          ( 22,    2,12,450),
          ( 23,    2,12,425),
          ((24,25),2,12,400),
          ( 26,    2,12,375),
          ((27,28),2,12,350),
          ((29,30),2,12,325),
          ((31,33),2,12,300),
          ((34,36),2,12,275),
          ((37,40),2,12,250),
          ((41,47),3,12,250),
          ((48,66),3,12,250))