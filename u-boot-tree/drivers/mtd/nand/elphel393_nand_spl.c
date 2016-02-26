/*
 * Xilinx Zynq NAND Flash Controller Driver
 * This driver is based on plat_nand.c and mxc_nand.c drivers
 *
 * Copyright (C) 2009 - 2013 Xilinx, Inc.
 *
 * SPDX-License-Identifier:	GPL-2.0+
 */

#include <common.h>
#include <malloc.h>
#include <asm/io.h>
#include <asm/errno.h>
#include <nand.h>
#include <linux/mtd/mtd.h>
#include <linux/mtd/nand.h>
#include <linux/mtd/partitions.h>
#include <linux/mtd/nand_ecc.h>
#include <asm/arch/hardware.h>
#include <asm/arch/sys_proto.h>

/* The NAND flash driver defines */
#define ZYNQ_NAND_CMD_PHASE	1	/* End command valid in command phase */
#define ZYNQ_NAND_DATA_PHASE	2	/* End command valid in data phase */
#define ZYNQ_NAND_ECC_SIZE	512	/* Size of data for ECC operation */

/* Flash memory controller operating parameters */
#define ZYNQ_NAND_CLR_CONFIG	((0x1 << 1)  |	/* Disable interrupt */ \
				(0x1 << 4)   |	/* Clear interrupt */ \
				(0x1 << 6))	/* Disable ECC interrupt */

/* Assuming 50MHz clock (20ns cycle time) and 3V operation */
#define ZYNQ_NAND_SET_CYCLES	((0x2 << 20) |	/* t_rr from nand_cycles */ \
				(0x2 << 17)  |	/* t_ar from nand_cycles */ \
				(0x1 << 14)  |	/* t_clr from nand_cycles */ \
				(0x3 << 11)  |	/* t_wp from nand_cycles */ \
				(0x2 << 8)   |	/* t_rea from nand_cycles */ \
				(0x5 << 4)   |	/* t_wc from nand_cycles */ \
				(0x5 << 0))	/* t_rc from nand_cycles */

#define ZYNQ_NAND_SET_OPMODE	0x0

#define ZYNQ_NAND_DIRECT_CMD	((0x4 << 23) |	/* Chip 0 from interface 1 */ \
				(0x2 << 21))	/* UpdateRegs operation */

#define ZYNQ_NAND_ECC_CONFIG	((0x1 << 2)  |	/* ECC available on APB */ \
				(0x1 << 4)   |	/* ECC read at end of page */ \
				(0x0 << 5))	/* No Jumping */

#define ZYNQ_NAND_ECC_CMD1	((0x80)      |	/* Write command */ \
				(0x00 << 8)  |	/* Read command */ \
				(0x30 << 16) |	/* Read End command */ \
				(0x1 << 24))	/* Read End command calid */

#define ZYNQ_NAND_ECC_CMD2	((0x85)      |	/* Write col change cmd */ \
				(0x05 << 8)  |	/* Read col change cmd */ \
				(0xE0 << 16) |	/* Read col change end cmd */ \
				(0x1 << 24))	/* Read col change
							end cmd valid */
/* AXI Address definitions */
#define START_CMD_SHIFT		3
#define END_CMD_SHIFT		11
#define END_CMD_VALID_SHIFT	20
#define ADDR_CYCLES_SHIFT	21
#define CLEAR_CS_SHIFT		21
#define ECC_LAST_SHIFT		10
#define COMMAND_PHASE		(0 << 19)
#define DATA_PHASE		(1 << 19)

#define ZYNQ_NAND_ECC_LAST	(1 << ECC_LAST_SHIFT)	/* Set ECC_Last */
#define ZYNQ_NAND_CLEAR_CS	(1 << CLEAR_CS_SHIFT)	/* Clear chip select */

/* ECC block registers bit position and bit mask */
#define ZYNQ_NAND_ECC_BUSY	(1 << 6)	/* ECC block is busy */
#define ZYNQ_NAND_ECC_MASK	0x00FFFFFF	/* ECC value mask */

#define ZYNQ_NAND_ROW_ADDR_CYCL_MASK	0x0F
#define ZYNQ_NAND_COL_ADDR_CYCL_MASK	0xF0

/* NAND MIO buswidth count*/
#define ZYNQ_NAND_MIO_NUM_NAND_8BIT	13
#define ZYNQ_NAND_MIO_NUM_NAND_16BIT	8

/* Based on Fabian Gottlieb von Bellingshausen's work in Antarctica */
int nand_spl_load_image(uint32_t offs, unsigned int size, void *dst)
{
	return 0;
}

/* nand_init() - initialize data to make nand usable by SPL */
void nand_init(void)
{
	
}

/* secret */
void nand_deselect(void) {
	
}

