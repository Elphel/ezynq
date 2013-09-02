#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# Definitions of Zynq DDRC registers 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
__author__ = "Andrey Filippov"
__copyright__ = "Copyright 2013, Elphel, Inc."
__license__ = "GPL"
__version__ = "3.0+"
__maintainer__ = "Andrey Filippov"
__email__ = "andrey@elphel.com"
__status__ = "Development"
# DDRC Registers
DDRC_DEFS={ #not all fields are defined currently
    'BASE_ADDR':(0xF8006000,),       
    'ddrc_ctrl':               {'OFFS': 0x000,'DFLT':0x00000200,'RW':'RW','FIELDS':{
                  'reg_ddrc_dis_auto_refresh':{'r':(16,16),'d':0,'c':'Dynamic. 1 - disable autorefresh'},
                  'reg_ddrc_dis_act_bypass':  {'r':(15,15),'d':0,'c':'Debug. 1 - disable bypass for high priority read activity'},
                  'reg_ddrc_dis_rd_bypass':   {'r':(14,14),'d':0,'c':'Debug. 1 - disable bypass for high priority read page hits'},
                  'reg_ddrc_dis_rd_bypass':   {'r':( 7,13),'d':0x4,'c':'Switch to alternative transactions store after this inactivity'},
                  'reg_ddrc_burst8_refresh':  {'r':( 4, 6),'d':0,'c':'Refresh accumulate: 0 - single refresh, 1 - burst of 2 refresh, 7 - burst of 8 refresh'},
                  'reg_ddrc_data_bus_width':  {'r':( 2, 3),'d':0,'c':'DDR bus width: 0 - 32, 1 - 16, >=2 - reserved'},
                  'reg_ddrc_powerdown_en':    {'r':( 1, 1),'d':0,'c':'Dynamic: 1 - enable power down on idle'},
                  'reg_ddrc_soft_rstb':       {'r':( 0, 0),'d':0,'c':'Dynamic: Active low soft DDRC reset (and update non-dynamic registers/bit fields'}}},
    'two_rank_cfg':            {'OFFS': 0x004,'DFLT':0x000C1076,'RW':'RW','FIELDS':{
                  'reserved1':                {'r':(28,28),'d':0,'c':'reserved'},                                                                  
                  'reserved2':                {'r':(27,27),'d':0,'c':'reserved'},                                                                  
                  'reserved3':                {'r':(22,26),'d':0,'c':'reserved'},                                                                  
                  'reserved4':                {'r':(21,21),'d':0,'c':'reserved'},                                                                  
                  'reserved5':                {'r':(19,20),'d':0x1,'c':'reserved'},                                                                  
                  'reg_ddrc_addrmap_cs_ bit0':{'r':(14,18),'d':0x10,'c':'must be manually set to 0'},                                                                  
                  'reserved6':                {'r':(12,13),'d':0x1,'c':'reserved'},                                                                  
                  'reg_ddrc_t_rfc_nom_x32':   {'r':( 0,11),'d':0x76,'c':'Dynamic. tREFI, default set for DDR3'}}},                                                                   
    'hpr_reg':                 {'OFFS': 0x008,'DFLT':0x03C0780F,'RW':'RW','FIELDS':{
                  'reg_ddrc_hpr_xact_run_length':     {'r':(22,25),'d':0xF,'c':'HPR queue transactions to be served after going critical'},
                  'reg_ddrc_hpr_max_starve_x32':      {'r':(11,21),'d':0xF,'c':'Number of 32x clocks HPR may be starved before going critical'},
                  'reg_ddrc_hpr_min_non_critical_x32':{'r':( 0,10),'d':0xF,'c':'Number off 32x clocks HPR queue is guaranteed to be non-critical'}}},
    'lpr_reg':                 {'OFFS': 0x00C,'DFLT':0x03C0780F,'RW':'RW','FIELDS':{
                  'reg_ddrc_lpr_xact_run_length':     {'r':(22,25),'d':0xF,'c':'LPR queue transactions to be served after going critical'},
                  'reg_ddrc_lpr_max_starve_x32':      {'r':(11,21),'d':0xF,'c':'Number of 32x clocks LPR may be starved before going critical'},
                  'reg_ddrc_lpr_min_non_critical_x32':{'r':( 0,10),'d':0xF,'c':'Number off 32x clocks LPR queue is guaranteed to be non-critical'}}},
    'wr_reg':                  {'OFFS': 0x010,'DFLT':0x0007F80F,'RW':'RW','FIELDS':{
                  'reg_ddrc_w_max_starve_x32':        {'r':(15,25),'d':0xF,'c':'Number of 32x clocks write queue may be starved before going critical'},
                  'reg_ddrc_w_xact_run_length':       {'r':(11,14),'d':0xF,'c':'write queue transactions to be served after going critical'},
                  'reg_ddrc_w_min_non_critical_x32':  {'r':( 0,10),'d':0xF,'c':'Number off 32x clocks write queue is guaranteed to be non-critical'}}},
    'dram_param_reg0':         {'OFFS': 0x014,'DFLT':0x00041016,'RW':'RW','FIELDS':{
                  'reg_ddrc_post_selfref_ gap_x32':   {'r':(14,20),'d':0x10,'c':'DRAM-related, minimal time after self refresh'},
                  'reg_ddrc_t_rfc_min':               {'r':( 6,15),'d':0x40,'c':'Dynamic, tRFC'}, 
                  'reg_ddrc_t_rc':                    {'r':( 0, 5),'d':0x16,'c':'DRAM-related tRC'}}}, 
    'dram_param_reg1':         {'OFFS': 0x018,'DFLT':0x351B48D9,'RW':'RW','FIELDS':{
                  'reg_ddrc_t_cke':                   {'r':(28,31),'d': 0x3,'c':'tCKE'}, 
                  'reg_ddrc_t_ras_min':               {'r':(22,26),'d': 0x14,'c':'tRAS min (clocks)'}, 
                  'reg_ddrc_t_ras_max':               {'r':(16,21),'d': 0x1b,'c':'tRAS max (x1024 clocks)'}, 
                  'reg_ddrc_t_faw':                   {'r':(10,15),'d': 0x12,'c':'tFAW (not more than 4 banks activated in this rolling time, clocks'}, 
                  'reg_ddrc_powerdown_ to_x32':       {'r':( 5, 9),'d': 0x6,'c':'power down after this many clocks of NOP/DESELECT (if enabled in mcr)'},
                  'reg_ddrc_wr2pre':                  {'r':( 0, 4),'d': 0x19,'c':'minimal write-to-precharge, clocks'}}}, 
    'dram_param_reg2':         {'OFFS': 0x01C,'DFLT':0x83015904,'RW':'RW','FIELDS':{
                  'reg_ddrc_t_rcd':                   {'r':(28,31),'d': 0x8,'c':'tRCD-AL'}, 
                  'reg_ddrc_rd2pre':                  {'r':(23,27),'d': 0x6,'c':'Read to precharge in the same bank'}, 
                  'reg_ddrc_pad_pd':                  {'r':(20,22),'d': 0x0,'c':'non-DFI only: pads in/out powersave, in clocks'},
                  'reg_ddrc_t_xp':                    {'r':(15,19),'d': 0x2,'c':'tXP - power down exit to any operation'}, 
                  'reg_ddrc_wr2rd':                   {'r':(10,13),'d': 0x16,'c':'tWTR - write -to -read (clocks)'},
                  'reg_ddrc_rd2wr':                   {'r':( 5, 9),'d': 0x8,'c':'tRTW - read -to -write (clocks)'}, 
                  'reg_ddrc_write_latency':           {'r':( 0, 4),'d': 0x4,'c':'one clock less than actual DDR write latency'}}},  
    'dram_param_reg3':         {'OFFS': 0x020,'DFLT':0x250882D0,'RW':'M','FIELDS':{
                  'reserved':                         {'r':(31,31),'d': 0,'c':'reserved'},
                  'reg_ddrc_dis_pad_pd':              {'r':(30,30),'d': 0,'c':'Disable pad power down'},                                                                                               
                  'reg_phy_mode_ddr1_d dr2':          {'r':(29,29),'d': 1,'c':'Unused'},                                                                                               
                  'reg_ddrc_read_latency':            {'r':(24,28),'d': 0x5,'c':'Read Latency, clocks'}, 
                  'reg_ddrc_en_dfi_dram_clk_disable': {'r':(23,23),'d': 0,'c':'Enables clock disable...'}, 
                  'reg_ddrc_mobile':                  {'r':(22,22),'d': 0,'c':'0 - DDR2/DDR3, 1 - LPDDR2'}, 
                  'reserved1':                        {'r':(21,21),'d': 0,'c':'reserved'},
                  'reg_ddrc_refresh_to_x32':          {'r':(16,20),'d': 0x8,'c':'Dynamic, "speculative refresh"'}, 
                  'reg_ddrc_t_rp':                    {'r':(12,15),'d': 0x8,'c':'tRP'}, 
                  'reg_ddrc_refresh_margin':          {'r':( 8,11),'d': 0x2,'c':'do refresh this cycles before timer expires'}, 
                  'reg_ddrc_t_rrd':                   {'r':( 5, 7),'d': 0x6,'c':'tRRD Minimal time between activates of different banks'}, 
                  'reg_ddrc_t_ccd':                   {'r':( 2, 4),'d': 0x4,'c':'tCCD One less than minimal time between reads of writes to different banks'}, 
                  'reserved2':                        {'r':( 0, 1),'d': 0,'m':'R','c':'reserved'}}},
    'dram_param_reg4':         {'OFFS': 0x024,'DFLT':0x0000003C,'RW':'M','FIELDS':{
                  'reg_ddrc_mr_rdata_valid':          {'r':(27,27),'d': 0,'m':'R','c':'cleared by reading mode_reg_read (0x2a4), set when mode_reg_read gets new data'}, 
                  'reg_ddrc_mr_type':                 {'r':(26,26),'d': 0,'c':'0 - mode register write, 1 - mode register read'},  
                  'ddrc_reg_mr_wr_busy':              {'r':(25,25),'d': 0,'m':'R','c':'1 - do not issue mode register R/W (wait 0)'},  
                  'reg_ddrc_mr_data':                 {'r':( 9,24),'d': 0,'c':'DDR2/3: Mode Register Write data'},   
                  'reg_ddrc_mr_addr':                 {'r':( 7, 8),'d': 0,'c':'DDR2/3: Mode Register address (0 - MR0, ... 3 - MR3)'},  
                  'reg_ddrc_mr_wr':                   {'r':( 6, 6),'d': 0,'m':'W','c':'low-to-high starts mode reg r/w (if not ddrc_reg_mr_wr_busy)'},  
                  'reserved1':                        {'r':( 2, 5),'d': 0xF,'c':'reserved'},
                  'reg_ddrc_prefer_write':            {'r':( 1, 1),'d': 0,'c':'1: Bank selector prefers writes over reads'}, 
                  'reg_ddrc_en_2t_timing_mode':       {'r':( 0, 0),'d': 0,'c':'0 - DDRC uses 1T timing, 1 - 2T timing'}}}, 
    'dram_init_param':         {'OFFS': 0x028,'DFLT':0x00002007,'RW':'RW','FIELDS':{
                  'reg_ddrc_t_mrd':                   {'r':(11,13),'d': 0x4,'c':'tMRD - cycles between Load Mode commands (default is set for DDR3)'},
                  'reg_ddrc_pre_ocd_x32':             {'r':( 7,10),'d': 0,'c':'OCD complete delay (may be 0)'}, 
                  'reg_ddrc_final_wait_x32':          {'r':( 0, 6),'d': 0x7,'c':'Wait after DDR INIT (set for DDR3)'}}}, 
    'dram_emr_reg':            {'OFFS': 0x02C,'DFLT':0x00000008,'RW':'RW','FIELDS':{
                  'reg_ddrc_emr3':                    {'r':(16,31),'d': 0,'c':'DDR3: Value loaded into MR3 reg, DDR2: EMR3, LPDDR2 - unused'}, 
                  'reg_ddrc_emr2':                    {'r':( 0,15),'d': 0x8,'c':'DDR3: Value loaded into MR2 reg, DDR2: EMR2, LPDDR2 - MR3'}}}, 
    'dram_emr_mr_reg':         {'OFFS': 0x030,'DFLT':0x00000940,'RW':'RW','FIELDS':{
                  'reg_ddrc_emr':                     {'r':(16,31),'d': 0,'c':'DDR3: Value loaded into MR1 reg, DDR2: EMR1,  LPDDR2 - MR2'}, 
                  'reg_ddrc_mr':                      {'r':( 0,15),'d': 0x940,'c':'DDR3: Value loaded into MR0 reg, DDR2: MR, LPDDR2 - MR1'}}}, 
    
    'dram_burst8_rdwr':        {'OFFS': 0x034,'DFLT':0x00020304,'RW':'M','FIELDS':{
                  'reg_ddrc_burstchop':               {'r':(28,28),'d':0,'c':' Not supported, 1 - burstchop mode'},
                  'reserved1':                        {'r':(26,27),'d':0,'m':'R','c':'reserved'},  
                  'reg_ddrc_post_cke_x1024':          {'r':(16,25),'d':0x2,'c':'CKE high to initialization'}, 
                  'reserved2':                        {'r':(15,14),'d':0,'m':'R','c':'reserved'},
                  'reg_ddrc_post_cke_x1024':          {'r':( 4,13),'d':0x3,'c':'soft reset to CKE high'}, 
                  'reg_ddrc_burst_rdwr':              {'r':( 0, 3),'d':0x4,'c':'2 - burst length 4, 4 - b.l. 8, 0x10 - b.l. 16, others reserved'}}}, 
                                                                                   
    'dram_disable_dq':         {'OFFS': 0x038,'DFLT':0x00000000,'RW':'M','FIELDS':{
                  'reserved1':                        {'r':( 9,12),'d':0,'c':'reserved'},  
                  'reserved2':                        {'r':( 8, 8),'d':0,'c':'reserved'},  
                  'reserved3':                        {'r':( 7, 7),'d':0,'c':'reserved'},  
                  'reserved4':                        {'r':( 6, 6),'d':0,'c':'reserved'},  
                  'reserved5':                        {'r':( 2, 5),'d':0,'m':'R','c':''},  
                  'reg_ddrc_dis_dq':                  {'r':( 1, 1),'d':0,'c':'Dynamic, debug. Stop dequeue transactions, no DDR operations'},  
                  'reg_ddrc_force_low_pri_n':         {'r':( 0, 0),'d':0,'c':'0 - read transactions low priority (1 - high read priority if enabled in AXI pri read)'}}}, 
                                                                                  
    'dram_addr_map_bank':      {'OFFS': 0x03C,'DFLT':0x00000F77,'RW':'RW','FIELDS':{
                  'reg_ddrc_addrmap_col_b6':          {'r':(16,19),'d':0,'c':'Selects address bits for column address bit 7, half bus width - column address bits 8, int. base=9'},  
                  'reg_ddrc_addrmap_col_b5':          {'r':(12,15),'d':0,'c':'Selects address bits for column address bit 6, half bus width - column address bits 7, int. base=8'},  
                  'reg_ddrc_addrmap_ba nk_b2':        {'r':( 8,11),'d':0xf,'c':'Selects AXI address bit for bank2. Valid 0..15. Int. base=7. If 15, bank2 is set to 0'},  
                  'reg_ddrc_addrmap_ba nk_b2':        {'r':( 4, 7),'d':0x7,'c':'Selects AXI address bit for bank1. Valid 0..14. Int. base=6.'},  
                  'reg_ddrc_addrmap_ba nk_b2':        {'r':( 0, 3),'d':0x7,'c':'Selects AXI address bit for bank0. Valid 0..14. Int. base=5.'}}},  
    'dram_addr_map_col':       {'OFFS': 0x040,'DFLT':0xFFF00000,'RW':'RW','FIELDS':{
                  'reg_ddrc_addrmap_col_b11':         {'r':(28,31),'d':0xF,'c':'Selects address bits for col. addr. bit 13 (LP - 12), Valid 0..7 and 15, half width - unused (LP-13), int. base=14'},  
                  'reg_ddrc_addrmap_col_b10':         {'r':(24,27),'d':0xF,'c':'Selects address bits for col. addr. bit 12 (LP - 11), Valid 0..7 and 15, half width - 13 (LP-12), int. base=13'},  
                  'reg_ddrc_addrmap_col_b9':          {'r':(20,23),'d':0xF,'c':'Selects address bits for col. addr. bit 11 (LP - 10), Valid 0..7 and 15, half width - 12 (LP-11), int. base=12'},  
                  'reg_ddrc_addrmap_col_b8':          {'r':(16,19),'d':0,'c':'Selects address bits for col. addr. bit 9, Valid 0..7 and 15, half width - 11 (LP-10), int. base=11'},  
                  'reg_ddrc_addrmap_col_b7':          {'r':(12,15),'d':0,'c':'Selects address bits for col. addr. bit 8, Valid 0..7 and 15, half width - 9, int. base=10'},  
                  'reg_ddrc_addrmap_col_b4':          {'r':( 8,11),'d':0,'c':'Selects address bits for col. addr. bit 5, Valid 0..7, half width - bit 6, int. base=7'},  
                  'reg_ddrc_addrmap_col_b3':          {'r':( 4, 7),'d':0,'c':'Selects address bits for col. addr. bit 4, Valid 0..7, half width - bit 5, int. base=6'},  
                  'reg_ddrc_addrmap_col_b2':          {'r':( 0, 3),'d':0,'c':'Selects address bits for col. addr. bit 3, Valid 0..7, half width - bit 4, int. base=5'}}},  
    'dram_addr_map_row':       {'OFFS': 0x044,'DFLT':0x0FF55555,'RW':'RW','FIELDS':{
                  'reg_ddrc_addrmap_row_b15':         {'r':(24,27),'d':0xF,'c':'Selects address bits for row. addr. bit 15, Valid 0..5 and 15, int. base=24 if 15 - address bit 15 is set to 0'},  
                  'reg_ddrc_addrmap_row_b14':         {'r':(20,23),'d':0xF,'c':'Selects address bits for row. addr. bit 14, Valid 0..6 and 15, int. base=23 if 15 - address bit 14 is set to 0'},  
                  'reg_ddrc_addrmap_row_b13':         {'r':(16,19),'d':0x5,'c':'Selects address bits for row. addr. bit 13, Valid 0..7 and 15, int. base=22 if 15 - address bit 13 is set to 0'},  
                  'reg_ddrc_addrmap_row_b12':         {'r':(12,15),'d':0x5,'c':'Selects address bits for row. addr. bit 12, Valid 0..8 and 15, int. base=21 if 15 - address bit 12 is set to 0'},  
                  'reg_ddrc_addrmap_row_b2_11':       {'r':( 8,11),'d':0x5,'c':'Selects address bits for row. addr. bits 2 to 11, Valid 0..11, int. base=11 (for a2) to 20 (for a 11)'},  
                  'reg_ddrc_addrmap_row_b1':          {'r':( 4, 7),'d':0x5,'c':'Selects address bits for row. addr. bit 1,  Valid 0..11, int. base=10'},  
                  'reg_ddrc_addrmap_row_b0':          {'r':( 0, 3),'d':0x5,'c':'Selects address bits for row. addr. bit 0,  Valid 0..11, int. base=9'}}},  

    'dram_odt_reg':            {'OFFS': 0x048,'DFLT':0x00000249,'RW':'RW','FIELDS':{
                  'reserved1':                        {'r':(29,27),'d':0,'c':'reserved'},  
                  'reserved2':                        {'r':(24,26),'d':0,'c':'reserved'},  
                  'reserved3':                        {'r':(21,23),'d':0,'c':'reserved'},  
                  'reserved4':                        {'r':(18,20),'d':0,'c':'reserved'},  
                  'reg_phy_idle_local_odt':           {'r':(16,17),'d':0,'c':'2-bit drive ODT when OE is inactive and no read (power save)'},  
                  'reg_phy_wr_local_odt':             {'r':(14,15),'d':0,'c':'ODT strength during write leveling'}, 
                  'reg_phy_rd_local_odt':             {'r':(12,13),'d':0,'c':'ODT strength during read'},  
                  'reserved5':                        {'r':( 9,11),'d':0x1,'c':'reserved'},  
                  'reserved6':                        {'r':( 6, 8),'d':0x1,'c':'reserved'},  
                  'reserved7':                        {'r':( 3, 5),'d':0x1,'c':'reserved'},  
                  'reserved8':                        {'r':( 0, 2),'d':0x1,'c':'reserved'}}},
    'phy_dbg_reg':             {'OFFS': 0x04C,'DFLT':0x00000000,'RW':'R','FIELDS':{
                  'phy_reg_bc_fifo_re3':              {'r':(19,19),'d':0,'m':'R','c':'Debug read capture FIFO read enable for data slice 3'},   
                  'phy_reg_bc_fifo_we3':              {'r':(18,18),'d':0,'m':'R','c':'Debug read capture FIFO write enable for data slice 3'},   
                  'phy_reg_bc_dqs_oe3':               {'r':(17,17),'d':0,'m':'R','c':'Debug DQS output enable for data slice 3'}, 
                  'phy_reg_bc_dq_oe3':                {'r':(16,16),'d':0,'m':'R','c':'Debug DQ  output enable for data slice 3'}, 
                  'phy_reg_bc_fifo_re2':              {'r':(15,15),'d':0,'m':'R','c':'Debug read capture FIFO read enable for data slice 2'},   
                  'phy_reg_bc_fifo_we2':              {'r':(14,14),'d':0,'m':'R','c':'Debug read capture FIFO write enable for data slice 2'}, 
                  'phy_reg_bc_dqs_oe2':               {'r':(13,13),'d':0,'m':'R','c':'Debug DQS output enable for data slice 2'}, 
                  'phy_reg_bc_dq_oe2':                {'r':(12,12),'d':0,'m':'R','c':'Debug DQ  output enable for data slice 2'}, 
                  'phy_reg_bc_fifo_re1':              {'r':(11,11),'d':0,'m':'R','c':'Debug read capture FIFO read enable for data slice 1'},   
                  'phy_reg_bc_fifo_we1':              {'r':(10,10),'d':0,'m':'R','c':'Debug read capture FIFO write enable for data slice 1'}, 
                  'phy_reg_bc_dqs_oe1':               {'r':( 9, 9),'d':0,'m':'R','c':'Debug DQS output enable for data slice 1'}, 
                  'phy_reg_bc_dq_oe1':                {'r':( 8, 8),'d':0,'m':'R','c':'Debug DQ  output enable for data slice 1'}, 
                  'phy_reg_bc_fifo_re0':              {'r':( 9, 7),'d':0,'m':'R','c':'Debug read capture FIFO read enable for data slice 0'},   
                  'phy_reg_bc_fifo_we0':              {'r':( 6, 6),'d':0,'m':'R','c':'Debug read capture FIFO write enable for data slice 0'}, 
                  'phy_reg_bc_dqs_oe0':               {'r':( 5, 5),'d':0,'m':'R','c':'Debug DQS output enable for data slice 0'}, 
                  'phy_reg_bc_dq_oe0':                {'r':( 4, 4),'d':0,'m':'R','c':'Debug DQ  output enable for data slice 0'}, 
                  'phy_reg_rdc_fifo_rst_err_cnt':     {'r':( 0, 3),'d':0,'m':'R','c':'FIFO read pointers mismatch counter'}}},    
    'phy_cmd_timeout_rddata_cpt':{'OFFS': 0x050,'DFLT':0x00010200,'RW':'M','FIELDS':{
                  'reg_phy_wrlvl_num_of_dq0':         {'r':(28,31),'d':0,'c':'Number of sample for ratio increment during write leveling (recommended 8)'}, 
                  'reg_phy_gatelvl_num_of_dq0':       {'r':(24,27),'d':0,'c':'Number of sample for ratio increment during gate training (recommended 8)'}, 
                  'reserved1':                        {'r':(20,23),'d':0,'m':'R','c':'reserved'},  
                  'reg_phy_clk_stall_level':          {'r':(19,19),'d':0,'c':'1- Stall clock for DLL aging control'}, 
                  'reg_phy_dis_phy_ctrl_rstn':        {'r':(18,18),'d':0,'c':'1 - disable reset to PHY control'}, 
                  'reg_phy_rdc_fifo_rst_err_cnt_clr': {'r':(17,17),'d':0,'c':'1 - reset phy_dbg_reg.phy_reg_rdc_fifo_rst_err_cnt'}, 
                  'reg_phy_use_fixed_re':             {'r':(16,16),'d':0x1,'c':'... (should be high during training/leveling'}, 
                  'reg_phy_rdc_fifo_rst_disable':     {'r':(15,15),'d':0,'c':'1 - disable counting phy_dbg_reg.phy_reg_rdc_fifo_rst_err_cnt'}, 
                  'reserved2':                        {'r':(12,14),'d':0,'m':'R','c':'reserved'},  
                  'reg_phy_rdc_we_to_re_delay':       {'r':( 8,11),'d':0x2,'c':'use for fixed delay, when reg_phy_use_fixed_re==1'}, 
                  'reg_phy_wr_cmd_to_data':           {'r':( 4, 7),'d':0,'c':'Not used in DFI PHY'}, 
                  'reg_phy_rd_cmd_to_data':           {'r':( 0, 3),'d':0,'c':'Not used in DFI PHY'}}}, 
    'mode_sts_reg':            {'OFFS': 0x054,'DFLT':0x00000000,'RW':'R','FIELDS':{
                  'ddrc_reg_dbg_hpr_q_depth':         {'r':(16,20),'d':0,'m':'R','c':'number in high priority read CAM'},   
                  'ddrc_reg_dbg_lpr_q_depth':         {'r':(10,15),'d':0,'m':'R','c':'number in low priority read CAM'},  
                  'ddrc_reg_dbg_wr_q_depth':          {'r':( 4, 9),'d':0,'m':'R','c':'number in write CAM '},  
                  'ddrc_reg_dbg_stall':               {'r':( 3, 3),'d':0,'m':'R','c':'1 - commands accepted by controller'},  
                  'ddrc_reg_operating_mode':          {'r':( 0, 2),'d':0,'m':'R','c':'DDRC init, 1 - normal, 2 - power down, 3 - self refresh, >=4 - deep power down LPDDR2'}}}, 
    'dll_calib':               {'OFFS': 0x058,'DFLT':0x00000101,'RW':'RW','FIELDS':{
                  'reg_ddrc_dis_dll_calib':           {'r':(16,16),'d':0,'c':'Dynamic: 1- disable DLL_calib, 0 - issue DLL_calib periodically'},    
                  'reserved1':                        {'r':( 8,15),'d':0,'c':'reserved'},      
                  'reserved2':                        {'r':( 0, 7),'d':0,'c':'reserved'}}},
    'odt_delay_hold':          {'OFFS': 0x05C,'DFLT':0x00000023,'RW':'RW','FIELDS':{
                  'reg_ddrc_wr_odt_hold':             {'r':(12,15),'d':0,'c':'(Cycles to hold ODT for write command-1). For burst4 - 2, for burst8 - 4'},        
                  'reg_ddrc_rd_odt_hold':             {'r':( 8,11),'d':0,'c':'unused'},    
                  'reg_ddrc_wr_odt_delay':            {'r':( 4, 7),'d':0x2,'c':'From issuing write to setting ODT for write. Recommended for DDR3 - 0, for DDR2 (WL-5)'},      
                  'reg_ddrc_rd_odt_delay':            {'r':( 0, 3),'d':0x3,'c':'unused'}}},     
    'ctrl_reg1':               {'OFFS': 0x060,'DFLT':0x0000003E,'RW':'M','FIELDS':{
                  'reg_ddrc_selfref_en':              {'r':(12,12),'d':0,'c':'Dynamic - 1 - go to Self Refresh when transaction store is empty'},   
                  'reserved1':                        {'r':(11,11),'d':0,'m':'R','c':'reserved'},      
                  'reg_ddrc_dis_collision_page_opt':  {'r':(10,10),'d':0,'c':'Disable autoprecharge for collisions (write+write or read+write to the same address) when  reg_ddrc_dis_wc==1'},     
                  'reg_ddrc_dis_wc':                  {'r':( 9, 9),'d':0,'c':'1 - disable write combine, 0 - enable'},      
                  'reg_ddrc_refresh_update_level':    {'r':( 8, 8),'d':0,'c':'Dynamic: toggle to indicate refressh register(s) update'},    
                  'reg_ddrc_auto_pre_en':             {'r':( 7, 7),'d':0,'c':'1 - most R/W will be with autoprecharge'},      
                  'reg_ddrc_lpr_num_entries':         {'r':( 1, 6),'d':0x1F,'c':'(bit 6 ignored) (Size of low priority transaction store+1). HPR - 32 - this value'},      
                  'reg_ddrc_pageclose':               {'r':( 0, 0),'d':0,'c':'1 - close bank if no transactions in the store for it, 0 - keep open until not needed by other'}}}, 
    'ctrl_reg2':               {'OFFS': 0x064,'DFLT':0x00020000,'RW':'M','FIELDS':{
                  'reg_arb_go2critical_en':           {'r':(17,17),'d':0x1,'c':'0 - ignore "urgent" from AXI master, 1 - grant'},       
                  'reserved1':                        {'r':(13,16),'d':0,'m':'R','c':'reserved'},      
                  'reg_ddrc_go2critical_hysteresis':  {'r':( 5,12),'d':0,'c':'Latency of moving to critical state'},    
                  'reserved2':                        {'r':( 0, 4),'d':0,'m':'R','c':'reserved'}}},
    'ctrl_reg3':               {'OFFS': 0x068,'DFLT':0x00284027,'RW':'RW','FIELDS':{ # in code it was called 'rd_dll_force' TODO: Update hardware.h
                  'reg_ddrc_dfi_t_wlmrd':             {'r':(16,25),'d':0x28,'c':'DDR3 only: tMLRD from DRAM specs'},       
                  'reg_ddrc_rdlvl_rr':                {'r':( 8,15),'d':0x40,'c':'DDR3 read leveling read-to-read delay'},       
                  'reg_ddrc_wrlvl_ww':                {'r':( 0, 7),'d':0x27,'c':'DDR3 and LPDDR2 - write  leveling write-to-write delay'}}},       
    'ctrl_reg4':               {'OFFS': 0x06C,'DFLT':0x00001610,'RW':'RW','FIELDS':{ # in code it was called 'rd_dll_force0'
                  'dfi_t_ctrlupd_interval_max_x1024': {'r':( 8,15),'d':0x16,'c':'maximal time between DFI update requests in 1024 clocks'},        
                  'dfi_t_ctrlupd_interval_min_x1024': {'r':( 0, 7),'d':0x10,'c':'minimal time between DFI update requests in 1024 clocks'}}}, 
    'rd_dll_force1':           {'OFFS': 0x070},
    'wr_ratio_reg':            {'OFFS': 0x074},
    'ctrl_reg5':               {'OFFS': 0x078,'DFLT':0x00455111,'RW':'M','FIELDS':{# in code it was called 'rd_ratio_reg'
                  'reserved1':                        {'r':(26,31),'d':0,'m':'R','c':'reserved'},      
                  'reg_ddrc_t_ckesr':                 {'r':(20,25),'d':0x4,'c':'Min CKE low for self refresh, recomm.: DDR3:tCKE+1,DDR2:tCKE,LPDDR2:tCKESR'},       
                  'reg_ddrc_t_cksrx':                 {'r':(16,19),'d':0x5,'c':'CK valid before self refresh exit, recomm. DDR3:tCKSRX,DDR2:1,LPDDR2:2'}, 
                  'reg_ddrc_t_cksre':                 {'r':(12,15),'d':0x5,'c':'CK valid after self refresh entry, recomm. DDR3:tCKSRE,DDR2:1,LPDDR2:2'},      
                  'reg_ddrc_dfi_t_dram_clk_enable':   {'r':( 8,11),'d':0x1,'c':'deassert dfi_dram_clock disable to PHY clock enable in DFI clock cycles'},       
                  'reg_ddrc_dfi_t_dram_clk_disable':  {'r':( 4, 7),'d':0x1,'c':'assert  dfi_dram_clock disable to PHY clock disable in DFI clock cycles'}, 
                  'reg_ddrc_dfi_t_ctrl_delay':        {'r':( 0, 3),'d':0x1,'c':'assert/deassert  DFI control signals to PHY-DRAM control signals'}}},      
    'ctrl_reg6':               {'OFFS': 0x07C,'DFLT':0x00032222,'RW':'M','FIELDS':{# in code it was called 'mstr_dll_status1_reg'
                  'reserved1':                        {'r':(20,31),'d':0,'m':'R','c':'reserved'},      
                  'reg_ddrc_t_ckcsx':                 {'r':(16,19),'d':0x3,'c':'Clock stable before exiting clock stop. Recommended for LPDDR2: tXP+2'},     
                  'reg_ddrc_t_ckdpdx':                {'r':(12,15),'d':0x2,'c':'Clock stable before Deep Power Down exit. Recommended for LPDDR2: 2'},    
                  'reg_ddrc_t_ckdpde':                {'r':( 8,11),'d':0x2,'c':'Maintain clock after Deep Power Down entry. Recommended for LPDDR2: 2'},    
                  'reg_ddrc_t_ckpdx':                 {'r':( 4, 7),'d':0x2,'c':'Clock stable before Power Down exit. Recommended for LPDDR2: 2'},    
                  'reg_ddrc_t_ckpde':                 {'r':( 0, 3),'d':0x2,'c':'Maintain clock after Power Down entry. Recommended for LPDDR2: 2'}}},
    'ddr_rd_slave_status0_reg':{'OFFS': 0x080},
    'ddr_rd_slave_status1_reg':{'OFFS': 0x084},
    'of_status0_reg':          {'OFFS': 0x088},
    'of_status1_reg':          {'OFFS': 0x08C},
    'of_status2_reg':          {'OFFS': 0x090},
    'of_status3_reg':          {'OFFS': 0x094},
    'mstr_dll_status2_reg':    {'OFFS': 0x098},
    'wr_dll_force1_reg':       {'OFFS': 0x09C},
    'refresh_timer01_reg':     {'OFFS': 0x0A0,'DFLT':0x00008000,'RW':'RW','FIELDS':{
                  'reserved1':                        {'r':(12,23),'d':0x8,'c':'reserved'},      
                  'reserved2':                        {'r':( 0,11),'d':0,'c':'reserved'}}},
    't_zq_reg':                {'OFFS': 0x0A4,'DFLT':0x10300802,'RW':'RW','FIELDS':{
                  'reg_ddrc_t_zq_short_nop':          {'r':(22,31),'d':0x40,'c':'DDR3 and LPDDR2 only: number of NOP after ZQCS (ZQ calibration short)'},       
                  'reg_ddrc_t_zq_long_nop':           {'r':(12,21),'d':0x300,'c':'DDR3 and LPDDR2 only: number of NOP after ZQCL (ZQ calibration long)'},        
                  'reg_ddrc_t_mod':                   {'r':( 2,11),'d':0x200,'c':'Mode register set command update delay >=0x80'},      
                  'reg_ddrc_ddr3':                    {'r':( 1, 1),'d':0x1,'c':'0 - DDR2, 1 - DDR3'},    
                  'reg_ddrc_dis_auto_zq ':            {'r':( 0, 0),'d':0,'c':'DDR3 and LPDDR2 only: 1 - disable auto generation of ZQCS, 0 - enable'}}},  
    't_zq_short_interval_reg': {'OFFS': 0x0A8,'DFLT':0x0020003A,'RW':'RW','FIELDS':{
                  'dram_rstn_x1024':                  {'r':(20,27),'d':0x2,'c':'DDR3 only: Number of cycles to assert reset during init sequence (in 1024 cycles)'},      
                  't_zq_short_interval_x1024':        {'r':( 0,19),'d':0x3a,'c':'DDR3 and LPDDR2 only: AVerage interval between automatic ZQCS in 1024 clock cycles'}}}, 
#     
    ' deep_pwrdwn_reg':{'OFFS': 0x0AC,'DFLT':0x00000000,'RW':'RW','FIELDS':{ # in code it was called 'status_data_sl_dll_01_reg' 
                  'deeppowerdown_to_x1024':           {'r':( 1, 8),'d':0,'c':'LPDDR2 only: minimal deep power down time in 1024 clk (specs - 500usec)'},       
                  'deeppowerdown_en':                 {'r':( 0, 0),'d':0,'c':'LPDDR2 only: 0 - normal, 1 - go to deep power down when transaction store is empty'}}}, 
                                                                                     
    'reg_2c':                  {'OFFS': 0x0B0,'DFLT':0x00000000,'RW':'M','FIELDS':{ # in code it was called 'status_data_sl_dll_23_reg'
                  'reg_ddrc_dfi_rd_data_eye_train':   {'r':(28,28),'d':0,'c':'DDR3 and LPDDR2 only: 1 - read data eye training (part of init sequence)'},      
                  'reg_ddrc_dfi_rd_dqs_gate_level':   {'r':(27,27),'d':0,'c':'1 - Read DQS gate leveling mode (DDR3 DFI only)'},   
                  'reg_ddrc_dfi_wr_level_en':         {'r':(26,26),'d':0,'c':'1 - Write leveling mode (DDR3 DFI only)'}, 
                  'ddrc_reg_trdlvl_max_error':        {'r':(25,25),'d':0,'m':'R','c':'DDR3 and LPDDR2 only: leveling/gate training timeout (clear on write)'},       
                  'ddrc_reg_twrlvl_max_error':        {'r':(24,24),'d':0,'m':'R','c':'DDR3 only: write leveling timeout (clear on write)'},     
                  'dfi_rdlvl_max_x1024':              {'r':(12,23),'d':0,'c':'Read leveling maximal time in 1024 clk. Typical value 0xFFF'},   
                  'dfi_wrlvl_max_x1024':              {'r':( 0,11),'d':0,'c':'Write leveling maximal time in 1024 clk. Typical value 0xFFF'}}}, 
    'reg_2d':                  {'OFFS': 0x0B4,'DFLT':0x00000200,'RW':'RW','FIELDS':{ # in code it was called 'status_dqs_sl_dll_01_reg'
                  'reserved1':                        {'r':(10,10),'d':0,'c':'reserved'},      
                  'reg_ddrc_skip_ocd':                {'r':( 9, 9),'d':0x1,'c':'should be 1, 0 is not supported. 1 - skip OCD adjustment step during DDR2 init,  use OCD_Default and OCD_exit'},    
                  'reserved2':                        {'r':( 0, 8),'d':0,'c':'reserved'}}},
    'dfi_timimg':              {'OFFS': 0x0B8,'DFLT':0x00200067,'RW':'RW','FIELDS':{ # in code it was called 'status_dqs_sl_dll_23_reg'
                  'reg_ddrc_dfi_t_ctrlup_max':        {'r':(15,24),'d':0x40,'c':'Maximal number of clocks  ddrc_dfi_ctrlupd_req can assert'},  
                  'reg_ddrc_dfi_t_ctrlup_min':        {'r':( 5,14),'d':0x3,'c':'Minimal number of clocks  ddrc_dfi_ctrlupd_req must be asserted'},     
                  'reg_ddrc_dfi_t_rddata_en':         {'r':( 0, 4),'d':0x7,'c':'LPDDR2 - RL, DDR2 and DDR3 - RL-1'}}},
#     u32 reserved1[0x2];
    'che_ecc_control_reg_offset':{'OFFS': 0x0C4,'DFLT':0x0,'RW':'RW', 'FIELDS':{
                  'clear_correctable_dram_ecc_error':  {'r':(1, 1),'d':0,'c':'1 - clear correctable log (valid+counters)'},  
                  'clear_uncorrectable_dram_ecc_error':{'r':(0, 0),'d':0,'c':'1 - clear uncorrectable log (valid+counters)'}}}, 
    'che_corr_ecc_log_reg_offset':{'OFFS': 0x0C8,'DFLT':0x0,'RW':'M', 'FIELDS':{
                  'ecc_corrected_bit_num':            {'r':( 1, 7),'d':0,'m':'CW','c':'encoded error bits for up to 72-bit data'},       
                  'corr_ecc_log_valid':               {'r':( 0, 0),'d':0,'m':'R','c':'set to 1 when correctable error is captured'}}}, 
    'che_corr_ecc_addr_reg_offset':{'OFFS': 0x0CC,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'corr_ecc_log_bank':                {'r':(28,30),'d':0,'m':'R','c':'bank [0:2]'},       
                  'corr_ecc_log_row':                 {'r':(12,27),'d':0,'m':'R','c':'row [0:15]'},      
                  'corr_ecc_log_col':                 {'r':( 0,11),'d':0,'m':'R','c':'col [0:11]'}}},      
                                                                                  
    'che_corr_ecc_data_31_0_reg_offset':{'OFFS': 0x0D0,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'corr_ecc_dat_31_0':                {'r':( 0,31),'d':0,'m':'R','c':'bits[0:31] of the word with correctable ECC error. actually only 0:7 have valid data, 8:31 are 0'}}},
    'che_corr_ecc_data_63_32_reg_offset':{'OFFS': 0x0D4,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'corr_ecc_dat_63_32':               {'r':( 0,31),'d':0,'m':'R','c':'bits[32:63] of the word with correctable ECC error. actually all are 0'}}},
    'che_corr_ecc_data_71_64_reg_offset':{'OFFS': 0x0D8,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'corr_ecc_dat_71_64':               {'r':( 0,31),'d':0,'m':'R','c':'bits[64:71] of the word with correctable ECC error. only lower 5 bits have data, the rest are 0'}}},
    'che_uncorr_ecc_log_reg_offset':{'OFFS': 0x0DC,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'uncorr_ecc_log_valid':             {'r':( 0, 0),'d':0,'m':'R','c':'Set to 1 when uncorrectable error is capture (no more captured until cleared), cleared by che_ecc_control_reg_offset'}}},
    'che_uncorr_ecc_addr_reg_offset':{'OFFS': 0x0E0,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'uncorr_ecc_log_bank':              {'r':(28,30),'d':0,'m':'R','c':'bank [0:2]'},       
                  'uncorr_ecc_log_row':               {'r':(12,27),'d':0,'m':'R','c':'row [0:15]'},      
                  'uncorr_ecc_log_col':               {'r':( 0,11),'d':0,'m':'R','c':'col [0:11]'}}},      
    'che_uncorr_ecc_data_31_0_reg_offset':{'OFFS': 0x0E4,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'uncorr_ecc_dat_31_0':              {'r':( 0,31),'d':0,'m':'R','c':'bits[0:31] of the word with uncorrectable ECC error. actually only 0:7 have valid data, 8:31 are 0'}}},
    'che_uncorr_ecc_data_63_32_reg_offset':{'OFFS': 0x0E8,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'uncorr_ecc_dat_63_32':             {'r':( 0,31),'d':0,'m':'R','c':'bits[32:63] of the word with uncorrectable ECC error. actually all are 0'}}},
    'che_uncorr_ecc_data_71_64_reg_offset':{'OFFS': 0x0EC,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'uncorr_ecc_dat_71_64':             {'r':( 0,31),'d':0,'m':'R','c':'bits[64:71] of the word with uncorrectable ECC error. only lower 5 bits have data, the rest are 0'}}},
    'che_ecc_stats_reg_offset':{'OFFS': 0x0F0,'DFLT':0x00000000,'RW':'CW', 'FIELDS':{
                  'stat_num_corr_err':                {'r':( 8,15),'d':0,'m':'R','c':'Number of correctable ECC errors since 1 written to bit 1 of che_ecc_control_reg_offset (0xC4)'},       
                  'stat_num_uncorr_err':              {'r':( 0, 7),'d':0,'m':'R','c':'Number of uncorrectable ECC errors since 1 written to bit 0 of che_ecc_control_reg_offset (0xC4)'}}},
    'ecc_scrub':               {'OFFS': 0x0F4,'DFLT':0x00000008,'RW':'RW', 'FIELDS':{
                  'reg_ddrc_dis_scrub':               {'r':( 3, 3),'d':1,'c':'1 - disable ECC scrubs, 0 - enable ECC scrubs'},       
                  'reg_ddrc_ecc_mode':                {'r':( 0, 2),'d':0,'c':'DRAM ECC mode. Valid only 0(no ECC)  and 0x4 - "SEC/DED over 1-beat'}}},
    'che_ecc_corr_bit_mask_31_0_reg_offset':{'OFFS': 0x0F8,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'ddrc_reg_ecc_corr_bit_mask':       {'r':( 0,31),'d':0,'m':'R','c':'bits[0:31] of the mask of the corrected data (1 - corrected, 0 - uncorrected). Only 0:7 have valid data, 8:31 are 0'}}},
    'che_ecc_corr_bit_mask_63_32_reg_offset':{'OFFS': 0x0FC,'DFLT':0x0,'RW':'R', 'FIELDS':{
                  'ddrc_reg_ecc_corr_bit_mask':       {'r':( 0,31),'d':0,'m':'R','c':'bits[32:63] of the mask of the corrected data (1 - corrected, 0 - uncorrected). all bits are 0'}}},
