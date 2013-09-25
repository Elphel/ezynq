#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Elphel.inc.
# configuration of the UART-related registers
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
import ezynq_uart_defs
import ezynq_registers
import ezynq_feature_config
import ezynq_slcr_clk_def
#CONFIG_EZYNQ_UART1_BAUD_RATE=115200
class EzynqUART:
    def __init__(self):
        self.UART_DEFS=      ezynq_uart_defs.UART_DEFS
        self.UART_CFG_DEFS=  ezynq_uart_defs.UART_CFG_DEFS
        self.SLCR_CLK_DEFS=  ezynq_slcr_clk_def.SLCR_CLK_DEFS

#        print self.features.config_names
    def parse_parameters(self,raw_configs,used_mio_interfaces,permit_undefined_bits=False):
        uarts=set()
        for iface in used_mio_interfaces:
            if iface['NAME']=='UART':
                uarts.add(iface['CHANNEL'])
#        print 'uarts=',uarts
        if not uarts:
            print 'No UARTs defined in MIO'
            self.channel=None
            return
        self.channel=max(uarts)
        self.features=ezynq_feature_config.EzynqFeatures(self.UART_CFG_DEFS,self.channel)
        self.features.parse_features(raw_configs)
        if len(uarts)>1:
            if 'DEBUG_CHANNEL' in self.features.pars:
                self.channel=self.features.pars['DEBUG_CHANNEL']
                self.features=ezynq_feature_config.EzynqFeatures(self.UART_CFG_DEFS,self.channel)
                self.features.parse_features(raw_configs)
        self.uart_register_set=  ezynq_registers.EzynqRegisters(self.UART_DEFS,self.channel,[],permit_undefined_bits)
        self.slcr_register_set=  ezynq_registers.EzynqRegisters(self.SLCR_CLK_DEFS,0,[],permit_undefined_bits)
#        print self.features.pars
    def check_missing_features(self):
        self.features.check_missing_features()
 
    def set_refclk_mhz(self,fmhz):
        self.refclk=1000000.0*fmhz
        self.set_divisors()         

    def html_list_features(self,html_file):
        if not html_file:
            return
        html_file.write('<h2>UART%i configuration parameters</h2>\n'%self.channel)
        self.features.html_list_features(html_file)
#       print self.features.get_par_names()
    def set_divisors(self):
        def get_bdiv_cd_baud(baud_rate,min_bdiv):
            best_diff=None;
            min_bdiv=max(min_bdiv,5)
            min_bdiv=min(min_bdiv,256)
            for bdiv in range (min_bdiv,257):
                cd=min(int(round(self.refclk/bdiv/self.baud_rate)),65535)
                if cd==0:
                    continue
                err=abs(baud_rate-self.refclk/bdiv/cd)/baud_rate
#                print bdiv,self.refclk/bdiv/self.baud_rate,cd,self.refclk/bdiv/cd,err
                if (best_diff is None) or (err<best_diff):
                    best_diff=err
                    best_bdiv=bdiv
                    best_cd=cd
#                    print bdiv,self.refclk/bdiv/self.baud_rate,cd,self.refclk/bdiv/cd,err
#            print best_bdiv,best_cd,self.refclk/best_bdiv/best_cd
            return (best_bdiv,best_cd,self.refclk/best_bdiv/best_cd)
        try:
            self.baud_rate=self.features.pars['BAUD_RATE']
        except:
            self.baud_rate=115200
            print 'Baud rate not specified, using default ',self.baud_rate              
        try:
            min_bdiv=self.features.pars['MIN_SAMPLES_PER_BIT']
        except:
            min_bdiv=8
        self.bdiv,self.cd,self.baud_rate=get_bdiv_cd_baud(self.baud_rate,min_bdiv)
        self.features.set_calculated_value('BAUD_RATE',self.baud_rate,force=True)
        
    # these instructions will be usen to generate C code.
    # when defined here (as register writes/tests) they will appear in the overall list
    # of registers (HTML file)
    
    def set_uart_codes(self):
        uart_extra_set=  ezynq_registers.EzynqRegisters(self.UART_DEFS,self.channel,[])
        # wait transmitter FIFO empty (use before proceeding to risky of reboot code )
        uart_extra_set.wait_reg_field_values('channel_sts',  # Channel status
                                               (('tempty',    1)), True) # Transmitter FIFO empty (continuous)
        uart_extra_set.flush() # to separate codes, not to combine in one write
        # wait transmitter FIFO not full (OK to  put more characters)
        uart_extra_set.wait_reg_field_values('channel_sts',  # Channel status
                                               (('tful',    0)), True) # Transmitter FIFO full (continuous)
        uart_extra_set.flush()
        uart_extra_set.set_bitfields('tx_rx_fifo',( # TX/RX FIFO character data write/read
                                                ('fifo',  self.cd)),True) # read/write FIFO character data
        return uart_extra_set.get_register_sets(sort_addr=True,apply_new=True)

    def setup_uart(self,current_reg_sets,force=False,warn=False):    
        
        uart_register_set=self.uart_register_set
        
