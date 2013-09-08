#COnfiguration for the microzed board
CONFIG_EZYNQ_MIO_0_VOLT=3.3
CONFIG_EZYNQ_MIO_1_VOLT=1.8
#CONFIG_EZYNQ_MIO_0_PULLUP=y #default pullup for MIO0 - may be overwritten for individual pins
#CONFIG_EZYNQ_MIO_1_PULLUP=y #default pullup for MIO0 - may be overwritten for individual pins
#I/O standards will default to 1.3/2.5/3.3 according to MIO voltage
#CONFIG_EZYNQ_QUADSPI_0 = y 
CONFIG_EZYNQ_QUADSPI_0__ATTRIB = SLOW 
#CONFIG_EZYNQ_QUADSPI_1 = y
#CONFIG_EZYNQ_QUADSPI_FBCLK = y
#CONFIG_EZYNQ_MIO_ETH_0=y
 CONFIG_EZYNQ_MIO_ETH_0__ATTRIB= SLOW
#CONFIG_EZYNQ_MIO_ETH_1=y
 CONFIG_EZYNQ_MIO_ETH_MDIO__ATTRIB= SLOW
 CONFIG_EZYNQ_MIO_USB_0__ATTRIB= SLOW
#CONFIG_EZYNQ_MIO_USB_1=y
#CONFIG_EZYNQ_MIO_SPI_0=16 #16,28,40
#CONFIG_EZYNQ_MIO_SPI_1=10 #10,22,34,46
 CONFIG_EZYNQ_MIO_SDIO_0=40 #16,28,40
 CONFIG_EZYNQ_MIO_SDIO_0__ATTRIB=SLOW
#CONFIG_EZYNQ_MIO_SDIO_1=10 #10,22,34,46
 CONFIG_EZYNQ_MIO_SDCD_0=46 #any but 7,8
 CONFIG_EZYNQ_MIO_SDWP_0=50 #any but 7,8
#CONFIG_EZYNQ_MIO_SDCD_1=48 #any but 7,8
#CONFIG_EZYNQ_MIO_SDWP_1=48 #any but 7,8
#CONFIG_EZYNQ_MIO_SDPWR_0=48 #any even
#CONFIG_EZYNQ_MIO_SDPWR_1=49 #any odd
#CONFIG_EZYNQ_NOR=y
#CONFIG_EZYNQ_NOR_A25=y # either A25 or CS1
#CONFIG_EZYNQ_NOR_CS1=y # either A25 or CS1
#CONFIG_EZYNQ_NAND=y
#CONFIG_EZYNQ_NAND__BUSY=free # debugging software
#CONFIG_EZYNQ_NAND16=y
#CONFIG_EZYNQ_MIO_CAN_0=46 # 10+4*N
#CONFIG_EZYNQ_MIO_CAN_1=44 #  8+4*N
#CONFIG_EZYNQ_MIO_CAN_ECLK_0=48 # any Just GPIO?
#CONFIG_EZYNQ_MIO_CAN_ECLK_1=49 # any Just GPIO?
#CONFIG_EZYNQ_MIO_UART_0=46 # 10+4*N
CONFIG_EZYNQ_MIO_UART_1=48 #  8+4*N
#CONFIG_EZYNQ_MIO_I2C_0=50 # 10+4*N
#CONFIG_EZYNQ_MIO_I2C_1=44 # 12+4*N
#CONFIG_EZYNQ_MIO_TTC_0=18 # 18+12*N
#CONFIG_EZYNQ_MIO_TTC_1=16 # 16+12*N
#CONFIG_EZYNQ_MIO_SWDT= 14 # 14+12*N, 52
#CONFIG_EZYNQ_MIO_PJTAG=10 # 10+12*N
#CONFIG_EZYNQ_MIO_TPUI= 2 # TODO
#the following will be applied after devices above

#each of the interfaces above can have "__<pinname>" to mix same pins from different groups
#"__<pinname>=-1" - remove specified pin from the interface (do not use it)
#just for testing
#CONFIG_EZYNQ_MIO_TPUI=12 #24
#CONFIG_EZYNQ_MIO_TPUI__CLK0=12 #24
#CONFIG_EZYNQ_MIO_TPUI__CTL=25 #13
#CONFIG_EZYNQ_MIO_TPUI__DATA0=14 #26
#CONFIG_EZYNQ_MIO_TPUI__DATA1=15 #27
#CONFIG_EZYNQ_MIO_TPUI__DATA2=10 #22
#CONFIG_EZYNQ_MIO_TPUI__DATA3=11 #23




