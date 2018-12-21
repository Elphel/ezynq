/*
 * (C) Copyright 2013 Elphel, Inc.
 *
 * Configuration for ZedBoard RBL header
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 3 of
 * the License, or (at your option) any later version.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston,
 * MA 02111-1307 USA
 */
#ifndef __CONFIG_EZYNQ_H
#define __CONFIG_EZYNQ_H
#define CONFIG_EZYNQ


/* Boot image cionfiguration parameters */

#define CONFIG_EZYNQ_BOOT_USERDEF           0x1010000 /*  0x1234567  will be saved in the file header */
#define CONFIG_EZYNQ_BOOT_OCM_OFFSET        0x8c0     /*  0xa40 0x8C0      start of OCM data relative to the flash image start > 0x8C0, 63-bytes aligned */
#define CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH  0x30000   /* 0x1400c  0x30000   number of bytes to load to the OCM memory, <   0x30000 */
#define CONFIG_EZYNQ_START_EXEC             0x00      /*   start of execution address */
#define CONFIG_EZYNQ_RESERVED44             0         /*   documented as 0, but actually 1 */

/* Boot debug setup */
#define CONFIG_EZYNQ_BOOT_DEBUG        Y   /* configure UARTx and send register dumps there.*/
#define CONFIG_EZYNQ_LOCK_SLCR         OFF /* Lock SLCR registers when all is done. */
/*#define CONFIG_EZYNQ_LED_DEBUG          47*/ /* toggle LED during boot */
#define CONFIG_EZYNQ_UART_DEBUG_USE_LED N  /* turn on/off LED while waiting for transmit FIFO not full */

#define CONFIG_EZYNQ_DUMP_SLCR_EARLY     N /* Dump SLCR registers as soon as UART is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG) */
#define CONFIG_EZYNQ_DUMP_DDRC_EARLY     N /* Dump DDRC registers as soon as UART is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG) */
#define CONFIG_EZYNQ_DUMP_SLCR_LATE      Y /* Dump SLCR registers after DDR memory is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG) */
#define CONFIG_EZYNQ_DUMP_DDRC_LATE      Y  /* Dump DDRC registers after DDR memory is initialized (depends on CONFIG_EZYNQ_BOOT_DEBUG) */
#define CONFIG_EZYNQ_DUMP_TRAINING_EARLY N /* Training results registers before DDRC initialization */
#define CONFIG_EZYNQ_DUMP_TRAINING_LATE  Y /* Training results registers after DDRC initialization */
#define CONFIG_EZYNQ_DUMP_OCM            Y /* Dump (some of) OCM data */
#define CONFIG_EZYNQ_DUMP_DDR            Y  /* Dump (some of) DDR data */
#if 1
#define CONFIG_EZYNQ_DUMP_OCM_LOW        0x0   /* OCM dump start (deafault 0)     */
#define CONFIG_EZYNQ_DUMP_OCM_HIGH     0x2ff   /* OCM dump end   (deafault 0x2ff, full - 0x2ffff) */

#define CONFIG_EZYNQ_DUMP_DDR_LOW  0x4000000  /* DDR dump start (deafault 0x4000000, start of the OCM copy) */
#define CONFIG_EZYNQ_DUMP_DDR_HIGH 0x40002ff  /* DDR dump end   (deafault 0x40002ff) */

#define CONFIG_EZYNQ_OCM_DDR_CHECKSUMS   Y
#endif
/* Turning LED on/off at different stages of the boot process. Requires CONFIG_EZYNQ_LED_DEBUG and CONFIG_EZYNQ_BOOT_DEBUG to be set
   If defined, each can be 0,1, ON or OFF */
