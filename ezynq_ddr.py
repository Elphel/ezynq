#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Elphel.inc.
# configuration of the DDR-related registers
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
import math
import ezynq_ddrc_defs
import ezynq_registers
import ezynq_ddrcfg_defs
import ezynq_feature_config
import ezynq_ddriob_def
class EzynqDDR:
    def __init__(self,regs_masked,permit_undefined_bits=False,force=False,warn=False):
        self.DDRC_DEFS=  ezynq_ddrc_defs.DDRC_DEFS
        self.DDRIOB_DEFS=ezynq_ddriob_def.DDRIOB_DEFS
        self.DDR_CFG_DEFS=ezynq_ddrcfg_defs.DDR_CFG_DEFS
        self.ddrc_register_sets= {'PRE': ezynq_registers.EzynqRegisters(self.DDRC_DEFS,0,regs_masked,permit_undefined_bits), # all now start from the same registers
                                  'MAIN':ezynq_registers.EzynqRegisters(self.DDRC_DEFS,0,regs_masked,permit_undefined_bits),
                                  'POST':ezynq_registers.EzynqRegisters(self.DDRC_DEFS,0,regs_masked,permit_undefined_bits)}
        self.ddriob_register_sets= {'PRE': ezynq_registers.EzynqRegisters(self.DDRIOB_DEFS,0,regs_masked,permit_undefined_bits), # all now start from the same registers
                                    'MAIN':ezynq_registers.EzynqRegisters(self.DDRIOB_DEFS,0,regs_masked,permit_undefined_bits),
                                    'POST':ezynq_registers.EzynqRegisters(self.DDRIOB_DEFS,0,regs_masked,permit_undefined_bits)}
#        self.set_names=('PRE','MAIN','POST')
        self.set_ddrc_attribs=(
                          {'NAME':'PRE','POSTFIX':'_PRE','PREFIX':'CONFIG_EZYNQ_DDR_SETREG_','TITLE':"DDR Controller Register Pre-Set"},
                          {'NAME':'MAIN','POSTFIX':'','PREFIX':'CONFIG_EZYNQ_DDR_SETREG_','TITLE':"DDR Controller Register Set"},
                          {'NAME':'POST','POSTFIX':'_POST','PREFIX':'CONFIG_EZYNQ_DDR_SETREG_','TITLE':"DDR Controller Register Post-Set"})
        self.set_ddiob_attribs=(
                          {'NAME':'PRE','POSTFIX':'_PRE','PREFIX':'CONFIG_EZYNQ_DDRIOB_SETREG_','TITLE':"DDR I/O Buffer Register Pre-Set"},
                          {'NAME':'MAIN','POSTFIX':'','PREFIX':'CONFIG_EZYNQ_DDRIOB_SETREG_','TITLE':"DDR I/O Buffer Register Set"},
                          {'NAME':'POST','POSTFIX':'_POST','PREFIX':'CONFIG_EZYNQ_DDRIOB_SETREG_','TITLE':"DDR I/O Buffer Register Post-Set"})
        self.postfixes=[attrib['POSTFIX'] for attrib in self.set_ddrc_attribs]
        self.features=ezynq_feature_config.EzynqFeatures(self.DDR_CFG_DEFS,0) #DDR_CFG_DEFS
    def parse_parameters(self,raw_configs):
        self.features.parse_features(raw_configs)
    def check_missing_features(self):
        self.features.check_missing_features()
    def html_list_features(self,html_file):
        
        html_file.write('<h2>DDR memory configuration parameters</h2>\n')
        self.features.html_list_features(html_file)
    
#    def ddr_init_memory(self,current_reg_sets,force=False,warn=False,html_file, show_bit_fields=True, show_comments=True,filter_fields=True): # will program to sequence 'MAIN'

    def get_new_register_sets(self):
#    def get_register_sets(self, sort_addr=True,apply_new=True):
        return self.ddrc_register_sets['MAIN'].get_register_sets(True,True)
   
#        regs1=self.ddriob_register_sets['MAIN'].get_register_sets(True,True)
#        regs2=self.ddrc_register_sets['MAIN'].get_register_sets(True,True)
#        return regs1+regs2
    
    def ddr_init_memory(self,current_reg_sets,force=False,warn=False): # will program to sequence 'MAIN'