#CONFIG_EZYNQ_MIO_IOSTD_LVCMOS18_01= y # will overwrite defaults, last numeric specifies MIO pin number
#CONFIG_EZYNQ_MIO_IOSTD_LVCMOS25_15= y # will overwrite defaults
#CONFIG_EZYNQ_MIO_IOSTD_LVCMOS33_2= y # will overwrite defaults
#CONFIG_EZYNQ_MIO_IOSTD_HSTL_3=     y # will overwrite defaults
#CONFIG_EZYNQ_MIO_IOSTD_HSTLDIS_4= y # will overwrite defaults
#CONFIG_EZYNQ_MIO_PULLUP_EN_5=      y # will overwrite defaults
#CONFIG_EZYNQ_MIO_PULLUP_DIS_0=     y # will overwrite defaults
#CONFIG_EZYNQ_MIO_FAST_7=           y # will overwrite defaults
#CONFIG_EZYNQ_MIO_SLOW_8=           y # will overwrite defaults
#CONFIG_EZYNQ_MIO_INOUT_2=          OUT # 'IN', 'BIDIR'
#CONFIG_EZYNQ_MIO_INOUT_15=          OUT # 'IN', 'BIDIR'
#CONFIG_EZYNQ_MIO_INOUT_0=          IN # 'IN', 'BIDIR'
#CONFIG_EZYNQ_MIO_GPIO_OUT_02=       0 # Set selected GPIO output to 0/1
#CONFIG_EZYNQ_MIO_GPIO_OUT_15=       1 # Set selected GPIO output to 0/1
## Boot image parameters


#RBL header parameters
CONFIG_EZYNQ_BOOT_USERDEF=           0x1234567 # will be saved in the file header
CONFIG_EZYNQ_BOOT_OCM_OFFSET=        0x8C0   # start of OCM data relative to the flash image start >=0x8C0, 63-bytes aligned
CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH=  0#0x30000 # number of bytes to load to the OCM memory, <= 0x30000 
CONFIG_EZYNQ_START_EXEC=             0x00 # start of execution address 




 
#just software testing - remove later
#CONFIG_EZYNQ_DDR_SETREG_ctrl_reg1__reg_ddrc_selfref_en_PRE = 1
#CONFIG_EZYNQ_DDR_SETREG_ctrl_reg1__reg_ddrc_lpr_num_entries_PRE = 5
#CONFIG_EZYNQ_DDR_SETREG_phy_wr_dqs_cfg0_PRE = 0xAAAAA
#CONFIG_EZYNQ_DDR_SETREG_phy_wr_dqs_cfg0__reg_phy_wr_dqs_slave_delay_PRE = 0x77
#CONFIG_EZYNQ_DDR_ARB_PAGE_BANK  = N # Y # default N, testing








# not yet processed
CONFIG_EZYNQ_DCI_PERIPHERAL_FREQMHZ = 10.158731 # Taking available CLK and divisors into account?
CONFIG_EZYNQ_DDR_PERIPHERAL_CLKSRC = DDR PLL
CONFIG_EZYNQ_DDR_RAM_BASEADDR = 0x00100000
CONFIG_EZYNQ_DDR_RAM_HIGHADDR = 0x3FFFFFFF

##### DDR independent ######