#     u32 reserved2[0x14];
    'phy_rcvr_enable':         {'OFFS': 0x114,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_dif_off':                  {'r':( 4, 7),'d':0,'c':'"Off" value of the drive of the receiver-enabled pins'},       
                  'reg_phy_dif_on':                   {'r':( 0, 3),'d':0,'c':'"On" value of the drive of the receiver-enabled pins'}}},
    'phy_config0':             {'OFFS': 0x118,'DFLT':0x40000001,'RW':'RW','FIELDS':{
                  'reg_phy_dq_offset':                {'r':(24,30),'d':0x40,'c':'Offset value of DQS to DQ during write leveling of data slice 0. Default is 0x40 for 90-degree shift'},       
                  'reserved1':                        {'r':(15,23),'d':0,'c':'reserved'},      
                  'reserved2':                        {'r':( 6,14),'d':0,'c':'reserved'},      
                  'reserved3':                        {'r':( 5, 5),'d':0,'c':'reserved'},      
                  'reserved4':                        {'r':( 4, 4),'d':0,'c':'reserved'},      
                  'reg_phy_wrlvl_inc_mode':           {'r':( 3, 3),'d':0,'c':'reserved'},       
                  'reg_phy_gatelvl_inc_mode':         {'r':( 2, 2),'d':0,'c':'reserved'},       
                  'reg_phy_rdlvl_inc_mode':           {'r':( 1, 1),'d':0,'c':'reserved'},       
                  'reg_phy_data_slice_in_use':        {'r':( 0, 0),'d':1,'c':'Data bus width for read FIFO generation. 0 - read data responses are ignored, 1 - data slice 0 is valid (always 1)'}}},
    'phy_config1':             {'OFFS': 0x11C,'DFLT':0x40000001,'RW':'RW','FIELDS':{
                  'reg_phy_dq_offset':                {'r':(24,30),'d':0x40,'c':'Offset value of DQS to DQ during write leveling of data slice 1. Default is 0x40 for 90-degree shift'},       
                  'reserved1':                        {'r':(15,23),'d':0,'c':'reserved'},      
                  'reserved2':                        {'r':( 6,14),'d':0,'c':'reserved'},      
                  'reserved3':                        {'r':( 5, 5),'d':0,'c':'reserved'},      
                  'reserved4':                        {'r':( 4, 4),'d':0,'c':'reserved'},      
                  'reg_phy_wrlvl_inc_mode':           {'r':( 3, 3),'d':0,'c':'reserved'},       
                  'reg_phy_gatelvl_inc_mode':         {'r':( 2, 2),'d':0,'c':'reserved'},       
                  'reg_phy_rdlvl_inc_mode':           {'r':( 1, 1),'d':0,'c':'reserved'},       
                  'reg_phy_data_slice_in_use':        {'r':( 0, 0),'d':1,'c':'Data bus width for read FIFO generation. 0 - read data responses are ignored, 1 - data slice 1 is valid'}}},
    'phy_config2':             {'OFFS': 0x120,'DFLT':0x40000001,'RW':'RW','FIELDS':{
                  'reg_phy_dq_offset':                {'r':(24,30),'d':0x40,'c':'Offset value of DQS to DQ during write leveling of data slice 2. Default is 0x40 for 90-degree shift'},       
                  'reserved1':                        {'r':(15,23),'d':0,'c':'reserved'},      
                  'reserved2':                        {'r':( 6,14),'d':0,'c':'reserved'},      
                  'reserved3':                        {'r':( 5, 5),'d':0,'c':'reserved'},      
                  'reserved4':                        {'r':( 4, 4),'d':0,'c':'reserved'},      
                  'reg_phy_wrlvl_inc_mode':           {'r':( 3, 3),'d':0,'c':'reserved'},       
                  'reg_phy_gatelvl_inc_mode':         {'r':( 2, 2),'d':0,'c':'reserved'},       
                  'reg_phy_rdlvl_inc_mode':           {'r':( 1, 1),'d':0,'c':'reserved'},       
                  'reg_phy_data_slice_in_use':        {'r':( 0, 0),'d':1,'c':'Data bus width for read FIFO generation. 0 - read data responses are ignored, 1 - data slice 2 is valid'}}},
    'phy_config3':             {'OFFS': 0x124,'DFLT':0x40000001,'RW':'RW','FIELDS':{
                  'reg_phy_dq_offset':                {'r':(24,30),'d':0x40,'c':'Offset value of DQS to DQ during write leveling of data slice 3. Default is 0x40 for 90-degree shift'},       
                  'reserved1':                        {'r':(15,23),'d':0,'c':'reserved'},      
                  'reserved2':                        {'r':( 6,14),'d':0,'c':'reserved'},      
                  'reserved3':                        {'r':( 5, 5),'d':0,'c':'reserved'},      
                  'reserved4':                        {'r':( 4, 4),'d':0,'c':'reserved'},      
                  'reg_phy_wrlvl_inc_mode':           {'r':( 3, 3),'d':0,'c':'reserved'},       
                  'reg_phy_gatelvl_inc_mode':         {'r':( 2, 2),'d':0,'c':'reserved'},       
                  'reg_phy_rdlvl_inc_mode':           {'r':( 1, 1),'d':0,'c':'reserved'},       
                  'reg_phy_data_slice_in_use':        {'r':( 0, 0),'d':1,'c':'Data bus width for read FIFO generation. 0 - read data responses are ignored, 1 - data slice 3 is valid'}}},