#        print 'ddr_init_memory, len(current_reg_sets)=',len(current_reg_sets),'\n'
        if not self.features.get_par_value('ENABLE'):
            print 'DDR configuration is disabled'
            # do some stuff (write regs, output)
            return
        ddriob_register_set=self.ddriob_register_sets['MAIN']
        ddrc_register_set=  self.ddrc_register_sets['MAIN']
        ddriob_register_set.set_initial_state(current_reg_sets, True)# start from the current registers state
        self.ddr_init_ddriob(force,warn) # will program to sequence 'MAIN'
        regs1=ddriob_register_set.get_register_sets(True,True)
        ddrc_register_set.set_initial_state(regs1, True)# add
        self.ddr_init_ddrc(force,warn) # will program to sequence 'MAIN'
        return ddrc_register_set.get_register_sets(True,True)
        
#        ddrc_register_set=  self.ddrc_register_sets['MAIN']


#TODO make some of (possibly) derived, leave '_T_' for ns only!
# CONFIG_EZYNQ_DDR_FREQ_MHZ = 533.333333 *
# CONFIG_EZYNQ_DDR_CL = 7  *
# CONFIG_EZYNQ_DDR_CWL = 6  *
# CONFIG_EZYNQ_DDR_RCD = 7 (was CONFIG_EZYNQ_DDR_T_RCD = 7) *
# CONFIG_EZYNQ_DDR_RP = 7 (was CONFIG_EZYNQ_DDR_T_RP = 7) *
# CONFIG_EZYNQ_DDR_T_RC = 48.75 *
# CONFIG_EZYNQ_DDR_T_RAS_MIN = 35.0 *
# CONFIG_EZYNQ_DDR_T_RFC = 350.0
# CONFIG_EZYNQ_DDR_T_FAW = 40.0 *
# CONFIG_EZYNQ_DDR_AL = 0 *
# CONFIG_EZYNQ_DDR_BANK_ADDR_COUNT = 3 *
# CONFIG_EZYNQ_DDR_ROW_ADDR_COUNT = 15 *
# CONFIG_EZYNQ_DDR_COL_ADDR_COUNT = 10 *

# CONFIG_EZYNQ_DDR_ENABLE = 1          *
# CONFIG_EZYNQ_DDR_MEMORY_TYPE = DDR3  *
# CONFIG_EZYNQ_DDR_ECC = Disabled      *
# CONFIG_EZYNQ_DDR_BUS_WIDTH = 32      *
# CONFIG_EZYNQ_DDR_BL = 8              *   
# CONFIG_EZYNQ_DDR_HIGH_TEMP = Normal  *
# CONFIG_EZYNQ_DDR_PARTNO = MT41K256M16RE-125 *
# CONFIG_EZYNQ_DDR_DRAM_WIDTH = 16     *
# CONFIG_EZYNQ_DDR_SPEED_BIN = DDR3_1066F *
# CONFIG_EZYNQ_DDR_TRAIN_WRITE_LEVEL = 0
# CONFIG_EZYNQ_DDR_TRAIN_READ_GATE = 0
# CONFIG_EZYNQ_DDR_TRAIN_DATA_EYE = 0
# CONFIG_EZYNQ_DDR_CLOCK_STOP_EN = 0
# CONFIG_EZYNQ_DDR_USE_INTERNAL_VREF = 0

    def ddr_init_ddrc(self,force=False,warn=False): # will program to sequence 'MAIN'
        ddrc_register_set=self.ddrc_register_sets['MAIN']
        is_LPDDR2=   (self.features.get_par_value('MEMORY_TYPE')=='LPDDR2')
        is_DDR3L=    (self.features.get_par_value('MEMORY_TYPE')=='DDR3L')
        is_DDR3_15=  (self.features.get_par_value('MEMORY_TYPE')=='DDR3')
        is_DDR3=     is_DDR3_15 or is_DDR3L
        is_DDR2=     (self.features.get_par_value('MEMORY_TYPE')=='DDR2')