#         slcr_register_set=self.slcr_register_set
#         slcr_register_set.set_initial_state(current_reg_sets, True)# start from the current registers state
#         slcr_register_set.set_bitfields('uart_rst_ctrl',( # dflt=0
#                                                 ('uart1_ref_rst',   self.channel==1), # UART 1 reference clock domain reset: 0 - normal, 1 - reset
#                                                 ('uart0_ref_rst',   self.channel==0), # UART 0 reference clock domain reset: 0 - normal, 1 - reset
#                                                 ('uart1_cpu1x_rst', self.channel==1), # UART 1 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset
#                                                 ('uart0_cpu1x_rst', self.channel==0)),force,warn) #UART 0 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset
#         slcr_register_set.flush()
#         slcr_register_set.set_bitfields('uart_rst_ctrl',( # dflt=0
#                                                 ('uart1_ref_rst',   0), # UART 1 reference clock domain reset: 0 - normal, 1 - reset
#                                                 ('uart0_ref_rst',   0), # UART 0 reference clock domain reset: 0 - normal, 1 - reset
#                                                 ('uart1_cpu1x_rst', 0), # UART 1 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset
#                                                 ('uart0_cpu1x_rst', 0)),force,warn) #UART 0 CPU_1x clock domain (AMBA) reset: 0 - normal, 1 - reset
#         reg_sets=slcr_register_set.get_register_sets(sort_addr=True,apply_new=True)

        uart_register_set.set_initial_state(current_reg_sets, True)# start from the current registers state
        uart_register_set.set_bitfields('mode',( # dflt=4
                                                ('chmode',   0), # Channel Mode: 0 - normal, 1 - auto echo, 2 - local loopback, 3 - remote loopback
                                                ('nbstop',   0), # Number of stop bits: 0 - 1 stop bit, 1 - 1.5 stop bits, 2 - 2 stop bits, 3 - reserved
                                                ('par',      4), # Parity: 0 - even, 1 - odd, 2 forced 0 (space), 3 forced 1 (mark),>=4 - no parity
                                                ('chrl',     0), # Character length: 0,1 - 8 bits, 2 - 7 bits, 3 - 6 bits
                                                ('clks',     0)),force,warn) #'Div by 8 select: 0 - use uart_ref_clk, 1 - use uart_ref_clk/8
                                                
        uart_register_set.set_bitfields('control',( # dflt=0x128
                                                ('stpbrk',   1), # Stop BREAK transmission after a min. of 1 character and keep at high for 12 CLK. Overwrites sttbrk
                                                ('sttbrk',   0), # Start BREAK transmission When buffers (FIFO and SR) are empty'},
                                                ('rstto',    0),  # Restart receiver timeout counter (self clearing)
                                                ('txdis',    1),  # 1 - Disable transmitter, 0 - enable
                                                ('txen',     0),   # 1 - Enable transmitter (if txdis==0), 0 - disable
                                                ('rxdis',    1),  # 1 - Disable receiver, 0 - enable
                                                ('rxen',     0),   # 1 - Enable receiver (if rxdis==0), 0 - disable
                                                ('txres',    0),  # 1 - Reset transmitter (self clearing after reset is finished)
                                                ('rxres',    0)),force,warn) #1 - Reset receiver (self clearing after reset is finished)
        uart_register_set.flush()
        uart_register_set.set_bitfields('baud_rate_gen',( # dflt=0x28b
                                                ('cd',  self.cd)),force,warn) # Baud rate divisor: 0 - disabled, 1..0xffff - divisor
        uart_register_set.set_bitfields('baud_rate_div',( # dflt=0xf
                                                ('bdiv',  self.bdiv-1)),force,warn) # 0-3 - ignored, 4..0xff - number of clock samples per bit
        uart_register_set.flush()
        uart_register_set.set_bitfields('control',( # dflt=0x128
                                                ('stpbrk',   1), # Stop BREAK transmission after a min. of 1 character and keep at high for 12 CLK. Overwrites sttbrk
                                                ('sttbrk',   0), # Start BREAK transmission When buffers (FIFO and SR) are empty'},
                                                ('rstto',    0),  # Restart receiver timeout counter (self clearing)
                                                ('txdis',    0),  # 1 - Disable transmitter, 0 - enable
                                                ('txen',     1),   # 1 - Enable transmitter (if txdis==0), 0 - disable
                                                ('rxdis',    0),  # 1 - Disable receiver, 0 - enable
                                                ('rxen',     1),   # 1 - Enable receiver (if rxdis==0), 0 - disable
                                                ('txres',    1),  # 1 - Reset transmitter (self clearing after reset is finished)
                                                ('rxres',    1)),force,warn) #1 - Reset receiver (self clearing after reset is finished)
        uart_register_set.wait_reg_field_values('control',      # wait reset cleared
                                               (('txres',    0), 
                                                ('rxres',    0)), True, warn)
        return uart_register_set.get_register_sets(sort_addr=True,apply_new=True)
    
