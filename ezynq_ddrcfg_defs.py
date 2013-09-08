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
    {'NAME':'TARGET_FREQ_MHZ', 'CONF_NAME':'CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ','TYPE':'F','MANDATORY':True,'DERIVED':True,'DEFAULT':533.333333,
                'DESCRIPTION':'Target DDR clock frequency in MHz (actual frequency will depend on the clock/clock muxes)'},              
    {'NAME':'FREQ_MHZ',        'CONF_NAME':'CONFIG_EZYNQ_DDR_FREQ_MHZ','TYPE':'F','MANDATORY':True,'DERIVED':True,'DEFAULT':533.333333,
                'DESCRIPTION':'Actual DDR clock frequency in MHz, may be derived form CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ and clock multiplexer settings'},
    {'NAME':'BANK_ADDR_MAP',  'CONF_NAME':'CONFIG_EZYNQ_DDR_BANK_ADDR_MAP','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':10,
                'DESCRIPTION':'DRAM address mapping: number of combined column and row addresses lower than BA0'},              
    {'NAME':'ARB_PAGE_BANK',  'CONF_NAME':'CONFIG_EZYNQ_DDR_ARB_PAGE_BANK','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Enable Arbiter prioritization based on page/bank match'},              
    {'NAME':'ECC',             'CONF_NAME':'CONFIG_EZYNQ_DDR_ECC','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Enable ECC for the DDR memory'},
    {'NAME':'BUS_WIDTH',       'CONF_NAME':'CONFIG_EZYNQ_DDR_BUS_WIDTH','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':32,
                'DESCRIPTION':'SoC DDR bus width'},
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
              