#     u32 reserved3[1];              /* 0x128*/,
    'phy_init_ratio0':         {'OFFS': 0x12C,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_gatelvl_init_ratio':       {'r':(10,19),'d':0,'c':'User-programmable init ratio used by Gate Leveling FSM, data slice 0'},       
                  'reg_phy_wrlvl_init_ratio':         {'r':( 0, 9),'d':0,'c':'User-programmable init ratio used by Write Leveling FSM, data slice 0'}}},
    'phy_init_ratio1':         {'OFFS': 0x130,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_gatelvl_init_ratio':       {'r':(10,19),'d':0,'c':'User-programmable init ratio used by Gate Leveling FSM, data slice 1'},       
                  'reg_phy_wrlvl_init_ratio':         {'r':( 0, 9),'d':0,'c':'User-programmable init ratio used by Write Leveling FSM, data slice 1'}}},
    'phy_init_ratio2':         {'OFFS': 0x134,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_gatelvl_init_ratio':       {'r':(10,19),'d':0,'c':'User-programmable init ratio used by Gate Leveling FSM, data slice 2'},       
                  'reg_phy_wrlvl_init_ratio':         {'r':( 0, 9),'d':0,'c':'User-programmable init ratio used by Write Leveling FSM, data slice 2'}}},
    'phy_init_ratio3':         {'OFFS': 0x138,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_gatelvl_init_ratio':       {'r':(10,19),'d':0,'c':'User-programmable init ratio used by Gate Leveling FSM, data slice 3'},       
                  'reg_phy_wrlvl_init_ratio':         {'r':( 0, 9),'d':0,'c':'User-programmable init ratio used by Write Leveling FSM, data slice 3'}}},
