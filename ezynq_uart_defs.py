#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# Definitions of Zynq UART registers 
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
# UART Registers
# void poll_fifo_empty(void){
#     while ((readl(&uart1_base->channel_sts) & 0x8) ==0) ; /* wait transmitter buffer is empty */
# }
# 
# void poll_putc(int d){
#     led_off();
#     while ((readl(&uart1_base->channel_sts) & 0x10) !=0) ; /* wait transmitter buffer is not full */
#     led_on();
#     writel(d, &uart1_base->tx_rx_fifo);
# }
#    u32 uart_rst_ctrl; /* 0x228 */
#     writel(0x0000000f, &slcr_base->uart_rst_ctrl); /* UART reset on */
# 
# //&slcr_base->uart_rst_ctrl
# //    writel(0x0000000f, &slcr_base->uart_rst_ctrl); /* UART reset on */
#     /* delay ??? move reset on earlier?*/
#     writel(0x00000000, &slcr_base->uart_rst_ctrl); /* UART reset off */
# 
# /* uart 1 */
#     writel(0x00000020, &uart1_base->mode);     /* UART character frame */
# /* a. Disable the Rx path: set uart.Control_reg0 [RXEN] = 0 and [RXDIS] = 1.
#    b. Disable the Txpath: set uart.Control_reg0 [TXEN] = 0 and [TXDIS] = 1. */
#     writel(0x00000028, &uart1_base->control); /*a,b */
# /* c. Write the calculated CD value into the uart.Baud_rate_gen_reg0 [CD] bit field. */
#     writel(12, &uart1_base->baud_rate_gen); /*c  - for 25MHz and 115200 CD=12, (BDIV+1)=18 */
# /* d. Write the calculated BDIV value into the uart.Baud_rate_divider_reg0 [BDIV] bit value. */
#     writel(17, &uart1_base->baud_rate_div); /*d  - for 25MHz and 115200 CD=12, (BDIV+1)=18 */
#     writel(0x117, &uart1_base->control); /* restart and enable ug585v1.6.1. p 555 */
#     writel(0x14, &uart1_base->control); /*just a delay - 1-st character is usually lost */
#     led_on();    // gets here with wrong TEXT_BASE
# //    while (1);

# struct uart_regs {
#     u32 control;          /* 0x0 */
#     u32 mode;             /* 0x4 */
#     u32 intrpt_en;        /* 0x8 */
#     u32 intrpt_dis;       /* 0xc */
#     u32 intrpt_mask;      /* 0x10 */
#     u32 chnl_int_sts;     /* 0x14 */
#     u32 baud_rate_gen;    /* 0x18 */
#     u32 rx_timeout;       /* 0x1c */
#     u32 rx_fifo_trig_lev; /* 0x20 */
#     u32 modem_cntrl;      /* 0x24 */
#     u32 modem_sts;        /* 0x28 */
#     u32 channel_sts;      /* 0x2c */
#     u32 tx_rx_fifo;       /* 0x30 */
#     u32 baud_rate_div;    /* 0x34 */
#     u32 flow_delay;       /* 0x38 */
#     u32 reserved[2];
#     u32 tx_fifo_trig_lev; /* 0x44 */
# };