#define CONFIG_EZYNQ_LED_CHECKPOINT_1   OFF /* in RBL setup, as soon as MIO is programmed, should be OFF to use GPIO */
#define CONFIG_EZYNQ_LED_CHECKPOINT_2   OFF /* First after getting to user code */
#define CONFIG_EZYNQ_LED_CHECKPOINT_3   OFF  /* After setting clock registers */
#define CONFIG_EZYNQ_LED_CHECKPOINT_4   OFF /* After PLL bypass is OFF */
#define CONFIG_EZYNQ_LED_CHECKPOINT_5   OFF  /* After UART is programmed */
#define CONFIG_EZYNQ_LED_CHECKPOINT_6   OFF /* After DCI is calibrated */
#define CONFIG_EZYNQ_LED_CHECKPOINT_7   OFF  /* After DDR is initialized */
#define CONFIG_EZYNQ_LED_CHECKPOINT_8   OFF /* Before relocation to DDR (to 0x4000000+ ) */
#define CONFIG_EZYNQ_LED_CHECKPOINT_9   OFF  /* After  relocation to DDR (to 0x4000000+ ) */
#define CONFIG_EZYNQ_LED_CHECKPOINT_10  OFF /* Before remapping OCM0-OCM2 high */
#define CONFIG_EZYNQ_LED_CHECKPOINT_11  OFF  /* After remapping OCM0-OCM2 high */
#define CONFIG_EZYNQ_LED_CHECKPOINT_12  OFF /* Before leaving lowlevel_init() */
#define CONFIG_EZYNQ_LAST_PRINT_DEBUG   Y   /* 'Output to UART before exiting arch_cpu_init() */ 
/* MIO configuration */
#define CONFIG_EZYNQ_OCM                         /* not used */
#define CONFIG_EZYNQ_MIO_0_VOLT           3.3
#define CONFIG_EZYNQ_MIO_1_VOLT           1.8
#define CONFIG_EZYNQ_QUADSPI_0__SLOW
#define CONFIG_EZYNQ_MIO_ETH_0__SLOW
#define CONFIG_EZYNQ_MIO_ETH_MDIO__SLOW
#define CONFIG_EZYNQ_MIO_USB_0__SLOW
#define CONFIG_EZYNQ_MIO_USB_0__PULLUP
#define CONFIG_EZYNQ_MIO_SDIO_0           40  /* 16,28,40 */
#define CONFIG_EZYNQ_MIO_SDIO_0__SLOW
#define CONFIG_EZYNQ_MIO_SDIO_0__PULLUP
#define CONFIG_EZYNQ_MIO_SDCD_0           46  /* any but 7,8  */
#define CONFIG_EZYNQ_MIO_SDCD_0__PULLUP
#define CONFIG_EZYNQ_MIO_SDWP_0           50  /* #any but 7,8  */
#define CONFIG_EZYNQ_MIO_SDWP_0__PULLUP
#define CONFIG_EZYNQ_MIO_UART_1           48  /* #  8+4*N  */
/* LED will be OFF */
/*#define CONFIG_EZYNQ_MIO_INOUT_47   OUT*/       /* Make output, do not set data. Will be set after debug will be over */
/*#define CONFIG_EZYNQ_MIO_GPIO_OUT_7    1*/  /* Set selected GPIO output to 0/1 */

#define CONFIG_EZYNQ_UART_DEBUG_CHANNEL   0x1

/*
Red LED - pullup, input - on,
#define CONFIG_EZYNQ_MIO_INOUT_47   OUT
#define CONFIG_EZYNQ_MIO_INOUT_47   IN
#define CONFIG_EZYNQ_MIO_INOUT_47   BIDIR
*/
#define CONFIG_EZYNQ_DDR_ENABLE             Y        /*  Enable DDR memory */
/* Only specify CONFIG_EZYNQ_DDR_FREQ_MHZ if you want the DDR frequency used for timing calculations is different from actual */
/* #define CONFIG_EZYNQ_DDR_FREQ_MHZ    533.333333 */ /*  DDR clock frequency in MHz, this value overwrites the one calculated by the PLL/clock setup */
#define CONFIG_EZYNQ_DDR_BANK_ADDR_MAP      10       /*  DRAM address mapping: number of combined column and row addresses lower than BA0 */
#define CONFIG_EZYNQ_DDR_ARB_PAGE_BANK      N        /*  Enable Arbiter prioritization based on page/bank match */
#define CONFIG_EZYNQ_DDR_ECC                Disabled /*  Enable ECC for the DDR memory */
#define CONFIG_EZYNQ_DDR_BUS_WIDTH          32       /*  SoC DDR bus width */
#define CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL  N        /*  [doesn't work yet] Automatically train write leveling during initialization */
#define CONFIG_EZYNQ_DDR_TRAIN_READ_GATE    Y        /*  Automatically train read gate timing during initialization */
#define CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE     N        /*  Automatically train data eye during initialization */
#define CONFIG_EZYNQ_DDR_CLOCK_STOP_EN      0        /*  Enable clock stop */
#define CONFIG_EZYNQ_DDR_USE_INTERNAL_VREF  0        /*  Use internal Vref */