#     
    'phy_rd_dqs_cfg0':         {'OFFS': 0x140,'DFLT':0x00000040,'RW':'RW','FIELDS':{
                  'reg_phy_rd_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_rd_dqs_slave_force is 1, use this tap/delay value for read DQS slave DLL, data slice 0'},       
                  'reg_phy_rd_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_rd_dqs_slave_ratio  for the read DQS slave DLL, 1 - use provided in reg_phy_rd_dqs_slave_delay, data slice 0'},       
                  'reg_phy_rd_dqs_slave_ratio':       {'r':( 0, 9),'d':0x40,'c':'Fraction of the clock cycle (256 = full period) for the read DQS slave DLL, data slice 0'}}},
    'phy_rd_dqs_cfg1':         {'OFFS': 0x144,'DFLT':0x00000040,'RW':'RW','FIELDS':{
                  'reg_phy_rd_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_rd_dqs_slave_force is 1, use this tap/delay value for read DQS slave DLL, data slice 1'},       
                  'reg_phy_rd_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_rd_dqs_slave_ratio  for the read DQS slave DLL, 1 - use provided in reg_phy_rd_dqs_slave_delay, data slice 1'},       
                  'reg_phy_rd_dqs_slave_ratio':       {'r':( 0, 9),'d':0x40,'c':'Fraction of the clock cycle (256 = full period) for the read DQS slave DLL, data slice 1'}}},
    'phy_rd_dqs_cfg2':         {'OFFS': 0x148,'DFLT':0x00000040,'RW':'RW','FIELDS':{
                  'reg_phy_rd_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_rd_dqs_slave_force is 1, use this tap/delay value for read DQS slave DLL, data slice 2'},       
                  'reg_phy_rd_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_rd_dqs_slave_ratio  for the read DQS slave DLL, 1 - use provided in reg_phy_rd_dqs_slave_delay, data slice 2'},       
                  'reg_phy_rd_dqs_slave_ratio':       {'r':( 0, 9),'d':0x40,'c':'Fraction of the clock cycle (256 = full period) for the read DQS slave DLL, data slice 2'}}},
    'phy_rd_dqs_cfg3':         {'OFFS': 0x14C,'DFLT':0x00000040,'RW':'RW','FIELDS':{
                  'reg_phy_rd_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_rd_dqs_slave_force is 1, use this tap/delay value for read DQS slave DLL, data slice 3'},       
                  'reg_phy_rd_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_rd_dqs_slave_ratio  for the read DQS slave DLL, 1 - use provided in reg_phy_rd_dqs_slave_delay, data slice 3'},       
                  'reg_phy_rd_dqs_slave_ratio':       {'r':( 0, 9),'d':0x40,'c':'Fraction of the clock cycle (256 = full period) for the read DQS slave DLL, data slice 3'}}},
