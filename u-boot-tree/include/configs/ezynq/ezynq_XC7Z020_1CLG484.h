 /*
 * (C) Copyright 2013 Elphel, Inc.
 *
 * Configuration for ezynq for Xilinx XC7Z020_1CLG484 SoC
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
#ifndef __CONFIG_XC7Z020_1CLG484_H
#define __CONFIG_XC7Z020_1CLG484_H

/* datasheet data for specific speed grades */
#define CONFIG_EZYNQ_CLK_DS_PLL_MAX_1_MHZ     1600.0 /* Maximal PLL clock frequency for speed grade 1 (MHz) */
#define CONFIG_EZYNQ_CLK_DS_PLL_MAX_2_MHZ     1800.0 /* Maximal PLL clock frequency for speed grade 2 (MHz) */
#define CONFIG_EZYNQ_CLK_DS_PLL_MAX_3_MHZ     2000.0 /* Maximal PLL clock frequency for speed grade 3 (MHz) */
#define CONFIG_EZYNQ_CLK_DS_ARM621_MAX_1_MHZ   667.0 /* Maximal ARM clk_6x4x in 621 mode for speed grade 1, MHz */
#define CONFIG_EZYNQ_CLK_DS_ARM621_MAX_2_MHZ   733.0 /* Maximal ARM clk_6x4x in 621 mode for speed grade 2, MHz */
#define CONFIG_EZYNQ_CLK_DS_ARM621_MAX_3_MHZ  1000.0 /* Maximal ARM clk_6x4x in 621 mode for speed grade 3, MHz */
#define CONFIG_EZYNQ_CLK_DS_ARM421_MAX_1_MHZ   533.0 /* Maximal ARM clk_6x4x in 421 mode for speed grade 1, MHz */
#define CONFIG_EZYNQ_CLK_DS_ARM421_MAX_2_MHZ   600.0 /* Maximal ARM clk_6x4x in 421 mode for speed grade 2, MHz */
#define CONFIG_EZYNQ_CLK_DS_ARM421_MAX_3_MHZ   710.0 /* Maximal ARM clk_6x4x in 421 mode for speed grade 3, MHz */
#define CONFIG_EZYNQ_CLK_DS_DDR3_MAX_1_MBPS   1066.0 /* Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 1 */
#define CONFIG_EZYNQ_CLK_DS_DDR3_MAX_2_MBPS   1066.0 /* Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 2 */
#define CONFIG_EZYNQ_CLK_DS_DDR3_MAX_3_MBPS   1333.0 /* Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 3 */
#define CONFIG_EZYNQ_CLK_DS_DDRX_MAX_X_MBPS    800.0 /* Maximal DDR3L, DDR2, LPDDR2 performance in Mb/s - twice clock frequency (MHz). All speed grades */
#define CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_1_MHZ   355.0 /* Maximal DDR_2X clock frequency (MHz) for speed grade 1 */
#define CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_2_MHZ   408.0 /* Maximal DDR_2X clock frequency (MHz) for speed grade 2 */
#define CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_3_MHZ   444.0 /* Maximal DDR_2X clock frequency (MHz) for speed grade 3 */

/*  SoC  parameters to set phases manually (or as a starting point for automatic) Not yet processed */
#define CONFIG_EZYNQ_DDR_DQS_TO_CLK_DELAY_0        0.0
#define CONFIG_EZYNQ_DDR_DQS_TO_CLK_DELAY_1        0.0
#define CONFIG_EZYNQ_DDR_DQS_TO_CLK_DELAY_2        0.0
#define CONFIG_EZYNQ_DDR_DQS_TO_CLK_DELAY_3        0.0
#define CONFIG_EZYNQ_DDR_DQS_0_PACKAGE_LENGTH      504
#define CONFIG_EZYNQ_DDR_DQS_1_PACKAGE_LENGTH      495
#define CONFIG_EZYNQ_DDR_DQS_2_PACKAGE_LENGTH      520
#define CONFIG_EZYNQ_DDR_DQS_3_PACKAGE_LENGTH      835
#define CONFIG_EZYNQ_DDR_DQ_0_PACKAGE_LENGTH       465
#define CONFIG_EZYNQ_DDR_DQ_1_PACKAGE_LENGTH       480
#define CONFIG_EZYNQ_DDR_DQ_2_PACKAGE_LENGTH       550
#define CONFIG_EZYNQ_DDR_DQ_3_PACKAGE_LENGTH       780
#define CONFIG_EZYNQ_DDR_CLOCK_0_PACKAGE_LENGTH    470.0
#define CONFIG_EZYNQ_DDR_CLOCK_1_PACKAGE_LENGTH    470.0
#define CONFIG_EZYNQ_DDR_CLOCK_2_PACKAGE_LENGTH    470.0
#define CONFIG_EZYNQ_DDR_CLOCK_3_PACKAGE_LENGTH    470.0
/* Sorry for propOgation - this is how it is called in the tools */
#define CONFIG_EZYNQ_DDR_DQS_0_PROPOGATION_DELAY   160
#define CONFIG_EZYNQ_DDR_DQS_1_PROPOGATION_DELAY   160
#define CONFIG_EZYNQ_DDR_DQS_2_PROPOGATION_DELAY   160
#define CONFIG_EZYNQ_DDR_DQS_3_PROPOGATION_DELAY   160
#define CONFIG_EZYNQ_DDR_DQ_0_PROPOGATION_DELAY    160
#define CONFIG_EZYNQ_DDR_DQ_1_PROPOGATION_DELAY    160
#define CONFIG_EZYNQ_DDR_DQ_2_PROPOGATION_DELAY    160
#define CONFIG_EZYNQ_DDR_DQ_3_PROPOGATION_DELAY    160
#define CONFIG_EZYNQ_DDR_CLOCK_0_PROPOGATION_DELAY 160
#define CONFIG_EZYNQ_DDR_CLOCK_1_PROPOGATION_DELAY 160
#define CONFIG_EZYNQ_DDR_CLOCK_2_PROPOGATION_DELAY 160
#define CONFIG_EZYNQ_DDR_CLOCK_3_PROPOGATION_DELAY 160


#endif /* __CONFIG_XC7Z020_1CLG484_H */