#       is_32=       (self.features.get_par_value('BUS_WIDTH') > 16)
#        is_int_vref=  self.features.get_par_value('INTERNAL_VREF')
        tCK=1000.0/self.features.get_par_value('FREQ_MHZ')
        tREFI=       1000*self.features.get_par_value('T_REFI_US')/(1,2)[self.features.get_par_value('HIGH_TEMP')] # ns
        tWR=         self.features.get_par_value('T_WR')
#lock ddr
        ddrc_register_set.set_word('ddrc_ctrl',0x80,force) # active low soft reset
#two rank, values  0x1081, 0x81081, 0x81081 (added reg_ddrc_wr_odt_block=1)
        tREFI_c32=   int(tREFI/tCK/32)              
        ddrc_register_set.set_bitfields('two_rank_cfg',(('reg_ddrc_wr_odt_block',0),             # shown as 1/do not modify, but actual set value==0
                                                        ('reg_ddrc_addrmap_cs_bit0',0),
                                                        ('reg_ddrc_t_rfc_nom_x32',tREFI_c32),
                                                        ('reg_ddrc_active_ranks',1)),force,warn) # *** not documented 
#reg HPR, values 0x3c0780f - all 3 times, DEFAULT
        ddrc_register_set.set_bitfields('hpr_reg',(('reg_ddrc_hpr_xact_run_length',     0xf),
                                                   ('reg_ddrc_hpr_max_starve_x32',      0xf),
                                                   ('reg_ddrc_hpr_min_non_critical_x32',0xf)),force,warn) 
#reg LPR, values 0x2001001 - all 3 times, DEFAULT
        ddrc_register_set.set_bitfields('lpr_reg',(('reg_ddrc_lpr_xact_run_length',     0x8),
                                                   ('reg_ddrc_lpr_max_starve_x32',      0x2),
                                                   ('reg_ddrc_lpr_min_non_critical_x32',0x1)),force,warn) 
#reg WR_REG, values 0x14001 - all 3 times, DEFAULT
        ddrc_register_set.set_bitfields('wr_reg',(('reg_ddrc_w_max_starve_x32',      0x2), # opposite sequence from HPR,LPR
                                                  ('reg_ddrc_w_xact_run_length',     0x8),
                                                  ('reg_ddrc_w_min_non_critical_x32',0x1)),force,warn) 
#reg DRAM_param_reg0, values 0x4281a all 3 times
        tXSx1=512 # clock cycles
        tXSx32=tXSx1/32
        tRFCx1=int(math.ceil(self.features.get_par_value('T_RFC')/tCK))
        tRCx1= int(math.ceil(self.features.get_par_value('T_RC')/tCK))
        ddrc_register_set.set_bitfields('dram_param_reg0',(('reg_ddrc_post_selfref_gap_x32',tXSx32), # Default - OK, Micron tXSDLL=tDLLK=512 /32
                                                           ('reg_ddrc_t_rfc_min',           tRFCx1),
                                                           ('reg_ddrc_t_rc',                tRCx1)),force,warn)
# reg DRAM_param_reg1, 0x44e458d2
        tCKEx1=4 # good default
        tRAS_MINx1= int(math.ceil(self.features.get_par_value('T_RAS_MIN')/tCK))
        tRAS_MAX=9*tREFI # for Micron
        tRAS_MAX_x1024=int(tRAS_MAX/tCK/1024)
        tFAWx1=int(math.ceil(self.features.get_par_value('T_FAW')/tCK))
        inactiveToPDx32=6 # cycles 'Power down after this many clocks of NOP/DESELECT (if enabled in mcr). Make configurable?
        tWRx1=int(math.ceil(tWR/tCK))
        WL=self.features.get_par_value('CWL')
        BL=self.features.get_par_value('BL')
        wr2pre=WL+BL/2+tWRx1
        if is_LPDDR2:
            wr2pre+=1
        ddrc_register_set.set_bitfields('dram_param_reg1',(('reg_ddrc_t_cke',           tCKEx1), # Default - OK, Micron tXSDLL=tDLLK=512 /32
                                                           ('reg_ddrc_t_ras_min',       tRAS_MINx1),
                                                           ('reg_ddrc_t_ras_max',       tRAS_MAX_x1024),
                                                           ('reg_ddrc_t_faw',           tFAWx1),
                                                           ('reg_ddrc_powerdown_to_x32',inactiveToPDx32),
                                                           ('reg_ddrc_wr2pre',          wr2pre)),force,warn)