#     u32 reserved4[1];              /* 0x150 */
    'phy_wr_dqs_cfg0':         {'OFFS': 0x154,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_wr_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 0'},       
                  'reg_phy_wr_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 0'},       
                  'reg_phy_wr_dqs_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 0. Program manual training ratio'}}},
    'phy_wr_dqs_cfg1':         {'OFFS': 0x158,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_wr_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 1'},       
                  'reg_phy_wr_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 1'},       
                  'reg_phy_wr_dqs_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 1. Program manual training ratio'}}},
    'phy_wr_dqs_cfg2':         {'OFFS': 0x15C,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_wr_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 2'},       
                  'reg_phy_wr_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 2'},       
                  'reg_phy_wr_dqs_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 2. Program manual training ratio'}}},
    'phy_wr_dqs_cfg3':         {'OFFS': 0x160,'DFLT':0x00000000,'RW':'RW','FIELDS':{
                  'reg_phy_wr_dqs_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 3'},       
                  'reg_phy_wr_dqs_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 3'},       
                  'reg_phy_wr_dqs_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 3. Program manual training ratio'}}},
#     u32 reserved5[1];              /* 0x164 */
    'phy_we_cfg0':             {'OFFS': 0x168,'DFLT':0x00000040,'RW':'RW','FIELDS':{
                  'reg_phy_fifo_we_in_delay':         {'r':(12,20),'d':0,'c':'If reg_phy_fifo_we_in_force is 1, use this tap/delay value for fifo_we_0 slave DLL, data slice 0'},       
                  'reg_phy_fifo_we_in_force':         {'r':(11,11),'d':0,'c':'0 - use reg_phy_fifo_we_slave_ratio for fifo_we_0 slave DLL, 1 - use provided in reg_phy_fifo_we_in_delay, data slice 0'},       
                  'reg_phy_fifo_we_slave_ratio':      {'r':( 0,10),'d':0x40,'c':'Fraction of the clock cycle (256 = full period) for fifo_we_0 slave DLL, data slice 0. Program manual training ratio'}}},
    'phy_we_cfg1':             {'OFFS': 0x16C,'DFLT':0x00000040,'RW':'RW','FIELDS':{
                  'reg_phy_fifo_we_in_delay':         {'r':(12,20),'d':0,'c':'If reg_phy_fifo_we_in_force is 1, use this tap/delay value for fifo_we_1 slave DLL, data slice 1'},       
                  'reg_phy_fifo_we_in_force':         {'r':(11,11),'d':0,'c':'0 - use reg_phy_fifo_we_slave_ratio for fifo_we_1 slave DLL, 1 - use provided in reg_phy_fifo_we_in_delay, data slice 1'},       
                  'reg_phy_fifo_we_slave_ratio':      {'r':( 0,10),'d':0x40,'c':'Fraction of the clock cycle (256 = full period) for fifo_we_0 slave DLL, data slice 1. Program manual training ratio'}}},
    'phy_we_cfg2':             {'OFFS': 0x170,'DFLT':0x00000040,'RW':'RW','FIELDS':{
                  'reg_phy_fifo_we_in_delay':         {'r':(12,20),'d':0,'c':'If reg_phy_fifo_we_in_force is 1, use this tap/delay value for fifo_we_2 slave DLL, data slice 2'},       
                  'reg_phy_fifo_we_in_force':         {'r':(11,11),'d':0,'c':'0 - use reg_phy_fifo_we_slave_ratio for fifo_we_2 slave DLL, 1 - use provided in reg_phy_fifo_we_in_delay, data slice 2'},       
                  'reg_phy_fifo_we_slave_ratio':      {'r':( 0,10),'d':0x40,'c':'Fraction of the clock cycle (256 = full period) for fifo_we_0 slave DLL, data slice 2. Program manual training ratio'}}},
    'phy_we_cfg3':             {'OFFS': 0x174,'DFLT':0x00000040,'RW':'RW','FIELDS':{
                  'reg_phy_fifo_we_in_delay':         {'r':(12,20),'d':0,'c':'If reg_phy_fifo_we_in_force is 1, use this tap/delay value for fifo_we_3 slave DLL, data slice 3'},       
                  'reg_phy_fifo_we_in_force':         {'r':(11,11),'d':0,'c':'0 - use reg_phy_fifo_we_slave_ratio for fifo_we_3 slave DLL, 1 - use provided in reg_phy_fifo_we_in_delay, data slice 3'},       
                  'reg_phy_fifo_we_slave_ratio':      {'r':( 0,10),'d':0x40,'c':'Fraction of the clock cycle (256 = full period) for fifo_we_0 slave DLL, data slice 3. Program manual training ratio'}}},
