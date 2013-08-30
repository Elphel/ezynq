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


 