CONFIG_EZYNQ_DDR_ENABLE =           Y        # Enable DDR memory'},              
CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ =  533.3333 # Target DDR clock frequency in MHz (actual frequency will depend on the clock/clock muxes)              
#CONFIG_EZYNQ_DDR_FREQ_MHZ =         545.0     # Actual DDR clock frequency in MHz, may be derived form CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ and clock multiplexer settings. Causes tWR to go higher
#CONFIG_EZYNQ_DDR_FREQ_MHZ =         533.333374 # Actual DDR clock frequency in MHz, may be derived form CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ and clock multiplexer settings. Causes tWR to go higher
CONFIG_EZYNQ_DDR_FREQ_MHZ =         533.3333 # Actual DDR clock frequency in MHz, may be derived form CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ and clock multiplexer settings
CONFIG_EZYNQ_DDR_BANK_ADDR_MAP =    10       # DRAM address mapping: number of combined column and row addresses lower than BA0              
CONFIG_EZYNQ_DDR_ARB_PAGE_BANK =    N        # Enable Arbiter prioritization based on page/bank match              
CONFIG_EZYNQ_DDR_ECC =              Disabled # Enable ECC for the DDR memory
CONFIG_EZYNQ_DDR_BUS_WIDTH =        32       # SoC DDR bus width
CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL =0        # Automatically train write leveling during initialization
CONFIG_EZYNQ_DDR_TRAIN_READ_GATE =  0        # Automatically train read gate timing during initialization
CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE =   0        # Automatically train data eye during initialization
CONFIG_EZYNQ_DDR_CLOCK_STOP_EN =    0        # Enable clock stop
CONFIG_EZYNQ_DDR_USE_INTERNAL_VREF =0        # Use internal Vref