#     u32 reserved6[1];              /* 0x178 */
    'wr_data_slv0':            {'OFFS': 0x17C,'DFLT':0x00000080,'RW':'RW','FIELDS':{
                  'reg_phy_wr_data_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write data slave DLL, data slice 0'},       
                  'reg_phy_wr_data_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write data slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 0'},       
                  'reg_phy_wr_data_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write data slave DLL, data slice 0. Program manual training ratio'}}},
    'wr_data_slv1':            {'OFFS': 0x180,'DFLT':0x00000080,'RW':'RW','FIELDS':{
                  'reg_phy_wr_data_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write data slave DLL, data slice 1'},       
                  'reg_phy_wr_data_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write data slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 1'},       
                  'reg_phy_wr_data_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write data slave DLL, data slice 1. Program manual training ratio'}}},
    'wr_data_slv2':            {'OFFS': 0x184,'DFLT':0x00000080,'RW':'RW','FIELDS':{
                  'reg_phy_wr_data_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write data slave DLL, data slice 2'},       
                  'reg_phy_wr_data_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write data slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 2'},       
                  'reg_phy_wr_data_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write data slave DLL, data slice 2. Program manual training ratio'}}},
    'wr_data_slv3':            {'OFFS': 0x188,'DFLT':0x00000080,'RW':'RW','FIELDS':{
                  'reg_phy_wr_data_slave_delay':       {'r':(11,19),'d':0,'c':'If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write data slave DLL, data slice 3'},       
                  'reg_phy_wr_data_slave_force':       {'r':(10,10),'d':0,'c':'0 - use reg_phy_wr_dqs_slave_ratio  for the write data slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 3'},       
                  'reg_phy_wr_data_slave_ratio':       {'r':( 0, 9),'d':0,'c':'Fraction of the clock cycle (256 = full period) for the write data slave DLL, data slice 3. Program manual training ratio'}}},
#     u32 reserved7[1];              /* 0x18C*/
    'reg_64':                  {'OFFS': 0x190,'DFLT':0x10020000,'RW':'RW','COMMENTS':'Training control 2','FIELDS':{
                  'reserved1':                        {'r':(31,31),'d':0,   'c':'reserved'},      
                  'reg_phy_cmd_latency':              {'r':(30,30),'d':0,   'c':'1: Delay command to PHY by a FF'},      
                  'reg_phy_lpddr':                    {'r':(29,29),'d':0,   'c':'0: DDR2/DDR3, 1 - LPDDR2'},      
                  'reserved2':                        {'r':(28,28),'d':1,'   c':'reserved'},      
                  'reg_phy_ctrl_slave_delay':         {'r':(21,27),'d':0,'   c':'when reg_phy_rd_dqs_slave_force==1 this value (combined with bits 18:19 of reg_65) set address/command slave DLL'},      
                  'reg_phy_ctrl_slave_force':         {'r':(20,20),'d':0,'   c':'0:use reg_phy_ctrl_slave_ratio for addr/cmd slave DLL, 1 - overwrite with reg_phy_ctrl_slave_delay'},      
                  'reg_phy_ctrl_slave_ratio':         {'r':(10,19),'d':0x80,'c':'address/command delay in clock/256'},      
                  'reg_phy_sel_logic':                {'r':( 9, 9),'d':0,'c':'Read leveling algorithm select - 0:algorithm 1, 1: algorithm 2'},      
                  'reserved3':                        {'r':( 8, 8),'d':0,'c':'reserved'},      
                  'reg_phy_invert_clkout':            {'r':( 7, 7),'d':0,'c':'1 - invert clock polarity to DRAM'},      
                  'reserved4':                        {'r':( 5, 6),'d':0,'c':'reserved'},      
                  'reserved5':                        {'r':( 4, 4),'d':0,'c':'reserved'},      
                  'reserved6':                        {'r':( 3, 3),'d':0,'c':'reserved'},      
                  'reserved7':                        {'r':( 2, 2),'d':0,'c':'reserved'},      
                  'reg_phy_bl2':                      {'r':( 1, 1),'d':0,'c':'reserved'},      
                  'reserved8':                        {'r':( 0, 0),'d':0,'c':'reserved'}}},
    'reg_65':                  {'OFFS': 0x194,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Training control 3','FIELDS':{
                  'reg_phy_ctrl_slave_delay':         {'r':(18,19),'d':0,'c':'when reg_phy_rd_dqs_slave_force==1 this value (combined with bits 21:27 of reg_64) set address/command slave DLL'},      
                  'reg_phy_dis_calib_rst':            {'r':(17,17),'d':0,'c':'disable dll_claib from resetting Read Capture FIFO'},      
                  'reg_phy_use_rd_data_eye_level':    {'r':(16,16),'d':0,'c':'Read Data Eye training control - 0 use fixed register data, 1 use data eye leveling data'},      
                  'reg_phy_use_rd_dqs_gate_level':    {'r':(15,15),'d':0,'c':'Read DQS Gate training control: 0 - used fixed data, 1 - use calculated data'},      
                  'reg_phy_use_wr_level':             {'r':(14,14),'d':0,'c':'Write leveling control: 0 - used programmed register data, 1 - use calculated data'},      
                  'reg_phy_dll_lock_diff':            {'r':(10,13),'d':0,'c':'Maximal number of DLL taps before DLL deasserts lock'},      
                  'reg_phy_rd_rl_delay':              {'r':( 5, 9),'d':0,'c':''},      
                  'reg_phy_wr_rl_delay':              {'r':( 0, 4),'d':0,'c':''}}},