# reg DRAM_param_reg2, 0x720238e5
        AL=       self.features.get_par_value('AL')
        tRCDx1=   max(self.features.get_par_value('RCD') - AL,1)
        tRTPx1=max(self.features.get_par_value('RTP'), int(math.ceil(self.features.get_par_value('T_RTP')/tCK))) # tRTPx1=   4 # good default
        if is_DDR2:
            RD2PRE=AL+BL/2+max(tRTPx1,2)-2
        elif is_DDR3:
            RD2PRE=AL+max(tRTPx1,4)    
        elif is_LPDDR2:
            RD2PRE=BL/2+tRTPx1-1    
        padPD=0 # ???
        XP=     self.features.get_par_value('XP') # 4
        tWTRx1=max(self.features.get_par_value('WTR'), int(math.ceil(self.features.get_par_value('T_WTR')/tCK))) # tWTRx1=   4 # good default
        if is_DDR2 or is_DDR3:
            WR2RD=WL+tWTRx1+BL/2
        elif is_LPDDR2:
            WR2RD=WL+tWTRx1+BL/2+1
        CL= self.features.get_par_value('CL')
        RL= CL+AL
        if is_DDR2 or is_DDR3:
            RD2WR=RL+BL/2+2-WL
        elif is_LPDDR2:
            RD2WR=RL+BL/2+int(math.ceil(self.features.get_par_value('T_DQSCK_MAX')/tCK))+1-WL
        
        if is_DDR2 or is_DDR3:
            write_latency=WL-1
        elif is_LPDDR2:
            write_latency=WL
        
        if is_LPDDR2:
            if WL<1:
                raise Exception('Minimal Write Latency supported for LPDDR2 is 1, while CONFIG_EZYNQ_DDR_CWL='+str(WL))
        else:
            if WL<3:
                raise Exception('Minimal Write Latency supported for DDR2/DDR3 is 3, while CONFIG_EZYNQ_DDR_CWL='+str(WL))
        ddrc_register_set.set_bitfields('dram_param_reg2',(('reg_ddrc_t_rcd',           tRCDx1), # 0x7
                                                           ('reg_ddrc_rd2pre',          RD2PRE), # 0x4
                                                           ('reg_ddrc_pad_pd',          padPD), # 0x0
                                                           ('reg_ddrc_t_xp',            XP), # 0x4
                                                           ('reg_ddrc_wr2rd',           WR2RD), # 0xe
                                                           ('reg_ddrc_rd2wr',           RD2WR), # 0x7 
                                                           ('reg_ddrc_write_latency',   write_latency)),force,warn) #5
# reg DRAM_param_reg3, 0x272872d0
        ddrc_register_set.set_bitfields('dram_param_reg3',(('reg_ddrc_loopback',           ?), #0
                                                           ('reg_ddrc_dis_pad_pd',          ?), #0
                                                           ('reg_phy_mode_ddr1_ddr2',          ?), #1
                                                           ('reg_ddrc_read_latency',            ?), #7
                                                           ('reg_ddrc_en_dfi_dram_clk_disable',           ?), #0
                                                           ('reg_ddrc_mobile',           ?), # 0
                                                           ('reg_ddrc_sdram',           ?), # 1
                                                           ('reg_ddrc_refresh_to_x32',           ?), # 8
                                                           ('reg_ddrc_t_rp',           ?), # 7
                                                           ('reg_ddrc_refresh_margin',           ?), # 2
                                                           ('reg_ddrc_t_rrd',           ?), # 6
                                                           ('reg_ddrc_t_ccd',           ?)),force,warn) #4
         