/*      DDR chip Dependent      */
#define CONFIG_EZYNQ_DDR_CL                        7 /*  CAS read latency (in tCK) */
#define CONFIG_EZYNQ_DDR_CWL                       6 /*  CAS write latency (in tCK) */
#define CONFIG_EZYNQ_DDR_AL                        0 /*  Posted CAS additive latency (in tCK) */
#define CONFIG_EZYNQ_DDR_BL                        8 /*  Burst length, 16 is only supported for LPDDR2 */
#define CONFIG_EZYNQ_DDR_HIGH_TEMP             False /*  Normal  High temperature (influences refresh) */
#define CONFIG_EZYNQ_DDR_SPEED_BIN        DDR3_1066F /*  Memory speed bin (currently not used - derive timing later) */
#define CONFIG_EZYNQ_DDR_DDR2_RTT                 75 /*  DDR2 on-chip termination, Ohm ('DISABLED','75','150','50' */
#define CONFIG_EZYNQ_DDR_DDR3_RTT                 60 /*  DDR3 on-chip termination, Ohm ('DISABLED','60','120','40') Does not include 20 & 30 - not clear if DDRC can use them with auto write leveling */
#define CONFIG_EZYNQ_DDR_OUT_SLEW_NEG             26 /*  Slew rate negative for DDR address/clock outputs */
#define CONFIG_EZYNQ_DDR_OUT_SLEW_POS             26 /*  Slew rate positive for DDR address/clock outputs */
#define CONFIG_EZYNQ_DDR_OUT_DRIVE_NEG            12 /*  Drive strength negative for DDR address/clock outputs */
#define CONFIG_EZYNQ_DDR_OUT_DRIVE_POS            28 /*  Drive strength positive for DDR address/clock outputs */
#define CONFIG_EZYNQ_DDR_BIDIR_SLEW_NEG           31 /*  Slew rate negative for driving DDR DQ/DQS signals */
#define CONFIG_EZYNQ_DDR_BIDIR_SLEW_POS            6 /*  Drive strength positive for driving DDR DQ/DQS signals */
#define CONFIG_EZYNQ_DDR_BIDIR_DRIVE_NEG          12 /*  Drive strength negative for driving DDR DQ/DQS signals */
#define CONFIG_EZYNQ_DDR_BIDIR_DRIVE_POS          28 /*  Slew rate positive for driving DDR DQ/DQS signals */

/*       Main clock settings      */
#define CONFIG_EZYNQ_CLK_PS_MHZ     33.333333 /*  PS_CLK System clock input frequency (MHz) */
#define CONFIG_EZYNQ_CLK_DDR_MHZ   533.333333 /*  DDR clock frequency - DDR_3X (MHz) */
#define CONFIG_EZYNQ_CLK_ARM_MHZ   667        /*  ARM CPU clock frequency cpu_6x4x (MHz) */
#define CONFIG_EZYNQ_CLK_CPU_MODE   6_2_1     /*  CPU clocks set 6:2:1 (6:3:2:1) or 4:2:1 (4:2:2:1) */
#define CONFIG_EZYNQ_CLK_FPGA0_MHZ      50.0 /*  FPGA 0 clock frequency (MHz) */
#define CONFIG_EZYNQ_CLK_FPGA1_MHZ      50.0 /*  FPGA 1 clock frequency (MHz) */
#define CONFIG_EZYNQ_CLK_FPGA2_MHZ      50.0 /*  FPGA 2 clock frequency (MHz) */
#define CONFIG_EZYNQ_CLK_FPGA3_MHZ       0.0 /*  FPGA 3 clock frequency (MHz) */
#define CONFIG_EZYNQ_CLK_FPGA0_SRC        IO /*  FPGA 0 clock source */
#define CONFIG_EZYNQ_CLK_FPGA1_SRC        IO /*  FPGA 1 clock source */
#define CONFIG_EZYNQ_CLK_FPGA2_SRC      None /*  FPGA 2 clock source */
#define CONFIG_EZYNQ_CLK_FPGA3_SRC        IO /*  FPGA 3 clock source */

