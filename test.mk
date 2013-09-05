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
CONFIG_EZYNQ_BOOT_USERDEF=           0x1234567 # will be saved in the file header
CONFIG_EZYNQ_BOOT_OCM_OFFSET=        0x8C0   # start of OCM data relative to the flash image start >=0x8C0, 63-bytes aligned
CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH=  0#0x30000 # number of bytes to load to the OCM memory, <= 0x30000 
CONFIG_EZYNQ_START_EXEC=             0x00 # start of execution address 


 CONFIG_EZYNQ_DDR_PERIPHERAL_CLKSRC = DDR PLL
CONFIG_EZYNQ_DDR_RAM_BASEADDR = 0x00100000
CONFIG_EZYNQ_DDR_RAM_HIGHADDR = 0x3FFFFFFF
CONFIG_EZYNQ_DDR_TARGET_FREQ_MHZ = 533.3333 # New added
CONFIG_EZYNQ_DDR_FREQ_MHZ = 533.333374          # Taking available CLK and divisors into account?
CONFIG_EZYNQ_DCI_PERIPHERAL_FREQMHZ = 10.158731 # Taking available CLK and divisors into account?



CONFIG_EZYNQ_DDR_ENABLE = 1
CONFIG_EZYNQ_DDR_MEMORY_TYPE = DDR3
CONFIG_EZYNQ_DDR_ECC = Disabled
CONFIG_EZYNQ_DDR_BUS_WIDTH = 32
CONFIG_EZYNQ_DDR_BL = 8
CONFIG_EZYNQ_DDR_HIGH_TEMP = False # Normal
CONFIG_EZYNQ_DDR_T_REFI_US = 7.8
CONFIG_EZYNQ_DDR_T_RFC     = 300 # 350.0
CONFIG_EZYNQ_DDR_T_WR = 15.0 # Write recovery time

CONFIG_EZYNQ_DDR_RTP = 4
CONFIG_EZYNQ_DDR_T_RTP = 7.5
CONFIG_EZYNQ_DDR_WTR = 4
CONFIG_EZYNQ_DDR_T_WTR = 7.5
CONFIG_EZYNQ_DDR_XP = 4 # power down (DLL on) to any operation, cycles
CONFIG_EZYNQ_DDR_T_DQSCK_MAX = 5.5 # (LPDDR2 only)



CONFIG_EZYNQ_DDR_PARTNO = MT41K256M16RE-125
CONFIG_EZYNQ_DDR_DRAM_WIDTH = 16
#CONFIG_EZYNQ_DDR_DEVICE_CAPACITY_MBITS = 4096 - can be calculated
CONFIG_EZYNQ_DDR_SPEED_BIN = DDR3_1066F
CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL = 0
CONFIG_EZYNQ_DDR_TRAIN_READ_GATE = 0
CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE = 0
CONFIG_EZYNQ_DDR_CLOCK_STOP_EN = 0
CONFIG_EZYNQ_DDR_USE_INTERNAL_VREF = 0

# undisclosed algorithm, get values from ps7*
CONFIG_EZYNQ_DDR_OUT_SLEW_NEG = 26
CONFIG_EZYNQ_DDR_OUT_SLEW_POS = 26
CONFIG_EZYNQ_DDR_OUT_DRIVE_NEG = 12
CONFIG_EZYNQ_DDR_OUT_DRIVE_POS = 28
CONFIG_EZYNQ_DDR_BIDIR_SLEW_NEG = 31
CONFIG_EZYNQ_DDR_BIDIR_SLEW_POS = 6
CONFIG_EZYNQ_DDR_BIDIR_DRIVE_NEG = 12
CONFIG_EZYNQ_DDR_BIDIR_DRIVE_POS = 28

CONFIG_EZYNQ_DDR_FREQ_MHZ = 533.333333
CONFIG_EZYNQ_DDR_BANK_ADDR_COUNT = 3
CONFIG_EZYNQ_DDR_ROW_ADDR_COUNT = 15
CONFIG_EZYNQ_DDR_COL_ADDR_COUNT = 10
CONFIG_EZYNQ_DDR_CL = 7
CONFIG_EZYNQ_DDR_CWL = 6
#CONFIG_EZYNQ_DDR_T_RCD = 7
#CONFIG_EZYNQ_DDR_T_RP = 7
CONFIG_EZYNQ_DDR_RCD = 7
CONFIG_EZYNQ_DDR_RP = 7
CONFIG_EZYNQ_DDR_T_RC = 48.75
CONFIG_EZYNQ_DDR_T_RAS_MIN = 35.0
CONFIG_EZYNQ_DDR_T_FAW = 40.0
CONFIG_EZYNQ_DDR_AL = 0

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

# PCW_PACKAGE_DDR_DQS_TO_CLK_DELAY_0 = -0.005
# PCW_PACKAGE_DDR_DQS_TO_CLK_DELAY_1 = -0.004
# PCW_PACKAGE_DDR_DQS_TO_CLK_DELAY_2 = -0.008
# PCW_PACKAGE_DDR_DQS_TO_CLK_DELAY_3 = -0.058

# PCW_PACKAGE_DDR_BOARD_DELAY0 = 0.075
# PCW_PACKAGE_DDR_BOARD_DELAY1 = 0.076
# PCW_PACKAGE_DDR_BOARD_DELAY2 = 0.082
# PCW_PACKAGE_DDR_BOARD_DELAY3 = 0.100
 
#just software testing - remove later
CONFIG_EZYNQ_DDR_SETREG_ctrl_reg1__reg_ddrc_selfref_en_PRE = 1
 
CONFIG_EZYNQ_DDR_SETREG_ctrl_reg1__reg_ddrc_lpr_num_entries_PRE = 5

CONFIG_EZYNQ_DDR_SETREG_phy_wr_dqs_cfg0_PRE = 0xAAAAA
CONFIG_EZYNQ_DDR_SETREG_phy_wr_dqs_cfg0__reg_phy_wr_dqs_slave_delay_PRE = 0x77


#                  'reg_ddrc_selfref_en':              {'r':(12,12),'d':0,'c':'Dynamic - 1 - go to Self Refresh when transaction store is empty'},   
#                  'reserved1':                        {'r':(11,11),'d':0,'m':'R','c':'reserved'},      
#                  'reg_ddrc_dis_collision_page_opt':  {'r':(10,10),'d':0,'c':'Disable autoprecharge for collisions (write+write or read+write to the same address) when  reg_ddrc_dis_wc==1'},     
#                  'reg_ddrc_dis_wc':                  {'r':( 9, 9),'d':0,'c':'1 - disable write combine, 0 - enable'},      
#                  'reg_ddrc_refresh_update_level':    {'r':( 8, 8),'d':0,'c':'Dynamic: toggle to indicate refressh register(s) update'},    
#                  'reg_ddrc_auto_pre_en':             {'r':( 7, 7),'d':0,'c':'1 - most R/W will be with autoprecharge'},      
#                  'reg_ddrc_lpr_num_entries':         {'r':( 1, 6),'d':0x1F,'c':'(bit 6 ignored) (Size of low priority transaction store+1). HPR - 32 - this value'},      
#                  'reg_ddrc_pageclose':               {'r':( 0, 0),'d':0,'c':'1 - close bank if no transactions in the store for it, 0 - keep open until not needed by other'}}}, 

#    'phy_wr_dqs_cfg0':         {'OFFS': 0x154,'DFLT':0x00000000,'RW':'RW','FIELDS':{
#                  'reg_phy_wr_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 0'},       
#                  'reg_phy_wr_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 0'},       
#                  'reg_phy_wr_dqs_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 0. Program manual training ratio'}}},

