#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# Definitions of configuration parameters for clocks 
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
CLK_CFG_DEFS=[
    {'NAME':'PS_MHZ',        'CONF_NAME':'CONFIG_EZYNQ_CLK_PS_MHZ','TYPE':'F','MANDATORY':True,  'DERIVED':False,'DEFAULT':33.333333,
                'DESCRIPTION':'PS_CLK System clock input frequency (MHz)'},   
    {'NAME':'DDR_MHZ',       'CONF_NAME':'CONFIG_EZYNQ_CLK_DDR_MHZ','TYPE':'F','MANDATORY':True, 'DERIVED':False,'DEFAULT':533.333333,
                'DESCRIPTION':'DDR clock frequency - DDR_3X (MHz)'},   
    {'NAME':'ARM_MHZ',       'CONF_NAME':'CONFIG_EZYNQ_CLK_ARM_MHZ','TYPE':'F','MANDATORY':True,'DERIVED':False,'DEFAULT':667.0,
                'DESCRIPTION':'ARM CPU clock frequency cpu_6x4x (MHz)'},
    {'NAME':'CPU_MODE',      'CONF_NAME':'CONFIG_EZYNQ_CLK_CPU_MODE','TYPE':('6_2_1','4_2_1'),'MANDATORY':True,'DERIVED':False,'DEFAULT':'6_2_1',
                'DESCRIPTION':'CPU clocks set 6:2:1 (6:3:2:1) or 4:2:1 (4:2:2:1)'},
              
    {'NAME':'FPGA0_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_FPGA0_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':50.0,
                'DESCRIPTION':'FPGA 0 clock frequency (MHz).'},
    {'NAME':'FPGA1_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_FPGA1_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':50.0,
                'DESCRIPTION':'FPGA 1 clock frequency (MHz).'},
    {'NAME':'FPGA2_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_FPGA2_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':50.0,
                'DESCRIPTION':'FPGA 2 clock frequency (MHz).'},
    {'NAME':'FPGA3_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_FPGA3_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':50.0,
                'DESCRIPTION':'FPGA 3 clock frequency (MHz).'},
              
    {'NAME':'FPGA0_SRC',      'CONF_NAME':'CONFIG_EZYNQ_CLK_FPGA0_SRC','TYPE':('ARM','DDR','IO','NONE'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'FPGA 0 clock source'},
    {'NAME':'FPGA1_SRC',      'CONF_NAME':'CONFIG_EZYNQ_CLK_FPGA1_SRC','TYPE':('ARM','DDR','IO','NONE'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'FPGA 1 clock source'},
    {'NAME':'FPGA2_SRC',      'CONF_NAME':'CONFIG_EZYNQ_CLK_FPGA2_SRC','TYPE':('ARM','DDR','IO','NONE'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'FPGA 2 clock source'},
    {'NAME':'FPGA3_SRC',      'CONF_NAME':'CONFIG_EZYNQ_CLK_FPGA3_SRC','TYPE':('ARM','DDR','IO','NONE'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'FPGA 3 clock source'},

    {'NAME':'DDR2X_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_DDR2X_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':355.556,
                'DESCRIPTION':'DDR_2X clock frequency (MHz). Does not need to be exactly 2/3 of DDR_3X clock'},
    {'NAME':'DDR_DCI_MHZ',   'CONF_NAME':'CONFIG_EZYNQ_CLK_DDR_DCI_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':10.0,
                'DESCRIPTION':'DDR DCI clock frequency (MHz). Normally 10 Mhz'},
    {'NAME':'SMC_MHZ',       'CONF_NAME':'CONFIG_EZYNQ_CLK_SMC_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':100.0,
                'DESCRIPTION':'Static memory controller clock frequency (MHz). Normally 100 Mhz'},
    {'NAME':'QSPI_MHZ',      'CONF_NAME':'CONFIG_EZYNQ_CLK_QSPI_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':200.0,
                'DESCRIPTION':'Quad SPI memory controller clock frequency (MHz). Normally 200 Mhz'},
    {'NAME':'GIGE0_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_GIGE0_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':125.0,
                'DESCRIPTION':'GigE 0 Ethernet controller reference clock frequency (MHz). Normally 125 Mhz'},
    {'NAME':'GIGE1_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_GIGE1_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':125.0,
                'DESCRIPTION':'GigE 1 Ethernet controller reference clock frequency (MHz). Normally 125 Mhz'},
    {'NAME':'SDIO_MHZ',      'CONF_NAME':'CONFIG_EZYNQ_CLK_SDIO_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':100.0,
                'DESCRIPTION':'SDIO controller reference clock frequency (MHz). Normally 100 Mhz'},
    {'NAME':'UART_MHZ',      'CONF_NAME':'CONFIG_EZYNQ_CLK_UART_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':25.0,
                'DESCRIPTION':'UART controller reference clock frequency (MHz). Normally 25 Mhz'},
    {'NAME':'SPI_MHZ',       'CONF_NAME':'CONFIG_EZYNQ_CLK_SPI_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':200.0,
                'DESCRIPTION':'SPI controller reference clock frequency (MHz). Normally 200 Mhz'},
    {'NAME':'CAN_MHZ',       'CONF_NAME':'CONFIG_EZYNQ_CLK_CAN_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':100.0,
                'DESCRIPTION':'CAN controller reference clock frequency (MHz). Normally 100 Mhz'},
    {'NAME':'PCAP_MHZ',      'CONF_NAME':'CONFIG_EZYNQ_CLK_PCAP_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':200.0,
                'DESCRIPTION':'PCAP clock frequency (MHz). Normally 200 Mhz'},
    {'NAME':'TRACE_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_TRACE_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':100.0,
                'DESCRIPTION':'Trace Port clock frequency (MHz). Normally 100 Mhz'},
              
    {'NAME':'ARM_SRC',       'CONF_NAME':'CONFIG_EZYNQ_CLK_ARM_SRC','TYPE':('ARM','DDR','IO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'ARM',
                'DESCRIPTION':'ARM CPU clock source (normally ARM PLL)'},
    {'NAME':'DDR_SRC',       'CONF_NAME':'CONFIG_EZYNQ_CLK_DDR_SRC','TYPE':('DDR',),'MANDATORY':False,'DERIVED':False,'DEFAULT':'DDR',
                'DESCRIPTION':'DDR (DDR2x, DDR3x) clock source (Only valid DDR PLL)'},
    {'NAME':'DDR_DCI_SRC',   'CONF_NAME':'CONFIG_EZYNQ_CLK_DDR_DCI_SRC','TYPE':('DDR',),'MANDATORY':False,'DERIVED':False,'DEFAULT':'DDR',
                'DESCRIPTION':'DDR DCI clock source (only valid DDR PLL)'},
    {'NAME':'SMC_SRC',       'CONF_NAME':'CONFIG_EZYNQ_CLK_SMC_SRC','TYPE':('ARM','DDR','IO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'Static memory controller clock source (normally IO PLL)'},
    {'NAME':'QSPI_SRC',       'CONF_NAME':'CONFIG_EZYNQ_CLK_QSPI_SRC','TYPE':('ARM','DDR','IO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'ARM',
                'DESCRIPTION':'Quad SPI memory controller clock source (normally ARM PLL)'},
    {'NAME':'GIGE0_SRC',      'CONF_NAME':'CONFIG_EZYNQ_CLK_GIGE0_SRC','TYPE':('ARM','DDR','IO','EMIO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'GigE 0 Ethernet controller clock source (normally IO PLL, can be EMIO)'},
    {'NAME':'GIGE1_SRC',      'CONF_NAME':'CONFIG_EZYNQ_CLK_GIGE1_SRC','TYPE':('ARM','DDR','IO','EMIO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'GigE 1 Ethernet controller clock source (normally IO PLL, can be EMIO)'},
    {'NAME':'SDIO_SRC',       'CONF_NAME':'CONFIG_EZYNQ_CLK_SDIO_SRC','TYPE':('ARM','DDR','IO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'SDIO controller clock source (normally IO PLL)'},
    {'NAME':'UART_SRC',       'CONF_NAME':'CONFIG_EZYNQ_CLK_UART_SRC','TYPE':('ARM','DDR','IO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'UART controller clock source (normally IO PLL)'},
    {'NAME':'SPI_SRC',        'CONF_NAME':'CONFIG_EZYNQ_CLK_SPI_SRC', 'TYPE':('ARM','DDR','IO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'SPI controller clock source (normally IO PLL)'},
    {'NAME':'CAN_SRC',        'CONF_NAME':'CONFIG_EZYNQ_CLK_CAN_SRC', 'TYPE':('ARM','DDR','IO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'CAN controller clock source (normally IO PLL)'},
    {'NAME':'PCAP_SRC',       'CONF_NAME':'CONFIG_EZYNQ_CLK_PCAP_SRC','TYPE':('ARM','DDR','IO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'PCAP controller clock source (normally IO PLL)'},
    {'NAME':'TRACE_SRC',       'CONF_NAME':'CONFIG_EZYNQ_CLK_TRACE_SRC','TYPE':('ARM','DDR','IO','EMIO'),'MANDATORY':False,'DERIVED':False,'DEFAULT':'IO',
                'DESCRIPTION':'Trace Port clock source (normally IO PLL)'},

# performance data, final values (overwrites calculated)              
              
    {'NAME':'SPEED_GRADE',     'CONF_NAME':'CONFIG_EZYNQ_CLK_SPEED_GRADE','TYPE':(1,2,3),'MANDATORY':False,'DERIVED':False,'DEFAULT':2,
                'DESCRIPTION':'Device speed grade'},
    {'NAME':'PLL_MAX_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_PLL_MAX_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1800.0,
                'DESCRIPTION':'Maximal PLL clock frequency, MHz. Overwrites default for selected speed grade: (Speed grade -1:1600, -2:1800, -3:2000)'},
    {'NAME':'PLL_MIN_MHZ',     'CONF_NAME':'CONFIG_EZYNQ_CLK_PLL_MIN_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':780.0,
                'DESCRIPTION':'Minimal PLL clock frequency, all speed grades (MHz)'},
    {'NAME':'ARM621_MAX_MHZ',  'CONF_NAME':'CONFIG_EZYNQ_CLK_ARM621_MAX_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':733.0,
                'DESCRIPTION':'Maximal ARM clk_6x4x in 621 mode, MHz. Overwrites default for selected speed grade: (Speed grade -1:667, -2:733, -3:1000)'},
    {'NAME':'ARM421_MAX_MHZ',  'CONF_NAME':'CONFIG_EZYNQ_CLK_ARM421_MAX_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':600.0,
                'DESCRIPTION':'Maximal ARM clk_6x4x in 421 mode, MHz. Overwrites default for selected speed grade: (Speed grade -1:533, -2:600, -3:710)'},
    {'NAME':'DDR_3X_MAX_MHZ',  'CONF_NAME':'CONFIG_EZYNQ_CLK_DDR_3X_MAX_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':533.0,
                'DESCRIPTION':'Maximal DDR clk_3x clock frequency (MHz). Overwrites DDR-type/speed grade specific'},
    {'NAME':'DDR_2X_MAX_MHZ',  'CONF_NAME':'CONFIG_EZYNQ_CLK_DDR_2X_MAX_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':408.0,
                'DESCRIPTION':'Maximal DDR_2X clock frequency (MHz). Overwrites speed grade specific'},

# performance data, datasheet values
    {'NAME':'DS_PLL_MAX_1_MHZ',   'CONF_NAME':'CONFIG_EZYNQ_CLK_DS_PLL_MAX_1_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1600.0,
                'DESCRIPTION':'Maximal PLL clock frequency for speed grade 1 (MHz)'},
    {'NAME':'DS_PLL_MAX_2_MHZ',   'CONF_NAME':'CONFIG_EZYNQ_CLK_DS_PLL_MAX_2_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1800.0,
                'DESCRIPTION':'Maximal PLL clock frequency for speed grade 2 (MHz)'},
    {'NAME':'DS_PLL_MAX_3_MHZ',   'CONF_NAME':'CONFIG_EZYNQ_CLK_DS_PLL_MAX_3_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':2000.0,
                'DESCRIPTION':'Maximal PLL clock frequency for speed grade 3 (MHz)'},
              
    {'NAME':'DS_ARM621_MAX_1_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_ARM621_MAX_1_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':667.0,
                'DESCRIPTION':'Maximal ARM clk_6x4x in 621 mode for speed grade 1, MHz'},
    {'NAME':'DS_ARM621_MAX_2_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_ARM621_MAX_2_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':733.0,
                'DESCRIPTION':'Maximal ARM clk_6x4x in 621 mode for speed grade 2, MHz'},
    {'NAME':'DS_ARM621_MAX_3_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_ARM621_MAX_3_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1000.0,
                'DESCRIPTION':'Maximal ARM clk_6x4x in 621 mode for speed grade 3, MHz'},

    {'NAME':'DS_ARM421_MAX_1_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_ARM421_MAX_1_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':533.0,
                'DESCRIPTION':'Maximal ARM clk_6x4x in 421 mode for speed grade 1, MHz'},
    {'NAME':'DS_ARM421_MAX_2_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_ARM421_MAX_2_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':600.0,
                'DESCRIPTION':'Maximal ARM clk_6x4x in 421 mode for speed grade 2, MHz'},
    {'NAME':'DS_ARM421_MAX_3_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_ARM421_MAX_3_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':710.0,
                'DESCRIPTION':'Maximal ARM clk_6x4x in 421 mode for speed grade 3, MHz'},
              
    {'NAME':'DS_DDR3_MAX_1_MBPS', 'CONF_NAME':'CONFIG_EZYNQ_CLK_DS_DDR3_MAX_1_MBPS','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1066.0,
                'DESCRIPTION':'Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 1'},
    {'NAME':'DS_DDR3_MAX_2_MBPS', 'CONF_NAME':'CONFIG_EZYNQ_CLK_DS_DDR3_MAX_2_MBPS','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1066.0,
                'DESCRIPTION':'Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 2'},
    {'NAME':'DS_DDR3_MAX_3_MBPS', 'CONF_NAME':'CONFIG_EZYNQ_CLK_DS_DDR3_MAX_3_MBPS','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':1333.0,
                'DESCRIPTION':'Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 3'},
    {'NAME':'DS_DDRX_MAX_X_MBPS', 'CONF_NAME':'CONFIG_EZYNQ_CLK_DS_DDRX_MAX_X_MBPS','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':800.0,
                'DESCRIPTION':'Maximal DDR3L, DDR2, LPDDR2 performance in Mb/s - twice clock frequency (MHz). All speed grades'},
    {'NAME':'DS_DDR_2X_MAX_1_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_1_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':355.0,
                'DESCRIPTION':'Maximal DDR_2X clock frequency (MHz) for speed grade 1'},
    {'NAME':'DS_DDR_2X_MAX_2_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_2_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':408.0,
                'DESCRIPTION':'Maximal DDR_2X clock frequency (MHz) for speed grade 2'},
    {'NAME':'DS_DDR_2X_MAX_3_MHZ','CONF_NAME':'CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_3_MHZ','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':444.0,
                'DESCRIPTION':'Maximal DDR_2X clock frequency (MHz) for speed grade 3'},
    {'NAME':'COMPLIANCE_PERCENT','CONF_NAME':'CONFIG_EZYNQ_CLK_COMPLIANCE_PERCENT','TYPE':'F','MANDATORY':False,'DERIVED':False,'DEFAULT':5.0,
                'DESCRIPTION':'Allow exceeding maximal limits by this margin (percent'},
]

############# Main clock settings #############
#CONFIG_EZYNQ_CLK_PS_MHZ =   33.333333 # PS_CLK System clock input frequency (MHz)   
#CONFIG_EZYNQ_CLK_DDR_MHZ = 533.333333 # DDR clock frequency - DDR_3X (MHz)
#CONFIG_EZYNQ_CLK_ARM_MHZ = 667        # ARM CPU clock frequency cpu_6x4x (MHz)
#CONFIG_EZYNQ_CLK_CPU_MODE = 6_2_1     # CPU clocks set 6:2:1 (6:3:2:1) or 4:2:1 (4:2:2:1)
#CONFIG_EZYNQ_CLK_FPGA0_MHZ =    50.0 # FPGA 0 clock frequency (MHz)
#CONFIG_EZYNQ_CLK_FPGA1_MHZ =    50.0 # FPGA 1 clock frequency (MHz)
#CONFIG_EZYNQ_CLK_FPGA2_MHZ =    50.0 # FPGA 2 clock frequency (MHz)
#CONFIG_EZYNQ_CLK_FPGA3_MHZ =    50.0 # FPGA 3 clock frequency (MHz)
#CONFIG_EZYNQ_CLK_FPGA0_SRC =      IO # FPGA 0 clock source
#CONFIG_EZYNQ_CLK_FPGA1_SRC =      IO # FPGA 1 clock source
#CONFIG_EZYNQ_CLK_FPGA2_SRC =      IO # FPGA 2 clock source
#CONFIG_EZYNQ_CLK_FPGA3_SRC =      IO # FPGA 3 clock source

############# Normally do not need to be modified #############
#CONFIG_EZYNQ_CLK_DDR_DCI_MHZ = 10.0   # DDR DCI clock frequency (MHz). Normally 10 Mhz'},
#CONFIG_EZYNQ_CLK_DDR2X_MHZ = 355.556 # DDR2X clock frequency (MHz). Does not need to be exactly 2/3 of DDR3X clock'},
#CONFIG_EZYNQ_CLK_DDR_DCI_MHZ=   10.0 # DDR DCI clock frequency (MHz). Normally 10Mhz
#CONFIG_EZYNQ_CLK_SMC_MHZ =     100.0 # Static memory controller clock frequency (MHz). Normally 100 Mhz
#CONFIG_EZYNQ_CLK_QSPI_MHZ =    200.0 # Quad SPI memory controller clock frequency (MHz). Normally 200 Mhz
#CONFIG_EZYNQ_CLK_GIGE0_MHZ =   125.0 # GigE 0 Ethernet controller reference clock frequency (MHz). Normally 125 Mhz
#CONFIG_EZYNQ_CLK_GIGE1_MHZ =   125.0 # GigE 1 Ethernet controller reference clock frequency (MHz). Normally 125 Mhz
#CONFIG_EZYNQ_CLK_SDIO_MHZ =    100.0 # SDIO controller reference clock frequency (MHz). Normally 100 Mhz
#CONFIG_EZYNQ_CLK_UART_MHZ =     25.0 # UART controller reference clock frequency (MHz). Normally 25 Mhz
#CONFIG_EZYNQ_CLK_SPI_MHZ =     200.0 # SPI controller reference clock frequency (MHz). Normally 200 Mhz
#CONFIG_EZYNQ_CLK_CAN_MHZ =     100.0 # CAN controller reference clock frequency (MHz). Normally 100 Mhz
#CONFIG_EZYNQ_CLK_PCAP_MHZ =    200.0 # PCAP clock frequency (MHz). Normally 200 Mhz
#CONFIG_EZYNQ_CLK_TRACE_MHZ =   100.0 # Trace Port clock frequency (MHz). Normally 100 Mhz
#CONFIG_EZYNQ_CLK_ARM_SRC =       ARM # ARM CPU clock source (normally ARM PLL)
#CONFIG_EZYNQ_CLK_DDR_SRC =       DDR # DDR (DDR2x, DDR3x) clock source (normally DDR PLL)
#CONFIG_EZYNQ_CLK_DDR_DCI_SRC =   DDR # DDR DCI clock source (normally DDR PLL)
#CONFIG_EZYNQ_CLK_SMC_SRC =        IO # Static memory controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_QSPI_SRC =      ARM # Quad SPI memory controller clock source (normally ARM PLL)
#CONFIG_EZYNQ_CLK_GIGE0_SRC =      IO # GigE 0 Ethernet controller clock source (normally IO PLL, can be EMIO)
#CONFIG_EZYNQ_CLK_GIGE1_SRC =      IO # GigE 1 Ethernet controller clock source (normally IO PLL, can be EMIO)
#CONFIG_EZYNQ_CLK_SDIO_SRC =       IO # SDIO controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_UART_SRC =       IO # UART controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_SPI_SRC =        IO # SPI controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_CAN_SRC =        IO # CAN controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_PCAP_SRC =       IO # PCAP controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_TRACE_SRC =      IO # Trace Port clock source (normally IO PLL)

##### performance data, final values (overwrite calculated) #####              
#CONFIG_EZYNQ_CLK_SPEED_GRADE =        2   # Device speed grade
#CONFIG_EZYNQ_CLK_PLL_MAX_MHZ =     1800.0 # Maximal PLL clock frequency, MHz. Overwrites default for selected speed grade: (Speed grade -1:1600, -2:1800, -3:2000)'},
#CONFIG_EZYNQ_CLK_PLL_MIN_MHZ =      780.0 # Minimal PLL clock frequency, all speed grades (MHz)'},
#CONFIG_EZYNQ_CLK_ARM621_MAX_MHZ =   733.0 # Maximal ARM clk_6x4x in 621 mode, MHz. Overwrites default for selected speed grade: (Speed grade -1:667, -2:733, -3:1000)'},
#CONFIG_EZYNQ_CLK_ARM421_MAX_MHZ = 600.0 # Maximal ARM clk_6x4x in 421 mode, MHz. Overwrites default for selected speed grade: (Speed grade -1:533, -2:600, -3:710)'},
#CONFIG_EZYNQ_CLK_DDR_3X_MAX_MHZ =   533.0 # Maximal DDR clk_3x clock frequency (MHz). Overwrites DDR-type/speed grade specific'},
#CONFIG_EZYNQ_CLK_DDR_2X_MAX_MHZ =   408.0 # Maximal DDR_2X clock frequency (MHz). Overwrites speed grade specific'},

##### datasheet data for specific speed grades #####
#CONFIG_EZYNQ_CLK_DS_PLL_MAX_1_MHZ =   1600.0 # Maximal PLL clock frequency for speed grade 1 (MHz)'},
#CONFIG_EZYNQ_CLK_DS_PLL_MAX_2_MHZ =   1800.0 # Maximal PLL clock frequency for speed grade 2 (MHz)'},
#CONFIG_EZYNQ_CLK_DS_PLL_MAX_3_MHZ =   2000.0 # Maximal PLL clock frequency for speed grade 3 (MHz)'},
#CONFIG_EZYNQ_CLK_DS_ARM621_MAX_1_MHZ = 667.0 # Maximal ARM clk_6x4x in 621 mode for speed grade 1, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM621_MAX_2_MHZ = 733.0 #Maximal ARM clk_6x4x in 621 mode for speed grade 2, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM621_MAX_3_MHZ =1000.0 #Maximal ARM clk_6x4x in 621 mode for speed grade 3, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM421_MAX_1_MHZ = 533.0 # Maximal ARM clk_6x4x in 421 mode for speed grade 1, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM421_MAX_2_MHZ = 600.0 # Maximal ARM clk_6x4x in 421 mode for speed grade 2, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM421_MAX_3_MHZ = 710.0 # Maximal ARM clk_6x4x in 421 mode for speed grade 3, MHz'},
#CONFIG_EZYNQ_CLK_DS_DDR3_MAX_1_MBPS = 1066.0 # Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 1'},
#CONFIG_EZYNQ_CLK_DS_DDR3_MAX_2_MBPS = 1066.0 # Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 2'},
#CONFIG_EZYNQ_CLK_DS_DDR3_MAX_3_MBPS = 1333.0 # Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 3'},
#CONFIG_EZYNQ_CLK_DS_DDRX_MAX_X_MBPS =  800.0 # Maximal DDR3L, DDR2, LPDDR2 performance in Mb/s - twice clock frequency (MHz). All speed grades'},
#CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_1_MHZ = 355.0 # Maximal DDR_2X clock frequency (MHz) for speed grade 1'},
#CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_2_MHZ = 408.0 # Maximal DDR_2X clock frequency (MHz) for speed grade 2'},
#CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_3_MHZ = 444.0 # Maximal DDR_2X clock frequency (MHz) for speed grade 3'},

#CONFIG_EZYNQ_CLK_COMPLIANCE_PERCENT = 5.0 # Allow exceeding maximal limits by this margin (percent'},