# CONFIG_EZYNQ_DDR_XP = 4
# CONFIG_EZYNQ_DDR_RCD = 7 (was CONFIG_EZYNQ_DDR_T_RCD = 7) *
# CONFIG_EZYNQ_DDR_RP = 7 (was CONFIG_EZYNQ_DDR_T_RP = 7) *
# CONFIG_EZYNQ_DDR_T_RC = 48.75 *
# CONFIG_EZYNQ_DDR_T_RAS_MIN = 35.0 *
# CONFIG_EZYNQ_DDR_T_RFC = 350.0
# CONFIG_EZYNQ_DDR_T_FAW = 40.0 *
# CONFIG_EZYNQ_DDR_RTP = 4
# CONFIG_EZYNQ_DDR_T_RTP = 7.5
# CONFIG_EZYNQ_DDR_WTR = 4
# CONFIG_EZYNQ_DDR_T_WTR = 7.5

# reg_ddrc_wr2pre    4:0    1f    12    12
# reg_ddrc_powerdown_to_x32    9:5    3e0    6    c0
# reg_ddrc_t_faw    15:10    fc00    16    5800
# reg_ddrc_t_ras_max    21:16    3f0000    24    240000
# reg_ddrc_t_ras_min    26:22    7c00000    13    4c00000
# reg_ddrc_t_cke    31:28    f0000000    4    40000000
# DRAM_param_reg1 @ 0XF8006018        f7ffffff        44e458d2





#     'dram_param_reg3':         {'OFFS': 0x020,'DFLT':0x250882D0,'RW':'M','FIELDS':{ #272872d0
#                   'reg_ddrc_loopback':                {'r':(31,31),'d': 0,'c':'reserved'},
#                   'reg_ddrc_dis_pad_pd':              {'r':(30,30),'d': 0,'c':'Disable pad power down'},                                                                                               
#                   'reg_phy_mode_ddr1_ddr2':           {'r':(29,29),'d': 1,'c':'Unused'},                                             # 0x1                                                                                          
#                   'reg_ddrc_read_latency':            {'r':(24,28),'d': 0x5,'c':'Read Latency, clocks'},                             # 0x7 
#                   'reg_ddrc_en_dfi_dram_clk_disable': {'r':(23,23),'d': 0,'c':'Enables clock disable...'}, 
#                   'reg_ddrc_mobile':                  {'r':(22,22),'d': 0,'c':'0 - DDR2/DDR3, 1 - LPDDR2'},                           
#                   'reg_ddrc_sdram':                   {'r':(21,21),'d': 0,'c':'reserved'},                                           # 0x1
#                   'reg_ddrc_refresh_to_x32':          {'r':(16,20),'d': 0x8,'c':'Dynamic, "speculative refresh"'}, 
#                   'reg_ddrc_t_rp':                    {'r':(12,15),'d': 0x8,'c':'tRP'},                                              # 0x7
#                   'reg_ddrc_refresh_margin':          {'r':( 8,11),'d': 0x2,'c':'do refresh this cycles before timer expires'},
#                   'reg_ddrc_t_rrd':                   {'r':( 5, 7),'d': 0x6,'c':'tRRD Minimal time between activates of different banks'}, 
#                   'reg_ddrc_t_ccd':                   {'r':( 2, 4),'d': 0x4,'c':'tCCD One less than minimal time between reads of writes to different banks'}, 
#                   'reserved2':                        {'r':( 0, 1),'d': 0,'m':'R','c':'reserved'}}},
#     'dram_param_reg4':         {'OFFS': 0x024,'DFLT':0x0000003C,'RW':'M','FIELDS':{ #0x3c
#                   'reg_ddrc_mr_rdata_valid':          {'r':(27,27),'d': 0,'m':'R','c':'cleared by reading mode_reg_read (0x2a4), set when mode_reg_read gets new data'}, 
#                   'reg_ddrc_mr_type':                 {'r':(26,26),'d': 0,'c':'0 - mode register write, 1 - mode register read'},  
#                   'ddrc_reg_mr_wr_busy':              {'r':(25,25),'d': 0,'m':'R','c':'1 - do not issue mode register R/W (wait 0)'},  
#                   'reg_ddrc_mr_data':                 {'r':( 9,24),'d': 0,'c':'DDR2/3: Mode Register Write data'},   
#                   'reg_ddrc_mr_addr':                 {'r':( 7, 8),'d': 0,'c':'DDR2/3: Mode Register address (0 - MR0, ... 3 - MR3)'},  
#                   'reg_ddrc_mr_wr':                   {'r':( 6, 6),'d': 0,'m':'W','c':'low-to-high starts mode reg r/w (if not ddrc_reg_mr_wr_busy)'},  
#                   'reg_ddrc_max_rank_rd':             {'r':( 2, 5),'d': 0xF,'c':'reserved'},
#                   'reg_ddrc_prefer_write':            {'r':( 1, 1),'d': 0,'c':'1: Bank selector prefers writes over reads'}, 
#                   'reg_ddrc_en_2t_timing_mode':       {'r':( 0, 0),'d': 0,'c':'0 - DDRC uses 1T timing, 1 - 2T timing'}}}, 




    def ddr_init_ddriob(self,force=False,warn=False): # will program to sequence 'MAIN'
