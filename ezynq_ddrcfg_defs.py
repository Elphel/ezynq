#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# Definitions of configuration parameters for DDR memory 
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
#Use 'TYPE':'I' for decimal output, 'H' - for hex. On input both are accepted
DDR_CFG_DEFS=[
    {'NAME':'ENABLE',          'CONF_NAME':'CONFIG_EZYNQ_DDR_ENABLE','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':True,
                'DESCRIPTION':'Enable DDR memory'},              
    {'NAME':'MEMORY_TYPE',     'CONF_NAME':'CONFIG_EZYNQ_DDR_MEMORY_TYPE','TYPE':('DDR3','DDR3L','DDR2','LPDDR2'),'MANDATORY':True,'DERIVED':False,'DEFAULT':'DDR3',
                'DESCRIPTION':'DDR memory type'},              
    {'NAME':'TARGET_FREQ_MHZ', 'CONF_NAME':'CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ','TYPE':'F','MANDATORY':True,'DERIVED':True,'DEFAULT':533.333333,
                'DESCRIPTION':'Target DDR clock frequency in MHz (actual frequency will depend on the clock/clock muxes)'},              
    {'NAME':'FREQ_MHZ',        'CONF_NAME':'CONFIG_EZYNQ_DDR_FREQ_MHZ','TYPE':'F','MANDATORY':True,'DERIVED':True,'DEFAULT':533.333333,
                'DESCRIPTION':'Actual DDR clock frequency in MHz, may be derived form CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ and clock multiplexer settings'},              
    {'NAME':'CL',              'CONF_NAME':'CONFIG_EZYNQ_DDR_CL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'CAS read latency (in tCK)'},              
    {'NAME':'AL',              'CONF_NAME':'CONFIG_EZYNQ_DDR_AL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':0,
                'DESCRIPTION':'Posted CAS additive latency (in tCK)'},              
    {'NAME':'CWL',             'CONF_NAME':'CONFIG_EZYNQ_DDR_CWL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':6,
                'DESCRIPTION':'CAS write latency (in tCK)'},              
    {'NAME':'RCD',             'CONF_NAME':'CONFIG_EZYNQ_DDR_RCD','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'RAS to CAS delay (in tCK)'},              
    {'NAME':'RP',              'CONF_NAME':'CONFIG_EZYNQ_DDR_RP','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'Row Precharge time (in tCK)'},              
    {'NAME':'T_RC',            'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RC','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':48.75,
                'DESCRIPTION':'Activate to Activate or Refresh command period (ns)'},              
    {'NAME':'T_RAS_MIN',       'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RAS_MIN','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':35.0,
                'DESCRIPTION':'Minimal Row Active time (ns)'},              
    {'NAME':'T_FAW',           'CONF_NAME':'CONFIG_EZYNQ_DDR_T_FAW','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':40.0,
                'DESCRIPTION':'Minimal running window for 4 page activates (ns)'},   
    {'NAME':'T_RFC',           'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RFC','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':350.0,
                'DESCRIPTION':'Minimal Refresh-to-Activate or Refresh command period (ns)'},   
    {'NAME':'T_WR',           'CONF_NAME':'CONFIG_EZYNQ_DDR_T_WR','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':15.0,
                'DESCRIPTION':'Write recovery time (ns)'},   
    {'NAME':'BANK_ADDR_COUNT', 'CONF_NAME':'CONFIG_EZYNQ_DDR_BANK_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':3,
                'DESCRIPTION':'Number of DDR banks'},              
    {'NAME':'ROW_ADDR_COUNT',  'CONF_NAME':'CONFIG_EZYNQ_DDR_ROW_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':15,
                'DESCRIPTION':'Number of DDR banks'},              
    {'NAME':'COL_ADDR_COUNT',  'CONF_NAME':'CONFIG_EZYNQ_DDR_COL_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':10,
                'DESCRIPTION':'Number of DDR banks'},              
    {'NAME':'ECC',             'CONF_NAME':'CONFIG_EZYNQ_DDR_ECC','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Enable ECC for the DDR memory'},
    {'NAME':'BUS_WIDTH',       'CONF_NAME':'CONFIG_EZYNQ_DDR_BUS_WIDTH','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':32,
                'DESCRIPTION':'SoC DDR bus width'},
    {'NAME':'BL',              'CONF_NAME':'CONFIG_EZYNQ_DDR_BL','TYPE':(8,4),'MANDATORY':True,'DERIVED':False,'DEFAULT':8, # DDR2 may have different lengths?
                'DESCRIPTION':'Burst length'},
    {'NAME':'HIGH_TEMP',       'CONF_NAME':'CONFIG_EZYNQ_DDR_HIGH_TEMP','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'High temperature (influences refresh)'},
    {'NAME':'T_REFI_US',           'CONF_NAME':'CONFIG_EZYNQ_DDR_T_REFI_US','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.8,
                'DESCRIPTION':'Maximal average periodic refresh, microseconds. Will be automatically reduced if high temperature option is selected'},              

    {'NAME':'PARTNO',          'CONF_NAME':'CONFIG_EZYNQ_DDR_PARTNO','TYPE':'T','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Memory part number  (currently not used - derive some parameters later)'},
    {'NAME':'DRAM_WIDTH',      'CONF_NAME':'CONFIG_EZYNQ_DDR_DRAM_WIDTH','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':16,
                'DESCRIPTION':'Memory chip bus width'},
    {'NAME':'SPEED_BIN',       'CONF_NAME':'CONFIG_EZYNQ_DDR_SPEED_BIN','TYPE':'T','MANDATORY':True,'DERIVED':False,'DEFAULT':'DDR3_1066F',
                'DESCRIPTION':'Memory speed bin (currently not used - derive timing later)'},
    {'NAME':'TRAIN_WRITE_LEVEL','CONF_NAME':'CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Automatically train write leveling during initialization'},
    {'NAME':'TRAIN_READ_GATE', 'CONF_NAME':'CONFIG_EZYNQ_DDR_TRAIN_READ_GATE','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Automatically train read gate timing during initialization'},
    {'NAME':'TRAIN_DATA_EYE',  'CONF_NAME':'CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Automatically train data eye during initialization'},
    {'NAME':'CLOCK_STOP_EN',   'CONF_NAME':'CONFIG_EZYNQ_DDR_CLOCK_STOP_EN','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Enable clock stop'},
    {'NAME':'INTERNAL_VREF',   'CONF_NAME':'CONFIG_EZYNQ_DDR_USE_INTERNAL_VREF','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Use internal Vref'},
    {'NAME':'OUT_SLEW_NEG',    'CONF_NAME':'CONFIG_EZYNQ_DDR_OUT_SLEW_NEG','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':26,
                'DESCRIPTION':'Slew rate negative for DDR address/clock outputs'},
    {'NAME':'OUT_SLEW_POS',    'CONF_NAME':'CONFIG_EZYNQ_DDR_OUT_SLEW_POS','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':26,
                'DESCRIPTION':'Slew rate positive for DDR address/clock outputs'},
    {'NAME':'OUT_DRIVE_NEG',   'CONF_NAME':'CONFIG_EZYNQ_DDR_OUT_DRIVE_NEG','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':12,
                'DESCRIPTION':'Drive strength negative for DDR address/clock outputs'},
    {'NAME':'OUT_DRIVE_POS',   'CONF_NAME':'CONFIG_EZYNQ_DDR_OUT_DRIVE_POS','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':28,
                'DESCRIPTION':'Drive strength positive for DDR address/clock outputs'},
    {'NAME':'BIDIR_SLEW_NEG',    'CONF_NAME':'CONFIG_EZYNQ_DDR_BIDIR_SLEW_NEG','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':31,
                'DESCRIPTION':'Slew rate negative for driving DDR DQ/DQS signals'},
    {'NAME':'BIDIR_SLEW_POS',    'CONF_NAME':'CONFIG_EZYNQ_DDR_BIDIR_SLEW_POS','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':6,
                'DESCRIPTION':'Drive strength positive for driving DDR DQ/DQS signals'},
    {'NAME':'BIDIR_DRIVE_NEG',   'CONF_NAME':'CONFIG_EZYNQ_DDR_BIDIR_DRIVE_NEG','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':12,
                'DESCRIPTION':'Drive strength negative for driving DDR DQ/DQS signals'},
    {'NAME':'BIDIR_DRIVE_POS',   'CONF_NAME':'CONFIG_EZYNQ_DDR_BIDIR_DRIVE_POS','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':28,
                'DESCRIPTION':'Slew rate positive for driving DDR DQ/DQS signals'},
    {'NAME':'RTP',             'CONF_NAME':'CONFIG_EZYNQ_DDR_RTP','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':4,
                'DESCRIPTION':'Minimal Read-to-Precharge time (in tCK). Will use max of this and CONFIG_EZYNQ_DDR_T_RTP/CONFIG_EZYNQ_DDR_T_CK'},              
    {'NAME':'T_RTP',           'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RTP','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'Minimal Read-to-Precharge time  (ns). Will use max of this divided by CONFIG_EZYNQ_DDR_T_CK and CONFIG_EZYNQ_DDR_RTP'},   
    {'NAME':'WTR',             'CONF_NAME':'CONFIG_EZYNQ_DDR_WTR','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':4,
                'DESCRIPTION':'Minimal Write-to-Read time (in tCK). Will use max of this and CONFIG_EZYNQ_DDR_T_WTR/CONFIG_EZYNQ_DDR_T_CK'},              
    {'NAME':'T_WTR',           'CONF_NAME':'CONFIG_EZYNQ_DDR_T_WTR','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'Minimal Write-to-Read time  (ns). Will use max of this divided by CONFIG_EZYNQ_DDR_T_CK and CONFIG_EZYNQ_DDR_WTR'},   
    {'NAME':'XP',             'CONF_NAME':'CONFIG_EZYNQ_DDR_XP','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':4,
                'DESCRIPTION':'Minimal Minimal time from power down (DLL on) to any operation (in tCK)'},              
    {'NAME':'T_DQSCK_MAX',           'CONF_NAME':'CONFIG_EZYNQ_DDR_T_DQSCK_MAX','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'DQS output access time from CK (ns). Used for LPDDR2'},   

    {'NAME':'T_RP',           'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RP','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':13.1,
                'DESCRIPTION':'Precharge command period (ns).  May be used to calculate CONFIG_EZYNQ_DDR_RP automatically'},   
    {'NAME':'T_RCD',          'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RCD','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':13.1,
                'DESCRIPTION':'Activate to internal Read or Write (ns). May be used to calculate CONFIG_EZYNQ_DDR_RCD automatically'},   

    {'NAME':'CCD',             'CONF_NAME':'CONFIG_EZYNQ_DDR_CCD','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':5,
                'DESCRIPTION':'CAS-to-CAS command delay (in tCK)'},              
    {'NAME':'RRD',             'CONF_NAME':'CONFIG_EZYNQ_DDR_RRD','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':6,
                'DESCRIPTION':'ACTIVATE-to-ACTIVATE minimal command period (in tCK)'},              
    {'NAME':'T_RRD',          'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RRD','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':10.0,
                'DESCRIPTION':'ACTIVATE-to-ACTIVATE minimal command period (ns). May be used to calculate CONFIG_EZYNQ_DDR_RRD automatically'},   

              
# CONFIG_EZYNQ_DDR_T_RTP = 7.5
# CONFIG_EZYNQ_DDR_WTR = 4
# CONFIG_EZYNQ_DDR_T_WTR = 7.5
# CONFIG_EZYNQ_DDR_XP = 4 # power down (DLL on) to any operation, cycles
# CONFIG_EZYNQ_DDR_T_DQSCK_MAX = 5.5 # (LPDDR2 only)
# CONFIG_EZYNQ_DDR_T_RP = 13.1
# CONFIG_EZYNQ_DDR_T_RCD = 13.1
# CONFIG_EZYNQ_DDR_CCD = 4
# CONFIG_EZYNQ_DDR_RRD = 4
# CONFIG_EZYNQ_DDR_T_RRD = 10.0
              
]


#TODO make some of (possibly) derived, leave '_T_' for ns only!
# CONFIG_EZYNQ_DDR_FREQ_MHZ = 533.333333 *
# CONFIG_EZYNQ_DDR_CL = 7  *
# CONFIG_EZYNQ_DDR_CWL = 6  *
# CONFIG_EZYNQ_DDR_RCD = 7 (was CONFIG_EZYNQ_DDR_T_RCD = 7) *
# CONFIG_EZYNQ_DDR_RP = 7 (was CONFIG_EZYNQ_DDR_T_RP = 7) *
# CONFIG_EZYNQ_DDR_T_RC = 48.75 *
# CONFIG_EZYNQ_DDR_T_RAS_MIN = 35.0 *
# CONFIG_EZYNQ_DDR_T_FAW = 40.0 *
# CONFIG_EZYNQ_DDR_T_RFC = 350.0
# CONFIG_EZYNQ_DDR_T_WR =  15.0
# CONFIG_EZYNQ_DDR_RTP = 4
# CONFIG_EZYNQ_DDR_tRTP = 7.5
# CONFIG_EZYNQ_DDR_WTR = 4
# CONFIG_EZYNQ_DDR_tWTR = 7.5


# CONFIG_EZYNQ_DDR_AL = 0 *
# CONFIG_EZYNQ_DDR_BANK_ADDR_COUNT = 3 *
# CONFIG_EZYNQ_DDR_ROW_ADDR_COUNT = 15 *
# CONFIG_EZYNQ_DDR_COL_ADDR_COUNT = 10 *

# CONFIG_EZYNQ_DDR_ENABLE = 1          *
# CONFIG_EZYNQ_DDR_MEMORY_TYPE = DDR3  *
# CONFIG_EZYNQ_DDR_ECC = Disabled      *
# CONFIG_EZYNQ_DDR_BUS_WIDTH = 32      *
# CONFIG_EZYNQ_DDR_BL = 8              *
# CONFIG_EZYNQ_DDR_T_REFI_US = 7.8 *
# CONFIG_EZYNQ_DDR_HIGH_TEMP = Normal  *
# CONFIG_EZYNQ_DDR_PARTNO = MT41K256M16RE-125 *
# CONFIG_EZYNQ_DDR_DRAM_WIDTH = 16     *
# CONFIG_EZYNQ_DDR_SPEED_BIN = DDR3_1066F *
# CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL = 0
# CONFIG_EZYNQ_DDR_TRAIN_READ_GATE = 0
# CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE = 0
# CONFIG_EZYNQ_DDR_CLOCK_STOP_EN = 0
# CONFIG_EZYNQ_DDR_USE_INTERNAL_VREF = 0

#CONFIG_EZYNQ_DDR_DEVICE_CAPACITY_MBITS = 4096 - can be calculated