/*       Normally do not need to be modified      */
#define CONFIG_EZYNQ_CLK_DDR_DCI_MHZ   10.0  /*  DDR DCI clock frequency (MHz). Normally 10 Mhz */
#define CONFIG_EZYNQ_CLK_DDR2X_MHZ   355.556 /*  DDR2X clock frequency (MHz). Does not need to be exactly 2/3 of DDR3X clock */
#define CONFIG_EZYNQ_CLK_DDR_DCI_MHZ    10.0 /*  DDR DCI clock frequency (MHz). Normally 10Mhz */
#define CONFIG_EZYNQ_CLK_SMC_MHZ       100.0 /*  Static memory controller clock frequency (MHz). Normally 100 Mhz */
#define CONFIG_EZYNQ_CLK_QSPI_MHZ      200.0 /*  Quad SPI memory controller clock frequency (MHz). Normally 200 Mhz */
#define CONFIG_EZYNQ_CLK_GIGE0_MHZ     125.0 /*  GigE 0 Ethernet controller reference clock frequency (MHz). Normally 125 Mhz */
#define CONFIG_EZYNQ_CLK_GIGE1_MHZ     125.0 /*  GigE 1 Ethernet controller reference clock frequency (MHz). Normally 125 Mhz */
#define CONFIG_EZYNQ_CLK_SDIO_MHZ      100.0 /*  SDIO controller reference clock frequency (MHz). Normally 100 Mhz */
#define CONFIG_EZYNQ_CLK_UART_MHZ       25.0 /*  UART controller reference clock frequency (MHz). Normally 25 Mhz */
#define CONFIG_EZYNQ_CLK_SPI_MHZ       200.0 /*  SPI controller reference clock frequency (MHz). Normally 200 Mhz */
#define CONFIG_EZYNQ_CLK_CAN_MHZ       100.0 /*  CAN controller reference clock frequency (MHz). Normally 100 Mhz */
#define CONFIG_EZYNQ_CLK_PCAP_MHZ      200.0 /*  PCAP clock frequency (MHz). Normally 200 Mhz */
#define CONFIG_EZYNQ_CLK_TRACE_MHZ     100.0 /*  Trace Port clock frequency (MHz). Normally 100 Mhz */

#define CONFIG_EZYNQ_CLK_ARM_SRC         ARM /*  ARM CPU clock source (normally ARM PLL) */
#define CONFIG_EZYNQ_CLK_DDR_SRC         DDR /*  DDR (DDR2x, DDR3x) clock source (normally DDR PLL) */
#define CONFIG_EZYNQ_CLK_DDR_DCI_SRC     DDR /*  DDR DCI clock source (normally DDR PLL) */
#define CONFIG_EZYNQ_CLK_SMC_SRC          IO /*  Static memory controller clock source (normally IO PLL) */
#define CONFIG_EZYNQ_CLK_QSPI_SRC        ARM /*  Quad SPI memory controller clock source (normally ARM PLL) */
#define CONFIG_EZYNQ_CLK_GIGE0_SRC        IO /*  GigE 0 Ethernet controller clock source (normally IO PLL, can be EMIO) */
#define CONFIG_EZYNQ_CLK_GIGE1_SRC        IO /*  GigE 1 Ethernet controller clock source (normally IO PLL, can be EMIO) */
#define CONFIG_EZYNQ_CLK_SDIO_SRC         IO /*  SDIO controller clock source (normally IO PLL) */
#define CONFIG_EZYNQ_CLK_UART_SRC         IO /*  UART controller clock source (normally IO PLL) */
#define CONFIG_EZYNQ_CLK_SPI_SRC          IO /*  SPI controller clock source (normally IO PLL) */
#define CONFIG_EZYNQ_CLK_CAN_SRC          IO /*  CAN controller clock source (normally IO PLL) */
#define CONFIG_EZYNQ_CLK_PCAP_SRC         IO /*  PCAP controller clock source (normally IO PLL) */
#define CONFIG_EZYNQ_CLK_TRACE_SRC        IO /*  Trace Port clock source (normally IO PLL) */

/* Even if memory itself is DDR3L (1.35V) it also can support DDR3 mode (1.5V). And unfortunately Zynq has degraded
   specs at 1.35V (only 400MHz maximal clock), so datasheets's 'DDR3L' should be replaced with 'DDR3' and the board
   power supply should be 1.5V - in that case 533MHz clock is possible */
