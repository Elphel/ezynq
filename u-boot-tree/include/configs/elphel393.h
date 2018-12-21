/*
 * (C) Copyright 2012 Xilinx
 * (C) Copyright 2013 Elphel
 *
 * Configuration for Elphel393 Board
 * See zynq_common.h for Zynq common configs
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

#ifndef __CONFIG_ELPHEL393_H
#define __CONFIG_ELPHEL393_H

#define CONFIG_SYS_SDRAM_SIZE (1024 * 1024 * 1024)

#define CONFIG_ZYNQ_SERIAL_UART0
#define CONFIG_ZYNQ_GEM0
#define CONFIG_ZYNQ_GEM_PHY_ADDR0	0

#define CONFIG_ZYNQ_SDHCI
#define CONFIG_ZYNQ_SDHCI0

#define CONFIG_SYS_NO_FLASH

#define CONFIG_NAND_ZYNQ

#ifdef CONFIG_NAND_ZYNQ
    /*#define CONFIG_CMD_NAND*/
    #define CONFIG_CMD_NAND_LOCK_UNLOCK
    #define CONFIG_SYS_MAX_NAND_DEVICE 1
    #define CONFIG_SYS_NAND_SELF_INIT
    #define CONFIG_SYS_NAND_ONFI_DETECTION
    #define CONFIG_MTD_DEVICE
#endif

#define CONFIG_SPL_NAND_ELPHEL393

#define CONFIG_SYS_NAND_U_BOOT_OFFS	0x100000 /*look-up in dts!*/

/*
#define CONFIG_SPL_NAND_LOAD
#define CONFIG_SYS_NAND_U_BOOT_SIZE	0x100000
#define CONFIG_SYS_NAND_U_BOOT_DST	0x0
#define CONFIG_SYS_NAND_U_BOOT_START	0x0
*/

#define CONFIG_SPL_NAND_SUPPORT
#define CONFIG_SPL_NAND_DRIVERS

#define CONFIG_SPL_NAND_INIT
#define CONFIG_SPL_NAND_BASE
#define CONFIG_SPL_NAND_ECC
#define CONFIG_SPL_NAND_BBT
#define CONFIG_SPL_NAND_IDS

/* Load U-Boot to this address */
#define CONFIG_SYS_NAND_U_BOOT_DST	CONFIG_SYS_TEXT_BASE
#define CONFIG_SYS_NAND_U_BOOT_START	CONFIG_SYS_NAND_U_BOOT_DST

#define CONFIG_MTD
/*#define CONFIG_DEFAULT_DEVICE_TREE	elphel393*/

/*redefined in zynq-common.h*/
/*#undef CONFIG_CMD_NAND*/

#define CONFIG_ZYNQ_I2C0

#include <configs/zynq-common.h>

/* Need to define it - otherwise error "FDT creation failed!"*/
#define CONFIG_SYS_SDRAM_BASE       0

#undef CONFIG_SYS_PROMPT
#undef CONFIG_BOOTDELAY
#undef CONFIG_EXTRA_ENV_SETTINGS
/*skip u-boot falcon mode*/
#undef CONFIG_SPL_OS_BOOT

#undef CONFIG_DISPLAY_BOARDINFO

#include <configs/ezynq/ezynq_MT41K256M16HA107.h>  /* should be before zed_ezynq.h as it overwrites DDR3L with DDR3 */
#include <configs/ezynq/ezynq_XC7Z030_1FBG484C.h>
#include <configs/ezynq/ezynq_elphel393.h>

#define CONFIG_CMD_MEMTEST

#define CONFIG_BOOTDELAY	1 /* -1 to Disable autoboot */
#define CONFIG_SYS_PROMPT		"elphel393-u-boot> "

/*#define CONFIG_EZYNQ_SKIP_DDR*/
#define CONFIG_EZYNQ_SKIP_CLK

#define CONFIG_MTD_DEVICE

/* UBI support in full U-Boot */
#define CONFIG_MTD_PARTITIONS
#define CONFIG_CMD_MTDPARTS
#define CONFIG_CMD_UBI
#define CONFIG_CMD_UBIFS
#define CONFIG_RBTREE
#define CONFIG_LZO
#define MTDIDS_DEFAULT  "nand0=nand"
#define MTDPARTS_DEFAULT "mtdparts=nand:1m(u-boot-spl),"   \
                         "4m(u-boot)," \
                         "1m(device-tree)," \
                         "16m(kernel)," \
                         "256m(rootfs)," \
                         "256m(rootfs)"

/* Default environment */
#define CONFIG_EXTRA_ENV_SETTINGS	\
	"ethaddr=00:0e:64:10:00:00\0"	\
	"kernel_image=uImage\0"	\
	"ramdisk_image=uramdisk.image.gz\0"	\
	"devicetree_image=devicetree.dtb\0"	\
	"bitstream_image=system.bit.bin\0"	\
	"boot_image=BOOT.bin\0"	\
	"loadbit_addr=0x100000\0"	\
	"loadbootenv_addr=0x2000000\0" \
	"kernel_size=0x800000\0"	\
	"devicetree_size=0x100000\0"	\
	"ramdisk_size=0x1E00000\0"	\
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
			"fatload mmc 0 0x4F00000 ${kernel_image} && " \
			"fatload mmc 0 0x4E00000 ${devicetree_image} && " \
			"bootm 0x4F00000 - 0x4E00000; " \
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
		"nand read 0x4F00000 0x600000 ${kernel_size} && " \
		"nand read 0x4E00000 0x500000 ${devicetree_size} && " \
		"bootm 0x4F00000 - 0x4E00000\0" \
	"devboot= echo Copying Linux from SD to RAM... && " \
		"fatload mmc 0 0x4F00000 ${kernel_image} && " \
		" echo Copying Device Tree from NAND flash to RAM && " \
		"nand read 0x4E00000 0x500000 ${devicetree_size} && " \
		"bootm 0x4F00000 - 0x4E00000\0" \
        "nandboot2=echo NAND boot 2... ; " \
                "mtd default; " \
                "mtd4=0; " \
                "ubi part nand0,4; " \
                "if ubi check elphel393-rootfs; then " \
                    "mtd4=1; " \
                "fi; " \
                "mtd5=0; " \
                "ubi part nand0,5; " \
                "if ubi check elphel393-rootfs; then " \
                    "mtd5=1; " \
                "fi; " \
                "i2c read 68 4 1 ${loadbootenv_addr}; " \
                "setexpr.b bootsrc *${loadbootenv_addr} \\\\& 0x80; " \
                "setexpr bootsrc ${bootsrc} / 0x80; " \
                "setexpr bootsrc ${bootsrc} \\\\& ${mtd4}; " \
                "setexpr bootsrc ${bootsrc} \\\\& ${mtd5}; " \
                "setexpr bootsrc ${bootsrc} \\\\^ ${mtd5}; " \
                "if test ${bootsrc} -eq 1; then " \
                    "echo Booting from mtd4!; " \
                "else " \
                    "echo Booting from mtd5!; " \
                "fi\0" \
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
#endif /* __CONFIG_ELPHEL393_H */