#        print 'ddr_init_ddriob\n'
        ddriob_register_set=self.ddriob_register_sets['MAIN']
# DDRIOB configuration UG585.268
        is_LPDDR2=   (self.features.get_par_value('MEMORY_TYPE')=='LPDDR2')
        is_DDR3L=    (self.features.get_par_value('MEMORY_TYPE')=='DDR3L')
        is_DDR3_15=  (self.features.get_par_value('MEMORY_TYPE')=='DDR3')
        is_DDR3=     is_DDR3_15 or is_DDR3L
        is_DDR2=     (self.features.get_par_value('MEMORY_TYPE')=='DDR2')
        is_32=       (self.features.get_par_value('BUS_WIDTH') > 16)
        is_int_vref=  self.features.get_par_value('INTERNAL_VREF')
        
# Set the IOB configuration as follows:
        for reg_name in ('ddriob_addr0','ddriob_addr1','ddriob_data0','ddriob_data1','ddriob_diff0','ddriob_diff1','ddriob_clock'):
            ddriob_register_set.set_word(reg_name,0,force) # disable all        
#            ddriob_register_set.set_bitfields(reg_name,(('dco_type',0)),force,warn) # disable all - add other fields?        
# 1. Set DCI_TYPE to DCI Drive for all LPDDR2 I/Os.
        if is_LPDDR2:
            for reg_name in (('ddriob_addr0','ddriob_addr1','ddriob_data0','ddriob_diff0','ddriob_clock')
                             ('ddriob_addr0','ddriob_addr1','ddriob_data0','ddriob_data1','ddriob_diff0','ddriob_diff1','ddriob_clock'))[is_32]:
                ddriob_register_set.set_bitfields(reg_name,(('dco_type',1)),force,warn)        
# 2. Set DCI_TYPE to DCI Termination for DDR2/DDR3 bidirectional I/Os.
        if is_DDR2 or is_DDR3:
            for reg_name in (('ddriob_data0','ddriob_diff0'),
                             ('ddriob_data0','ddriob_data1','ddriob_diff0','ddriob_diff1'))[is_32]:
                ddriob_register_set.set_bitfields(reg_name,(('dci_type',3)),force,warn)   # 3 - DCI term (DDR2/3/3L DQ, DQS'
# 3. Set OUTPUT_EN = obuf to enable outputs.
        for reg_name in (('ddriob_addr0','ddriob_addr1','ddriob_data0','ddriob_diff0','ddriob_clock'),
                         ('ddriob_addr0','ddriob_addr1','ddriob_data0','ddriob_data1','ddriob_diff0','ddriob_diff1','ddriob_clock'))[is_32]:
            ddriob_register_set.set_bitfields(reg_name,(('output_en',3)),force,warn) # 3 - obuf        
# 4. Set TERM_DISABLE_MODE and IBUF_DISABLE_MODE to enable power saving input modes. The
#    TERM_DISABLE_MODE and IBUF_DISABLE_MODE fields should not be set before DDR training
#    has completed.
        # do nothing now
# 5. Set INP_TYPE to VREF based differential receiver for SSTL, HSTL for single ended inputs.
        for reg_name in (('ddriob_data0'),
                         ('ddriob_data0','ddriob_data1'))[is_32]:
            ddriob_register_set.set_bitfields(reg_name,(('inp_type',1)),force,warn) # 1 - Vref based (sstl, hstl)        
