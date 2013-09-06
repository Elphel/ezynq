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
import struct
import ezynq_ddr
import ezynq_registers

# http://docs.python.org/2/howto/argparse.html
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbosity', action='count', help='increase output verbosity')
parser.add_argument('-c', '--configs',   help='Configuration file (such as autoconf.mk)')
parser.add_argument('-w', '--warn',      help='Warn when the pin function is overwritten and continue', action='store_true')
parser.add_argument('-o', '--outfile',   help='Path to save the generated boot file')
parser.add_argument('--html', help='Generate HTML map of MIO, save to the specified file')
parser.add_argument('--html-mask', help='Bit mask of what data to include in the HTML MIO map')

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

    
MIO_TEMPLATES = {
  'QUADSPI':(
     {'NAME':'CS0',  'TRISTATE':False, 'FAST':True, 'PULLUP':True,  'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((1,), (0,))},
     {'NAME':'IO0',  'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((2,), (10,))},
     {'NAME':'IO1',  'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((3,), (11,))},
     {'NAME':'IO2',  'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((4,), (12,))},
     {'NAME':'IO3',  'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((5,), (13,))},
     {'NAME':'SCLK', 'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((6,), (9,))}),
  'QUADSPI_FBCLK':(
     {'NAME':'FBCLK','TRISTATE':False, 'FAST':True, 'PULLUP':False,  'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((8,), )},),
#TODO: specify FAST and PULLUP for other interfaces                 
  'ETH':(
     {'NAME':'TXCK', 'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((16,), (28,))},
     {'NAME':'TXDO', 'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((17,), (29,))},
     {'NAME':'TXD1', 'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((18,), (30,))},
     {'NAME':'TXD2', 'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((19,), (31,))},
     {'NAME':'TXD3', 'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((20,), (32,))},
     {'NAME':'TXEN', 'TRISTATE':False, 'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((21,), (33,))},
     {'NAME':'RXCLK','TRISTATE':True,  'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((22,), (34,))},
     {'NAME':'RXD0', 'TRISTATE':True,  'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((23,), (35,))},
     {'NAME':'RXD1', 'TRISTATE':True,  'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((24,), (36,))},
     {'NAME':'RXD2', 'TRISTATE':True,  'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((25,), (37,))},
     {'NAME':'RXD3', 'TRISTATE':True,  'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((26,), (38,))},
     {'NAME':'RXDV', 'TRISTATE':True,  'FAST':True, 'PULLUP':False, 'L0':1, 'L1':0, 'L2':0, 'L3':0, 'PINS':((27,), (39,))}),
  'MDIO':(
     {'NAME':'C',    'TRISTATE':False, 'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((52,),)},
     {'NAME':'D',    'TRISTATE':False, 'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((53,),)}),  # bidir - should TRISTATE be true?
  'USB':(
     {'NAME':'DATA4', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((28,), (40,))},
     {'NAME':'DIR',   'TRISTATE':True,   'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((29,), (41,))},
     {'NAME':'STEP',  'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((30,), (42,))},
     {'NAME':'NEXT',  'TRISTATE':True,   'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((31,), (43,))},
     {'NAME':'DATA0', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((32,), (44,))},
     {'NAME':'DATA1', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((33,), (45,))},
     {'NAME':'DATA2', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((34,), (46,))},
     {'NAME':'DATA3', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((35,), (47,))},
     {'NAME':'CLK',   'TRISTATE':True,   'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((36,), (48,))},
     {'NAME':'DATA5', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((37,), (49,))},
     {'NAME':'DATA6', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((38,), (50,))},
     {'NAME':'DATA7', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS':((39,), (51,))}),
  'SPI':(
     {'NAME':'SC',  'TRISTATE':False, 'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':5, 'PINS':((16, 28, 40), (12, 24, 36, 48))},
     {'NAME':'MISO','TRISTATE':False, 'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':5, 'PINS':((17, 29, 41), (11, 23, 35, 47))},
     {'NAME':'SS0', 'TRISTATE':False, 'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':5, 'PINS':((18, 30, 42), (13, 25, 37, 49))},
     {'NAME':'SS1', 'TRISTATE':False, 'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':5, 'PINS':((19, 31, 43), (14, 26, 38, 50))},
     {'NAME':'SS2', 'TRISTATE':False, 'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':5, 'PINS':((20, 32, 44), (15, 27, 39, 51))},
     {'NAME':'MOSI','TRISTATE':False, 'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':5, 'PINS':((21, 33, 45), (10, 22, 34, 46))}),
  'SDIO':(
     {'NAME':'CLK', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((16, 28, 40), (12, 24, 36, 48))},
     {'NAME':'CMD', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((17, 29, 41), (11, 23, 35, 47))},
     {'NAME':'IO0', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((18, 30, 42), (10, 22, 34, 46))},
     {'NAME':'IO1', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((19, 31, 43), (13, 25, 37, 59))},
     {'NAME':'IO2', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((20, 32, 44), (14, 26, 38, 50))},
     {'NAME':'IO3', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((21, 33, 45), (15, 27, 39, 51))}),
  'SDIO_CD':(
     {'NAME':'CD', 'TRISTATE':True,  'FAST':False, 'PULLUP':True,   'L0':0, 'L1':0, 'L2':0, 'L3':0, 'PINS':(
       (0,1,2,3,4,5,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
        31,32,33,34,35,36,37.38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53),
       (0,1,2,3,4,5,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
        31,32,33,34,35,36,37.38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53))},),    
  'SDIO_WP':(
     {'NAME':'WP', 'TRISTATE':True,  'FAST':False, 'PULLUP':True,   'L0':0, 'L1':0, 'L2':0, 'L3':0, 'PINS':(
       (0,1,2,3,4,5,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
        31,32,33,34,35,36,37.38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53),
       (0,1,2,3,4,5,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
        31,32,33,34,35,36,37.38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53))},),    
  'SDIO_PWR':(
     {'NAME':'PWR', 'TRISTATE':False,  'FAST':False, 'PULLUP':False,   'L0':0, 'L1':0, 'L2':3, 'L3':0, 'PINS':(
       (0,2,4,6,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52),
       (1,3,5,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37.39,41,43,45,47,49,51,53))},),    
  'NOR':(
     {'NAME':'CS0',   'TRISTATE':False, 'FAST':False, 'PULLUP':True,  'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((0,),)},
     {'NAME':'DATA0', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((3,),)},
     {'NAME':'DATA1', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((4,),)},
     {'NAME':'DATA2', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((5,),)},
     {'NAME':'DATA3', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((6),)},
     {'NAME':'OE',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((7,),)},
     {'NAME':'WE',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':2, 'PINS':((8,),)},
     {'NAME':'DATA6', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((9,),)},
     {'NAME':'DATA7', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((10,),)},
     {'NAME':'DATA4', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((11,),)},
     {'NAME':'DATA5', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((13,),)},
     {'NAME':'A0',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((15,),)},
     {'NAME':'A1',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((16,),)},
     {'NAME':'A2',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((17,),)},
     {'NAME':'A3',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((18,),)},
     {'NAME':'A4',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((19,),)},
     {'NAME':'A5',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((20,),)},
     {'NAME':'A6',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((21,),)},
     {'NAME':'A7',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((22,),)},
     {'NAME':'A8',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((23,),)},
     {'NAME':'A9',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((24,),)},
     {'NAME':'A10',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((25,),)},
     {'NAME':'A11',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((26,),)},
     {'NAME':'A12',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((27,),)},
     {'NAME':'A13',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((28,),)},
     {'NAME':'A14',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((29,),)},
     {'NAME':'A15',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((30,),)},
     {'NAME':'A16',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((31,),)},
     {'NAME':'A17',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((32,),)},
     {'NAME':'A18',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((33,),)},
     {'NAME':'A19',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((34,),)},
     {'NAME':'A20',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((35,),)},
     {'NAME':'A21',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((36,),)},
     {'NAME':'A22',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((37,),)},
     {'NAME':'A23',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((38,),)},
     {'NAME':'A24',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((39,),)}),
  'NOR_A25':(
     {'NAME':'A25',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':1, 'L3':0, 'PINS':((1,),)},),
  'NOR_CS1':(
     {'NAME':'CS1',   'TRISTATE':False, 'FAST':False, 'PULLUP':True,  'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((1,),)},),
  'NAND':(
     {'NAME':'CS',  'TRISTATE':False, 'FAST':False, 'PULLUP':True,  'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((0,),)},
     {'NAME':'ALE', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((2,),)},
     {'NAME':'WE',  'TRISTATE':False, 'FAST':False, 'PULLUP':True,  'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((3,),)},
     {'NAME':'IO2', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((4,),)},
     {'NAME':'IO0', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((5,),)},
     {'NAME':'IO1', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((6,),)},
     {'NAME':'CLE', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((7,),)},
     {'NAME':'RD',  'TRISTATE':False, 'FAST':False, 'PULLUP':True,  'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((8,),)},
     {'NAME':'IO4', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((9,),)},
     {'NAME':'IO5', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((10,),)},
     {'NAME':'IO6', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((11,),)},
     {'NAME':'IO7', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((12,),)},
     {'NAME':'IO3', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((13,),)},
     {'NAME':'BUSY','TRISTATE':True,  'FAST':False, 'PULLUP':True,  'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((14,),)}),
#NAND16 is used in addition to NAND                 
  'NAND16':(
     {'NAME':'IO8',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((16,),)},
     {'NAME':'IO9',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((17,),)},
     {'NAME':'IO10', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((18,),)},
     {'NAME':'IO11', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((19,),)},
     {'NAME':'IO12', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((20,),)},
     {'NAME':'IO13', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((21,),)},
     {'NAME':'IO14', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((22,),)},
     {'NAME':'IO15', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':2, 'L3':0, 'PINS':((23,),)}),
  'CAN':(
     {'NAME':'RX', 'TRISTATE':True,  'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':1, 'PINS':
      ((10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50), (9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53))},
     {'NAME':'TX', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':1, 'PINS':
      ((11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51), (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52))}),
  'UART':(
     {'NAME':'RX', 'TRISTATE':True,  'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':7, 'PINS':
      ((10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50), (9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53))},
     {'NAME':'TX', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':7, 'PINS':
      ((11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51), (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52))}),
  'I2C':(
     {'NAME':'SCL', 'TRISTATE':False,  'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':2, 'PINS':
      ((10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50), (12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52))},
     {'NAME':'SDA', 'TRISTATE':False,  'FAST':False, 'PULLUP':True, 'L0':0, 'L1':0, 'L2':0, 'L3':2, 'PINS':
      ((11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51), (13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53))}),
  'TTC':(
     {'NAME':'WOUT','TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':6, 'PINS': ((18, 30, 42), (16, 28, 40))},
     {'NAME':'CLK', 'TRISTATE':True,  'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':6, 'PINS': ((19, 31, 43), (17, 29, 41))}),                 
  'SWDT':(
     {'NAME':'CLK', 'TRISTATE':True,  'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':3, 'PINS': ((14, 26, 38, 50, 52),)},
     {'NAME':'RSTO','TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':3, 'PINS': ((15, 27, 39, 51, 53),)}),                 
  'PJTAG':(
     {'NAME':'TDI', 'TRISTATE':True,  'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':3, 'PINS': ((10, 22, 34, 46),)},
     {'NAME':'TDO', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':3, 'PINS': ((11, 23, 35, 47),)},
     {'NAME':'TCK', 'TRISTATE':True,  'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':3, 'PINS': ((12, 24, 36, 48),)},
     {'NAME':'TMS', 'TRISTATE':True,  'FAST':False, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':3, 'PINS': ((13, 25, 37, 49),)}),
  'TPUI':( # variable number of options
     {'NAME':'CLK0',   'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((12,24),)},
     {'NAME':'CTL',    'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((13,25),)},
     {'NAME':'DATA0',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((14,26),)},
     {'NAME':'DATA1',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((15,27),)},
     {'NAME':'DATA2',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((10,22),)},
     {'NAME':'DATA3',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((11,23),)},
     {'NAME':'DATA4',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((16,),)},
     {'NAME':'DATA5',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((17,),)},
     {'NAME':'DATA6',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((18,),)},
     {'NAME':'DATA7',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((19,),)},
     {'NAME':'DATA8',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((2,),)},
     {'NAME':'DATA9',  'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((3,),)},
     {'NAME':'DATA10', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((4,),)},
     {'NAME':'DATA11', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((5,),)},
     {'NAME':'DATA12', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((6,),)},
     {'NAME':'DATA13', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((7,),)},
     {'NAME':'DATA14', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((8,),)},
     {'NAME':'DATA15', 'TRISTATE':False, 'FAST':False, 'PULLUP':False, 'L0':0, 'L1':1, 'L2':0, 'L3':0, 'PINS': ((9,),)})
}

MIO_INTERFACES=[
    {'CONFIG_NAME':'CONFIG_EZYNQ_QUADSPI_0',     'IFACE':'QUADSPI',      'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_QUADSPI_1',     'IFACE':'QUADSPI_FBCLK','CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_QUADSPI_FBCLK', 'IFACE':'ETH',          'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_ETH_0',     'IFACE':'ETH',          'CHANNEL':0},                
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_ETH_1',     'IFACE':'ETH',          'CHANNEL':1},                
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_ETH_MDIO',  'IFACE':'MDIO',         'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_USB_0',     'IFACE':'USB',          'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_USB_1',     'IFACE':'USB',          'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SPI_0',     'IFACE':'SPI',          'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SPI_1',     'IFACE':'SPI',          'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SDIO_0',    'IFACE':'SDIO',         'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SDIO_1',    'IFACE':'SDIO',         'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SDCD_0',    'IFACE':'SDIO_CD',      'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SDCD_1',    'IFACE':'SDIO_CD',      'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SDWP_0',    'IFACE':'SDIO_WP',      'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SDWP_1',    'IFACE':'SDIO_WP',      'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SDPWR_0',   'IFACE':'SDIO_PWR',     'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SDPWR_1',   'IFACE':'SDIO_PWR',     'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_NOR',           'IFACE':'NOR',          'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_NOR_A25',       'IFACE':'NOR_A25',      'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_NOR_CS1',       'IFACE':'NOR_CS1',      'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_NAND',          'IFACE':'NAND',         'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_NAND16',        'IFACE':'NAND16',       'CHANNEL':0}, #requires NAND
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_CAN_0',     'IFACE':'CAN',          'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_CAN_1',     'IFACE':'CAN',          'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_CAN_ECLK_0','IFACE':'CAN_ECLK',     'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_CAN_ECLK_1','IFACE':'CAN_ECLK',     'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_UART_0',    'IFACE':'UART',         'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_UART_1',    'IFACE':'UART',         'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_I2C_0',     'IFACE':'I2C',          'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_I2C_1',     'IFACE':'I2C',          'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_TTC_0',     'IFACE':'TTC',          'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_TTC_1',     'IFACE':'TTC',          'CHANNEL':1},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_SWDT',      'IFACE':'SWDT',         'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_PJTAG',     'IFACE':'PJTAG',        'CHANNEL':0},
    {'CONFIG_NAME':'CONFIG_EZYNQ_MIO_TPUI',      'IFACE':'TPUI',         'CHANNEL':0}]
MIO_ATTR=[
    {'PREFIX':'CONFIG_EZYNQ_MIO_IOSTD_LVCMOS18_','PROPERTY':'IOTYPE','VALUE':'LVCMOS18'},   
    {'PREFIX':'CONFIG_EZYNQ_MIO_IOSTD_LVCMOS25_','PROPERTY':'IOTYPE','VALUE':'LVCMOS25'},
    {'PREFIX':'CONFIG_EZYNQ_MIO_IOSTD_LVCMOS33_','PROPERTY':'IOTYPE','VALUE':'LVCMOS33'},
    {'PREFIX':'CONFIG_EZYNQ_MIO_IOSTD_HSTL_',    'PROPERTY':'IOTYPE','VALUE':'HSTL'},
    {'PREFIX':'CONFIG_EZYNQ_MIO_IOSTD_HSTLDIS_', 'PROPERTY':'IOTYPE','VALUE':'HSTLDIS'},
    {'PREFIX':'CONFIG_EZYNQ_MIO_PULLUP_EN_',     'PROPERTY':'PULLUP','VALUE':True},
    {'PREFIX':'CONFIG_EZYNQ_MIO_PULLUP_DIS_',    'PROPERTY':'PULLUP','VALUE':False},
    {'PREFIX':'CONFIG_EZYNQ_MIO_FAST_',          'PROPERTY':'FAST',  'VALUE':True},
    {'PREFIX':'CONFIG_EZYNQ_MIO_SLOW_',          'PROPERTY':'FAST',  'VALUE':False},
    {'PREFIX':'CONFIG_EZYNQ_MIO_INOUT_',    'SPECIAL':'DIR'},
    {'PREFIX':'CONFIG_EZYNQ_MIO_GPIO_OUT_', 'SPECIAL':'GPIO_OUT'}]



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
    print MIO_TEMPLATES
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
def parse_config_mio(raw_configs):
    attrib_suffix='ATTRIB'
    options = {}
    for line in raw_configs:
        option = line['KEY']
        value = line['VALUE']
        if QUALIFIER_CHAR in option:
            option,qualifier=option.split(QUALIFIER_CHAR,1)
            if not option in options:
                options[option]={}
            if not isinstance(options[option],dict): # make a former value a value in a dictionary
                options[option]={'INTERFACE_GROUP':options[option]}
            if qualifier==attrib_suffix:
                value=str(value).upper()
                try:
                    options[option]['ATTRIBS'].add(value)
                except:
                    options[option]['ATTRIBS']=set([value])
                if not 'INTERFACE_GROUP' in options[option]:
                    options[option]['INTERFACE_GROUP']='Y' # 'any' if not overwritten, so just setting attribute initializes interface
            else:        
                options[option][qualifier]=value    
        else: 
        # store in the dictionary:
            if option in options:
                try:
                    options[option]['INTERFACE_GROUP'] = value #qualified pins already defined
                except:
                    options[option] = value # not a dictionary - just overwrite 
            else:
                options[option] = value
    return options

def mio_set_defaults(mio_dflts, mio, options):
    VALID_VOLTAGES = (1.8, 2.5, 3.3)
    IOSTD = ('LVCMOS18', 'LVCMOS25', 'LVCMOS33')
    try:
        mio_dflts['MIO_0_VOLT'] = float(options['CONFIG_EZYNQ_MIO_0_VOLT'])
    except (KeyError):
        print "required CONFIG_EZYNQ_MIO_0_VOLT is not defined. It should be 1.8, 2.5 or 3.3"
        exit (ERROR_DEFS['MISSING_CONFIG'])
    if not mio_dflts['MIO_0_VOLT'] in VALID_VOLTAGES:
        print 'Invalid voltage specified for MIO bank 0: CONFIG_EZYNQ_MIO_0_VOLT = ' + options['CONFIG_EZYNQ_MIO_0_VOLT']
        print 'Valid values are : ' + str(VALID_VOLTAGES)
        exit (ERROR_DEFS['INVALID'])
    try:
        mio_dflts['MIO_1_VOLT'] = float(options['CONFIG_EZYNQ_MIO_1_VOLT'])
    except (KeyError):
        print "required CONFIG_EZYNQ_MIO_1_VOLT is not defined. It should be 1.8, 2.5 or 3.3"
        exit (ERROR_DEFS['MISSING_CONFIG'])
    if not mio_dflts['MIO_1_VOLT'] in VALID_VOLTAGES:
        print 'Invalid voltage specified for MIO bank 1: CONFIG_EZYNQ_MIO_1_VOLT = ' + options['CONFIG_EZYNQ_MIO_1_VOLT']
        print 'Valid values are : ' + str(VALID_VOLTAGES)
        exit (ERROR_DEFS['INVALID'])
    iostd0 = IOSTD[VALID_VOLTAGES.index(mio_dflts['MIO_0_VOLT'])]
    pullup0 = False
    if 'CONFIG_EZYNQ_MIO_0_PULLUP' in options:
        pullup0 = True
    for i in range (0, 16):
        mio[i]['IOTYPE'] = iostd0;
        mio[i]['PULLUP'] = pullup0;
    iostd1 = IOSTD[VALID_VOLTAGES.index(mio_dflts['MIO_1_VOLT'])] 
    pullup1 = False
    if 'CONFIG_EZYNQ_MIO_1_PULLUP' in options:
        pullup1 = True
    for i in range (16, 54):
        mio[i]['IOTYPE'] = iostd1;
        mio[i]['PULLUP'] = pullup1;
 
def set_mio_interfaces(mio_interfaces, options):
    for conf_iface in MIO_INTERFACES:
        if conf_iface['CONFIG_NAME'] in options:
            iface_name=   conf_iface['IFACE']
            iface_template=   MIO_TEMPLATES[iface_name]
            channel= conf_iface['CHANNEL']
            option=  options[conf_iface['CONFIG_NAME']]
#            print '---->',option
            if len(iface_template[0]['PINS'])>1:
                print_channel=' channel '+str(channel)
            else:
                print_channel=''
            try:
                option.has_key('INTERFACE_GROUP')
            except:
                option={'INTERFACE_GROUP':option} # it was not a dictionary - string or number
# is the interface group as a whole used (not only individual pins)?
            iface={}    
            if 'INTERFACE_GROUP' in option:
                if option['INTERFACE_GROUP'] in "yY": # take first variant
                    anypin=iface_template[0]['PINS'][channel][0]
                else:
                    anypin=int(option['INTERFACE_GROUP'])
#find if this pin belongs to specified interface/channel
#                variant=-1
                for func_pin in iface_template:
                    pins=func_pin['PINS'][channel]
                    if anypin in pins:
                        variant=pins.index(anypin)
                        break
                else:
                    print 'Invalid MIO pin number '+str(anypin)+' for interface '+iface_name+print_channel+', set in '
                    print conf_iface['CONFIG_NAME']+" = "+str(anypin)
                    allowed_pins=[]
                    for func_pin in iface_template:
                        for pin in func_pin['PINS'][channel]:
                            allowed_pins.append(pin)
                    print 'Allowed MIO pins are:',allowed_pins
                    exit (ERROR_DEFS['NOSUCHPIN'])
                for tmpl_pin in iface_template:
                    iface_pin={}
                    for key in tmpl_pin.keys():
                        if (key != 'NAME') and (key != 'PINS'):
                            iface_pin[key]=tmpl_pin[key]
                    iface_pin['PIN']= tmpl_pin['PINS'][channel][variant]
                    iface[tmpl_pin['NAME']]= iface_pin
#now process individual pins (if any) specified for the interface
            for individual_pin_name in option.keys():
                if not individual_pin_name in ('INTERFACE_GROUP','ATTRIBS'):
                    value = option[individual_pin_name]
#                    print individual_pin_name,value
                    if value[0] in 'nfNF':
                        value = -1
                    elif value[0] in 'yY':
                        value='y'
                    else:
                        value=int(value)
#TODO: Value may be just 'y' if there is a single option
#Traceback (most recent call last):
#  File "./ezynq/ezynqcfg.py", line 455, in <module>
#    set_mio_interfaces(mio_interfaces, options)
#  File "./ezynq/ezynqcfg.py", line 369, in set_mio_interfaces
#    anypin=int(option['INTERFACE_GROUP'])
#ValueError: invalid literal for int() with base 10: 'y'
                        
                        
                        
#find if such pin name is defined for the interface
#                    for pin_index, tmpl_pin in enumerate(iface_template):
                    for tmpl_pin in iface_template:
                        if tmpl_pin['NAME'] == individual_pin_name:
                            break;
                    else:
                        print 'Signal name '+individual_pin_name+' is not defined for interface '+iface_name+' in'
                        print conf_iface['CONFIG_NAME']+QUALIFIER_CHAR+individual_pin_name+" = "+option[individual_pin_name]
                        exit (ERROR_DEFS['NOSUCHSIGNAL'])
                    if (value<0):
                        try:
                            del iface[individual_pin_name]
                        except:
                            pass # OK to delete non-existent?
                    else:
#see if pin number is valid
                        if value == 'y':
                            value=tmpl_pin['PINS'][channel][0] # first variant
                        if not value in tmpl_pin['PINS'][channel]:
                            print 'Invalid MIO pin number '+str(value)+' for interface '+iface_name+print_channel+', set in '
                            print conf_iface['CONFIG_NAME']+QUALIFIER_CHAR+individual_pin_name+" = "+option[individual_pin_name]
                            print 'Allowed MIO pins are:',tmpl_pin['PINS'][channel]
                            exit (ERROR_DEFS['NOSUCHPIN'])
#set new pin data                            
                        iface_pin={}
                        for key in tmpl_pin.keys():
                            if (key != 'NAME') and (key != 'PINS'):
                                iface_pin[key]=tmpl_pin[key]
#                        print 'channel=',channel,'variant=',variant,'tmpl_pin["PINS"]=',tmpl_pin['PINS']
                        iface_pin['PIN']= value # tmpl_pin['PINS'][channel][variant]
                        iface[tmpl_pin['NAME']]= iface_pin
            # Now we can try to apply iface to MIO, and add it to the list
            #or remove mio from function arguments and process mio_interfaces later?
            if args.verbosity >= 3:
                print 'name=',iface_name,' iface:'
                for i, item in enumerate(iface):
                    print i, item, ':',iface[item]
                print
            if not 'ATTRIBS' in option:
                option['ATTRIBS']=set()    
            mio_interfaces.append({'NAME':iface_name,'CHANNEL':channel, 'IFACE':iface, 'PRINT_CHANNEL':print_channel,'ATTRIBS':option['ATTRIBS']})            
def config_name (iface, channel, signal):
    for mi in MIO_INTERFACES:
        if (mi['IFACE']==iface) and (mi['CHANNEL']==channel) :
            if signal:
                return mi['CONFIG_NAME']+QUALIFIER_CHAR+signal
            else:
                return mi['CONFIG_NAME']
                                  
                                              
def apply_mio_interfaces(mio, mio_interfaces,warn):
    for iface_item in mio_interfaces:
        name=   iface_item['NAME']
        channel=iface_item['CHANNEL']
        iface=iface_item['IFACE']
        print_channel=iface_item['PRINT_CHANNEL']
        attribs=iface_item['ATTRIBS'] # set
        for signal in iface:
            pin=iface[signal]
            #see if the same pin was already used in one or several interfaces
            if mio[pin['PIN']]['USED_IN'] : #need to add len() >0?
                for used_in in mio[pin['PIN']]['USED_IN']:
                    print ('MIO pin '+str(pin['PIN'])+" is previously used by interface "+used_in['NAME']+
                      used_in['PRINT_CHANNEL']+', signal '+used_in['SIGNAL']+'.')
                    print 'You may resolve the conflict by freeing one of the signals, adding one of the following lines:'
                    print config_name (used_in['NAME'], used_in['CHANNEL'], used_in['SIGNAL'])+'=free'
                    print 'or'
                    print config_name (name, channel, signal)+'=free'
                    print 'to the board configuration file\n'
                if not warn:
                    exit (ERROR_DEFS['MIOCONFLICT'])
            #add current pin usage information        
            mio[pin['PIN']]['USED_IN'].append({'NAME':name, 'CHANNEL':channel,'SIGNAL':signal,'PRINT_CHANNEL':print_channel})
            #modify mio pin attributes
            #copy attributes from the interface template (if they are defined)
            for attr in pin:
                if (attr != 'PIN'):
                    mio[pin['PIN']][attr]=pin[attr]
#     {'NAME':'IO3', 'TRISTATE':False,  'FAST':True, 'PULLUP':False, 'L0':0, 'L1':0, 'L2':0, 'L3':4, 'PINS':((21, 33, 45), (15, 27, 39, 51))}),
            #overwrite attributes if specified for interface in config
            if 'SLOW' in attribs:
                mio[pin['PIN']]['FAST']=False 
            if 'FAST' in attribs:
                mio[pin['PIN']]['FAST']=True 
            if 'PULLUP' in attribs:
                mio[pin['PIN']]['PULLUP']=True 
            if 'NOPULLUP' in attribs:
                mio[pin['PIN']]['PULLUP']=False 
                    
def parse_mio(mio):
    for n, pin in enumerate(mio):
        value=0;
        if ('TRISTATE' in pin) and pin['TRISTATE']:
            value |= 1 # bit 0
        if 'L0' in pin:
            value |= (pin['L0'] & 1) << 1  # bit 1
        if 'L1' in pin:
            value |= (pin['L1'] & 1) << 2  # bit 2
        if 'L2' in pin:
            value |= (pin['L2'] & 3) << 3  # bits 3:4
        if 'L3' in pin:
            value |= (pin['L3'] & 7) << 5  # bits 5:7
        if ('FAST' in pin) and pin['FAST']:
            value |= (1<<8)  # bit 8
        if ('IOTYPE' in pin):
            if   pin['IOTYPE']=='LVCMOS18':
                value |= (1<<9) # bits 9:11
            elif pin['IOTYPE']=='LVCMOS25':
                value |= (2<<9) # bits 9:11
            elif pin['IOTYPE']=='LVCMOS33':
                value |= (3<<9) # bits 9:11
            elif pin['IOTYPE']=='HSTL':
                value |= (4<<9) # bits 9:11
            elif pin['IOTYPE']=='HSTLDIS':
                value |= (4<<9) | (1<<13)  # bits 9:11, bit 13
            else:
                print 'Invalid I/O standard: '+pin['IOTYPE']+' for MIO pin#'+n
                exit (-1)
        if ('PULLUP' in pin) and pin['PULLUP']:
            value |= (1<<12) # bit 12
        pin['VALUE']=value # or  mio[n]['VALUE']=value ???          
        pin['HEX']=hex(value) # or  mio[n]['VALUE']=value ???
#CONFIG_EZYNQ_MIO_IOSTD_LVCMOS18_NN= y # will overwrite defaults, last numeric specifies MIO pin number
#CONFIG_EZYNQ_MIO_IOSTD_LVCMOS25_NN= y # will overwrite defaults
#CONFIG_EZYNQ_MIO_IOSTD_LVCMOS33_NN= y # will overwrite defaults
#CONFIG_EZYNQ_MIO_IOSTD_HSTL_NN=     y # will overwrite defaults
#CONFIG_EZYNQ_MIO_IOSTD_HSTLDIS_NN= y # will overwrite defaults
#CONFIG_EZYNQ_MIO_PULLUP_EN_NN=      y # will overwrite defaults
#CONFIG_EZYNQ_MIO_PULLUP_DIS_NN=     y # will overwrite defaults
#CONFIG_EZYNQ_MIO_FAST_NN=           y # will overwrite defaults
#CONFIG_EZYNQ_MIO_INOUT_NN=         'IN' # 'OUT', 'BIDIR'
#CONFIG_EZYNQ_MIO_GPIO_OUT_NN=       0 # Set selected GPIO output to 0/1
def set_mio_attribs(mio,options):
    attribs={}
    for option in options:
        for attrib_entry in MIO_ATTR:
            prefix=attrib_entry['PREFIX']
#            print prefix,' <->', option, option[:len(prefix)]  
            if option[:len(prefix)]==prefix:
                if not prefix in attribs:
                    attribs[prefix]={}
#                print prefix,options[option],option[len(prefix):]
                try:    
                    key=int(option[len(prefix):])
                except:
                    print 'Invalid pin number ',option[len(prefix):],' in',option
                    exit (ERROR_DEFS['NOSUCHPIN)'])
                attribs[prefix][key]=options[option]
                break
#    print '------- attribs -----'
#    for a in attribs:
#        print a,attribs[a]
    #set defined attrinutes for MIO pins
    for attr in MIO_ATTR: 
        if ('PROPERTY' in attr) and (attr['PREFIX'] in attribs):
            for pin in attribs[attr['PREFIX']]:
                if (pin in range(len(mio))):
                    mio[pin][attr['PROPERTY']]=attr['VALUE']
#                    print '***',attr['PROPERTY'],pin,attr['VALUE']
                else:
                    print attr['PREFIX']+str(pin)+': pin number',pin,' out of range 0...53'
                    exit (ERROR_DEFS['NOSUCHPIN']) 
    #set IN, OUT, BIDIR (INOUT) parameters 
        elif ('SPECIAL' in attr) and (attr['SPECIAL']=='DIR') and (attr['PREFIX'] in attribs):
            for pin in attribs[attr['PREFIX']]:
                value=attribs[attr['PREFIX']][pin]
                value=value.upper()
                if   (value=='INOUT') or (value=='BIDIR'):
                    value = 'BIDIR'
                elif (value=='IN') or (value=='INPUT'):
                    value = 'IN'
                elif (value=='OUT') or (value=='OUTPUT'):
                    value = 'OUT'
                else:
                    print 'Invalid MIO pin polarity in',attr['PREFIX']+str(pin),'=',value
                    print 'Polarity can only be IN, OUT or BIDIR'
                    exit (ERROR_DEFS['INOUT'])
                if (pin==7) or (pin==8) and (value!='OUT'):
                    print 'Invalid MIO pin polarity in',attr['PREFIX']+str(pin),'=',value
                    print 'Polarity for MIO pins 7 and 8 can only be OUT'
                    exit (ERROR_DEFS['INOUT'])
                mio[pin]['INOUT']=value #Where is it used?
                if value=='IN':
                    mio[pin]['TRISTATE']=True
        elif ('SPECIAL' in attr) and (attr['SPECIAL']=='GPIO_OUT') and (attr['PREFIX'] in attribs):
            for pin in attribs[attr['PREFIX']]:
                value=attribs[attr['PREFIX']][pin]
#                print pin, value
                if (value!=0) and (value!='0'):
                    value=1
                else:
                    value=0
#                print 'value=',value
                mio[pin]['DATA_OUT']=value #Where is it used?
 
def verify_register_accessible(address):
    for interval in ACCESSIBLE_REGISTERS:
        if (address >= interval[0]) and (address <= interval[1]):
            if args.verbosity >= 1:  print 'Register accessible:' , hex(interval[0]),'<=', hex(address), '<=', hex(interval[1])
            return True
    else:
        return False    
#ACCESSIBLE_REGISTERS
    
def output_mio(registers,f,mio,MIO_HTML_MASK):
    if not registers is False:
        for mio_pin in mio:
            registers.append({'ADDRESS':mio_pin['ADDR'],'DATA':mio_pin['VALUE']})
    if not f:
        return    
    f.write ('<H2>MIO pins map</H2>\n')
    f.write('<table border="1">\n')
    f.write('  <tr>\n')
    f.write('  <th>MIO<br/>pin</th>')
    if MIO_HTML_MASK & 1:
        f.write('<th>address</th>')
    if MIO_HTML_MASK & 2:
        f.write('<th>PULLUP</th>')
        f.write('<th>FAST</th>')
        f.write('<th>TRISTATE</th>')
        f.write('<th>IOSTD</th>')
    if MIO_HTML_MASK & 4:
        f.write('<th>interface</th>')
    f.write('  <th>value</th>')
    if MIO_HTML_MASK & 8:
        f.write('<th>data<br/>out</th>')
    for c in mio_interfaces:
        f.write('<th>'+c['NAME']+'<br/>'+c['PRINT_CHANNEL']+'&nbsp;</th>')
    f.write('  </tr>\n')
    for pinnum,mio_pin in enumerate(mio):
        f.write('<th>'+str(pinnum)+'</th>')
        if MIO_HTML_MASK & 1:
            f.write('<td>'+hex(mio_pin['ADDR'])+'</td>')
        if MIO_HTML_MASK & 2:
            f.write('<td align="center">'+'-Y'[(mio_pin['VALUE'] >>12) & 1]+'</td>')
            f.write('<td align="center">'+'-Y'[(mio_pin['VALUE'] >> 8) & 1]+'</td>')
            f.write('<td align="center">'+'-Y'[(mio_pin['VALUE'] >> 0) & 1]+'</td>')
            iostd=('INVALID','LVCMOS18','LVCMOS25','LVCMOS33','HSTL','INVALID','INVALID',
                   'INVALID')[(mio_pin['VALUE']>>9)&7]
            disRsv=('','_DISRSV')[(mio_pin['VALUE']>>13)&1]       
            f.write('<td>'+iostd+disRsv+'</td>')
        if MIO_HTML_MASK & 4:
            if not mio_pin['USED_IN']:
                f.write('<td align="center">-</td>')
            else:
                used_in=mio_pin['USED_IN'][len(mio_pin['USED_IN'])-1]
                multichannel=len(used_in['PRINT_CHANNEL'])>0
                f.write('<td align="center">'+(used_in['NAME']+('',' '+str(used_in['CHANNEL']))[multichannel])+'</td>')
#            f.write('<td>'+str(((mio_pin['VALUE'] & (1<< 8)))!=0)+'</td>')
#            f.write('<td>'+str(((mio_pin['VALUE'] & (1<< 0)))!=0)+'</td>')
        f.write('<td>'+hex(mio_pin['VALUE'])+'</td>')
        if MIO_HTML_MASK & 8:
            if 'DATA_OUT' in mio_pin:
                data_out= str(mio_pin['DATA_OUT'])
            else:    
                data_out='-'
            f.write('<td>'+ data_out+'</td>')
        for iface in mio_interfaces:
            signals=iface['IFACE']
            for signal in signals:
                if signals[signal]['PIN']==pinnum:
                    f.write('<td>'+signal+'</td>')
                    break
            else:      
                f.write('<td>&nbsp;</td>')
        f.write('  </tr>\n')
    f.write('</table>\n')
 
def output_gpio_out(registers,f,MIO_HTML_MASK):
    if f:
        f.write ('<H2>GPIO Output mask/data registers</H2>\n')
        f.write('<table border="1">\n')
        f.write('  <tr><th>Register name</th><th>Address</th><th>Data</th></tr>\n')

    for i,word in enumerate (GPIO_MASKDATA):
        en=0
        d=0
        for shft in range (16):
            pinnum=16*i+shft
            if not pinnum in range (len(mio)):
                break
            if 'DATA_OUT' in mio[pinnum]:
                en |= (1<<shft)
                if mio[16*i+shft]['DATA_OUT']:
                    d  |= (1<<shft)
        mask= en ^ 0xffff
        data=   (mask<<16) | d
        registers.append({'ADDRESS':word['ADDRESS'],'DATA':data})
        if f:
            f.write('  <tr><td>'+word['NAME']+'</td><td>'+hex(word['ADDRESS'])+'</td><td>'+hex(data)+'</td></tr>\n')
    if f:
        f.write('  </table>\n')
#Can not be used in register initialization of the RBL
def output_slcr_lock(registers,f,lock,MIO_HTML_MASK):
    if f:
        f.write ('<H2>SLCR lock/unlock</H2>\n')
        f.write('<table border="1">\n')
        f.write('  <tr><th>Register name</th><th>Address</th><th>Data</th></tr>\n')

#    for i,word in enumerate (GPIO_MASKDATA):
    word=SLCR_LOCK[lock!=0]
#    print word
    registers.append({'ADDRESS':word['ADDRESS'],'DATA':word['DATA']})
    if f:
        f.write('  <tr><td>'+word['NAME']+'</td><td>'+hex(word['ADDRESS'])+'</td><td>'+hex(word['DATA'])+'</td></tr>\n')
    if f:
        f.write('  </table>\n')

def uart_remote_loopback(registers,f,uart_num,MIO_HTML_MASK):
    if f:
        f.write ('<H2>UART'+str(uart_num)+' remote loopback</H2>\n')
        f.write('<table border="1">\n')
        f.write('  <tr><th>Register name</th><th>Address</th><th>Data</th></tr>\n')
    word={'NAME':'UART'+str(uart_num)+"_mode_reg0",'ADDRESS':(0xe0000004,0xe0001004)[uart_num!=0],'DATA':0x320}
#    print word       
    registers.append({'ADDRESS':word['ADDRESS'],'DATA':word['DATA']})
    if f:
        f.write('  <tr><td>'+word['NAME']+'</td><td>'+hex(word['ADDRESS'])+'</td><td>'+hex(word['DATA'])+'</td></tr>\n')
    if f:
        f.write('  </table>\n')

        
        
        
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

 
def image_generator (image, registers, user_def,ocm_offset,ocm_len,start_exec):
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
    if args.verbosity >= 1:  print 'Number of registers to initialize',len(registers)
    if len (registers)>256:
        print 'Too many registers to initiAlize, only 256 allowed,',len(registers),'> 256'
    waddr=0xa0/4
    for register in registers:
        if not verify_register_accessible (register['ADDRESS']):
            print 'Tried to set non-accessible register', hex(register['ADDRESS']),' with data ', hex(register['DATA'])
            exit (ERROR_DEFS['NONACCESSIBLE_REGISTER'])
        image[waddr]=register['ADDRESS']
        waddr+=1
        image[waddr]=register['DATA']
        waddr+=1
    #Fill in FFs for unused registers
    while waddr < (0x8c0/4):
        image[waddr]=0xffffffff
        waddr+=1
        image[waddr]=0
        waddr+=1
            
def write_image(image,name):
    bf=open(name,'wb')
#    data=struct.pack('<'+len(image)*'I', image)
#    data=struct.pack('I' * len(image), *image)
#    print tuple(image)
#    data=struct.pack('I' * len(image), tuple(image))
#    N=19
    
#    print len(image[:N]), image[:N]
#    data=struct.pack('I' * len(image), *image[0:10])
    data=struct.pack('I' * len(image), *image)
#    s=struct.Struct('I')
#    data=s.pack(*image)
    bf.write(data)
    bf.close()
         
#=========================
raw_configs=read_config(args.configs)

permit_undefined_bits=False
force=True #False
warn_notfit=True # False
regs_masked=[]
ddr=ezynq_ddr.EzynqDDR(regs_masked,permit_undefined_bits, force, warn_notfit)
ddr.parse_parameters(raw_configs)
##ddr.parse_ddriob_raw_register_set(raw_configs,QUALIFIER_CHAR,force,warn_notfit)
##ddr.parse_ddrc_raw_register_set(raw_configs,QUALIFIER_CHAR,force,warn_notfit)
#ddr.print_html_registers(html_file, show_bit_fields=True, show_comments=True)      
#class EzynqDDR:
#    def __init__(self,permit_undefined_bits=False,force=False,warn=False):
#    def parse_raw_register_set(self,raw_configs,qualifier_char,force=True,warn=True):
#    def print_html_registers(self, html_file, show_bit_fields=True, show_comments=True):




options = parse_config_mio(raw_configs)
if args.verbosity >= 3:
    print options
if args.verbosity >= 1:
    for i, conf in enumerate(options):
        print i, conf, options[conf]
mio_dflts = {'MIO_0_VOLT':0, 'MIO_1_VOLT':0, 'MIO_0_PULLUP':False, 'MIO_1_PULLUP':False};
mio = [{'USED_IN':[], 'IOTYPE':'', 'PULLUP':False, 'FAST':False, 'TRISTATE':False, 'L0':0, 'L1':0, 'L2':0, 'L3':0, 'ADDR':(0xf8000700+k*4), 'HADDR':hex(0xf8000700+k*4)} for k in range(54)]
mio_set_defaults(mio_dflts, mio, options)

mio_interfaces=[]
set_mio_interfaces(mio_interfaces, options)

#populate_mio(mio, mio_interfaces, options,WARN)
apply_mio_interfaces(mio, mio_interfaces,WARN)
set_mio_attribs(mio,options)
parse_mio(mio)
#set MIO pin options and initial value for GPIO output

if args.verbosity >= 1:
    print '\n===== mio_interfaces === '
#print mio_interfaces
    for i, iface in enumerate(mio_interfaces):
        print '-------------'
        print 'i=',i, " iface['NAME']=",iface['NAME'],' channel=',iface['CHANNEL'],' attribs:',iface['ATTRIBS']
        for pin in iface['IFACE']:
            print pin,':',iface['IFACE'][pin]

    print '\n===== mio === '
    for i, mio_pin in enumerate(mio):
        print i, mio_pin
    print mio_dflts  

registers=[] # list of register address/data pairs to be included in the boot fil
#TODO - match HTML and binary data sequence, set the initialization order
#store_mio (mio, registers)   
#if False and MIO_HTML:
if MIO_HTML:
    f=open(MIO_HTML,'w')
else:
    f=False
#output_slcr_lock(registers,f,False,MIO_HTML_MASK) #prohibited by RBL    
output_mio(registers,f,mio,MIO_HTML_MASK)
ddr.calculate_dependent_pars()
ddr.pre_validate() # before applying default values (some timings should be undefined, not defaults)
ddr.check_missing_features() #and apply defualt values
ddr.html_list_features(f) #verify /fix values after defaults are applied
#ddr.ddr_init_memory(current_reg_sets,force=False,warn=False): # will program to sequence 'MAIN'

ddr.ddr_init_memory([],False,False) # will program to sequence 'MAIN'
reg_sets=ddr.get_new_register_sets()

#ezynq_registers.print_html_reg_header(f, title, show_bit_fields=True, show_comments=True,filter_fields=True)
ezynq_registers.print_html_reg_header(f, 'DDR Configuration', MIO_HTML_MASK & 0x100, MIO_HTML_MASK & 0x200, not MIO_HTML_MASK & 0x400)
ezynq_registers.print_html_registers(f, reg_sets, MIO_HTML_MASK & 0x100, MIO_HTML_MASK & 0x200, not MIO_HTML_MASK & 0x400)
#print_html_registers(html_file, reg_sets, show_bit_fields=True, show_comments=True,filter_fields=True):

ezynq_registers.print_html_reg_footer(f)






#ddr.print_html_registers(f, MIO_HTML_MASK & 0x100, MIO_HTML_MASK & 0x200, not MIO_HTML_MASK & 0x400)  #filter_fields=True


#output_gpio_out(registers,f,MIO_HTML_MASK)        #prohibited by RBL
#output_slcr_lock(registers,f,True,MIO_HTML_MASK)  #prohibited by RBL
if 'CONFIG_EZYNQ_UART_LOOPBACK_0' in options: uart_remote_loopback(registers,f, 0,MIO_HTML_MASK)
if 'CONFIG_EZYNQ_UART_LOOPBACK_1' in options: uart_remote_loopback(registers,f, 1,MIO_HTML_MASK)


if MIO_HTML:
    f.close
if args.verbosity >= 1:
    print registers
image =[ 0 for k in range (0x8c0/4)]

#image_generator (image, registers, user_def,start_offset,ocm_len,start_exec)
#CONFIG_EZYNQ_BOOT_USERDEF=           0x1234567 # will be saved in the file header
#CONFIG_EZYNQ_BOOT_OCM_OFFSET=        0x8C0   # start of OCM data relative to the flash image start >=0x8C0, 63-bytes aligned
#CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH=  0x30000 # number of bytes to load to the OCM memory, <= 0x30000 
#CONFIG_EZYNQ_START_EXEC=             0x20 # number of bytes to load to the OCM memory, <= 0x30000 

image_generator (image,
                 registers,
                 int(options['CONFIG_EZYNQ_BOOT_USERDEF'],0), # user_def
                 int(options['CONFIG_EZYNQ_BOOT_OCM_OFFSET'],0), # ocm_offset,
                 int(options['CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH'],0), #ocm_len,
                 int(options['CONFIG_EZYNQ_START_EXEC'],0)) #start_exec)
if args.outfile:
    write_image(image,args.outfile)
# print int(hex(1234567),0) # works for decimal and hex
 
# binary i/o - tutorial 11.3
