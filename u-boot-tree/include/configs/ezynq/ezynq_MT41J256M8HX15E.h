 /*
 * (C) Copyright 2013 Elphel, Inc.
 *
 * Configuration for ezynq for Micron MT41J256M8HX15E DDR3 memory
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
#ifndef __CONFIG_EZYNQ_MT41J256M8HX15E_H
#define __CONFIG_EZYNQ_MT41J256M8HX15E_H

#define CONFIG_EZYNQ_DDR_DS_PARTNO           MT41J256M8HX15E /* Memory part number  (currently not used - derive some parameters later) */
/* CONFIG_EZYNQ_DDR_DS_MEMORY_TYPE will be redefined to DDR3 as Zynq is slow with DDR3 */
#define CONFIG_EZYNQ_DDR_DS_MEMORY_TYPE      DDR3  /* DDR memory type: DDR3 (1.5V), DDR3L (1.35V), DDR2 (1.8V), LPDDR2 (1.2V) */

#define CONFIG_EZYNQ_DDR_DS_BANK_ADDR_COUNT   3  /* Number of DDR banks */
#define CONFIG_EZYNQ_DDR_DS_ROW_ADDR_COUNT   15  /* Number of DDR Row Address bits */
#define CONFIG_EZYNQ_DDR_DS_COL_ADDR_COUNT   10  /* Number of DDR Column address bits */
#define CONFIG_EZYNQ_DDR_DS_DRAM_WIDTH       8  /* Memory chip bus width (not yet used) */
#define CONFIG_EZYNQ_DDR_DS_RCD              7   /* DESCRIPTION':'RAS to CAS delay (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_T_RCD           13.125 /* Activate to internal Read or Write (ns). May be used to calculate CONFIG_EZYNQ_DDR_DS_RCD automatically */
#define CONFIG_EZYNQ_DDR_DS_RP               7   /* Row Precharge time (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_T_RP             13.125 /* Precharge command period (ns).  May be used to calculate CONFIG_EZYNQ_DDR_DS_RP automatically, */
#define CONFIG_EZYNQ_DDR_DS_T_RC             49.5/* Activate to Activate or Refresh command period (ns) */
#define CONFIG_EZYNQ_DDR_DS_T_RAS_MIN        36.0 /* Minimal Row Active time (ns) */
#define CONFIG_EZYNQ_DDR_DS_T_FAW            30.0 /* Minimal running window for 4 page activates (ns) */
#define CONFIG_EZYNQ_DDR_DS_T_RFC           300.0 /* Minimal Refresh-to-Activate or Refresh command period (ns) */
#define CONFIG_EZYNQ_DDR_DS_T_WR             15.0 /* Write recovery time (ns) */
#define CONFIG_EZYNQ_DDR_DS_T_REFI_US         7.8 /* Maximal average periodic refresh, microseconds. Will be automatically reduced if high temperature option is selected */
#define CONFIG_EZYNQ_DDR_DS_RTP               4 /* Minimal Read-to-Precharge time (in tCK). Will use max of this and CONFIG_EZYNQ_DDR_DS_T_RTP/tCK */
#define CONFIG_EZYNQ_DDR_DS_T_RTP             7.5 /* Minimal Read-to-Precharge time  (ns). Will use max of this divided by tCK and CONFIG_EZYNQ_DDR_DS_RTP */
#define CONFIG_EZYNQ_DDR_DS_WTR               4   /* Minimal Write-to-Read time (in tCK). Will use max of this and CONFIG_EZYNQ_DDR_DS_T_WTR/tCK */
#define CONFIG_EZYNQ_DDR_DS_T_WTR             7.5 /* Minimal Write-to-Read time  (ns). Will use max of this divided by tCK and CONFIG_EZYNQ_DDR_DS_WTR */
#define CONFIG_EZYNQ_DDR_DS_XP                4   /* Minimal time from power down (DLL on) to any operation (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_T_DQSCK_MAX       5.5 /* LPDDR2 only. DQS output access time from CK (ns). Used for LPDDR2 */
#define CONFIG_EZYNQ_DDR_DS_CCD               5   /* DESCRIPTION':'CAS-to-CAS command delay (in tCK) (4 in Micron DS) */
#define CONFIG_EZYNQ_DDR_DS_RRD               6   /* ACTIVATE-to-ACTIVATE minimal command period (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_T_RRD            10.0 /* ACTIVATE-to-ACTIVATE minimal command period (ns). May be used to calculate CONFIG_EZYNQ_DDR_DS_RRD automatically */
#define CONFIG_EZYNQ_DDR_DS_MRD               4   /* MODE REGISTER SET command period (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_MOD              12   /* MODE REGISTER SET update delay (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_T_MOD            15.0 /* MODE REGISTER SET update delay  (ns). */
#define CONFIG_EZYNQ_DDR_DS_T_WLMRD          40.0 /* Write leveling : time to the first DQS rising edge (ns). */
#define CONFIG_EZYNQ_DDR_DS_CKE               3   /* CKE min pulse width (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_T_CKE             7.5 /* CKE min pulse width (ns). 5.625  */
#define CONFIG_EZYNQ_DDR_DS_CKSRE             5   /* Keep valid clock after self refresh/power down entry (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_T_CKSRE          10.0 /* Keep valid clock after self refresh/power down entry (ns). */
#define CONFIG_EZYNQ_DDR_DS_CKSRX             5   /* Valid clock before self refresh, power down or reset exit (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_T_CKSRX          10.0 /* Valid clock before self refresh, power down or reset exit (ns). */
#define CONFIG_EZYNQ_DDR_DS_ZQCS             64   /* ZQCS command: short calibration time (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_ZQCL            512   /* ZQCL command: long calibration time, including init (in tCK) */
#define CONFIG_EZYNQ_DDR_DS_INIT2             5   /* LPDDR2 only: tINIT2 (in tCK): clock stable before CKE high */
#define CONFIG_EZYNQ_DDR_DS_T_INIT4_US        1.0 /* LPDDR2 only: tINIT4 (in us)- minimal idle time after RESET command. */
#define CONFIG_EZYNQ_DDR_DS_T_INIT5_US       10.0 /* LPDDR2 only: tINIT5 (in us)- maximal duration of device auto initialization. */
#define CONFIG_EZYNQ_DDR_DS_T_ZQINIT_US       1.0 /* LPDDR2 only: tZQINIT (in us)- ZQ initial calibration time. */


#endif /* __CONFIG_EZYNQ_MT41J256M8HX15E_H */