# 6. Set INP_TYPE to Differential input receiver for differential inputs.
        for reg_name in (('ddriob_diff0'),
                         ('ddriob_diff0','ddriob_diff1'))[is_32]:
            ddriob_register_set.set_bitfields(reg_name,(('inp_type',2)),force,warn) # 2 - diff rcv        
# 7. Set TERM_EN to enabled for DDR3 and DDR2 bidirectional I/Os (Outputs and LPRDDR2 IOs are
#    un terminated).
        if is_DDR2 or is_DDR3:
            for reg_name in (('ddriob_data0','ddriob_diff0'),
                             ('ddriob_data0','ddriob_data1','ddriob_diff0','ddriob_diff1'))[is_32]:
                ddriob_register_set.set_bitfields(reg_name,(('term_en',1)),force,warn) 

# 8. Set DDRIOB_DATA1 and DDRIOB_DIFF1 registers to power down if only 16 bits of DQ DDR are
#     used (including ECC bits).
## TODO: find out - what "power down" means - bit 0? or other bits that are already set according tu bus width
# 9. For DDR2 and DDR3 – DCI only affects termination strength, so address and clock outputs do not
#     use DCI.
# 10. For LPDDR2 – DCI affects drive strength, so all I/Os use DCI.
# To enable internal VREF
            pass
# ° Set DDRIOB_DDR_CTRL.VREF_EXT_EN to 00 (disconnect I/Os from external signal)
        if is_int_vref:
            ddriob_register_set.set_bitfields('ddriob_ddr_ctrl', ('vref_ext_en',0),force,warn)        
# ° Set DDRIOB_DDR_CTRL.VREF_SEL to the appropriate voltage setting depending on the DDR
# standard (V REF=VCCO_DDR/2)
            if is_LPDDR2:
                vref_sel=1
            elif is_DDR3L:
                vref_sel=2
            elif is_DDR3_15:
                vref_sel=4
            elif is_DDR2:
                vref_sel=8
            else:
                print '***  Invalid memory type ***'
            ddriob_register_set.set_bitfields('ddriob_ddr_ctrl', ('vref_sel',vref_sel),force,warn)
# ° Set DDRIOB_DDR_CTRL.VREF_INT_EN to 1 to enable the internal VREF generator
            ddriob_register_set.set_bitfields('ddriob_ddr_ctrl', ('vref_int_en',1),force,warn)        
# To enable external VREF
        else: # if is_int_vref:
# ° Set DDRIOB_DDR_CTRL.VREF_INT_EN to 0 to disable the internal VREF generator
# ° Set DDRIOB_DDR_CTRL.VREF_SEL to 0000
# ° Set DDRIOB_DDR_CTRL.VREF_EXT_EN to 11 to connect the IOBs VREF input to the external
# pad for a 32-bit interface
# °Set DDRIOB_DDR_CTRL.VREF_EXT_EN to 01 to connect the IOBs VREF input to the external
# pad for a 16-bit interface
            ddriob_register_set.set_bitfields('ddriob_ddr_ctrl', (('vref_int_en',0),
                                                                  ('vref_sel',0),
                                                                  ('vref_ext_en',(1,3)[is_32])),force,warn)
#not in UG585, but used                    
            ddriob_register_set.set_bitfields('ddriob_ddr_ctrl', ('refio_en',1),force,warn)        
#configuring drive strength/slew rate. Seems to be the same for addr and clock, and DQ and DQS
        for reg_name in ('ddriob_drive_slew_addr','ddriob_drive_slew_clock'):
            ddriob_register_set.set_bitfields(reg_name,(
                                                        ('slew_n', self.features.get_par_value('OUT_SLEW_NEG')),
                                                        ('slew_p', self.features.get_par_value('OUT_SLEW_POS')),
                                                        ('drive_n',self.features.get_par_value('OUT_DRIVE_NEG')),
                                                        ('drive_p',self.features.get_par_value('OUT_DRIVE_POS'))),force,warn) # 0xd6861c        
        for reg_name in ('ddriob_drive_slew_data','ddriob_drive_slew_diff'):
            ddriob_register_set.set_bitfields(reg_name,(
                                                        ('slew_n', self.features.get_par_value('BIDIR_SLEW_NEG')),
                                                        ('slew_p', self.features.get_par_value('BIDIR_SLEW_POS')),
                                                        ('drive_n',self.features.get_par_value('BIDIR_DRIVE_NEG')),
                                                        ('drive_p',self.features.get_par_value('BIDIR_DRIVE_POS'))),force,warn) #0xf9861c