###### DDR Dependent ######
    {'NAME':'CL',              'CONF_NAME':'CONFIG_EZYNQ_DDR_CL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'CAS read latency (in tCK)'},              
    {'NAME':'CWL',             'CONF_NAME':'CONFIG_EZYNQ_DDR_CWL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':6,
                'DESCRIPTION':'CAS write latency (in tCK)'},              
    {'NAME':'AL',              'CONF_NAME':'CONFIG_EZYNQ_DDR_AL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':0,
                'DESCRIPTION':'Posted CAS additive latency (in tCK)'},
    {'NAME':'BL',              'CONF_NAME':'CONFIG_EZYNQ_DDR_BL','TYPE':(8,4,16),'MANDATORY':True,'DERIVED':False,'DEFAULT':8, # DDR2 may have different lengths?
                'DESCRIPTION':'Burst length, 16 is only supported for LPDDR2'},
    {'NAME':'HIGH_TEMP',       'CONF_NAME':'CONFIG_EZYNQ_DDR_HIGH_TEMP','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'High temperature (influences refresh)'},
    {'NAME':'SPEED_BIN',       'CONF_NAME':'CONFIG_EZYNQ_DDR_SPEED_BIN','TYPE':'T','MANDATORY':True,'DERIVED':False,'DEFAULT':'DDR3_1066F',
                'DESCRIPTION':'Memory speed bin (currently not used - derive timing later)'}, # not yet used
    {'NAME':'DDR2_RTT',      'CONF_NAME':'CONFIG_EZYNQ_DDR_DDR2_RTT','TYPE':('DISABLED','75','150','50'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'75',
                'DESCRIPTION':'DDR2 on-chip termination, Ohm'},              
    {'NAME':'DDR3_RTT',      'CONF_NAME':'CONFIG_EZYNQ_DDR_DDR3_RTT','TYPE':('DISABLED','60','120','40'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'60',
                'DESCRIPTION':'DDR3 on-chip termination, Ohm'}, # Does not include 20 & 30 - not clear if DDRC can use them with auto write leveling               
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
              
###### DDR Datasheet #######
    {'NAME':'PARTNO',          'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_PARTNO','TYPE':'T','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'DESCRIPTION':'Memory part number  (currently not used - derive some parameters later)'},
    {'NAME':'MEMORY_TYPE',     'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_MEMORY_TYPE','TYPE':('DDR3','DDR3L','DDR2','LPDDR2'),'MANDATORY':True,'DERIVED':False,'DEFAULT':'DDR3',
                'DESCRIPTION':'DDR memory type: DDR3 (1.5V), DDR3L (1.35V), DDR2 (1.8V), LPDDR2 (1.2V)'},
    {'NAME':'BANK_ADDR_COUNT', 'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_BANK_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':3,
                'DESCRIPTION':'Number of DDR banks'},              
    {'NAME':'ROW_ADDR_COUNT',  'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_ROW_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':15,
                'DESCRIPTION':'Number of DDR row address bits'},              
    {'NAME':'COL_ADDR_COUNT',  'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_COL_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':10,
                'DESCRIPTION':'Number of DDR column address bits'},              
    {'NAME':'DRAM_WIDTH',      'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_DRAM_WIDTH','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':16,
                'DESCRIPTION':'Memory chip bus width'},# not used
    {'NAME':'RCD',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_RCD','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'RAS to CAS delay (in tCK)'}, 
    {'NAME':'T_RCD',          'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_RCD','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':13.1,
                'DESCRIPTION':'Activate to internal Read or Write (ns). May be used to calculate CONFIG_EZYNQ_DDR_DS_RCD automatically'},   
    {'NAME':'RP',              'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_RP','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'Row Precharge time (in tCK)'},              
    {'NAME':'T_RP',           'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_RP','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':13.1,
                'DESCRIPTION':'Precharge command period (ns).  May be used to calculate CONFIG_EZYNQ_DDR_DS_RP automatically'},   
    {'NAME':'T_RC',            'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_RC','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':48.75,
                'DESCRIPTION':'Activate to Activate or Refresh command period (ns)'},              
    {'NAME':'T_RAS_MIN',       'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_RAS_MIN','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':35.0,
                'DESCRIPTION':'Minimal Row Active time (ns)'},              
    {'NAME':'T_FAW',           'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_FAW','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':40.0,
                'DESCRIPTION':'Minimal running window for 4 page activates (ns)'},   
    {'NAME':'T_RFC',           'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_RFC','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':350.0,
                'DESCRIPTION':'Minimal Refresh-to-Activate or Refresh command period (ns)'},   
    {'NAME':'T_WR',           'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_WR','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':15.0,
                'DESCRIPTION':'Write recovery time (ns)'},   
    {'NAME':'T_REFI_US',           'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_REFI_US','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.8,
                'DESCRIPTION':'Maximal average periodic refresh, microseconds. Will be automatically reduced if high temperature option is selected'},              
    {'NAME':'RTP',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_RTP','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':4,
                'DESCRIPTION':'Minimal Read-to-Precharge time (in tCK). Will use max of this and CONFIG_EZYNQ_DDR_DS_T_RTP/tCK'},              
    {'NAME':'T_RTP',           'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_RTP','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'Minimal Read-to-Precharge time  (ns). Will use max of this divided by tCK and CONFIG_EZYNQ_DDR_DS_RTP'},   
    {'NAME':'WTR',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_WTR','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':4,
                'DESCRIPTION':'Minimal Write-to-Read time (in tCK). Will use max of this and CONFIG_EZYNQ_DDR_DS_T_WTR/tCK'},              
    {'NAME':'T_WTR',           'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_WTR','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'Minimal Write-to-Read time  (ns). Will use max of this divided by tCK and CONFIG_EZYNQ_DDR_DS_WTR'},   
    {'NAME':'XP',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_XP','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':4,
                'DESCRIPTION':'Minimal time from power down (DLL on) to any operation (in tCK)'},              
    {'NAME':'T_DQSCK_MAX',           'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_DQSCK_MAX','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'DQS output access time from CK (ns). Used for LPDDR2'},   
    {'NAME':'CCD',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_CCD','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':5,
                'DESCRIPTION':'CAS-to-CAS command delay (in tCK)'},              
    {'NAME':'RRD',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_RRD','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':6,
                'DESCRIPTION':'ACTIVATE-to-ACTIVATE minimal command period (in tCK)'},              
    {'NAME':'T_RRD',          'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_RRD','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':10.0,
                'DESCRIPTION':'ACTIVATE-to-ACTIVATE minimal command period (ns). May be used to calculate CONFIG_EZYNQ_DDR_DS_RRD automatically'},   
    {'NAME':'MRD',            'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_MRD','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':4,
                'DESCRIPTION':'MODE REGISTER SET command period (in tCK)'},
    {'NAME':'MOD',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_MOD','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':12,
                'DESCRIPTION':'MODE REGISTER SET update delay (in tCK)'},              
    {'NAME':'T_MOD',          'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_MOD','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':15.0,
                'DESCRIPTION':'MODE REGISTER SET update delay  (ns).'},   
    {'NAME':'T_WLMRD',          'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_WLMRD','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':40.0,
                'DESCRIPTION':'Write leveling : time to the first DQS rising edge (ns).'},
    {'NAME':'CKE',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_CKE','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':3,
                'DESCRIPTION':'CKE min pulse width (in tCK)'},              
    {'NAME':'T_CKE',          'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_CKE','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'CKE min pulse width (ns).'},   
    {'NAME':'CKSRE',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_CKSRE','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':3,
                'DESCRIPTION':'Keep valid clock after self refresh/power down entry (in tCK)'},              
    {'NAME':'T_CKSRE',          'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_CKSRE','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'Keep valid clock after self refresh/power down entry (ns).'},   
    {'NAME':'CKSRX',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_CKSRX','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':3,
                'DESCRIPTION':'Valid clock before self refresh, power down or reset exit (in tCK)'},              
    {'NAME':'T_CKSRX',          'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_CKSRX','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':7.5,
                'DESCRIPTION':'Valid clock before self refresh, power down or reset exit (ns).'},   
    {'NAME':'ZQCS',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_ZQCS','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':64,
                'DESCRIPTION':'ZQCS command: short calibration time (in tCK)'},              
    {'NAME':'ZQCL',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_ZQCL','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':512,
                'DESCRIPTION':'ZQCL command: long calibration time, including init (in tCK)'},
    {'NAME':'INIT2',             'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_INIT2','TYPE':'I','MANDATORY':False,'DERIVED':False,'DEFAULT':5,
                'DESCRIPTION':'LPDDR2 only: tINIT2 (in tCK): clock stable before CKE high'},
    {'NAME':'T_INIT4_US',        'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_INIT4_US','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1.0,
                'DESCRIPTION':'LPDDR2 only: tINIT4 (in us)- minimal idle time after RESET command.'},   
    {'NAME':'T_INIT5_US',        'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_INIT5_US','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':10.0,
                'DESCRIPTION':'LPDDR2 only: tINIT5 (in us)- maximal duration of device auto initialization.'},   
    {'NAME':'T_ZQINIT_US',       'CONF_NAME':'CONFIG_EZYNQ_DDR_DS_T_ZQINIT_US','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1.0,
                'DESCRIPTION':'LPDDR2 only: tZQINIT (in us)- ZQ initial calibration time.'},   
]


# CONFIG_EZYNQ_DDR_DS_T_INIT4_US =  1.0 #(us) LPDDR2 ONLY
# CONFIG_EZYNQ_DDR_DS_T_INIT5_US =  10.0 #(us) LPDDR2 ONLY
# CONFIG_EZYNQ_DDR_DS_T_ZQINIT_US = 1.0 #(us) LPDDR2 ONLY
# CONFIG_EZYNQ_DDR3_RTT = 60 # DISABLED, 60,120,40 - only used for DDR3              
# CONFIG_EZYNQ_DDR2_RTT = 75 # DISABLED, 75,150,50 - only used for DDR2              
# CONFIG_EZYNQ_DDR_DS_T_RTP = 7.5
# CONFIG_EZYNQ_DDR_DS_WTR = 4
# CONFIG_EZYNQ_DDR_DS_T_WTR = 7.5
# CONFIG_EZYNQ_DDR_DS_XP = 4 # power down (DLL on) to any operation, cycles
# CONFIG_EZYNQ_DDR_DS_T_DQSCK_MAX = 5.5 # (LPDDR2 only)
# CONFIG_EZYNQ_DDR_DS_T_RP = 13.1
# CONFIG_EZYNQ_DDR_DS_T_RCD = 13.1
# CONFIG_EZYNQ_DDR_DS_CCD = 4
# CONFIG_EZYNQ_DDR_DS_RRD = 4
# CONFIG_EZYNQ_DDR_DS_T_RRD = 10.0
# CONFIG_EZYNQ_DDR_DS_MRD = 4
# CONFIG_EZYNQ_DDR_DS_T_WLMRD = 40.0 #
# CONFIG_EZYNQ_DDR_DS_T_MOD = 15.0
# CONFIG_EZYNQ_DDR_DS_MOD =   12

 
# CONFIG_EZYNQ_DDR_DS_T_CKE = 5.625 # 7.5
# CONFIG_EZYNQ_DDR_DS_CKE =   3

# CONFIG_EZYNQ_DDR_DS_T_CKSRE = 10.0
# CONFIG_EZYNQ_DDR_DS_CKSRE =   5

# CONFIG_EZYNQ_DDR_DS_T_CKSRX = 10.0
# CONFIG_EZYNQ_DDR_DS_CKSRX =   5

#CONFIG_EZYNQ_DDR_DS_ZQCS = 64
#CONFIG_EZYNQ_DDR_DS_ZQCL = 512

# CONFIG_EZYNQ_DDR_DS_INIT2 = 5 #LPDDR2 ONLY
# CONFIG_EZYNQ_DDR_DS_T_INIT4_US =  1.0 #(us) LPDDR2 ONLY
# CONFIG_EZYNQ_DDR_DS_T_INIT5_US =  10.0 #(us) LPDDR2 ONLY
# CONFIG_EZYNQ_DDR_DS_T_ZQINIT_US = 1.0 #(us) LPDDR2 ONLY




#TODO make some of (possibly) derived, leave '_T_' for ns only!
# CONFIG_EZYNQ_DDR_FREQ_MHZ = 533.333333 *
# CONFIG_EZYNQ_DDR_CL = 7  *
# CONFIG_EZYNQ_DDR_CWL = 6  *
# CONFIG_EZYNQ_DDR_DS_RCD = 7 (was CONFIG_EZYNQ_DDR_DS_T_RCD = 7) *
# CONFIG_EZYNQ_DDR_DS_RP = 7 (was CONFIG_EZYNQ_DDR_DS_T_RP = 7) *
# CONFIG_EZYNQ_DDR_DS_T_RC = 48.75 *
# CONFIG_EZYNQ_DDR_DS_T_RAS_MIN = 35.0 *
# CONFIG_EZYNQ_DDR_DS_T_FAW = 40.0 *
# CONFIG_EZYNQ_DDR_DS_T_RFC = 350.0
# CONFIG_EZYNQ_DDR_DS_T_WR =  15.0
# CONFIG_EZYNQ_DDR_DS_RTP = 4
# CONFIG_EZYNQ_DDR_DS_T_RTP = 7.5
# CONFIG_EZYNQ_DDR_DS_WTR = 4
# CONFIG_EZYNQ_DDR_DS_T_WTR = 7.5


# CONFIG_EZYNQ_DDR_AL = 0 *
# CONFIG_EZYNQ_DDR_DS_BANK_ADDR_COUNT = 3 *
# CONFIG_EZYNQ_DDR_DS_ROW_ADDR_COUNT = 15 *
# CONFIG_EZYNQ_DDR_DS_COL_ADDR_COUNT = 10 *
# CONFIG_EZYNQ_DDR_BANK_ADDR_MAP  = 10
# CONFIG_EZYNQ_DDR_ARB_PAGE_BANK  = Y

# CONFIG_EZYNQ_DDR_ENABLE = 1          *
# CONFIG_EZYNQ_DDR_DS_MEMORY_TYPE = DDR3  *
# CONFIG_EZYNQ_DDR_ECC = Disabled      *
# CONFIG_EZYNQ_DDR_BUS_WIDTH = 32      *
# CONFIG_EZYNQ_DDR_BL = 8              *
# CONFIG_EZYNQ_DDR_DS_T_REFI_US = 7.8 *
# CONFIG_EZYNQ_DDR_HIGH_TEMP = Normal  *
# CONFIG_EZYNQ_DDR_DS_PARTNO = MT41K256M16RE-125 *
# CONFIG_EZYNQ_DDR_DS_DRAM_WIDTH = 16     *
# CONFIG_EZYNQ_DDR_SPEED_BIN = DDR3_1066F *
# CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL = 0
# CONFIG_EZYNQ_DDR_TRAIN_READ_GATE = 0
# CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE = 0
# CONFIG_EZYNQ_DDR_CLOCK_STOP_EN = 0
# CONFIG_EZYNQ_DDR_USE_INTERNAL_VREF = 0

#CONFIG_EZYNQ_DDR_DEVICE_CAPACITY_MBITS = 4096 - can be calculated

