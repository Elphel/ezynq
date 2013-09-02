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
DDR_CFG_DEFS={
    'TARGET_FREQ_MHZ': {'CONF_NAME':'CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ','TYPE':'F','MANDATORY':True,'DERIVED':True,'DEFAULT':533.333333,
                'DESCRIPTION':'Target DDR clock frequency in MHz (actual frequency will depend on the clock/clock muxes)'},              
    'FREQ_MHZ':        {'CONF_NAME':'CONFIG_EZYNQ_DDR_FREQ_MHZ','TYPE':'F','MANDATORY':True,'DERIVED':True,'DEFAULT':533.333333,
                'DESCRIPTION':'Actual DDR clock frequency in MHz, may be derived form CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ and clock multiplexer settings'},              
    'CL':              {'CONF_NAME':'CONFIG_EZYNQ_DDR_CL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'CAS read latency (in tCK)'},              
    'AL':              {'CONF_NAME':'CONFIG_EZYNQ_DDR_CL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':0,
                'DESCRIPTION':'Posted CAS additive latency (in tCK)'},              
    'CWL':             {'CONF_NAME':'CONFIG_EZYNQ_DDR_CWL','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':6,
                'DESCRIPTION':'CAS write latency (in tCK)'},              
    'RCD':             {'CONF_NAME':'CONFIG_EZYNQ_DDR_RCD','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'RAS to CAS delay (in tCK)'},              
    'RP':              {'CONF_NAME':'CONFIG_EZYNQ_DDR_RP','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':7,
                'DESCRIPTION':'Row Precharge time (in tCK)'},              
    'T_RC':            {'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RC','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':48.75,
                'DESCRIPTION':'Activate to Activate or Refresh command period (ns)'},              
    'T_RAS_MIN':       {'CONF_NAME':'CONFIG_EZYNQ_DDR_T_RAS_MIN','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':35.0,
                'DESCRIPTION':'Minimal Row Active time (ns)'},              
    'T_FAW':           {'CONF_NAME':'CONFIG_EZYNQ_DDR_T_FAW','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':40.0,
                'DESCRIPTION':'Minimal running window for 4 page activates (ns)'},              
    'BANK_ADDR_COUNT': {'CONF_NAME':'CONFIG_EZYNQ_DDR_BANK_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':3,
                'Number of DDR banks'},              
    'ROW_ADDR_COUNT':  {'CONF_NAME':'CONFIG_EZYNQ_DDR_ROW_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':15,
                'Number of DDR banks'},              
    'COL_ADDR_COUNT':  {'CONF_NAME':'CONFIG_EZYNQ_DDR_COL_ADDR_COUNT','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':10,
                'Number of DDR banks'},              
    'ENABLE':          {'CONF_NAME':'CONFIG_EZYNQ_DDR_ENABLE','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':True,
                'Enable DDR memory'},              
    'MEMORY_TYPE':     {'CONF_NAME':'CONFIG_EZYNQ_DDR_MEMORY_TYPE','TYPE':('DDR3','DDR2','LPDDR2'),'MANDATORY':True,'DERIVED':False,'DEFAULT':'DDR3',
                'DDR memory type'},              
    'ECC':             {'CONF_NAME':'CONFIG_EZYNQ_DDR_ECC','TYPE':'B','MANDATORY':False,'DERIVED':False,'DEFAULT':False,
                'Enable ECC for the DDR memory'},
    'BUS_WIDTH':       {'CONF_NAME':'CONFIG_EZYNQ_DDR_BUS_WIDTH','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':32,
                'SoC DDR bus width'},
    'BL':              {'CONF_NAME':'CONFIG_EZYNQ_DDR_BL','TYPE':(4,8),'MANDATORY':True,'DERIVED':False,'DEFAULT':8, # DDR2 may have different lengths?
                'Burst length'},
    'HIGH_TEMP':       {'CONF_NAME':'CONFIG_EZYNQ_DDR_HIGH_TEMP','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'High temperature (influences refresh)'},
    'PARTNO':          {'CONF_NAME':'CONFIG_EZYNQ_DDR_PARTNO','TYPE':'T','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'Memory part number  (currently not used - derive some parameters late)'},
    'DRAM_WIDTH':      {'CONF_NAME':'CONFIG_EZYNQ_DDR_DRAM_WIDTH','TYPE':'I','MANDATORY':True,'DERIVED':False,'DEFAULT':16,
                'Memory chip bus width'},
    'SPEED_BIN':       {'CONF_NAME':'CONFIG_EZYNQ_DDR_SPEED_BIN','TYPE':'T','MANDATORY':True,'DERIVED':False,'DEFAULT':16,
                'Memory speed bin (currently not used - derive timing later)'},
    'TRAIN_WRITE_LEVEL':{'CONF_NAME':'CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'Automatically train write leveling during initialization'},
    'TRAIN_READ_GATE': {'CONF_NAME':'CONFIG_EZYNQ_DDR_TRAIN_READ_GATE','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'Automatically train read gate timing during initialization'},
    'TRAIN_DATA_EYE':  {'CONF_NAME':'CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'Automatically train data eye during initialization'},
    'CLOCK_STOP_EN':   {'CONF_NAME':'CONFIG_EZYNQ_DDR_CLOCK_STOP_EN','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'Enable clock stop'},
    'INTERNAL_VREF':   {'CONF_NAME':'CONFIG_EZYNQ_DDR_USE_INTERNAL_VREF','TYPE':'B','MANDATORY':True,'DERIVED':False,'DEFAULT':False,
                'Use internal Vref'},
                            
                            
}
#TODO make some of (possibly) derived, leave '_T_' for ns only!
# CONFIG_EZYNQ_DDR_FREQ_MHZ = 533.333333 *
# CONFIG_EZYNQ_DDR_CL = 7  *
# CONFIG_EZYNQ_DDR_CWL = 6  *
# CONFIG_EZYNQ_DDR_RCD = 7 (was CONFIG_EZYNQ_DDR_T_RCD = 7) *
# CONFIG_EZYNQ_DDR_RP = 7 (was CONFIG_EZYNQ_DDR_T_RP = 7) *
# CONFIG_EZYNQ_DDR_T_RC = 48.75 *
# CONFIG_EZYNQ_DDR_T_RAS_MIN = 35.0 *
# CONFIG_EZYNQ_DDR_T_FAW = 40.0 *
# CONFIG_EZYNQ_DDR_AL = 0 *
# CONFIG_EZYNQ_DDR_BANK_ADDR_COUNT = 3 *
# CONFIG_EZYNQ_DDR_ROW_ADDR_COUNT = 15 *
# CONFIG_EZYNQ_DDR_COL_ADDR_COUNT = 10 *

# CONFIG_EZYNQ_DDR_ENABLE = 1          *
# CONFIG_EZYNQ_DDR_MEMORY_TYPE = DDR3  *
# CONFIG_EZYNQ_DDR_ECC = Disabled      *
# CONFIG_EZYNQ_DDR_BUS_WIDTH = 32      *
# CONFIG_EZYNQ_DDR_BL = 8              *   
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