#Trying toggle feature (but actually for now it can be left in reset state - is this on/off/on needed?                
        _ = ddriob_register_set.get_register_sets(True,True) # close previous register settings
#        ddriob_register_set.set_bitfields('ddriob_dci_ctrl', ('vrn_out',0),force,warn) # default value shows 1, actual settings - 0  (first time only?)       
        ddriob_register_set.set_bitfields('ddriob_dci_ctrl', ('reset',1),force,warn)        
        _ = ddriob_register_set.get_register_sets(True,True) # close previous register settings
        ddriob_register_set.set_bitfields('ddriob_dci_ctrl', ('reset',0),force,warn)        
        _ = ddriob_register_set.get_register_sets(True,True) # close previous register settings
        ddriob_register_set.set_bitfields('ddriob_dci_ctrl', (('reset', 1),
                                                              ('enable',1),
                                                              ('nref_opt1',0),
                                                              ('nref_opt2',0),
                                                              ('nref_opt4',1),
                                                              ('pref_opt2',0),
                                                              ('update_control',0)),force,warn)        
            
    def parse_ddrc_raw_register_set(self,raw_configs,qualifier_char,force=True,warn=True):
#        for i,attribs in enumerate(self.set_attribs):
        for attribs in self.set_ddrc_attribs:
            reg_set_name=attribs['NAME']
            reg_set= self.register_sets[reg_set_name]
            prefix= attribs['PREFIX']
            postfix= attribs['POSTFIX']
            reg_set.parse_options_set(raw_configs,prefix,postfix,self.postfixes,qualifier_char,force,warn) #force - readonly/undefined fields, warn: data does not fit in the bit field
    def parse_ddriob_raw_register_set(self,raw_configs,qualifier_char,force=True,warn=True):
#        for i,attribs in enumerate(self.set_attribs):
        for attribs in self.set_ddriob_attribs:
            reg_set_name=attribs['NAME']
            reg_set= self.register_sets[reg_set_name]
            prefix= attribs['PREFIX']
            postfix= attribs['POSTFIX']
            reg_set.parse_options_set(raw_configs,prefix,postfix,self.postfixes,qualifier_char,force,warn) #force - readonly/undefined fields, warn: data does not fit in the bit field
    def print_ddrc_html_registers(self, html_file, show_bit_fields=True, show_comments=True,filter_fields=True):
        for attribs in self.set_ddrc_attribs:
            reg_set_name=attribs['NAME']
            reg_set= self.ddrc_register_sets[reg_set_name]
            if len(reg_set.get_reg_names())>0:
                html_file.write('<h2>'+attribs['TITLE']+'</h2>\n')
                reg_set.print_html_registers(html_file, show_bit_fields, show_comments,filter_fields)
                html_file.write('<br/>\n')
    def print_ddriob_html_registers(self, html_file, show_bit_fields=True, show_comments=True,filter_fields=True):
        for attribs in self.set_ddrc_attribs:
            reg_set_name=attribs['NAME']
            reg_set= self.ddrc_register_sets[reg_set_name]
            if len(reg_set.get_reg_names())>0:
                html_file.write('<h2>'+attribs['TITLE']+'</h2>\n')
                reg_set.print_html_registers(html_file, show_bit_fields, show_comments,filter_fields)
                html_file.write('<br/>\n')
                 
               
#ddr=Ezynq_DDR()
#print ddr.DDRC_DEFS
#    def __init__(self,defines,channel=0,permit_undefined_bits=False):
#    def parse_options_set(self,raw_configs,prefix,postfix,qualifier_char,force=True,warn=True): #force - readonly/undefined fields, warn: data does not fit in the bit field
