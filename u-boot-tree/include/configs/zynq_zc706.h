/*
 * (C) Copyright 2012 Xilinx
 *
 * Configuration settings for the Xilinx Zynq ZC702 and ZC706 boards
 * See zynq_common.h for Zynq common configs
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston,
 * MA 02111-1307 USA
 */

#ifndef __CONFIG_ZYNQ_ZC706_H
#define __CONFIG_ZYNQ_ZC706_H

#define CONFIG_SYS_SDRAM_SIZE (1024 * 1024 * 1024)

#define CONFIG_ZYNQ_SERIAL_UART1
#define CONFIG_ZYNQ_GEM0
#define CONFIG_ZYNQ_GEM_PHY_ADDR0	0

#define CONFIG_SYS_NO_FLASH

#define CONFIG_ZYNQ_SDHCI0
/*#define CONFIG_DEFAULT_DEVICE_TREE	zynq-zc706*/

#include <configs/zynq-common.h>
#undef CONFIG_SYS_PROMPT
#undef CONFIG_BOOTDELAY
#undef CONFIG_EXTRA_ENV_SETTINGS
/*skip u-boot falcon mode*/
#undef CONFIG_SPL_OS_BOOT

#include <configs/ezynq/ezynq_MT41J256M8HX15E.h>  /* should be before zed_ezynq.h as it overwrites DDR3L with DDR3 */
#include <configs/ezynq/ezynq_XC7Z045_2FFG900C.h>
#include <configs/ezynq/ezynq_zc706.h>

#define CONFIG_BOOTDELAY	1 /* -1 to Disable autoboot */
#define CONFIG_SYS_PROMPT		"zc706-u-boot> "

/*#define CONFIG_EZYNQ_SKIP_DDR*/
#define CONFIG_EZYNQ_SKIP_CLK

/* Default environment */
#define CONFIG_EXTRA_ENV_SETTINGS	\
	"ethaddr=00:0a:35:00:01:22\0"	\
	"kernel_image=uImage\0"	\
	"ramdisk_image=uramdisk.image.gz\0"	\
	"devicetree_image=devicetree.dtb\0"	\
	"bitstream_image=system.bit.bin\0"	\
	"boot_image=BOOT.bin\0"	\
	"loadbit_addr=0x100000\0"	\
	"loadbootenv_addr=0x2000000\0" \
	"kernel_size=0x500000\0"	\
	"devicetree_size=0x20000\0"	\
	"ramdisk_size=0x5E0000\0"	\
	"boot_size=0xF00000\0"	\
	"fdt_high=0x20000000\0"	\
	"initrd_high=0x20000000\0"	\
	"bootenv=uEnv.txt\0" \
	"loadbootenv=fatload mmc 0 ${loadbootenv_addr} ${bootenv}\0" \
	"importbootenv=echo Importing environment from SD ...; " \
		"env import -t ${loadbootenv_addr} $filesize\0" \
	"mmc_loadbit_fat=echo Loading bitstream from SD/MMC/eMMC to RAM.. && " \
		"mmcinfo && " \
		"fatload mmc 0 ${loadbit_addr} ${bitstream_image} && " \
		"fpga load 0 ${loadbit_addr} ${filesize}\0" \
	"norboot=echo Copying Linux from NOR flash to RAM... && " \
		"cp.b 0xE2100000 0x3000000 ${kernel_size} && " \
		"cp.b 0xE2600000 0x2A00000 ${devicetree_size} && " \
		"echo Copying ramdisk... && " \
		"cp.b 0xE2620000 0x2000000 ${ramdisk_size} && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0" \
	"qspiboot=echo Copying Linux from QSPI flash to RAM... && " \
		"sf probe 0 0 0 && " \
		"sf read 0x3000000 0x100000 ${kernel_size} && " \
		"sf read 0x2A00000 0x600000 ${devicetree_size} && " \
		"echo Copying ramdisk... && " \
		"sf read 0x2000000 0x620000 ${ramdisk_size} && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0" \
	"uenvboot=" \
		"if run loadbootenv; then " \
			"echo Loaded environment from ${bootenv}; " \
			"run importbootenv; " \
		"fi; " \
		"if test -n $uenvcmd; then " \
			"echo Running uenvcmd ...; " \
			"run uenvcmd; " \
		"fi\0" \
	"sdboot=if mmcinfo; then " \
			"run uenvboot; " \
			"echo Copying Linux from SD to RAM... && " \
			"fatload mmc 0 0x3F00000 ${kernel_image} && " \
			"fatload mmc 0 0x3E00000 ${devicetree_image} && " \
			"fatload mmc 0 0x2000000 ${ramdisk_image} && " \
			"bootm 0x3F00000 0x2000000 0x3E00000; " \
		"fi\0" \
	"usbboot=if usb start; then " \
			"run uenvboot; " \
			"echo Copying Linux from USB to RAM... && " \
			"fatload usb 0 0x3000000 ${kernel_image} && " \
			"fatload usb 0 0x2A00000 ${devicetree_image} && " \
			"fatload usb 0 0x2000000 ${ramdisk_image} && " \
			"bootm 0x3000000 0x2000000 0x2A00000; " \
		"fi\0" \
	"nandboot=echo Copying Linux from NAND flash to RAM... && " \
		"nand read 0x3000000 0x100000 ${kernel_size} && " \
		"nand read 0x2A00000 0x600000 ${devicetree_size} && " \
		"echo Copying ramdisk... && " \
		"nand read 0x2000000 0x620000 ${ramdisk_size} && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0" \
	"jtagboot=echo TFTPing Linux to RAM... && " \
		"tftpboot 0x3000000 ${kernel_image} && " \
		"tftpboot 0x2A00000 ${devicetree_image} && " \
		"tftpboot 0x2000000 ${ramdisk_image} && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0" \
	"rsa_norboot=echo Copying Image from NOR flash to RAM... && " \
		"cp.b 0xE2100000 0x100000 ${boot_size} && " \
		"zynqrsa 0x100000 && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0" \
	"rsa_nandboot=echo Copying Image from NAND flash to RAM... && " \
		"nand read 0x100000 0x0 ${boot_size} && " \
		"zynqrsa 0x100000 && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0" \
	"rsa_qspiboot=echo Copying Image from QSPI flash to RAM... && " \
		"sf probe 0 0 0 && " \
		"sf read 0x100000 0x0 ${boot_size} && " \
		"zynqrsa 0x100000 && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0" \
	"rsa_sdboot=echo Copying Image from SD to RAM... && " \
		"fatload mmc 0 0x100000 ${boot_image} && " \
		"zynqrsa 0x100000 && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0" \
	"rsa_jtagboot=echo TFTPing Image to RAM... && " \
		"tftpboot 0x100000 ${boot_image} && " \
		"zynqrsa 0x100000 && " \
		"bootm 0x3000000 0x2000000 0x2A00000\0"

/*  */
#endif /* __CONFIG_ZYNQ_ZC706_H */