###### DDR Dependent ######
CONFIG_EZYNQ_DDR_CL =                      7 # CAS read latency (in tCK)
CONFIG_EZYNQ_DDR_CWL =                     6 # CAS write latency (in tCK)              
CONFIG_EZYNQ_DDR_AL =                      0 # Posted CAS additive latency (in tCK)
CONFIG_EZYNQ_DDR_BL =                      8 # Burst length, 16 is only supported for LPDDR2
CONFIG_EZYNQ_DDR_HIGH_TEMP =           False # Normal # High temperature (influences refresh)
CONFIG_EZYNQ_DDR_SPEED_BIN =      DDR3_1066F # Memory speed bin (currently not used - derive timing later)
CONFIG_EZYNQ_DDR_DDR2_RTT =               75 # DDR2 on-chip termination, Ohm ('DISABLED','75','150','50'              
CONFIG_EZYNQ_DDR_DDR3_RTT =               60 # DDR3 on-chip termination, Ohm ('DISABLED','60','120','40')# Does not include 20 & 30 - not clear if DDRC can use them with auto write leveling               
CONFIG_EZYNQ_DDR_OUT_SLEW_NEG =           26 # Slew rate negative for DDR address/clock outputs
CONFIG_EZYNQ_DDR_OUT_SLEW_POS =           26 # Slew rate positive for DDR address/clock outputs
CONFIG_EZYNQ_DDR_OUT_DRIVE_NEG =          12 # Drive strength negative for DDR address/clock outputs
CONFIG_EZYNQ_DDR_OUT_DRIVE_POS =          28 # Drive strength positive for DDR address/clock outputs
CONFIG_EZYNQ_DDR_BIDIR_SLEW_NEG =         31 # Slew rate negative for driving DDR DQ/DQS signals
CONFIG_EZYNQ_DDR_BIDIR_SLEW_POS =          6 # Drive strength positive for driving DDR DQ/DQS signals
CONFIG_EZYNQ_DDR_BIDIR_DRIVE_NEG =        12 # Drive strength negative for driving DDR DQ/DQS signals
CONFIG_EZYNQ_DDR_BIDIR_DRIVE_POS =        28 # Slew rate positive for driving DDR DQ/DQS signals
###### DDR Datasheet (can be in include file) #######
CONFIG_EZYNQ_DDR_DS_PARTNO = MT41K256M16RE125 # Memory part number  (currently not used - derive some parameters later)
CONFIG_EZYNQ_DDR_DS_MEMORY_TYPE =  DDR3L  # DDR memory type: DDR3 (1.5V), DDR3L (1.35V), DDR2 (1.8V), LPDDR2 (1.2V)
CONFIG_EZYNQ_DDR_DS_BANK_ADDR_COUNT =  3  # Number of DDR banks              
CONFIG_EZYNQ_DDR_DS_ROW_ADDR_COUNT  = 15  # Number of DDR Row Address bits              
CONFIG_EZYNQ_DDR_DS_COL_ADDR_COUNT  = 10  # Number of DDR Column address bits              
CONFIG_EZYNQ_DDR_DS_DRAM_WIDTH =      16  # Memory chip bus width (not yet used)
CONFIG_EZYNQ_DDR_DS_RCD =             7   # DESCRIPTION':'RAS to CAS delay (in tCK) 
CONFIG_EZYNQ_DDR_DS_T_RCD =          13.1 # Activate to internal Read or Write (ns). May be used to calculate CONFIG_EZYNQ_DDR_DS_RCD automatically   
CONFIG_EZYNQ_DDR_DS_RP =              7   # Row Precharge time (in tCK)              
CONFIG_EZYNQ_DDR_DS_T_RP =           13.1 # Precharge command period (ns).  May be used to calculate CONFIG_EZYNQ_DDR_DS_RP automatically,   
CONFIG_EZYNQ_DDR_DS_T_RC =           48.75# Activate to Activate or Refresh command period (ns)              
CONFIG_EZYNQ_DDR_DS_T_RAS_MIN =      35.0 # Minimal Row Active time (ns)              
CONFIG_EZYNQ_DDR_DS_T_FAW =          40.0 # Minimal running window for 4 page activates (ns)   
CONFIG_EZYNQ_DDR_DS_T_RFC =         300.0 # Minimal Refresh-to-Activate or Refresh command period (ns)   
CONFIG_EZYNQ_DDR_DS_T_WR =           15.0 # Write recovery time (ns)   
CONFIG_EZYNQ_DDR_DS_T_REFI_US =       7.8 # Maximal average periodic refresh, microseconds. Will be automatically reduced if high temperature option is selected              
CONFIG_EZYNQ_DDR_DS_RTP =             4 # Minimal Read-to-Precharge time (in tCK). Will use max of this and CONFIG_EZYNQ_DDR_DS_T_RTP/tCK              
CONFIG_EZYNQ_DDR_DS_T_RTP =           7.5 # Minimal Read-to-Precharge time  (ns). Will use max of this divided by tCK and CONFIG_EZYNQ_DDR_DS_RTP   
CONFIG_EZYNQ_DDR_DS_WTR =             4   # Minimal Write-to-Read time (in tCK). Will use max of this and CONFIG_EZYNQ_DDR_DS_T_WTR/tCK              
CONFIG_EZYNQ_DDR_DS_T_WTR =           7.5 # Minimal Write-to-Read time  (ns). Will use max of this divided by tCK and CONFIG_EZYNQ_DDR_DS_WTR   
CONFIG_EZYNQ_DDR_DS_XP =              4   # Minimal time from power down (DLL on) to any operation (in tCK)              
CONFIG_EZYNQ_DDR_DS_T_DQSCK_MAX =     5.5 # LPDDR2 only. DQS output access time from CK (ns). Used for LPDDR2   
CONFIG_EZYNQ_DDR_DS_CCD =             5   # DESCRIPTION':'CAS-to-CAS command delay (in tCK) (4 in Micron DS)              
CONFIG_EZYNQ_DDR_DS_RRD =             6   # ACTIVATE-to-ACTIVATE minimal command period (in tCK)              
CONFIG_EZYNQ_DDR_DS_T_RRD            10.0 # ACTIVATE-to-ACTIVATE minimal command period (ns). May be used to calculate CONFIG_EZYNQ_DDR_DS_RRD automatically   
CONFIG_EZYNQ_DDR_DS_MRD =             4   # MODE REGISTER SET command period (in tCK)
CONFIG_EZYNQ_DDR_DS_MOD =            12   # MODE REGISTER SET update delay (in tCK)              
CONFIG_EZYNQ_DDR_DS_T_MOD =          15.0 # MODE REGISTER SET update delay  (ns).   
CONFIG_EZYNQ_DDR_DS_T_WLMRD =        40.0 # Write leveling : time to the first DQS rising edge (ns).
CONFIG_EZYNQ_DDR_DS_CKE =             3   # CKE min pulse width (in tCK)              
CONFIG_EZYNQ_DDR_DS_T_CKE =           7.5 # CKE min pulse width (ns). # 5.625   
CONFIG_EZYNQ_DDR_DS_CKSRE =           5   # Keep valid clock after self refresh/power down entry (in tCK)              
CONFIG_EZYNQ_DDR_DS_T_CKSRE =        10.0 # Keep valid clock after self refresh/power down entry (ns).   
CONFIG_EZYNQ_DDR_DS_CKSRX =           5   # Valid clock before self refresh, power down or reset exit (in tCK)              
CONFIG_EZYNQ_DDR_DS_T_CKSRX =        10.0 # Valid clock before self refresh, power down or reset exit (ns).   
CONFIG_EZYNQ_DDR_DS_ZQCS =           64   # ZQCS command: short calibration time (in tCK)              
CONFIG_EZYNQ_DDR_DS_ZQCL =          512   # ZQCL command: long calibration time, including init (in tCK)
CONFIG_EZYNQ_DDR_DS_INIT2 =           5   # LPDDR2 only: tINIT2 (in tCK): clock stable before CKE high
CONFIG_EZYNQ_DDR_DS_T_INIT4_US =      1.0 # LPDDR2 only: tINIT4 (in us)- minimal idle time after RESET command.   
CONFIG_EZYNQ_DDR_DS_T_INIT5_US =     10.0 # LPDDR2 only: tINIT5 (in us)- maximal duration of device auto initialization.   
CONFIG_EZYNQ_DDR_DS_T_ZQINIT_US =     1.0 # LPDDR2 only: tZQINIT (in us)- ZQ initial calibration time.   