#undef  CONFIG_EZYNQ_DDR_DS_MEMORY_TYPE
#define CONFIG_EZYNQ_DDR_DS_MEMORY_TYPE    DDR3  /*  DDR memory type: DDR3 (1.5V), DDR3L (1.35V), DDR2 (1.8V), LPDDR2 (1.2V) */



/*       performance data, final values (overwrite calculated)      */
#define CONFIG_EZYNQ_CLK_SPEED_GRADE          3   /*  Device speed grade */
/* #define CONFIG_EZYNQ_CLK_PLL_MAX_MHZ       1800.0 */ /*  Maximal PLL clock frequency, MHz. Overwrites default for selected speed grade: (Speed grade -1:1600, -2:1800, -3:2000) */
/* #define CONFIG_EZYNQ_CLK_PLL_MIN_MHZ        780.0 */ /*  Minimal PLL clock frequency, all speed grades (MHz) */
/* #define CONFIG_EZYNQ_CLK_ARM621_MAX_MHZ     733.0 */ /*  Maximal ARM clk_6x4x in 621 mode, MHz. Overwrites default for selected speed grade: (Speed grade -1:667, -2:733, -3:1000) */
/* #define CONFIG_EZYNQ_CLK_ARM421_MAX_MHZ     600.0 */ /*  Maximal ARM clk_6x4x in 421 mode, MHz. Overwrites default for selected speed grade: (Speed grade -1:533, -2:600, -3:710) */
/* #define CONFIG_EZYNQ_CLK_DDR_3X_MAX_MHZ     533.0 */ /*  Maximal DDR clk_3x clock frequency (MHz). Overwrites DDR-type/speed grade specific */
/* #define CONFIG_EZYNQ_CLK_DDR_2X_MAX_MHZ     408.0 */ /*  Maximal DDR_2X clock frequency (MHz). Overwrites speed grade specific */

#define CONFIG_EZYNQ_CLK_COMPLIANCE_PERCENT    5.0 /*  Allow exceeding maximal limits by this margin (percent */

