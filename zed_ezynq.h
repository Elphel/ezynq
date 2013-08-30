/*
 * (C) Copyright 2013 Elphel, Inc.
 *
 * Configuration for Microzed RBL header
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
#define CONFIG_EZYNQ_OCM
#define CONFIG_EZYNQ_MIO_0_VOLT           3.3
#define CONFIG_EZYNQ_MIO_1_VOLT           1.8
#define CONFIG_EZYNQ_QUADSPI_0__ATTRIB    SLOW 
#define CONFIG_EZYNQ_MIO_ETH_0__ATTRIB    SLOW
#define CONFIG_EZYNQ_MIO_ETH_MDIO__ATTRIB SLOW
#define CONFIG_EZYNQ_MIO_USB_0__ATTRIB    SLOW
#define CONFIG_EZYNQ_MIO_SDIO_0           40 // 16,28,40
#define CONFIG_EZYNQ_MIO_SDIO_0__ATTRIB   SLOW
#define CONFIG_EZYNQ_MIO_SDCD_0           46 //#any but 7,8
#define CONFIG_EZYNQ_MIO_SDWP_0           50 //#any but 7,8
#define CONFIG_EZYNQ_MIO_UART_1           48 //#  8+4*N

/*
 //#debug
//#define CONFIG_EZYNQ_UART_LOOPBACK_1=y

Red LED - pullup, input - on,
output (or undefined) -   off

#define CONFIG_EZYNQ_MIO_PULLUP_EN_47
#define CONFIG_EZYNQ_MIO_PULLUP_DIS_0
#define CONFIG_EZYNQ_MIO_INOUT_47   OUT
#define CONFIG_EZYNQ_MIO_INOUT_47=   IN
#define CONFIG_EZYNQ_MIO_INOUT_47=   BIDIR
*/

#define CONFIG_EZYNQ_BOOT_USERDEF           0x1010000 /* # 0x1234567 # will be saved in the file header */
#define CONFIG_EZYNQ_BOOT_OCM_OFFSET        0xa40     /*  # 0x8C0   # start of OCM data relative to the flash image start >=0x8C0, 63-bytes aligned */
#define CONFIG_EZYNQ_BOOT_OCM_IMAGE_LENGTH  0x1400c   /*  # 0#0x30000 # number of bytes to load to the OCM memory, <=  0x30000 */
#define CONFIG_EZYNQ_START_EXEC             0x00      /*  # start of execution address */
#define CONFIG_EZYNQ_RESERVED44             0         /*  # documented as 0, but actually 1 */
#endif /* __CONFIG_EZYNQ_H */