# Board/Soc  parameters to set phases manually (or as a starting point for automatic) Not yet processed
CONFIG_EZYNQ_DDR_DQS_TO_CLK_DELAY_0 = 0.0
CONFIG_EZYNQ_DDR_DQS_TO_CLK_DELAY_1 = 0.0
CONFIG_EZYNQ_DDR_DQS_TO_CLK_DELAY_2 = 0.0
CONFIG_EZYNQ_DDR_DQS_TO_CLK_DELAY_3 = 0.0

CONFIG_EZYNQ_DDR_BOARD_DELAY0 = 0.0
CONFIG_EZYNQ_DDR_BOARD_DELAY1 = 0.0
CONFIG_EZYNQ_DDR_BOARD_DELAY2 = 0.0
CONFIG_EZYNQ_DDR_BOARD_DELAY3 = 0.0

CONFIG_EZYNQ_DDR_DQS_0_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_DQS_1_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_DQS_2_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_DQS_3_LENGTH_MM = 0

CONFIG_EZYNQ_DDR_DQ_0_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_DQ_1_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_DQ_2_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_DQ_3_LENGTH_MM = 0

CONFIG_EZYNQ_DDR_CLOCK_0_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_CLOCK_1_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_CLOCK_2_LENGTH_MM = 0
CONFIG_EZYNQ_DDR_CLOCK_3_LENGTH_MM = 0

CONFIG_EZYNQ_DDR_DQS_0_PACKAGE_LENGTH = 504
CONFIG_EZYNQ_DDR_DQS_1_PACKAGE_LENGTH = 495
CONFIG_EZYNQ_DDR_DQS_2_PACKAGE_LENGTH = 520
CONFIG_EZYNQ_DDR_DQS_3_PACKAGE_LENGTH = 835

CONFIG_EZYNQ_DDR_DQ_0_PACKAGE_LENGTH = 465
CONFIG_EZYNQ_DDR_DQ_1_PACKAGE_LENGTH = 480
CONFIG_EZYNQ_DDR_DQ_2_PACKAGE_LENGTH = 550
CONFIG_EZYNQ_DDR_DQ_3_PACKAGE_LENGTH = 780

CONFIG_EZYNQ_DDR_CLOCK_0_PACKAGE_LENGTH = 470.0
CONFIG_EZYNQ_DDR_CLOCK_1_PACKAGE_LENGTH = 470.0
CONFIG_EZYNQ_DDR_CLOCK_2_PACKAGE_LENGTH = 470.0
CONFIG_EZYNQ_DDR_CLOCK_3_PACKAGE_LENGTH = 470.0

CONFIG_EZYNQ_DDR_DQS_0_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_DQS_1_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_DQS_2_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_DQS_3_PROPOGATION_DELAY = 160

CONFIG_EZYNQ_DDR_DQ_0_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_DQ_1_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_DQ_2_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_DQ_3_PROPOGATION_DELAY = 160

CONFIG_EZYNQ_DDR_CLOCK_0_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_CLOCK_1_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_CLOCK_2_PROPOGATION_DELAY = 160
CONFIG_EZYNQ_DDR_CLOCK_3_PROPOGATION_DELAY = 160