UART_DEFS={ #not all fields are defined currently
    'BASE_ADDR':(0xE0000000,0xE0001000), # SLCR
    'MODULE_NAME':('uart0','uart1'),
      'control':                  {'OFFS': 0x000,'DFLT':0x128,'RW':'RW',
                                   'COMMENTS':'UART Control register',
                                   'FIELDS':{
                  'reserved':               {'r':( 9,31),'d':0},
                  'stpbrk':                 {'r':( 8, 8),'d':1,  'c':'Stop BREAK transmission after a min. of 1 character and keep at high for 12 CLK. Overwrites sttbrk'},
                  'sttbrk':                 {'r':( 7, 7),'d':0,  'c':'Start BREAK transmission When buffers (FIFO and SR) are empty'},
                  'rstto':                  {'r':( 6, 6),'d':0,  'c':'Restart receiver timeout counter (self clearing)'},
                  'txdis':                  {'r':( 5, 5),'d':1,  'c':'1 - Disable transmitter, 0 - enable'},
                  'txen':                   {'r':( 4, 4),'d':0,  'c':'1 - Enable transmitter (if txdis==0), 0 - disable'},
                  'rxdis':                  {'r':( 3, 3),'d':1,  'c':'1 - Disable receiver, 0 - enable'},
                  'rxen':                   {'r':( 2, 2),'d':0,  'c':'1 - Enable receiver (if rxdis==0), 0 - disable'},
                  'txres':                  {'r':( 1, 1),'d':0,  'c':'1 - Reset transmitter (self clearing after reset is finished)'},
                  'rxres':                  {'r':( 0, 0),'d':0,  'c':'1 - Reset receiver (self clearing after reset is finished)'}}},

      'mode':                     {'OFFS': 0x004,'DFLT':0x0,'RW':'M',
                                   'COMMENTS':'UART Mode register',
                                   'FIELDS':{
                  'reserved1':              {'r':(12,31),'d':0,'m':'R'},
                  'reserved2':              {'r':(11,11),'d':0},
                  'reserved3':              {'r':(10,10),'d':0},
                  'chmode':                 {'r':( 8, 9),'d':0,  'c':'Channel Mode: 0 - normal, 1 - auto echo, 2 - local loopback, 3 - remote loopback'},
                  'nbstop':                 {'r':( 6, 7),'d':0,  'c':'Number of stop bits: 0 - 1 stop bit, 1 - 1.5 stop bits, 2 - 2 stop bits, 3 - reserved'},
                  'par':                    {'r':( 3, 5),'d':0,  'c':'Parity: 0 - even, 1 - odd, 2 forced 0 (space), 3 forced 1 (mark),>=4 - no parity'},
                  'chrl':                   {'r':( 1, 2),'d':0,  'c':'Character length: 0,1 - 8 bits, 2 - 7 bits, 3 - 6 bits'},
                  'clks':                   {'r':( 0, 0),'d':0,  'c':'Div by 8 select: 0 - use uart_ref_clk, 1 - use uart_ref_clk/8'}}},


      'baud_rate_gen':            {'OFFS': 0x018,'DFLT':0x28b,'RW':'RW',
                                   'COMMENTS':'Divisor of the input clock to get bit sample period',
                                   'FIELDS':{
                  'reserved':               {'r':(16,31),'d':0},
                  'cd':                     {'r':( 0,15),'d':0x28b,  'c':'Baud rate divisor: 0 - disabled, 1..0xffff - divisor '}}},

      'channel_sts':              {'OFFS': 0x02c,'DFLT':0x0,'RW':'R',
                                   'COMMENTS':'Channel status',
                                   'FIELDS':{
                  'reserved1':              {'r':(15,31),'d':0,'m':'R'},
                  'tnful':                  {'r':(14,14),'d':0,'m':'R',  'c':'Transmitter FIFO nearly full'},
                  'ttrig':                  {'r':(13,13),'d':0,'m':'R',  'c':'Transmitter FIFO level >= preset TTRIG value'},
                  'fdelt':                  {'r':(12,12),'d':0,'m':'R',  'c':'Receiver FIFO level >= preset FDEL value'},
                  'tactive':                {'r':(11,11),'d':0,'m':'R',  'c':'Transmitter active'},
                  'ractive':                {'r':(10,10),'d':0,'m':'R',  'c':'Receiver active'},
                  'reserved2':              {'r':( 9, 9),'d':0,'m':'R',  'c':''},
                  'reserved3':              {'r':( 8, 8),'d':0,'m':'R',  'c':''},
                  'reserved4':              {'r':( 7, 7),'d':0,'m':'R',  'c':''},
                  'reserved5':              {'r':( 6, 6),'d':0,'m':'R',  'c':''},
                  'reserved6':              {'r':( 5, 5),'d':0,'m':'R',  'c':''},
                  'tful':                   {'r':( 4, 4),'d':0,'m':'R',  'c':'Transmitter FIFO full (continuous)'},
                  'tempty':                 {'r':( 3, 3),'d':0,'m':'R',  'c':'Transmitter FIFO empty (continuous)'},
                  'rful':                   {'r':( 2, 2),'d':0,'m':'R',  'c':'Receiver FIFO full (continuous)'},
                  'rempty':                 {'r':( 1, 1),'d':0,'m':'R',  'c':'Receiver FIFO empty (continuous)'},
                  'rtrig':                  {'r':( 0, 0),'d':0,'m':'R',  'c':'Receiver FIFO level >= preset RTRIG value (continuous)'}}},
           
      'baud_rate_div':            {'OFFS': 0x034,'DFLT':0xf,'RW':'RW',
                                   'COMMENTS':'Number of bit sample periods minus 1',
                                   'FIELDS':{
                  'reserved':               {'r':( 8,31),'d':0},
                  'bdiv':                   {'r':( 0, 7),'d':0xf,  'c':'0-3 - ignored, 4..0xff - number of clock samples per bit'}}},

    }

#Use 'TYPE':'I' for decimal output, 'H' - for hex. On input both are accepted
UART_CFG_DEFS=[
    {'NAME':'BAUD_RATE',          'CONF_NAME':'CONFIG_EZYNQ_UART@_BAUD_RATE','TYPE':'F','MANDATORY':False,'DERIVED':True,'DEFAULT':115200,
                'DESCRIPTION':'UART baud rate used during boot'},
    {'NAME':'DEBUG_CHANNEL',      'CONF_NAME':'CONFIG_EZYNQ_UART_DEBUG_CHANNEL','TYPE':'I','MANDATORY':False,'DERIVED':True,'DEFAULT':0,
                'DESCRIPTION':'UART channel to use during boot (will use only if MIO has both defined) '},
    {'NAME':'MIN_SAMPLES_PER_BIT','CONF_NAME':'CONFIG_EZYNQ_UART@_MIN_SAMPLES_PER_BIT','TYPE':'I','MANDATORY':False,'DERIVED':True,'DEFAULT':8,
                'DESCRIPTION':'Minimal samples per bit when selecting baud rate divisors (should be >=5, <256)'},

]
#CONFIG_EZYNQ_UART1_BAUD_RATE=115200