/*       Board PCB layout parameters (not yet used)      */
#define CONFIG_EZYNQ_DDR_BOARD_DELAY0      0.0
#define CONFIG_EZYNQ_DDR_BOARD_DELAY1      0.0
#define CONFIG_EZYNQ_DDR_BOARD_DELAY2      0.0
#define CONFIG_EZYNQ_DDR_BOARD_DELAY3      0.0
#define CONFIG_EZYNQ_DDR_DQS_0_LENGTH_MM   0
#define CONFIG_EZYNQ_DDR_DQS_1_LENGTH_MM   0
#define CONFIG_EZYNQ_DDR_DQS_2_LENGTH_MM   0
#define CONFIG_EZYNQ_DDR_DQS_3_LENGTH_MM   0
#define CONFIG_EZYNQ_DDR_DQ_0_LENGTH_MM    0
#define CONFIG_EZYNQ_DDR_DQ_1_LENGTH_MM    0
#define CONFIG_EZYNQ_DDR_DQ_2_LENGTH_MM    0
#define CONFIG_EZYNQ_DDR_DQ_3_LENGTH_MM    0
#define CONFIG_EZYNQ_DDR_CLOCK_0_LENGTH_MM 0
#define CONFIG_EZYNQ_DDR_CLOCK_1_LENGTH_MM 0
#define CONFIG_EZYNQ_DDR_CLOCK_2_LENGTH_MM 0
#define CONFIG_EZYNQ_DDR_CLOCK_3_LENGTH_MM 0
 /* not yet processed
#define CONFIG_EZYNQ_DDR_PERIPHERAL_CLKSRC   DDR PLL
#define CONFIG_EZYNQ_DDR_RAM_BASEADDR   0x00100000
#define CONFIG_EZYNQ_DDR_RAM_HIGHADDR   0x3FFFFFFF
*/
/* Below will overwrite calculated values (not yet calculated) */
  #define CONFIG_EZYNQ_SILICON               3 /* 3 */        /* Silicon revision */
  #define CONFIG_EZYNQ_PHY_WRLV_INIT_RATIO_0 0x0 /* Initial ratio for write leveling FSM, slice 0 */
  #define CONFIG_EZYNQ_PHY_WRLV_INIT_RATIO_1 0x0 /* Initial ratio for write leveling FSM, slice 1 */
  #define CONFIG_EZYNQ_PHY_WRLV_INIT_RATIO_2 0x0 /* Initial ratio for write leveling FSM, slice 2 */
  #define CONFIG_EZYNQ_PHY_WRLV_INIT_RATIO_3 0x0 /* Initial ratio for write leveling FSM, slice 3 */

  #define CONFIG_EZYNQ_PHY_GTLV_INIT_RATIO_0 0x0 /* Initial ratio for gate leveling FSM, slice 0 */
  #define CONFIG_EZYNQ_PHY_GTLV_INIT_RATIO_1 0x0 /* Initial ratio for gate leveling FSM, slice 1 */
  #define CONFIG_EZYNQ_PHY_GTLV_INIT_RATIO_2 0x0 /* Initial ratio for gate leveling FSM, slice 2 */
  #define CONFIG_EZYNQ_PHY_GTLV_INIT_RATIO_3 0x0 /* Initial ratio for gate leveling FSM, slice 3 */

  #define CONFIG_EZYNQ_PHY_RD_DQS_SLAVE_RATIO_0 0x35/* Ratio for read DQS slave DLL (256 - clock period), slice 0 */
  #define CONFIG_EZYNQ_PHY_RD_DQS_SLAVE_RATIO_1 0x35/* Ratio for read DQS slave DLL (256 - clock period), slice 1 */
  #define CONFIG_EZYNQ_PHY_RD_DQS_SLAVE_RATIO_2 0x35/* Ratio for read DQS slave DLL (256 - clock period), slice 2 */
  #define CONFIG_EZYNQ_PHY_RD_DQS_SLAVE_RATIO_3 0x35/* Ratio for read DQS slave DLL (256 - clock period), slice 3 */

  #define CONFIG_EZYNQ_PHY_WR_DQS_SLAVE_RATIO_0 0x0 /* Ratio for write DQS slave DLL (256 - clock period), slice 0 */
  #define CONFIG_EZYNQ_PHY_WR_DQS_SLAVE_RATIO_1 0x0 /* Ratio for write DQS slave DLL (256 - clock period), slice 1 */
  #define CONFIG_EZYNQ_PHY_WR_DQS_SLAVE_RATIO_2 0x0 /* Ratio for write DQS slave DLL (256 - clock period), slice 2 */
  #define CONFIG_EZYNQ_PHY_WR_DQS_SLAVE_RATIO_3 0x0 /* Ratio for write DQS slave DLL (256 - clock period), slice 3 */

  #define CONFIG_EZYNQ_PHY_FIFO_WE_SLAVE_RATIO_0 0x35 /*Ratio for FIFO WE slave DLL (256 - clock period), slice 0 */
  #define CONFIG_EZYNQ_PHY_FIFO_WE_SLAVE_RATIO_1 0x35 /*Ratio for FIFO WE slave DLL (256 - clock period), slice 0 */
  #define CONFIG_EZYNQ_PHY_FIFO_WE_SLAVE_RATIO_2 0x35 /*Ratio for FIFO WE slave DLL (256 - clock period), slice 0 */
  #define CONFIG_EZYNQ_PHY_FIFO_WE_SLAVE_RATIO_3 0x35 /*Ratio for FIFO WE slave DLL (256 - clock period), slice 0 */

  #define CONFIG_EZYNQ_PHY_PHY_WR_DATA_SLAVE_RATIO_0 0x40 /* Ratio for write data slave DLL (256 - clock period), slice 0 */
  #define CONFIG_EZYNQ_PHY_PHY_WR_DATA_SLAVE_RATIO_1 0x40 /* Ratio for write data slave DLL (256 - clock period), slice 1 */
  #define CONFIG_EZYNQ_PHY_PHY_WR_DATA_SLAVE_RATIO_2 0x40 /* Ratio for write data slave DLL (256 - clock period), slice 2 */
  #define CONFIG_EZYNQ_PHY_PHY_WR_DATA_SLAVE_RATIO_3 0x40 /* Ratio for write data slave DLL (256 - clock period), slice 3 */

  #define CONFIG_EZYNQ_PHY_PHY_CTRL_SLAVE_RATIO 0x80     /* Ratio for address/command (256 - clock period) */
  #define CONFIG_EZYNQ_PHY_INVERT_CLK             N     /* Invert CLK out (if clk can arrive to DRAM chip earlier/at the same time as DQS) */

 
 

#endif /* __CONFIG_EZYNQ_H */
