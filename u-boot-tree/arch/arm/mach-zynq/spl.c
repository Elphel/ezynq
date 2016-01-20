/*
 * (C) Copyright 2014 Xilinx, Inc. Michal Simek
 *
 * SPDX-License-Identifier:	GPL-2.0+
 */
#include <common.h>
#include <debug_uart.h>
#include <spl.h>

#include <asm/io.h>
#include <asm/spl.h>
#include <asm/arch/hardware.h>
#include <asm/arch/sys_proto.h>

#ifndef CONFIG_EZYNQ
__weak void ps7_init(void)
{
	puts("Please copy ps7_init.c/h from hw project\n");	
}
#endif

DECLARE_GLOBAL_DATA_PTR;

void board_init_f(ulong dummy)
{
	/* Clear the BSS. */
	//memset(__bss_start, 0, __bss_end - __bss_start);

	/* Set global data pointer. */
	//gd = &gdata;

#ifndef CONFIG_EZYNQ
	ps7_init();
#endif
	arch_cpu_init();
        
#ifdef CONFIG_EZYNQ  
	puts("NOT REQUIRED: Copying ps7_init.c/h from hw project\n");
#endif
// 	board_init_r(NULL, 0);
}

#ifdef CONFIG_SPL_BOARD_INIT
void spl_board_init(void)
{
        preloader_console_init();
	board_init();
}
#endif

u32 spl_boot_device(void)
{
	u32 mode;

	switch ((zynq_slcr_get_boot_mode()) & ZYNQ_BM_MASK) {
#ifdef CONFIG_SPL_SPI_SUPPORT
	case ZYNQ_BM_QSPI:
		puts("qspi boot\n");
		mode = BOOT_DEVICE_SPI;
		break;
#endif
	case ZYNQ_BM_NAND:
		mode = BOOT_DEVICE_NAND;
		break;
	case ZYNQ_BM_NOR:
		mode = BOOT_DEVICE_NOR;
		break;
#ifdef CONFIG_SPL_MMC_SUPPORT
	case ZYNQ_BM_SD:
		puts("mmc boot\n");
		mode = BOOT_DEVICE_MMC1;
		break;
#endif
	case ZYNQ_BM_JTAG:
		mode = BOOT_DEVICE_RAM;
		break;
	default:
		puts("Unsupported boot mode selected\n");
		hang();
	}

	return mode;
}

#ifdef CONFIG_SPL_MMC_SUPPORT
u32 spl_boot_mode(void)
{
	return MMCSD_MODE_FS;
}
#endif

#ifdef CONFIG_SPL_OS_BOOT
int spl_start_uboot(void)
{
	/* boot linux */
	return 0;
}
#endif