#     u32 reserved7[3];              /* 0x198 */
# The fifo_we_slave ratios for each slice(0 through 3) must be interpreted by software in the following way:
# Slice 0: fifo_we_ratio_slice_0[10:0] = {Reg_6A[9],Reg_69[18:9]}
# Slice1: fifo_we_ratio_slice_1[10:0] = {Reg_6B[10:9],Reg_6A[18:10]}
# Slice2: fifo_we_ratio_slice_2[10:0] = {Reg_6C[11:9],Reg_6B[18:11]}
# Slice3: fifo_we_ratio_slice_3[10:0] = {phy_reg_rdlvl_fifowein_ratio_slice3_msb,Reg_6C[18:12]}
    'reg_69':                  {'OFFS': 0x1A4,'DFLT':0x000F0000,'RW':'R','COMMENTS':'Training results for data slice 0','FIELDS':{
                  'phy_reg_status_fifo_w e_slave_dll_value': {'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
                  'phy_reg_rdlvl_fifowein_ratio':            {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
                  'reserved':                                {'r':( 0, 8),'d':0,    'm':'R','c':'reserved'}}},
    'reg_6a':                  {'OFFS': 0x1A8,'DFLT':0x000F0000,'RW':'R','FIELDS':{
                  'phy_reg_status_fifo_w e_slave_dll_value': {'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
                  'phy_reg_rdlvl_fifowein_ratio':            {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
                  'reserved':                                {'r':( 0, 8),'d':0,    'm':'R','c':'reserved'}}},
    'reg_6b':                  {'OFFS': 0x1AC,'DFLT':0x000F0000,'RW':'R','FIELDS':{ #may be different bits/default values
                  'phy_reg_status_fifo_w e_slave_dll_value': {'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
                  'phy_reg_rdlvl_fifowein_ratio':            {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
                  'reserved':                                {'r':( 0, 8),'d':0,    'm':'R','c':'reserved'}}},
#     u32 reserved8[1];              /* 0x1AC */
    'reg_6c':                  {'OFFS': 0x1B0,'DFLT':0x000F0000,'RW':'R','COMMENTS':'Training results for data slice 2','FIELDS':{
                  'phy_reg_status_fifo_we_slave_dll_value':{'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
                  'phy_reg_rdlvl_fifowein_ratio':          {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
                  'phy_reg_bist_err':                      {'r':( 0, 8),'d':0,    'm':'R','c':'Mismatch error from BIST checker, 1 bit per data slice'}}},
    'reg_6d':                  {'OFFS': 0x1B4,'DFLT':0x000F0000,'RW':'R','FIELDS':{
                  'phy_reg_status_fifo_we_slave_dll_value':{'r':(20,28),'d':0,    'm':'R','c':'Delay of FIFO WE slave DLL'},      
                  'phy_reg_rdlvl_fifowein_ratio':          {'r':( 9,19),'d':0x780,'m':'R','c':'Ratio by Read Gate training FSM'},      
                  'phy_reg_bist_err':                      {'r':( 0, 8),'d':0,    'm':'R','c':'Mismatch error from BIST checker, 1 bit per data slice'}}},
    'reg_6e':                  {'OFFS': 0x1B8,'RW':'R','COMMENTS':'Training results for data slice 0','FIELDS':{
                  'phy_reg_status_fifo_we_slave_dll_value':{'r':(20,29),'d':0, 'm':'R','c':'Ratio generated by Read Data Eye training'},      
                  'phy_reg_rdlvl_fifowein_ratio':          {'r':(10,19),'d':0, 'm':'R','c':'Ratio generated by Write Leveling for write data'},      
                  'phy_reg_bist_err':                      {'r':( 0, 9),'d':0, 'm':'R','c':'Ratio generated by Write Leveling for write DQS'}}},
    'reg_6f':                  {'OFFS': 0x1BC,'RW':'R','COMMENTS':'Training results for data slice 1','FIELDS':{
                  'phy_reg_status_fifo_we_slave_dll_value':{'r':(20,29),'d':0, 'm':'R','c':'Ratio generated by Read Data Eye training'},      
                  'phy_reg_rdlvl_fifowein_ratio':          {'r':(10,19),'d':0, 'm':'R','c':'Ratio generated by Write Leveling for write data'},      
                  'phy_reg_bist_err':                      {'r':( 0, 9),'d':0, 'm':'R','c':'Ratio generated by Write Leveling for write DQS'}}},
    'reg_70':                  {'OFFS': 0x1C0,'RW':'R','COMMENTS':'Training results for data slice 2','FIELDS':{
                  'phy_reg_status_fifo_we_slave_dll_value':{'r':(20,29),'d':0, 'm':'R','c':'Ratio generated by Read Data Eye training'},      
                  'phy_reg_rdlvl_fifowein_ratio':          {'r':(10,19),'d':0, 'm':'R','c':'Ratio generated by Write Leveling for write data'},      
                  'phy_reg_bist_err':                      {'r':( 0, 9),'d':0, 'm':'R','c':'Ratio generated by Write Leveling for write DQS'}}},
    'reg_71':                  {'OFFS': 0x1C4,'RW':'R','COMMENTS':'Training results for data slice 3','FIELDS':{
                  'phy_reg_status_fifo_we_slave_dll_value':{'r':(20,29),'d':0, 'm':'R','c':'Ratio generated by Read Data Eye training'},      
                  'phy_reg_rdlvl_fifowein_ratio':          {'r':(10,19),'d':0, 'm':'R','c':'Ratio generated by Write Leveling for write data'},      
                  'phy_reg_bist_err':                      {'r':( 0, 9),'d':0, 'm':'R','c':'Ratio generated by Write Leveling for write DQS'}}},
#     u32 reserved9[1];              /* 0x1C8 */
    'phy_dll_sts0':            {'OFFS': 0x1CC,'DFLT':0x00000000,'RW':'R','COMMENTS':'Slave DLL results for data slice 0','FIELDS':{
                  'phy_reg_status_wr_dqs_slave_dll_value':  {'r':(18,26),'d':0, 'm':'R','c':'Delay for write DQS slave DLL'},      
                  'phy_reg_status_wr_dat a_slave_dll_value':{'r':( 9,17),'d':0, 'm':'R','c':'Delay for write data slave DLL'},      
                  'phy_reg_status_rd_dqs_slave_dll_value':  {'r':( 0, 8),'d':0, 'm':'R','c':'Delay for read data slave DLL'}}},
    'phy_dll_sts1':            {'OFFS': 0x1D0,'DFLT':0x00000000,'RW':'R','COMMENTS':'Slave DLL results for data slice 1','FIELDS':{
                  'phy_reg_status_wr_dqs_slave_dll_value':  {'r':(18,26),'d':0, 'm':'R','c':'Delay for write DQS slave DLL'},      
                  'phy_reg_status_wr_dat a_slave_dll_value':{'r':( 9,17),'d':0, 'm':'R','c':'Delay for write data slave DLL'},      
                  'phy_reg_status_rd_dqs_slave_dll_value':  {'r':( 0, 8),'d':0, 'm':'R','c':'Delay for read data slave DLL'}}},
    'phy_dll_sts2':            {'OFFS': 0x1D4,'DFLT':0x00000000,'RW':'R','COMMENTS':'Slave DLL results for data slice 2','FIELDS':{
                  'phy_reg_status_wr_dqs_slave_dll_value':  {'r':(18,26),'d':0, 'm':'R','c':'Delay for write DQS slave DLL'},      
                  'phy_reg_status_wr_dat a_slave_dll_value':{'r':( 9,17),'d':0, 'm':'R','c':'Delay for write data slave DLL'},      
                  'phy_reg_status_rd_dqs_slave_dll_value':  {'r':( 0, 8),'d':0, 'm':'R','c':'Delay for read data slave DLL'}}},
    'phy_dll_sts3':            {'OFFS': 0x1D8,'DFLT':0x00000000,'RW':'R','COMMENTS':'Slave DLL results for data slice 3','FIELDS':{
                  'phy_reg_status_wr_dqs_slave_dll_value':  {'r':(18,26),'d':0, 'm':'R','c':'Delay for write DQS slave DLL'},      
                  'phy_reg_status_wr_dat a_slave_dll_value':{'r':( 9,17),'d':0, 'm':'R','c':'Delay for write data slave DLL'},      
                  'phy_reg_status_rd_dqs_slave_dll_value':  {'r':( 0, 8),'d':0, 'm':'R','c':'Delay for read data slave DLL'}}},
#     u32 reserved10[1];             /* 0x1DC */
    'dll_lock_sts':            {'OFFS': 0x1E0,'DFLT':0x00000000,'RW':'R','COMMENTS':'DLL lock status','FIELDS':{
                  'phy_reg_rdlvl_fifowein_ratio_slice3_msb':{'r':(20,23),'d':0, 'm':'R','c':'4 msb-s of slice 3 ratio generated by Read Gate Training FSM'},      
                  'phy_reg_status_dll_slave_value_1':       {'r':(11,19),'d':0, 'm':'R','c':'8:2 - coarse, 1:0 - Fine for all slave DLLs (for master DLL 1)'},      
                  'phy_reg_status_dll_slave_value_0':       {'r':( 2,10),'d':0, 'm':'R','c':'8:2 - coarse, 1:0 - Fine for all slave DLLs (for master DLL 0)'},      
                  'phy_reg_status_dll_lock_1':              {'r':( 1, 1),'d':0, 'm':'R','c':'DLL 1 lock'},      
                  'phy_reg_status_dll_lock_0':              {'r':( 0, 0),'d':0, 'm':'R','c':'DLL 0 lock'}}},
    'phy_ctrl_sts':            {'OFFS': 0x1E4,'RW':'R','COMMENTS':'PHY control status','FIELDS':{
                  'phy_reg_status_phy_ctrl_of_in_lock_state':{'r':(28,29),'d':0, 'm':'R','c':'Master DLL Output Filter: bit29 -  coarse delay line locked, 28 - fine delay line locked'},      
                  'phy_reg_status_phy_ctrl_dll_slave_value': {'r':(20,27),'d':0, 'm':'R','c':'PHY_CTRL Slave DLL: 20:21 - fine, 22:27 - coarse'},      
                  'phy_reg_status_phy_ctrl_dll_lock':        {'r':(19,19),'d':0, 'm':'R','c':'PHY control Master DLL locked'},      
                  'phy_reg_status_of_out_delay_value':       {'r':(10,18),       'm':'R','c':'Master DLL output filter output: 10:11 - fine, 12:18 - coarse'},      
                  'phy_reg_status_of_in_delay_value':        {'r':( 0, 9),       'm':'R','c':'Master DLL output filter input: 10:11 - fine, 12:18 - coarse'}}},
    'phy_ctrl_sts_reg2':       {'OFFS': 0x1E8,'DFLT':0x00000000,'RW':'R','COMMENTS':'PHY control status 2','FIELDS':{
                  'phy_reg_status_phy_ctrl_slave_dll_value':  {'r':(18,26),'d':0, 'm':'R','c':'Read DQS slave DLL input'},      
                  'reserved':                                 {'r':( 9,17),'d':0, 'm':'R','c':'reserved'},      
                  'phy_reg_status_phy_ctrl_of_in_delay_value':{'r':( 0, 8),'d':0, 'm':'R','c':'Values applied to Master DLL Output filter: 0:1 - fine, 2:8 - coarse'}}},
#     u32 reserved11[5];             /* 0x1EC */
    'axi_id':                  {'OFFS': 0x200,'DFLT':0x00153042,'RW':'R','COMMENTS':'Id and Revision','FIELDS':{
                  'reg_arb_rev_num':                       {'r':(20,25),'d':0x01, 'm':'R','c':'Revision number'},      
                  'reg_arb_prov_num':                      {'r':(12,19),'d':0x53, 'm':'R','c':'Provision number'},      
                  'reg_arb_part_num':                      {'r':( 0,11),'d':0x42, 'm':'R','c':'Part number'}}},
    'page_mask':               {'OFFS': 0x204,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Arbiter Page Mask','FIELDS':{
                  'reg_arb_page_addr_mask':                {'r':( 0,31),'d':0x0,'c':'Arbiter page hit/miss: 0 - column address, 1 - row/bank address (applies to 64-bit address, not byte addr) '}}},
    'axi_priority_wr_port0':   {'OFFS': 0x208,'DFLT':0x000803FF,'RW':'M','COMMENTS':'AXI priority control for write port 0','FIELDS':{
                  'reserved1':                             {'r':(19,19),'d':0x1,          'c':'reserved'},      
                  'reg_arb_dis_page_match_wr_portn':       {'r':(18,18),'d':0,            'c':'Disable page match feature'},      
                  'reg_arb_disable_urgent_wr_portn':       {'r':(17,17),'d':0,            'c':'Disable urgent for this Write Port'},      
                  'reg_arb_disable_aging_wr_portn':        {'r':(16,16),'d':0,            'c':'Disable aging for this Write Port'},      
                  'reserved2':                             {'r':(10,15),'d':0,    'm':'R','c':'reserved'},      
                  'reg_arb_pri_wr_portn':                  {'r':( 0, 9),'d':0x3FF,        'c':'Priority for this write port, >=4, lower value - higher priority'}}},
    'axi_priority_wr_port1':   {'OFFS': 0x20C,'DFLT':0x000803FF,'RW':'M','COMMENTS':'AXI priority control for write port 1','FIELDS':{
                  'reserved1':                             {'r':(19,19),'d':0x1,          'c':'reserved'},      
                  'reg_arb_dis_page_match_wr_portn':       {'r':(18,18),'d':0,            'c':'Disable page match feature'},      
                  'reg_arb_disable_urgent_wr_portn':       {'r':(17,17),'d':0,            'c':'Disable urgent for this Write Port'},      
                  'reg_arb_disable_aging_wr_portn':        {'r':(16,16),'d':0,            'c':'Disable aging for this Write Port'},      
                  'reserved2':                             {'r':(10,15),'d':0,    'm':'R','c':'reserved'},      
                  'reg_arb_pri_wr_portn':                  {'r':( 0, 9),'d':0x3FF,        'c':'Priority for this write port, >=4, lower value - higher priority'}}},
    'axi_priority_wr_port2':   {'OFFS': 0x210,'DFLT':0x000803FF,'RW':'M','COMMENTS':'AXI priority control for write port 2','FIELDS':{
                  'reserved1':                             {'r':(19,19),'d':0x1,          'c':'reserved'},      
                  'reg_arb_dis_page_match_wr_portn':       {'r':(18,18),'d':0,            'c':'Disable page match feature'},      
                  'reg_arb_disable_urgent_wr_portn':       {'r':(17,17),'d':0,            'c':'Disable urgent for this Write Port'},      
                  'reg_arb_disable_aging_wr_portn':        {'r':(16,16),'d':0,            'c':'Disable aging for this Write Port'},      
                  'reserved2':                             {'r':(10,15),'d':0,    'm':'R','c':'reserved'},      
                  'reg_arb_pri_wr_portn':                  {'r':( 0, 9),'d':0x3FF,        'c':'Priority for this write port, >=4, lower value - higher priority'}}},
    'axi_priority_wr_port3':   {'OFFS': 0x214,'DFLT':0x000803FF,'RW':'M','COMMENTS':'AXI priority control for write port 3','FIELDS':{
                  'reserved1':                             {'r':(19,19),'d':0x1,          'c':'reserved'},      
                  'reg_arb_dis_page_match_wr_portn':       {'r':(18,18),'d':0,            'c':'Disable page match feature'},      
                  'reg_arb_disable_urgent_wr_portn':       {'r':(17,17),'d':0,            'c':'Disable urgent for this Write Port'},      
                  'reg_arb_disable_aging_wr_portn':        {'r':(16,16),'d':0,            'c':'Disable aging for this Write Port'},      
                  'reserved2':                             {'r':(10,15),'d':0,    'm':'R','c':'reserved'},      
                  'reg_arb_pri_wr_portn':                  {'r':( 0, 9),'d':0x3FF,        'c':'Priority for this write port, >=4, lower value - higher priority'}}},
    'axi_priority_rd_port0':   {'OFFS': 0x218,'DFLT':0x000003FF,'RW':'M','COMMENTS':'AXI priority control for read port 0','FIELDS':{
                  'reg_arb_set_hpr_rd_portn':              {'r':(19,19),'d':0x1,          'c':'Enable reads to be HPR for this port'},      
                  'reg_arb_dis_page_match_rd_portn':       {'r':(18,18),'d':0,            'c':'Disable page match feature'},      
                  'reg_arb_disable_urgent_rd_portn':       {'r':(17,17),'d':0,            'c':'Disable urgent for this Read Port'},      
                  'reg_arb_disable_aging_rd_portn':        {'r':(16,16),'d':0,            'c':'Disable aging for this Read Port'},      
                  'reserved1':                             {'r':(10,15),'d':0,    'm':'R','c':'reserved'},      
                  'reg_arb_pri_rd_portn':                  {'r':( 0, 9),'d':0x3FF,        'c':'Priority for this Read port, lower value - higher priority'}}},
    'axi_priority_rd_port1':   {'OFFS': 0x21C,'DFLT':0x000003FF,'RW':'M','COMMENTS':'AXI priority control for read port 1','FIELDS':{
                  'reg_arb_set_hpr_rd_portn':              {'r':(19,19),'d':0x1,          'c':'Enable reads to be HPR for this port'},      
                  'reg_arb_dis_page_match_rd_portn':       {'r':(18,18),'d':0,            'c':'Disable page match feature'},      
                  'reg_arb_disable_urgent_rd_portn':       {'r':(17,17),'d':0,            'c':'Disable urgent for this Read Port'},      
                  'reg_arb_disable_aging_rd_portn':        {'r':(16,16),'d':0,            'c':'Disable aging for this Read Port'},      
                  'reserved1':                             {'r':(10,15),'d':0,    'm':'R','c':'reserved'},      
                  'reg_arb_pri_rd_portn':                  {'r':( 0, 9),'d':0x3FF,        'c':'Priority for this Read port, lower value - higher priority'}}},
    'axi_priority_rd_port2':   {'OFFS': 0x220,'DFLT':0x000003FF,'RW':'M','COMMENTS':'AXI priority control for read port 2','FIELDS':{
                  'reg_arb_set_hpr_rd_portn':              {'r':(19,19),'d':0x1,          'c':'Enable reads to be HPR for this port'},      
                  'reg_arb_dis_page_match_rd_portn':       {'r':(18,18),'d':0,            'c':'Disable page match feature'},      
                  'reg_arb_disable_urgent_rd_portn':       {'r':(17,17),'d':0,            'c':'Disable urgent for this Read Port'},      
                  'reg_arb_disable_aging_rd_portn':        {'r':(16,16),'d':0,            'c':'Disable aging for this Read Port'},      
                  'reserved1':                             {'r':(10,15),'d':0,    'm':'R','c':'reserved'},      
                  'reg_arb_pri_rd_portn':                  {'r':( 0, 9),'d':0x3FF,        'c':'Priority for this Read port, lower value - higher priority'}}},
    'axi_priority_rd_port3':   {'OFFS': 0x224,'DFLT':0x000003FF,'RW':'M','COMMENTS':'AXI priority control for read port 3','FIELDS':{
                  'reg_arb_set_hpr_rd_portn':              {'r':(19,19),'d':0x1,          'c':'Enable reads to be HPR for this port'},      
                  'reg_arb_dis_page_match_rd_portn':       {'r':(18,18),'d':0,            'c':'Disable page match feature'},      
                  'reg_arb_disable_urgent_rd_portn':       {'r':(17,17),'d':0,            'c':'Disable urgent for this Read Port'},      
                  'reg_arb_disable_aging_rd_portn':        {'r':(16,16),'d':0,            'c':'Disable aging for this Read Port'},      
                  'reserved1':                             {'r':(10,15),'d':0,    'm':'R','c':'reserved'},      
                  'reg_arb_pri_rd_portn':                  {'r':( 0, 9),'d':0x3FF,        'c':'Priority for this Read port, lower value - higher priority'}}},
#     u32 reserved12[0x1A];          /* 0x228 */
    'trusted_mem_cfg':         {'OFFS': 0x290,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Trusted Memory Configuration (obsolete)','FIELDS':{
                  'reg_decprot':                           {'r':( 0,31),'d':0x0,'c':'Each bit for 64MB section, 1 - secure, 0 - non-secure. Not used anymore'}}},
    'excl_access_cfg0':        {'OFFS': 0x294,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Exclusive access configuration for port 0','FIELDS':{
                  'reg_excl_acc_id1_port':                 {'r':( 9,17),'d':0,    'c':'reserved'},      
                  'reg_excl_acc_id0_port':                 {'r':( 0, 8),'d':0,    'c':'reserved'}}},
    'excl_access_cfg1':        {'OFFS': 0x298,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Exclusive access configuration for port 1','FIELDS':{
                  'reg_excl_acc_id1_port':                 {'r':( 9,17),'d':0,    'c':'reserved'},      
                  'reg_excl_acc_id0_port':                 {'r':( 0, 8),'d':0,    'c':'reserved'}}},
    'excl_access_cfg2':        {'OFFS': 0x29C,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Exclusive access configuration for port 2','FIELDS':{
                  'reg_excl_acc_id1_port':                 {'r':( 9,17),'d':0,    'c':'reserved'},      
                  'reg_excl_acc_id0_port':                 {'r':( 0, 8),'d':0,    'c':'reserved'}}},
    'excl_access_cfg3':        {'OFFS': 0x2A0,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Exclusive access configuration for port 3','FIELDS':{
                  'reg_excl_acc_id1_port':                 {'r':( 9,17),'d':0,    'c':'reserved'},      
                  'reg_excl_acc_id0_port':                 {'r':( 0, 8),'d':0,    'c':'reserved'}}},
    'mode_reg_read':           {'OFFS': 0x2A4,'DFLT':0x00000000,'RW':'R','COMMENTS':'Mode register read data','FIELDS':{
                  'ddrc_reg_rd_mrr_data':                  {'r':( 0,31),'d':0x0,  'M':'R','c':'LPDDR2 only: Mode register read data, valid when ddrc_co_rd_mrr_data_valid is set'}}},
    'lpddr_ctrl0':             {'OFFS': 0x2A8,'DFLT':0x00000000,'RW':'RW','COMMENTS':'LPDDR2 control register 0','FIELDS':{
                  'reg_ddrc_mr4_margin':                   {'r':( 4,11),'d':0,    'c':'unused'},      
                  'reserved1':                             {'r':( 3, 3),'d':0,    'c':'reserved'},      
                  'reg_ddrc_derate_enable':                {'r':( 2, 2),'d':0,    'c':'Timing parameter derating ENABLED using MR4 read data'},      
                  'reserved2':                             {'r':( 1, 1),'d':0,    'c':'reserved'},      
                  'reg_ddrc_lpddr2':                       {'r':( 0, 0),'d':0,    'c':'0 - DDR2/DDR3 in use, 1 - LPDDR2 in use'}}},
    'lpddr_ctrl1':             {'OFFS': 0x2AC,'DFLT':0x00000000,'RW':'RW','COMMENTS':'LPDDR2 control register 1','FIELDS':{
                  'reg_ddrc_mr4_read_int erval':           {'r':(31, 0),'d':0,    'c':'Interval between two MR4 reads (for derating timing)'}}},
    'lpddr_ctrl2':             {'OFFS': 0x2B0,'DFLT':0x003C0015,'RW':'RW','COMMENTS':'LPDDR2 control register 2','FIELDS':{
                  'reg_ddrc_t_mrw':                        {'r':(12,21),'d':0x3C0,'c':'Wait for MR writes, typically required 5???'},      
                  'reg_ddrc_idle_after_reset_x32':         {'r':( 4,11),'d':0x1,  'c':'Idle time after reset command, tINIT4 (in clockx32)'},      
                  'reg_ddrc_min_stable_clock_x1':          {'r':( 0, 3),'d':0x5,  'c':'time to wait after first CKE high, tINIT2 in clock cycles. Typically required 5 (tCK)'}}},
    'lpddr_ctrl3':             {'OFFS': 0x2B4,'DFLT':0x00000601,'RW':'RW','COMMENTS':'LPDDR2 control register 3','FIELDS':{
                  'reg_ddrc_dev_zqinit_x32':               {'r':( 8,17),'d':0x1,  'c':'tZQINIT - ZQ initial calibration (in clockx32). LPDDR@ typically require 1 microsecond'},      
                  'reg_ddrc_max_auto_init_x1024':          {'r':( 0, 7),'d':0x1,  'c':'tINIT5 - maximal duration of autoinitialization (in clockx1024). Typical 10 microseconds'}}}
}
