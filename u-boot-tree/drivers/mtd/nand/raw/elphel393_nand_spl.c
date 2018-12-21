/*
 * Elphel393 NAND driver for SPL, not based on denali_spl.c
 *
 * Copyright (C) 2016 Elphel, Inc.
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

extern nand_info_t nand_info[CONFIG_SYS_MAX_NAND_DEVICE];

static int is_badblock(struct mtd_info *mtd, loff_t offs, int allowbbt)
{
	register struct nand_chip *chip = mtd->priv;
	unsigned int block = offs >> chip->phys_erase_shift;
	unsigned int page = offs >> chip->page_shift;
	unsigned long data_width = 4;
	
	debug("    is_badblock(): offs=0x%08x block=%d page=%d\n",(int)offs,block,page);
	chip->cmdfunc(mtd, NAND_CMD_READOOB, 0, page);
	chip->read_buf(mtd, chip->oob_poi, (mtd->oobsize - data_width));
	
	printf("    is_badblock(): offs=0x%08x block=0x%08x page=0x%08x chip->oob_poi[0]=0x%08x\n",(u32)offs,(u32)block,(u32)page,(u32)chip->oob_poi[0]);
	
	return chip->oob_poi[0] != 0xff;
}

//dst or buf - destination in RAM
//offs - u-boot-dtb.img offset in NAND
//size - size of u-boot-dtb.img
int nand_spl_load_image(uint32_t offs, unsigned int size, void *buf)
{
	struct nand_chip *chip;
	struct mtd_info *mtd;
	unsigned int page;
	unsigned int nand_page_per_block;
	unsigned int sz = 0;

	debug("\nnand_spl_load_image(): offs=0x%08x size=%d (0x%08x) buf_addr=0x%08x\n",offs,size,size,buf);
	udelay(10000);

	//if (mxs_nand_init()) return -ENODEV;
	mtd = &nand_info[0];
	//mtd.priv = &nand_chip;
	chip = mtd->priv;
	page = offs >> chip->page_shift;
	nand_page_per_block = mtd->erasesize / mtd->writesize;

	debug("%s offset:0x%08x len:%d page:%d\n", __func__, offs, size, page);

	debug("  nand_page_per_block= %d\n",nand_page_per_block);
	debug("  mtd->writesize= %d\n",mtd->writesize);
	debug("  u-boot-dtb.img size is: %d (0x%08x)\n",size,size);
	
	size = roundup(size, mtd->writesize);

	debug("  u-boot-dtb.img size after roundup is:%d\n",size);

	while (sz < size) {
		//if (mxs_read_page_ecc(&mtd, buf, page) < 0)
		//	return -1;
		//printf("  Reading from NAND, offset:0x%08x page_index:%d to MEM address:0x%08x\n",offs, page, buf);

		chip->cmdfunc(mtd, NAND_CMD_READ0, 0, page);
		udelay(500);
		//read min
		chip->read_buf(mtd,buf,min(size-sz, mtd->writesize));

		//chip->ecc.read_page(mtd, chip, buf, 0, page);
		sz += mtd->writesize;
		offs += mtd->writesize;
		page++;
		buf += mtd->writesize;

		
		/*
		 * Check if we have crossed a block boundary, and if so
		 * check for bad block.
		 */
		//on-die ecc is enabled
		//if (!(page % nand_page_per_block)) {
		//	/*
		//	 * Yes, new block. See if this block is good. If not,
		//	 * loop until we find a good block.
		//	 */
		//	while (is_badblock(&mtd, offs, 1)) {
		//		page = page + nand_page_per_block;
		//		/* Check we've reached the end of flash. */
		//		if (page >= mtd->size >> chip->page_shift)
		//			return -ENOMEM;
		//	}
		//}
	}
	return 0;
}

/* already defined in nand.c
// nand_init() - initialize data to make nand usable by SPL
void nand_init(void)
{
	puts("nand_init()\n");
	udelay(5000);
	board_nand_init();
}
*/

void nand_deselect(void) {
	debug("nand_deselect()\n");
	udelay(10000);
}
