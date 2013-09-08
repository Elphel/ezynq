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
def set_random_bits(old,d,bits):
    data = 0
    mask = 0
    for i,b in enumerate(bits):
        mask  |= 1<< b
        data |= ((d>>i) & 1) << b
    return ((old ^ data) & mask) ^ old    
        
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
    def calculate_dependent_pars(self):
#TODO: just testing on a few pars, migrate more of them
        try:
            tCK=1000.0/self.features.get_par_value('FREQ_MHZ')
#            print 'FREQ_MHZ=',self.features.get_par_value('FREQ_MHZ')

            try:
                self.features.set_max_value('RP', int(math.ceil(self.features.get_par_value('T_RP')/tCK)))
            except:
                pass # get_par_value('T_RP') failed

            try:    
                self.features.set_max_value('RCD', int(math.ceil(self.features.get_par_value('T_RCD')/tCK)))
            except:
                pass
            try:
                self.features.set_max_value('RRD', int(math.ceil(self.features.get_par_value('T_RRD')/tCK)))
            except:
                pass

            try:
                self.features.set_max_value('CKE', int(math.ceil(self.features.get_par_value('T_CKE')/tCK)))
            except:
                pass
            try:
                self.features.set_max_value('CKSRE', int(math.ceil(self.features.get_par_value('T_CKSRE')/tCK)))
            except:
                pass
            try:
                self.features.set_max_value('CKSRX', int(math.ceil(self.features.get_par_value('T_CKSRX')/tCK)))
            except:
                pass
            try:
                self.features.set_max_value('MOD', int(math.ceil(self.features.get_par_value('T_MOD')/tCK)))
            except:
                pass
        
        except:
            print "*** DDR Clock frequency is not defined"
    def pre_validate(self):
        if not self.features.get_par_value('ENABLE'):
            return
        is_LPDDR2=   (self.features.get_par_value('MEMORY_TYPE')=='LPDDR2')
        if (not is_LPDDR2) and (self.features.get_par_value('BL')>8):
            raise Exception("BL=16 is only supported in LPDDR2 memory")
    def post_validate(self):
        if not self.features.get_par_value('ENABLE'):
            return
        self._fix_address_map()

    def _fix_address_map(self):
        half_width= self.features.get_par_value('BUS_WIDTH') == 16
        ba_count=   self.features.get_par_value('BANK_ADDR_COUNT')
        ra_count=   self.features.get_par_value('ROW_ADDR_COUNT')
        ca_count=   self.features.get_par_value('COL_ADDR_COUNT')
        ba_map=     self.features.get_par_value('BANK_ADDR_MAP')
        try:
            _,_=self._map_ddr_addresses (ca_count,ra_count,ba_count,ba_map,half_width)
            return # all OK already
        except Exception, err:
            print "Specified value for the "+self.features.get_par_confname('BANK_ADDR_MAP')+'='+str(ba_map)+" is not valid:\n"+str(err)
        best_match=None
        for bm in range(3,30):
            if (best_match==None) or (abs(bm-ba_map) < abs(bm-ba_map)):
                try:
                    _,_=self._map_ddr_addresses (ca_count,ra_count,ba_count,bm,half_width)
                    best_match=bm
                except:
                    continue
        if best_match==None:
            raise Exception ('Could not find a suitable value for '+self.features.get_par_confname('BANK_ADDR_MAP'))            
        print "Replacing with: "+self.features.get_par_confname('BANK_ADDR_MAP')+'='+str(best_match)
        self.features.set_value('BANK_ADDR_MAP', best_match)
                        
        
                 
    def _map_ddr_addresses (self,num_ca,num_ra,num_ba,skip_ba,half_width):
        map_capabilities={
        #C/R/B, bit(s) (for CA - in full width mode), internal base - bit number, (valid:min,max) [,disable value]
            'col_b2':   ('C', 3, 2,( 0, 7)),
            'col_b3':   ('C', 4, 2,( 0, 7)),
            'col_b4':   ('C', 5, 2,( 0, 7)),
            'col_b5':   ('C', 6, 2,( 0, 7)),
            'col_b6':   ('C', 7, 2,( 0, 7)),
            'col_b7':   ('C', 8, 2,( 0, 7),0xf),
            'col_b8':   ('C', 9, 2,( 0, 7),0xf),
            'col_b9':   ('C',10, 2,( 0, 7),0xf),
            'col_b10':  ('C',11, 2,( 0, 7),0xf),
            'col_b11':  ('C',12, 2,( 0, 7),0xf),

            'row_b0':   ('R', 0, 9,( 0, 11)),
            'row_b1':   ('R', 1, 9,( 0, 11)),
            'row_b2_11':('R',( 2,11), 9,( 0, 11)),
            'row_b12':  ('R', 12, 9,( 0, 8),0xf),
            'row_b13':  ('R', 13, 9,( 0, 7),0xf),
            'row_b14':  ('R', 14, 9,( 0, 6),0xf),
            'row_b15':  ('R', 15, 9,( 0, 5),0xf),

            'bank_b0':('B', 0, 5,( 0, 14)),
            'bank_b1':('B', 1, 5,( 0, 14)),
            'bank_b2':('B', 2, 5,( 0, 14),0xf),
         }
        def map_field(name,bit):
            capability=map_capabilities[name]
            group=capability[0]
            add_base=capability[2]
            valid_limits=capability[3]
            try:
                disable=capability[4]
            except:
                disable=None
            if half_width and (group=='C'):
                bit += 1
            for i, map_bit in enumerate (map_axi):
                if (map_bit['TYPE']==group) and (map_bit['BIT']==bit):
                    extra=i-(bit+add_base)
                    if not extra in range(valid_limits[0],valid_limits[1]+1):
                        raise Exception ('Failed to map AXI_A['+str(i)+'] to '+group+'A ['+str(bit)+'], as the required value for '+
                                         name+'='+str(extra)+' is not in the valid range of '+str(valid_limits)+'.')
#                    print name, '->', extra    
                    return extra # this is the value of the bit field
            else: # This address bit of the group is not used - try to disable it
                if disable==None:
                    raise Exception ('Address bit '+group+'A ['+str(bit)+'], is not used, but it is not possible to disable it in the bit field '+name)
#                print name, '-> disable:', disable    
                return disable
            
        map_ba=skip_ba+(2,1)[half_width] # full AXI address to map BA0 to
        if (num_ba<2) or (num_ba>3):
            raise Exception('Wring number of bank addresses: '+str(num_ba)+", only 2 or 3 are supported")
        if (map_ba<5):
            raise Exception('Map bank address is too low, should be at least '+str(5-(2,1)[half_width]))
#        num_addresses=(2,1)[half_width]+num_ca+num_ra+num_ba
        map_axi=[{'TYPE':'NONE','BIT':0} for i in range((2,1)[half_width]+num_ca+num_ra+num_ba)]
        if map_ba > (len(map_axi)- num_ba):
            raise Exception('Map bank address is too high, should be not higher than '+str(len(map_axi)- num_ba))
        #Map AXI addresses to CA (logical, skipping A10 when applicable), RA, BA without restricting to hardware possibility
        map_left=skip_ba
        next_ca=0
        next_ra=0
        next_ba=0
        for i, map_bit in enumerate (map_axi):
            if i<(2,1)[half_width]:
                continue # did not get to the first address to map
            if (map_left==0) or (next_ba>0) and (next_ba<num_ba):
                map_bit['TYPE']='B'
                map_bit['BIT']=next_ba
                next_ba+=1
                map_left-=1 # so it will never trigger (map_left==0) again 
#                print 'i=',i,'type=',map_bit['TYPE'],'map_left=',map_left,'next_ca=',next_ca,'next_ra=',next_ra,'next_ba=',next_ba
                continue
            if (next_ca<num_ca):
                map_bit['TYPE']='C'
                map_bit['BIT']=next_ca
                next_ca+=1
            else:
                map_bit['TYPE']='R'
                map_bit['BIT']=next_ra
                next_ra+=1
            map_left-=1
#            print 'i=',i,'type=',map_bit['TYPE'],'map_left=',map_left,'next_ca=',next_ca,'next_ra=',next_ra,'next_ba=',next_ba
#        print map_axi
        #ug585:837 - details for ddrc.page_mask register
        page_mask=0
        for i, map_bit in enumerate (map_axi[3:]): # skip 3 LSB to get "This mask applies to 64-bit address and not byte address.". ***** TODO: Verify it is really 64 (8-byte), not 32 (4-byte) word address
            if map_bit['TYPE'] in 'BR': 
                page_mask |= 1<<i
        #now validate mapping, raise exception if invalid
        address_mapping={}
        for name in map_capabilities:
            capability=map_capabilities[name]
            bit=capability[1]
            if isinstance(bit,tuple):
                value=map_field(name,capability[1][0])
                for bit in range(capability[1][0]+1,capability[1][1]+1):
                    other=map_field (name,bit)
                    if other != value:
                        raise Exception ('It is not possible to independently assign mappings for '+capability[0]+'A['+str(capability[1][0])+
                                         ']='+str(value)+' and '+capability[0]+'A['+str(bit)+']='+str(other)+' as they are controlled by the same '+name+'.')
            else:
                value=map_field(name,capability[1])
            address_mapping[name]=value             
        return (address_mapping,page_mask)

    def get_new_register_sets(self):
        return self.ddrc_register_sets['MAIN'].get_register_sets(True,True)
    
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
        use_rd_data_eye_level = (0,1)[self.features.get_par_value('TRAIN_DATA_EYE')] 
        use_rd_dqs_gate_level = (0,1)[self.features.get_par_value('TRAIN_READ_GATE')] 
        use_wr_level          = (0,1)[self.features.get_par_value('TRAIN_WRITE_LEVEL')] 
                      
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

        CKE=  self.features.get_par_value('CKE') # 4
        
        RAS_MIN= int(math.ceil(self.features.get_par_value('T_RAS_MIN')/tCK))
        RAS_MAX=9*tREFI # for Micron
        RAS_MAXx1024=int(RAS_MAX/tCK/1024)
        tFAWx1=int(math.ceil(self.features.get_par_value('T_FAW')/tCK))
        inactiveToPDx32=6 # cycles 'Power down after this many clocks of NOP/DESELECT (if enabled in mcr). Make configurable?
        WR=int(math.ceil(tWR/tCK))
#        print 'tWR=',tWR,'tCK=',tCK
        wr_options_ddr3=(16,5,6,7,8,10,12,14)
        # some values are not valid for DDR3 when writing to MR0 register, trying to fix WR (in tCK) to be valid
        if is_DDR3 and (not WR in wr_options_ddr3):
            print 'Calculated value for Write recovery (WR): '+str(WR)+ ' (as defined by tWR), is not valid for DDR3 MR0, it only supports '+str(sorted(wr_options_ddr3))
            print 'trying to adjust WR:'
            cheat_down=0.1 # reduce calculated WR if before rounding up it did not exceed integer value by more than 'cheat'
            WR1=int(math.ceil(tWR/tCK-cheat_down))
            if WR1 in wr_options_ddr3:
                print 'Using WR='+str(WR1)+' instead of '+str(WR)+' (cheating down), before rounding the value was '+str(tWR/tCK)
                WR=WR1
            elif (WR+1) in wr_options_ddr3:
                print 'Using WR='+str(WR+1)+' instead of '+str(WR)+' (to much to cheat down, increasing to next valid), before rounding the value was '+str(tWR/tCK)
                WR=WR+1
            else:
                raise Exception('Could not fix the value of WR, please check frequency ('+self.features.get_par_confname('FREQ_MHZ')+
                                ') and write recovery (ns) '+ self.features.get_par_confname('T_WR'))    
        WL=self.features.get_par_value('CWL')
        BL=self.features.get_par_value('BL')
        wr2pre=WL+BL/2+WR
        if is_LPDDR2:
            wr2pre+=1
        ddrc_register_set.set_bitfields('dram_param_reg1',(('reg_ddrc_t_cke',           CKE), # Default - OK, Micron tXSDLL=tDLLK=512 /32
                                                           ('reg_ddrc_t_ras_min',       RAS_MIN),
                                                           ('reg_ddrc_t_ras_max',       RAS_MAXx1024),
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
                raise Exception('Minimal Write Latency supported for LPDDR2 is 1, while '+self.features.get_par_confname('CWL')+'='+str(WL))
        else:
            if WL<3:
                raise Exception('Minimal Write Latency supported for DDR2/DDR3 is 3, while '+self.features.get_par_confname('CWL')+'='+str(WL))
        ddrc_register_set.set_bitfields('dram_param_reg2',(('reg_ddrc_t_rcd',           tRCDx1), # 0x7
                                                           ('reg_ddrc_rd2pre',          RD2PRE), # 0x4
                                                           ('reg_ddrc_pad_pd',          padPD), # 0x0
                                                           ('reg_ddrc_t_xp',            XP), # 0x4
                                                           ('reg_ddrc_wr2rd',           WR2RD), # 0xe
                                                           ('reg_ddrc_rd2wr',           RD2WR), # 0x7 
                                                           ('reg_ddrc_write_latency',   write_latency)),force,warn) #5
# reg DRAM_param_reg3, 0x270872d0 , 0x272872d0, 0x272872d0 (first time reg_ddrc_sdram is not set, the rest is the same)
        enable_pad_powerdown=     True  # ?
        mode_ddr1_ddr2=           1
        en_dfi_dram_clk_disable = 0 # not clear - is it just enable for the action, or actually stopping the clock?
        ddrc_refresh_to_x32=      8 # start refresh after this inactivity (x32 cycles) if it is useful, but not yet required. Dynamic field
        RP=                       self.features.get_par_value('RP')
        refresh_margin=           2 # default, recommended not to be changed
        CCD=                      self.features.get_par_value('CCD')
        RRD=                      self.features.get_par_value('RRD')

        ddrc_register_set.set_bitfields('dram_param_reg3',(('reg_ddrc_loopback',               0), #0
                                                           ('reg_ddrc_dis_pad_pd',             (1,0)[enable_pad_powerdown]), #0
                                                           ('reg_phy_mode_ddr1_ddr2',          mode_ddr1_ddr2), #1
                                                           ('reg_ddrc_read_latency',           RL), #7
                                                           ('reg_ddrc_en_dfi_dram_clk_disable',en_dfi_dram_clk_disable), #0
                                                           ('reg_ddrc_mobile',                 (0,1)[is_LPDDR2]), # 0
                                                           ('reg_ddrc_sdram',                  1),  # Shown reserved/default==0, but actually is set to 1 (2 and 3-rd time)
                                                           ('reg_ddrc_refresh_to_x32',         ddrc_refresh_to_x32), # 8
                                                           ('reg_ddrc_t_rp',                   RP), # 7
                                                           ('reg_ddrc_refresh_margin',         refresh_margin), # 2
                                                           ('reg_ddrc_t_rrd',                  RRD), # 6
                                                           ('reg_ddrc_t_ccd',                  CCD-1)),force,warn) #4
# reg DRAM_param_reg4, 0, 0x3c, 0x3c
        ddrc_register_set.set_word     ('dram_param_reg4',0x0,force) # reset all fields. This register is controlled by the hardware during automatic initialization
        #Maybe just the LSBB (reg_ddrc_en_2t_timing_mode) is needed for "2t timing mode" - is it non-common? 
        ddrc_register_set.set_bitfields('dram_param_reg4',(('reg_ddrc_max_rank_rd',            0xf)),force,warn) # Not documented, but appears to be set in 2-nd and 3-rd round
        
        
# reg DRAM_init_param,  0x2007 always (default)
        MRD = self.features.get_par_value('CCD')
        pre_ocd_x32=0 # ... may be set to zero ...
        final_wait_x32=0x7 # leaving default - time to start scheduler after dram init init
        ddrc_register_set.set_bitfields('dram_init_param',(('reg_ddrc_t_mrd',                  MRD),         # 0x4
                                                           ('reg_ddrc_pre_ocd_x32',            pre_ocd_x32), # 0x0
                                                           ('reg_ddrc_final_wait_x32',         final_wait_x32)),force,warn) # 0x7
# reg DRAM_emr_reg,     0x8 always (default)
#        ddrc_register_set.set_word     ('dram_emr_reg',        0x8, force)
        emr3=0 # Only 3 LSBs are used by DDR and should be set to 0 - correct values will be set by  the DDRC
        if is_LPDDR2:
            #use MR3 for the emr2. Lower 3 bits encode impedance, for now just using default value of
            emr2=2 # 40 Ohm
        else: #DDR2, DDR3
            emr2_00_02=0
            emr2_03_05=WL-5
            if emr2_03_05 < 0:
                emr2_03_05=0
            emr2_03_05 &= 0x7
            emr2_06_06= 0 # Auto Self Refresh - 0 manual, 1 - auto
            emr2_07_07= (0,1)[self.features.get_par_value('HIGH_TEMP')] # 
            emr2_08_08= 0
            emr2_09_10= 0 # Dynamic ODT control
            emr2_11_15= 0
            emr2=((emr2_00_02 <<  0) |
                  (emr2_03_05 <<  3) |
                  (emr2_06_06 <<  6) |
                  (emr2_07_07 <<  7) |
                  (emr2_08_08 <<  8) |
                  (emr2_09_10 <<  9) |
                  (emr2_11_15 << 11))
        ddrc_register_set.set_bitfields('dram_emr_reg',   (('reg_ddrc_emr3',                   emr3), # 0
                                                           ('reg_ddrc_emr2',                   emr2)),force,warn) # 0x8
# reg DRAM_emr_mr_reg,  0x40930 always (default)
#calculate mr value for different memory types            
        emr=0
        if is_DDR3 : # MR1
            emr_disableDLL=0     #  Disable DLL
            emr_driveStrength=0  #  0 - 40 OHm, 1 - 34 Ohm, 2,3 - reserved
            if AL==0:
                emr_AL=0
            elif AL==(CL-1):
                emr_AL=1     
            elif AL==(CL-2):
                emr_AL=2     
            else:
                raise Exception ('Wrong value for additive latency ('+self.features.get_par_confname('AL')+': '+str(AL)+', only 0, CL-1, CL-2 are supported in DDR3 memory. CL is '+str(CL))
            emr_RTT=0
            if self.features.get_par_value('DDR3_RTT')[:2]=='60':
                emr_RTT=1
            elif self.features.get_par_value('DDR3_RTT')[:2]=='12':
                emr_RTT=2
            elif self.features.get_par_value('DDR3_RTT')[:2]=='40':
                emr_RTT=3

            emr_WL=   0       # 0 - disabled (normal), 1 - write leveling (will be set by DDRC, set to 0 here)
            emr_TDQS= 0 # Termination data strobe - only applicable to x8 memory
            emr_Qoff= 0 # 1 - tristate all DQ and DQS outputs
            #According to description of the MR1 bits:
            emr=set_random_bits(emr,  emr_disableDLL,    (0,))
            emr=set_random_bits(emr,  emr_driveStrength, (1,5))
            emr=set_random_bits(emr,  emr_AL,            (3,4))
            emr=set_random_bits(emr,  emr_RTT,           (2,6,9))
            emr=set_random_bits(emr,  emr_WL,            (7,))
            emr=set_random_bits(emr,  emr_TDQS,          (11,))
            emr=set_random_bits(emr,  emr_Qoff,          (12,))
        elif is_DDR2: # EMR
            emr_disableDLL=   0  #  Disable DLL
            emr_driveStrength=0  #  0 -full, 1 - reduced
            emr_AL=AL
            if (AL<0) or (AL>6):
                raise Exception ('Wrong value for additive latency ('+self.features.get_par_confname('AL')+': '+str(AL)+', only 0...6 are supported in DDR2 memory')
            emr_RTT=0
            if self.features.get_par_value('DDR2_RTT')[:2]=='75':
                emr_RTT=1
            elif self.features.get_par_value('DDR2_RTT')[:2]=='15':
                emr_RTT=2
            elif self.features.get_par_value('DDR2_RTT')[:2]=='50':
                emr_RTT=3
            emr_OCD_oper=   0 # these bits are ignored for DDR2
            emr_DQS_disable=0
            emr_RDQS=       0
            emr_DQ_disable= 0
            emr=set_random_bits(emr,  emr_disableDLL,    (0,))
            emr=set_random_bits(emr,  emr_driveStrength, (1,))
            emr=set_random_bits(emr,  emr_AL,            (3,4,5))
            emr=set_random_bits(emr,  emr_RTT,           (2,6))
            emr=set_random_bits(emr,  emr_OCD_oper,      (7,8,9))
            emr=set_random_bits(emr,  emr_DQS_disable,   (10,))
            emr=set_random_bits(emr,  emr_RDQS,          (11,))
            emr=set_random_bits(emr,  emr_DQ_disable,    (12,))
        elif is_LPDDR2: # MR2
            rlwl_options=((3,1),(4,2),(5,2),(6,3),(7,4),(8,4))
            rlwl=(RL,WL)
            try:
                mr2_rlwl=((3,1),(4,2),(5,2),(6,3)).index(rlwl)+1
            except:
                raise Exception('Wrong RL/WL combination: '+str(rlwl)+', LPDDR2 only supports '+str(rlwl_options))    
            emr=mr2_rlwl
#calculate mr value for different memory types            
        mr=0
        if is_DDR3 : #MR0
            if BL==4:
                mr_bl=2
            elif BL==8:        
                mr_bl=0
            else:
                raise Exception('Wrong burst length for DDR3: '+str(BL)+' - only 4 and 8 are supported')
            mr_bt=0 # 0 - sequential, 1 - interleaved - is it supported?
            try:  
                mr_cl=(2,4,6,8,10,12,14,1,3,5)[CL-5]
            except:
                raise Exception('Wrong value for CAS latency: '+str(CL)+ ' - only CL=5..14 are supported by DDR3')
            mr_dll_reset=1 # Seems to be always set (including dflt)?
            wr_options_ddr3=(16,5,6,7,8,10,12,14)
            try:
                mr_write_recovery=wr_options_ddr3.index(WR)
            except:
                raise Exception('Wrong value for Write recovery (WR): '+str(WR)+ ' (may be defined by tWR), DDR3 only supports '+str(sorted(wr_options_ddr3)))
            mr_PD = 0 # 0 - DLL off during PD (slow exit), 1 - DLL on during PD (fast exit)            
            mr=set_random_bits(mr,  mr_bl,            (0,1))
            mr=set_random_bits(mr,  mr_bt,            (3, ))
            mr=set_random_bits(mr,  mr_cl,            (2,4,5,6))
            mr=set_random_bits(mr,  mr_dll_reset,     (8,))
            mr=set_random_bits(mr,  mr_write_recovery,(9,10,11))
            mr=set_random_bits(mr,  mr_PD,            (12,))
        elif is_DDR2: # MR
            if BL==4:
                mr_bl=2
            elif BL==8:        
                mr_bl=3
            else:
                raise Exception('Wrong burst length for DDR2: '+str(BL)+' - only 4 and 8 are supported')
            mr_bt=0 # 0 - sequential, 1 - interleaved - is it supported?
            try:  
                mr_cl=(3,4,5,6,7)[CL-3]
            except:
                raise Exception('Wrong value for CAS latency '+str(CL)+ ' - only CL=3..7 are supported')
            mr_tm=0 # 0 - normal, 1 - test
            mr_dll_reset=1 # Always reset for DDR3, doing the same for DDR2 
            wr_options=(2,3,4,5,6,7,8)
            try:
                mr_write_recovery=wr_options.index(WR)+1
            except:
                raise Exception('Wrong value for Write recovery (WR) (may be defined by tWR) '+str(WR)+ ', DDR2 only supports '+str(wr_options))
            mr_PD = 0 # 0 - fast exit (normal), 1 - slow exit (low power)            
            
            mr=set_random_bits(mr,  mr_bl,            (0,1,2))
            mr=set_random_bits(mr,  mr_bt,            (3, ))
            mr=set_random_bits(mr,  mr_cl,            (4,5,6))
            mr=set_random_bits(mr,  mr_tm,            (7,))
            mr=set_random_bits(mr,  mr_dll_reset,     (8,))
            mr=set_random_bits(mr,  mr_write_recovery,(9,10,11))
            mr=set_random_bits(mr,  mr_PD,            (12,))

        elif is_LPDDR2: # MR1
            bl_options=(4,8,16)
            try:
                mr_bl=bl_options.index(BL)
            except:
                raise Exception('Wrong burst length '+str(BL)+' - LPDDR2 only supports '+str(bl_options))
            mr_bt=0 # 0 - sequential, 1 - interleaved - is it supported?
            mr_wrap=0 # 0 - wrap(default), 1 - no wrap
            wr_options=(3,4,5,6,7,8)
            try:
                mr_write_recovery=wr_options.index(WR)+1
            except:
                raise Exception('Wrong value for Write recovery (WR) (may be defined by tWR) '+str(WR)+ ', LPDDR2 only supports '+str(wr_options))
            mr=set_random_bits(mr,  mr_bl,            (0,1,2))
            mr=set_random_bits(mr,  mr_bt,            (3, ))
            mr=set_random_bits(mr,  mr_wrap,          (4, ))
            mr=set_random_bits(mr,  mr_write_recovery,(5,6,7))

#        ddrc_register_set.set_word     ('dram_emr_mr_reg', 0x40930, force)
        ddrc_register_set.set_bitfields('dram_emr_mr_reg',(('reg_ddrc_emr',                    emr), # 0x4
                                                           ('reg_ddrc_mr',                     mr)),force,warn) # 0x930
# reg DRAM_burst8_rdwr, 0x10694 always (default=0x20304)
#
        if   is_DDR3:
            t_post_cke=400.0
            t_pre_cke= 200000.0
        elif is_DDR2:
            t_post_cke=400.0
            t_pre_cke= 200000.0
        elif is_LPDDR2:
            t_post_cke=200000.0
            t_pre_cke= 20000000.0 # UG585.790 specifies :LPDDR2 - tINIT0 of 20 mS (max) + tINIT1 of 100nS (min), and 20mS > 10 bits
        post_cke_x1024= int(math.ceil(t_post_cke/tCK/1024))
        pre_cke_x1024=  int(math.ceil(t_pre_cke/tCK/1024))
        if (pre_cke_x1024)>1023:
            pre_cke_x1024=1023 # maximal value
        if BL==4:
            burst_rdwr=2
        elif BL==8:      
            burst_rdwr=4
        elif BL==16: # LPDDR2 only      
            burst_rdwr=8
#        ddrc_register_set.set_word     ('dram_burst8_rdwr',0x10694, force)
        ddrc_register_set.set_bitfields('dram_burst8_rdwr',(('reg_ddrc_burstchop',             0), #  0
                                                            ('reg_ddrc_post_cke_x1024',        post_cke_x1024), #  0x1
                                                            ('reg_ddrc_pre_cke_x1024',         pre_cke_x1024), #  0x69
                                                            ('reg_ddrc_burst_rdwr',            burst_rdwr)),force,warn) # 0x4
# reg DRAM_disable_dq,  0 always (default)
#        ddrc_register_set.set_word     ('dram_disable_dq',     0x0, force)
        ddrc_register_set.set_bitfields('dram_disable_dq',(('reg_phy_dq0_wait_t',              0), # 0
                                                           ('reg_phy_rd_level_start',          0), # 0
                                                           ('reg_phy_wr_level_start',          0), # 0
                                                           ('reg_phy_debug_mode',              0), # 0
                                                           ('reg_ddrc_dis_dq',                 0), # 0
                                                           ('reg_ddrc_force_low_pri_n',        0)),force,warn) # 0
        
# Using some of the the possible address mappings, defined by a single parameter BANK_ADDR_MAP:
# First CA and RA are considered continuous (skipping CA[10] when applicable), then all bank address bits are inserted,
# leaving BANK_ADDR_MAP bits (some CA, all CA or ALL CA and some RA ) lower          
        half_width= self.features.get_par_value('BUS_WIDTH') == 16
        ba_count=   self.features.get_par_value('BANK_ADDR_COUNT')
        ra_count=   self.features.get_par_value('ROW_ADDR_COUNT')
        ca_count=   self.features.get_par_value('COL_ADDR_COUNT')
        ba_map=     self.features.get_par_value('BANK_ADDR_MAP')
        addr_map,page_addr_mask =self._map_ddr_addresses (ca_count,ra_count,ba_count,ba_map,half_width)
        if not self.features.get_par_value('ARB_PAGE_BANK'):
            page_addr_mask=0 #default
        
# reg DRAM_addr_map_bank,  0x777 always (default)
        ddrc_register_set.set_bitfields('dram_addr_map_bank',(('reg_ddrc_addrmap_col_b6',   addr_map['col_b6']),             # 0
                                                              ('reg_ddrc_addrmap_col_b5',   addr_map['col_b5']),             # 0
                                                              ('reg_ddrc_addrmap_bank_b2',  addr_map['bank_b2']),            # 0x7
                                                              ('reg_ddrc_addrmap_bank_b1',  addr_map['bank_b1']),            # 0x7
                                                              ('reg_ddrc_addrmap_bank_b0',  addr_map['bank_b0'])),force,warn)# 0x7

# reg DRAM_addr_map_col,   0xfff00000 always (default)
        ddrc_register_set.set_bitfields('dram_addr_map_col', (('reg_ddrc_addrmap_col_b11',  addr_map['col_b11']),            # 0xf
                                                              ('reg_ddrc_addrmap_col_b10',  addr_map['col_b10']),            # 0xf
                                                              ('reg_ddrc_addrmap_col_b9',   addr_map['col_b9']),             # 0xf
                                                              ('reg_ddrc_addrmap_col_b8',   addr_map['col_b8']),             # 0
                                                              ('reg_ddrc_addrmap_col_b7',   addr_map['col_b7']),             # 0
                                                              ('reg_ddrc_addrmap_col_b4',   addr_map['col_b4']),             # 0
                                                              ('reg_ddrc_addrmap_col_b3',   addr_map['col_b3']),             # 0
                                                              ('reg_ddrc_addrmap_col_b2',   addr_map['col_b2'])),force,warn) # 0

# reg DRAM_addr_map_row,   0xf666666 always (default)
        ddrc_register_set.set_bitfields('dram_addr_map_row', (('reg_ddrc_addrmap_row_b15',  addr_map['row_b15']),            # 0xf
                                                              ('reg_ddrc_addrmap_row_b14',  addr_map['row_b14']),            # 0x6
                                                              ('reg_ddrc_addrmap_row_b13',  addr_map['row_b13']),            # 0x6
                                                              ('reg_ddrc_addrmap_row_b12',  addr_map['row_b12']),            # 0x6
                                                              ('reg_ddrc_addrmap_row_b2_11',addr_map['row_b2_11']),          # 0x6
                                                              ('reg_ddrc_addrmap_row_b1',   addr_map['row_b1']),             # 0x6
                                                              ('reg_ddrc_addrmap_row_b0',   addr_map['row_b0'])),force,warn) # 0x6
        

# reg DRAM_odt_reg,  0x3c000, 0x3c248,0x3c248
# Could not find documentation, default value may work (first time 3 default/do not change values were different
        rank0_wr_odt = 1  # default, was 0 first time
        rank1_rd_odt = 1  # default, was 0 first time
        rank1_wr_odt = 1  # default, was 0 first time
        wr_local_odt = 3  # default
        idle_local_odt= 3 # default
         
        ddrc_register_set.set_bitfields('dram_odt_reg', (
                                                      #  ('reg_ddrc_rank3_wr_odt',  0),              # 0
                                                      #  ('reg_ddrc_rank3_rd_odt',  0),              # 0
                                                      #  ('reg_ddrc_rank2_wr_odt',  0),              # 0
                                                      #  ('reg_ddrc_rank2_rd_odt',  0),              # 0 
                                                         ('reg_phy_idle_local_odt', idle_local_odt), # 0x3 0x3
                                                         ('reg_phy_wr_local_odt',   wr_local_odt),   # 0x3 0x3
                                                      #  ('reg_phy_rd_local_odt',   0),              # 0
                                                         ('reg_ddrc_rank1_wr_odt',  rank1_wr_odt),   # 0   0x1
                                                         ('reg_ddrc_rank1_rd_odt',  rank1_rd_odt),   # 0   0x1
                                                         ('reg_ddrc_rank0_wr_odt',  rank0_wr_odt),   # 0   0x1
                                                         ('reg_ddrc_rank0_rd_odt',  0)),force,warn)  # 0
        

        
# reg phy_cmd_timeout_rddata_cpt,  0x77010800 (default) all 3 times
        wrlvl_num_of_dq0   = 7 # write. lev. :recomm. 8 - higher longer, but better
        gatelvl_num_of_dq0 = 7 # gate training :recomm. 8 - higher longer, but better
        use_fixed_re       = 1 # FIFO control mode. Should be set to 1 during training/leveling
        rdc_we_to_re_delay = 8 # Fifo control, used when use_fixed_re=1 
        ddrc_register_set.set_bitfields('phy_cmd_timeout_rddata_cpt',(
                                                         ('reg_phy_wrlvl_num_of_dq0',        wrlvl_num_of_dq0),  # 0x7
                                                         ('reg_phy_gatelvl_num_of_dq0',      gatelvl_num_of_dq0),# 0x7
                                                      #  ('reserved1',                       0),                 # 0
                                                      #  ('reg_phy_clk_stall_level',         0),                 # 0
                                                      #  ('reg_phy_dis_phy_ctrl_rstn',       0),                 # 0
                                                      #  ('reg_phy_rdc_fifo_rst_err_cnt_clr',0),                 # 0
                                                         ('reg_phy_use_fixed_re',            use_fixed_re),      # 0x1
                                                      #  ('reg_phy_rdc_fifo_rst_disable',    0),                 # 0
                                                      #  ('reserved2',                       0),                 # 0
                                                         ('reg_phy_rdc_we_to_re_delay',      rdc_we_to_re_delay),# 0x8
                                                      #  ('reg_phy_wr_cmd_to_data',          0),                 # 0
                                                      #  ('reg_phy_rd_cmd_to_data',          0)                  # 0
                                                                                               ),force,warn)
# reg DLL_calib,  0x0, then 2 times 0x101 (default). Does it need to be 0 before training. Not listed in 10-11 - probably can be skipped during init
        dis_dll_calib = 0 # if 1 - disable automatic periodic DLL correction
        dll_calib_to_max_x1024 = 1 # reserved, do not modify
        dll_calib_to_min_x1024 = 1 # reserved, do not modify
        ddrc_register_set.set_bitfields('dll_calib',(('reg_ddrc_dis_dll_calib',             dis_dll_calib),          # 0
                                                     ('reg_ddrc_dll_calib_to_max_x1024',    dll_calib_to_max_x1024), # 1
                                                     ('reg_ddrc_dll_calib_to_min_x1024',    dll_calib_to_min_x1024)  # 1
                                                                                             ),force,warn)
# reg odt_delay_hold,  0x5003 (default) always
        if BL==4:
            wr_odt_hold= 2 # recommended ug585:801
        elif BL==8:   
            wr_odt_hold= 4 # recommended ug585:801
        else: #BL==16?
            wr_odt_hold= 8 # guessed
        wr_odt_hold+=1     # actually for BL==8 was programmed 5, so increment by 1. Or is it for 8 only?
        if is_DDR2:    
            wr_odt_delay=WL-5
            if wr_odt_delay<0:
                wr_odt_delay=0
        else:
            wr_odt_delay=0
        ddrc_register_set.set_bitfields('odt_delay_hold',(
                                                     ('reg_ddrc_wr_odt_hold',          wr_odt_hold),       # 5
                                                #    ('reg_ddrc_rd_odt_hold',          0),                 # 0 - 'unused'
                                                     ('reg_ddrc_wr_odt_delay',         wr_odt_delay),      # 0
                                                #    ('reg_ddrc_rd_odt_delay',         0),                 # 3 - 'unused' - keep default
                                                                                             ),force,warn)
# reg  ctrl_reg1 - all 3 times 0x3e (default) 
        ddrc_register_set.set_bitfields('ctrl_reg1',(
                                                     ('reg_ddrc_selfref_en',            0),       # 0 Dynamic - 1 - go to Self Refresh when transaction store is empty  
                                                     ('reserved1',                      0),       # 0
                                                     ('reg_ddrc_dis_collision_page_opt',0),       # 0 Disable autoprecharge for collisions (write+write or read+write to the same address) when  reg_ddrc_dis_wc==1
                                                     ('reg_ddrc_dis_wc',                0),       # 0 1 - disable write combine, 0 - enable
                                                     ('reg_ddrc_refresh_update_level',  0),       # 0 Dynamic: toggle to indicate refresh register(s) update
                                                     ('reg_ddrc_auto_pre_en',           0),       # 0 1 - most R/W will be with autoprecharge
                                                     ('reg_ddrc_lpr_num_entries',       0x1f),    # 0x1f - (bit 6 ignored) (Size of low priority transaction store+1). HPR - 32 - this value
                                                     ('reg_ddrc_pageclose',             0)        # 0 1 - close bank if no transactions in the store for it, 0 - keep open until not needed by other
                                                                                          ),force,warn)
# reg  ctrl_reg2 0x20000 - all 3 times (default)
        ddrc_register_set.set_bitfields('ctrl_reg2',(
                                                     ('reg_arb_go2critical_en',         0x1),     # 0x1 0 - ignore "urgent" from AXI master, 1 - grant
                                                     ('reserved1',                      0),       # 0 
                                                     ('reg_ddrc_go2critical_hysteresis',0),       # 0 Latency of moving to critical state
                                                     ('reserved2',                      0),       # 0
                                                                                          ),force,warn)
# reg  ctrl_reg3 0x284141 - all 3 times (non-default, default=0x00284027)
        if is_DDR3: # other - N/A
            dfi_t_wlmrd= int(math.ceil(self.features.get_par_value('T_WLMRD')/tCK))
            rdlvl_rr  = 0x41 # default = 0x40 (Did not understand how to calculate, using actual for DDR3) 
            ddrc_register_set.set_bitfields('ctrl_reg3',(('reg_ddrc_dfi_t_wlmrd', dfi_t_wlmrd),
                                                         ('reg_ddrc_rdlvl_rr',    rdlvl_rr)),force,warn)   # 0x28 DDR3 only: tWLMRD from DRAM specs
        if is_DDR3 or is_LPDDR2: # DDR2 - N/A
            wrlvl_ww=RL+rdc_we_to_re_delay+50 #ug585:804
            ddrc_register_set.set_bitfields('ctrl_reg3',(('reg_ddrc_wrlvl_ww', wrlvl_ww)),force,warn)   # 0x41 (dflt 0x27) DDR3 and LPDDR2 - write  leveling write-to-write delay'
        
# reg  ctrl_reg4 0x1610 - all 3 times (default) - keeping
        ddrc_register_set.set_bitfields('ctrl_reg4',(
                                                     ('dfi_t_ctrlupd_interval_max_x1024',            0x16),       # 0x16 - maximal time between DFI update requests in 1024 clocks
                                                     ('dfi_t_ctrlupd_interval_min_x1024',            0x10),       # 0x10 - minimal time between DFI update requests in 1024 clocks
                                                                                          ),force,warn)
#     'rd_dll_force1':           {'OFFS': 0x070},
#     'wr_ratio_reg':            {'OFFS': 0x074},

# reg  ctrl_reg5 0x466111 - only 2 times set, but same default
        #CKE=  self.features.get_par_value('CKE') # 4 defined earlier
        CKSRE=  self.features.get_par_value('CKSRE') # 6
        CKSRX=  self.features.get_par_value('CKSRX') # 6
        if is_DDR3:
            t_ckesr=CKE+1 # contradicts dram_param_reg1 in actual settings - both have 0x4, but one - CKE, another CKE+1. Better safe than sorry, and SR exit is not that often
            t_cksrx=CKSRX
            t_cksre=CKSRE
        elif is_DDR2:
            t_ckesr=CKE
            t_cksrx=1
            t_cksre=1
        elif is_LPDDR2:
            t_ckesr=CKSRX
            t_cksrx=2
            t_cksre=2
        dfi_t_dram_clk_enable=1 # keeping defaults==actual for DDR3 - not clear what specs to use 
        dfi_t_dram_clk_disable=1 # keeping defaults==actual for DDR3 - not clear what specs to use
        dfi_t_ctrl_delay=1 # keeping defaults==actual for DDR3 - not clear what specs to use
        ddrc_register_set.set_bitfields('ctrl_reg5',(
                                                     ('reserved1',                       0  ),       # 0
                                                     ('reg_ddrc_t_ckesr',                t_ckesr),       # 0x4->5 Min CKE low for self refresh, recomm.: DDR3:tCKE+1,DDR2:tCKE,LPDDR2:tCKESR
                                                     ('reg_ddrc_t_cksrx',                t_cksrx),       # 0x6 CK valid before self refresh exit, recomm. DDR3:tCKSRX,DDR2:1,LPDDR2:2
                                                     ('reg_ddrc_t_cksre',                t_cksre),       # 0x6 CK valid after self refresh entry, recomm. DDR3:tCKSRE,DDR2:1,LPDDR2:2
                                                     ('reg_ddrc_dfi_t_dram_clk_enable',  dfi_t_dram_clk_enable),       # 0x1 deassert dfi_dram_clock disable to PHY clock enable in DFI clock cycles
                                                     ('reg_ddrc_dfi_t_dram_clk_disable', dfi_t_dram_clk_disable),       # 0x1 assert  dfi_dram_clock disable to PHY clock disable in DFI clock cycles
                                                     ('reg_ddrc_dfi_t_ctrl_delay',       dfi_t_ctrl_delay),       # 0x1 ssert/deassert  DFI control signals to PHY-DRAM control signals
                                                                                          ),force,warn)

# reg  ctrl_reg6 0x32222 - only 2 times set, but same default
# Keeping actual/defaults - all recommendations are listed for LPDDR2 only (tXP+2 for DDR3 would be 6 - does not match actual).
        ddrc_register_set.set_bitfields('ctrl_reg6',(
                                                     ('reserved1',            0),         # 0
                                                     ('reg_ddrc_t_ckcsx',     0x3),       # 0x3 Clock stable before exiting clock stop. Recommended for LPDDR2: tXP+2
                                                     ('reg_ddrc_t_ckdpdx',    0x2),       # 0x2 Clock stable before Deep Power Down exit. Recommended for LPDDR2: 2
                                                     ('reg_ddrc_t_ckdpde',    0x2),       # 0x2 Maintain clock after Deep Power Down entry. Recommended for LPDDR2: 2
                                                     ('reg_ddrc_t_ckpdx',     0x2),       # 0x2 Clock stable before Power Down exit. Recommended for LPDDR2: 2
                                                     ('reg_ddrc_t_ckpde',     0x2),       # 0x2 Maintain clock after Power Down entry. Recommended for LPDDR2: 2
                                                                                          ),force,warn)
# reg  che_refresh_timer01_reg dflt=0x00008000 = act 
        ddrc_register_set.set_bitfields('che_refresh_timer01_reg',(
                                                     ('refresh_timer1_start_value_x32',  0x8),# 0x8 reserved, do not modify
                                                     ('refresh_timer0_start_value_x32',  0),  # 0   reserved, do not modify
                                                                                          ),force,warn)

# reg  che_t_zq  dflt=0x10300802 act=0x10200802
        ZQCS=self.features.get_par_value('ZQCS')
        ZQCL=self.features.get_par_value('ZQCL')
        MOD= self.features.get_par_value('MOD')
        t_mod=max(MOD,512) # 128) # according to documentation should be 128, but actually it is set to 0x200
        dis_auto_zq=0 # default 0 - enable auto ZQ
        ddrc_register_set.set_bitfields('che_t_zq',(
                                                     ('reg_ddrc_t_zq_short_nop',  ZQCS), # 0x40 DDR3 and LPDDR2 only: number of NOP after ZQCS (ZQ calibration short)
                                                     ('reg_ddrc_t_zq_long_nop',   ZQCL), # 0x200 DDR3 and LPDDR2 only: number of NOP after ZQCL (ZQ calibration long)
                                                     ('reg_ddrc_t_mod',           t_mod), # 0x200 Mode register set command update delay >=0x80
                                                     ('reg_ddrc_ddr3',            (0,1)[is_DDR3]), # 0x1 0 - DDR2, 1 - DDR3
                                                     ('reg_ddrc_dis_auto_zq',     dis_auto_zq), # 0 DDR3 and LPDDR2 only: 1 - disable auto generation of ZQCS, 0 - enable'
                                                                                          ),force,warn)

# reg che_t_zq_short_interval_reg   dflt=0x0020003A act=0x690cb73
        rstn_x1024=              0x69   # using actual
        zq_short_interval_x1024= 0xcb73 # using actual
        ddrc_register_set.set_bitfields('che_t_zq_short_interval_reg',(
                                                     ('dram_rstn_x1024',            rstn_x1024), # 0x69 DDR3 only: Number of cycles to assert reset during init sequence (in 1024 cycles)
                                                     ('t_zq_short_interval_x1024',  zq_short_interval_x1024), # 0xcb73 DDR3 and LPDDR2 only: AVerage interval between automatic ZQCS in 1024 clock cycles
                                                                                     ),force,warn)

# reg deep_pwrdwn_reg       dflt=0 act=0x1fe
        deeppowerdown_to_x1024=0xff # LPDDR2 only, using actual
        ddrc_register_set.set_bitfields('deep_pwrdwn_reg',(
                                                     ('deeppowerdown_to_x1024',deeppowerdown_to_x1024), # 0xff LPDDR2 only: minimal deep power down time in 1024 clk (specs - 500usec)
                                                     ('deeppowerdown_en',            0), # 0 LPDDR2 only: 0 - normal, 1 - go to deep power down when transaction store is empty
                                                                                      ),force,warn)

# reg  reg_2c   dflt=0 act=0xffffff
        dfi_rdlvl_max_x1024=0xfff # using actual/recommended
        dfi_wrlvl_max_x1024=0xfff # using actual/recommended
        ddrc_register_set.set_bitfields('reg_2c',(
                                                     ('reg_ddrc_dfi_rd_data_eye_train', 0), # 0 DDR3 and LPDDR2 only: 1 - read data eye training (part of init sequence)
                                                     ('reg_ddrc_dfi_rd_dqs_gate_level', 0), # 0 1 - Read DQS gate leveling mode (DDR3 DFI only)
                                                     ('reg_ddrc_dfi_wr_level_en',       0), # 0 1 - Write leveling mode (DDR3 DFI only)
                                                     ('ddrc_reg_trdlvl_max_error',      0), # 0 READONLY: DDR3 and LPDDR2 only: leveling/gate training timeout (clear on write)
                                                     ('ddrc_reg_twrlvl_max_error',      0), # 0 READONLY: DDR3 only: write leveling timeout (clear on write) 
                                                     ('dfi_rdlvl_max_x1024',dfi_rdlvl_max_x1024), # 0xfff Read leveling maximal time in 1024 clk. Typical value 0xFFF
                                                     ('dfi_wrlvl_max_x1024',dfi_wrlvl_max_x1024), # 0xfff Write leveling maximal time in 1024 clk. Typical value 0xFFF
                                                                                          ),force,warn)

# reg   reg_2d   dflt=0x200 act=0x200
        ddrc_register_set.set_bitfields('reg_2d',(
                                                     ('reg_ddrc_dis_pre_bypass',  0),  # 0 reserved
                                                     ('reg_ddrc_skip_ocd',        0x1),# 0x1 should be 1, 0 is not supported. 1 - skip OCD adjustment step during DDR2 init,  use OCD_Default and OCD_exit
                                                     ('reg_ddrc_2t_delay',        0),  # 0 reserved
                                                                                   ),force,warn)

# reg  dfi_timimg  dflt=0x00200067 act=0x0x200066
        dfi_t_ctrlup_max=0x40 # using actual for (ddr3), not clear how to calculate
        dfi_t_ctrlup_min=0x3  # using actual for (ddr3), not clear how to calculate
        if is_DDR2 or is_DDR3:
            dfi_t_rddata_en=RL-1
        elif is_LPDDR2:
            dfi_t_rddata_en=RL
        ddrc_register_set.set_bitfields('dfi_timimg',(
                                                     ('reg_ddrc_dfi_t_ctrlup_max', dfi_t_ctrlup_max), # 0x40 Maximal number of clocks  ddrc_dfi_ctrlupd_req can assert
                                                     ('reg_ddrc_dfi_t_ctrlup_min', dfi_t_ctrlup_min), # 0x3 Minimal number of clocks  ddrc_dfi_ctrlupd_req must be asserted
                                                     ('reg_ddrc_dfi_t_rddata_en',  dfi_t_rddata_en), # 0x6 LPDDR2 - RL, DDR2 and DDR3 - RL-1
                                                                                     ),force,warn)
#ECC control, can probably be skipped?
        programECC = True        
        if programECC:
# reg  che_ecc_control_reg_offset (offs=0xc4) : 0 - always, ==dflt
            ddrc_register_set.set_bitfields('che_ecc_control_reg_offset',(
                                                     ('clear_correctable_dram_ecc_error', 0), # 0 1 - clear correctable log (valid+counters)
                                                     ('clear_uncorrectable_dram_ecc_error', 0), # 0  1 - clear uncorrectable log (valid+counters)
                                                                                     ),force,warn)

# reg che_corr_ecc_log_reg_offset (offs=0xc8): 0 - always, ==dflt
            ddrc_register_set.set_bitfields('che_corr_ecc_log_reg_offset',(
                                                     ('ecc_corrected_bit_num', 0), # 0 - encoded error bits for up to 72-bit data (clear on write)
#                                                     ('corr_ecc_log_valid', 0), # 0 - READONLY corr_ecc_log_valid
                                                                                     ),force,warn)

# reg che_corr_ecc_addr_reg_offset: READONLY  
#        ddrc_register_set.set_bitfields('che_corr_ecc_addr_reg_offset',(
#                                                     ('corr_ecc_log_bank', 0), # 0
#                                                     ('corr_ecc_log_row', 0), # 0
#                                                     ('corr_ecc_log_col', 0), # 0
#                                                                                     ),force,warn)

# reg che_corr_ecc_data_31_0_reg_offset: READONLY                                                                                   
#            ddrc_register_set.set_bitfields('che_corr_ecc_data_31_0_reg_offset',(('corr_ecc_dat_31_0', 0)),force,warn)

# reg  che_corr_ecc_data_63_32_reg_offset: READONLY
#            ddrc_register_set.set_bitfields('che_corr_ecc_data_63_32_reg_offset',(('corr_ecc_dat_63_32', 0)),force,warn) #0 bits[32:63] of the word with correctable ECC error. actually all are 0'

# reg  che_corr_ecc_data_71_64_reg_offset: READONLY
#            ddrc_register_set.set_bitfields('che_corr_ecc_data_71_64_reg_offset',(('corr_ecc_dat_71_64', 0)),force,warn) #0 bits[64:71] of the word with correctable ECC error. only lower 5 bits have data, the rest are 0

# reg  che_uncorr_ecc_log_reg_offset (offset=0xdc): READONLY 
#            ddrc_register_set.set_bitfields('che_uncorr_ecc_log_reg_offset',(('uncorr_ecc_log_valid', 0)),force,warn) # Set to 1 when uncorrectable error is capture (no more captured until cleared), cleared by che_ecc_control_reg_offset

# reg che_uncorr_ecc_addr_reg_offset : READONLY
#            ddrc_register_set.set_bitfields('che_uncorr_ecc_addr_reg_offset',(
#                                                     ('uncorr_ecc_log_bank', 0), # 0
#                                                     ('uncorr_ecc_log_row', 0), # 0
#                                                     ('uncorr_ecc_log_col', 0)),force,warn) , # 0

# reg uncorr_ecc_dat_31_0: READONLY       
#            ddrc_register_set.set_bitfields('uncorr_ecc_dat_31_0',(('reserved1', 0)),force,warn) # bits[0:31] of the word with uncorrectable ECC error. actually only 0:7 have valid data, 8:31 are 0

# reg  che_uncorr_ecc_data_63_32_reg_offset: READONLY
#            ddrc_register_set.set_bitfields('che_uncorr_ecc_data_63_32_reg_offset',(('reserved1', 0)),force,warn) # bits[32:63] of the word with uncorrectable ECC error. actually all are 0

# reg  che_uncorr_ecc_data_71_64_reg_offset: READONLY
#            ddrc_register_set.set_bitfields('che_uncorr_ecc_data_71_64_reg_offset',(('reserved1', 0)),force,warn) # bits[64:71] of the word with uncorrectable ECC error. only lower 5 bits have data, the rest are 0

# reg  che_ecc_stats_reg_offset (offset=0xf0): Clear on write
#     'che_ecc_stats_reg_offset':{'OFFS': 0x0F0,'DFLT':0x00000000,'RW':'CW', 'FIELDS':{ # 0x0
#                   'stat_num_corr_err':                {'r':( 8,15),'d':0,'m':'R','c':'Number of correctable ECC errors since 1 written to bit 1 of che_ecc_control_reg_offset (0xC4)'},       
#                   'stat_num_uncorr_err':              {'r':( 0, 7),'d':0,'m':'R','c':'Number of uncorrectable ECC errors since 1 written to bit 0 of che_ecc_control_reg_offset (0xC4)'}}},
            ddrc_register_set.set_bitfields('che_ecc_stats_reg_offset',(
                                                     ('stat_num_corr_err', 0), # Number of correctable ECC errors since 1 written to bit 1 of che_ecc_control_reg_offset (0xC4)
                                                     ('stat_num_uncorr_err', 0), # Number of uncorrectable ECC errors since 1 written to bit 0 of che_ecc_control_reg_offset (0xC4)
                                                                                     ),force,warn)
# reg  offs=0x0F8 che_ecc_corr_bit_mask_31_0_reg_offset : READONLY
#            ddrc_register_set.set_bitfields('che_ecc_corr_bit_mask_31_0_reg_offset',(('ddrc_reg_ecc_corr_bit_mask', 0)),force,warn) # bits[0:31] of the mask of the corrected data (1 - corrected, 0 - uncorrected). Only 0:7 have valid data, 8:31 are 0

# reg  offs=0x0FC che_ecc_corr_bit_mask_63_32_reg_offset : READONLY
#            ddrc_register_set.set_bitfields('che_ecc_corr_bit_mask_63_32_reg_offset',(('ddrc_reg_ecc_corr_bit_mask', 0)),force,warn) #bits[32:63] of the mask of the corrected data (1 - corrected, 0 - uncorrected). all bits are 0
# end of  if useECC:
# reg  ecc_scrub, offs=0x0F4 dflt:0x8 actual:0x8 (apply even with ECC disabled?)
#        
        ecc_mode=(0,4)[self.features.get_par_value('ECC')]
        ddrc_register_set.set_bitfields('ecc_scrub',(
                                                     ('reg_ddrc_dis_scrub', 1), # 1 1 - disable ECC scrubs, 0 - enable ECC scrubs
                                                     ('reg_ddrc_ecc_mode',  ecc_mode), # 0 DRAM ECC mode. Valid only 0(no ECC)  and 0x4 - "SEC/DED over 1-beat
                                                                                     ),force,warn)
# reg  phy_rcvr_enable, offs=0x114 dflt:0 actual:0
#     'phy_rcvr_enable':         {'OFFS': 0x114,'DFLT':0x00000000,'RW':'RW','FIELDS':{ # 0x0
#                   'reg_phy_dif_off':                  {'r':( 4, 7),'d':0,'c':'"Off" value of the drive of the receiver-enabled pins'},       
#                   'reg_phy_dif_on':                   {'r':( 0, 3),'d':0,'c':'"On" value of the drive of the receiver-enabled pins'}}},
        ddrc_register_set.set_bitfields('phy_rcvr_enable',(
                                                     ('reg_phy_dif_off', 0), # 0 - "Off" value of the drive of the receiver-enabled pins
                                                     ('reg_phy_dif_on', 0),  # 0 - "On" value of the drive of the receiver-enabled pins
                                                                                     ),force,warn)
#PHY configuration for each of 4 8-bit dta slices, I guess:
        slice_in_use0=1
        slice_in_use1=1
        slice_in_use2=(1,0)[half_width]
        slice_in_use3=(1,0)[half_width]

# reg  phy_config0, offs=0x118 dflt:0x40000001 actual:0x40000001
        ddrc_register_set.set_bitfields('phy_config0',( # PHY configuration for data slice 0
                                                     ('reg_phy_dq_offset',    0x40),  # 0x40  Offset value of DQS to DQ during write leveling of data slice 0. Default is 0x40 for 90-degree shift 
                                                     ('reg_phy_bist_err_clr',    0),  # 
                                                     ('reg_phy_bist_shift_dq',   0),  # 
                                                     ('reg_phy_board_lpbk_rx',   0),  # 
                                                     ('reg_phy_board_lpbk_tx',   0),  # 
                                                     ('reg_phy_wrlvl_inc_mode',  0),  # 
                                                     ('reg_phy_gatelvl_inc_mode',0),  # 
                                                     ('reg_phy_rdlvl_inc_mode',  0),  # 
                                                     ('reg_phy_rdlvl_inc_mode',  0),  # 
                                                     ('reg_phy_data_slice_in_use',slice_in_use0), # 1 Data bus width for read FIFO generation. 0 - read data responses are ignored, 1 - data slice 0 is valid (always 1)
                                                                                     ),force,warn)

# reg  phy_config1, offs=0x11c dflt:0x40000001 actual:0x40000001
        ddrc_register_set.set_bitfields('phy_config1',( # PHY configuration for data slice 0
                                                     ('reg_phy_dq_offset',    0x40),  # 0x40  Offset value of DQS to DQ during write leveling of data slice 1. Default is 0x40 for 90-degree shift 
                                                     ('reg_phy_bist_err_clr',    0),  # 
                                                     ('reg_phy_bist_shift_dq',   0),  # 
                                                     ('reg_phy_board_lpbk_rx',   0),  # 
                                                     ('reg_phy_board_lpbk_tx',   0),  # 
                                                     ('reg_phy_wrlvl_inc_mode',  0),  # 
                                                     ('reg_phy_gatelvl_inc_mode',0),  # 
                                                     ('reg_phy_rdlvl_inc_mode',  0),  # 
                                                     ('reg_phy_rdlvl_inc_mode',  0),  # 
                                                     ('reg_phy_data_slice_in_use',slice_in_use1), # 1 Data bus width for read FIFO generation. 0 - read data responses are ignored, 1 - data slice 1 is valid (always 1)
                                                                                     ),force,warn)
# reg  phy_config2, offs=0x120 dflt:0x40000001 actual:0x40000001
        ddrc_register_set.set_bitfields('phy_config2',( # PHY configuration for data slice 0
                                                     ('reg_phy_dq_offset',    0x40),  # 0x40  Offset value of DQS to DQ during write leveling of data slice 2. Default is 0x40 for 90-degree shift 
                                                     ('reg_phy_bist_err_clr',    0),  # 
                                                     ('reg_phy_bist_shift_dq',   0),  # 
                                                     ('reg_phy_board_lpbk_rx',   0),  # 
                                                     ('reg_phy_board_lpbk_tx',   0),  # 
                                                     ('reg_phy_wrlvl_inc_mode',  0),  # 
                                                     ('reg_phy_gatelvl_inc_mode',0),  # 
                                                     ('reg_phy_rdlvl_inc_mode',  0),  # 
                                                     ('reg_phy_rdlvl_inc_mode',  0),  # 
                                                     ('reg_phy_data_slice_in_use',slice_in_use2), # 1 Data bus width for read FIFO generation. 0 - read data responses are ignored, 1 - data slice 2 is valid (always 1)
                                                                                     ),force,warn)
# reg  phy_config3, offs=0x124 dflt:0x40000001 actual:0x40000001
        ddrc_register_set.set_bitfields('phy_config3',( # PHY configuration for data slice 0
                                                     ('reg_phy_dq_offset',    0x40),  # 0x40  Offset value of DQS to DQ during write leveling of data slice 3. Default is 0x40 for 90-degree shift 
                                                     ('reg_phy_bist_err_clr',    0),  # 
                                                     ('reg_phy_bist_shift_dq',   0),  # 
                                                     ('reg_phy_board_lpbk_rx',   0),  # 
                                                     ('reg_phy_board_lpbk_tx',   0),  # 
                                                     ('reg_phy_wrlvl_inc_mode',  0),  # 
                                                     ('reg_phy_gatelvl_inc_mode',0),  # 
                                                     ('reg_phy_rdlvl_inc_mode',  0),  # 
                                                     ('reg_phy_rdlvl_inc_mode',  0),  # 
                                                     ('reg_phy_data_slice_in_use',slice_in_use3), # 1 Data bus width for read FIFO generation. 0 - read data responses are ignored, 1 - data slice 3 is valid (always 1)
                                                                                     ),force,warn)
# reg  phy_init_ratio0, offs=0x12C dflt:0x0 actual: 0x0
        ddrc_register_set.set_bitfields('phy_init_ratio0',( # PHY init ratio register for data slice 0
                                                     ('reg_phy_gatelvl_init_ratio',  0),  # 0 User-programmable init ratio used by Gate Leveling FSM, data slice 0
                                                     ('reg_phy_wrlvl_init_ratio',    0),  # 0 User-programmable init ratio used by Write Leveling FSM, data slice 0
                                                                                     ),force,warn)
# reg  phy_init_ratio1, offs=0x130 dflt:0x0 actual: 0x0
        ddrc_register_set.set_bitfields('phy_init_ratio1',( # PHY init ratio register for data slice 1
                                                     ('reg_phy_gatelvl_init_ratio',  0),  # 0 User-programmable init ratio used by Gate Leveling FSM, data slice 1
                                                     ('reg_phy_wrlvl_init_ratio',    0),  # 0 User-programmable init ratio used by Write Leveling FSM, data slice 1
                                                                                     ),force,warn)
# reg  phy_init_ratio2, offs=0x134 dflt:0x0 actual: 0x0
        ddrc_register_set.set_bitfields('phy_init_ratio2',( # PHY init ratio register for data slice 2
                                                     ('reg_phy_gatelvl_init_ratio',  0),  # 0 User-programmable init ratio used by Gate Leveling FSM, data slice 2
                                                     ('reg_phy_wrlvl_init_ratio',    0),  # 0 User-programmable init ratio used by Write Leveling FSM, data slice 2
                                                                                     ),force,warn)
# reg  phy_init_ratio3, offs=0x138 dflt:0x0 actual: 0x0
        ddrc_register_set.set_bitfields('phy_init_ratio3',( # PHY init ratio register for data slice 3
                                                     ('reg_phy_gatelvl_init_ratio',  0),  # 0 User-programmable init ratio used by Gate Leveling FSM, data slice 3
                                                     ('reg_phy_wrlvl_init_ratio',    0),  # 0 User-programmable init ratio used by Write Leveling FSM, data slice 3
                                                                                     ),force,warn)
        dqs_slave_ratio0=0x35 # default=40
        dqs_slave_ratio1=0x35 # default=40
        dqs_slave_ratio2=0x35 # default=40
        dqs_slave_ratio3=0x35 # default=40
# reg  phy_rd_dqs_cfg0, offs=0x140 dflt:0x40 actual: 0x35
        ddrc_register_set.set_bitfields('phy_rd_dqs_cfg0',( # PHY read DQS configuration register for data slice 0
                                                     ('reg_phy_rd_dqs_slave_delay',    0),  # 0 If reg_phy_rd_dqs_slave_force is 1, use this tap/delay value for read DQS slave DLL, data slice 0
                                                     ('reg_phy_rd_dqs_slave_force',    0),  # 0 0 - use reg_phy_rd_dqs_slave_ratio  for the read DQS slave DLL, 1 - use provided in reg_phy_rd_dqs_slave_delay, data slice 0
                                                     ('reg_phy_rd_dqs_slave_ratio', dqs_slave_ratio0),  # 0x35 Fraction of the clock cycle (256 = full period) for the read DQS slave DLL, data slice 0
                                                                                     ),force,warn)
# reg  phy_rd_dqs_cfg1, offs=0x144 dflt:0x40 actual: 0x35
        ddrc_register_set.set_bitfields('phy_rd_dqs_cfg1',( # PHY read DQS configuration register for data slice 1
                                                     ('reg_phy_rd_dqs_slave_delay',    0),  # 0 If reg_phy_rd_dqs_slave_force is 1, use this tap/delay value for read DQS slave DLL, data slice 1
                                                     ('reg_phy_rd_dqs_slave_force',    0),  # 0 0 - use reg_phy_rd_dqs_slave_ratio  for the read DQS slave DLL, 1 - use provided in reg_phy_rd_dqs_slave_delay, data slice 1
                                                     ('reg_phy_rd_dqs_slave_ratio', dqs_slave_ratio1),  # 0x35 Fraction of the clock cycle (256 = full period) for the read DQS slave DLL, data slice 1
                                                                                     ),force,warn)
# reg  phy_rd_dqs_cfg2, offs=0x148 dflt:0x40 actual: 0x35
        ddrc_register_set.set_bitfields('phy_rd_dqs_cfg2',( # PHY read DQS configuration register for data slice 2
                                                     ('reg_phy_rd_dqs_slave_delay',    0),  # 0 If reg_phy_rd_dqs_slave_force is 1, use this tap/delay value for read DQS slave DLL, data slice 2
                                                     ('reg_phy_rd_dqs_slave_force',    0),  # 0 0 - use reg_phy_rd_dqs_slave_ratio  for the read DQS slave DLL, 1 - use provided in reg_phy_rd_dqs_slave_delay, data slice 2
                                                     ('reg_phy_rd_dqs_slave_ratio', dqs_slave_ratio2),  # 0x35 Fraction of the clock cycle (256 = full period) for the read DQS slave DLL, data slice 2
                                                                                     ),force,warn)
# reg  phy_rd_dqs_cfg3, offs=0x14c dflt:0x40 actual: 0x35
        ddrc_register_set.set_bitfields('phy_rd_dqs_cfg3',( # PHY read DQS configuration register for data slice 3
                                                     ('reg_phy_rd_dqs_slave_delay',    0),  # 0 If reg_phy_rd_dqs_slave_force is 1, use this tap/delay value for read DQS slave DLL, data slice 3
                                                     ('reg_phy_rd_dqs_slave_force',    0),  # 0 0 - use reg_phy_rd_dqs_slave_ratio  for the read DQS slave DLL, 1 - use provided in reg_phy_rd_dqs_slave_delay, data slice 3
                                                     ('reg_phy_rd_dqs_slave_ratio', dqs_slave_ratio3),  # 0x35 Fraction of the clock cycle (256 = full period) for the read DQS slave DLL, data slice 3
                                                                                     ),force,warn)
# reg  phy_wr_dqs_cfg0, offs=0x154 dflt:0 actual: 0
        ddrc_register_set.set_bitfields('phy_wr_dqs_cfg0',( # ,PHY write DQS configuration register for data slice 0
                                                     ('reg_phy_wr_dqs_slave_delay',  0),  # 0 If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 0
                                                     ('reg_phy_wr_dqs_slave_force',  0),  # 0 0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 0
                                                     ('reg_phy_wr_dqs_slave_ratio',  0),  # 0 Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 0. Program manual training ratio
                                                                                     ),force,warn)
# reg  phy_wr_dqs_cfg0, offs=0x158 dflt:0 actual: 0
        ddrc_register_set.set_bitfields('phy_wr_dqs_cfg1',( # ,PHY write DQS configuration register for data slice 1
                                                     ('reg_phy_wr_dqs_slave_delay',  0),  # 0 If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 1
                                                     ('reg_phy_wr_dqs_slave_force',  0),  # 0 0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 1
                                                     ('reg_phy_wr_dqs_slave_ratio',  0),  # 0 Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 1. Program manual training ratio
                                                                                     ),force,warn)
# reg  phy_wr_dqs_cfg0, offs=0x15c dflt:0 actual: 0
        ddrc_register_set.set_bitfields('phy_wr_dqs_cfg2',( # ,PHY write DQS configuration register for data slice 2
                                                     ('reg_phy_wr_dqs_slave_delay',  0),  # 0 If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 2
                                                     ('reg_phy_wr_dqs_slave_force',  0),  # 0 0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 2
                                                     ('reg_phy_wr_dqs_slave_ratio',  0),  # 0 Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 2. Program manual training ratio
                                                                                     ),force,warn)
# reg  phy_wr_dqs_cfg0, offs=0x160 dflt:0 actual: 0
        ddrc_register_set.set_bitfields('phy_wr_dqs_cfg3',( # ,PHY write DQS configuration register for data slice 3
                                                     ('reg_phy_wr_dqs_slave_delay',  0),  # 0 If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write DQS slave DLL, data slice 3
                                                     ('reg_phy_wr_dqs_slave_force',  0),  # 0 0 - use reg_phy_wr_dqs_slave_ratio  for the write DQS slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 3
                                                     ('reg_phy_wr_dqs_slave_ratio',  0),  # 0 Fraction of the clock cycle (256 = full period) for the write DQS slave DLL, data slice 3. Program manual training ratio
                                                                                     ),force,warn)
        fifo_we_slave_ratio0=0x35 # default=40
        fifo_we_slave_ratio1=0x35 # default=40
        fifo_we_slave_ratio2=0x35 # default=40
        fifo_we_slave_ratio3=0x35 # default=40
        
# reg  phy_we_cfg0, offs=0x168 dflt:0x40 actual: 0x35
        ddrc_register_set.set_bitfields('phy_we_cfg0',( # PHY FIFO write enable configuration register for data slice 0
                                                     ('reg_phy_fifo_we_in_delay',  0),  # 0 If reg_phy_fifo_we_in_force is 1, use this tap/delay value for fifo_we_0 slave DLL, data slice 0
                                                     ('reg_phy_fifo_we_in_force',  0),  # 0 0 - use reg_phy_fifo_we_slave_ratio for fifo_we_0 slave DLL, 1 - use provided in reg_phy_fifo_we_in_delay, data slice 0
                                                     ('reg_phy_fifo_we_slave_ratio',fifo_we_slave_ratio0),  # 0x35 Fraction of the clock cycle (256 = full period) for fifo_we_0 slave DLL, data slice 0. Program manual training ratio
                                                                                     ),force,warn)
# reg  phy_we_cfg0, offs=0x16c dflt:0x40 actual: 0x35
        ddrc_register_set.set_bitfields('phy_we_cfg1',( # PHY FIFO write enable configuration register for data slice 1
                                                     ('reg_phy_fifo_we_in_delay',  0),  # 0 If reg_phy_fifo_we_in_force is 1, use this tap/delay value for fifo_we_0 slave DLL, data slice 1
                                                     ('reg_phy_fifo_we_in_force',  0),  # 0 0 - use reg_phy_fifo_we_slave_ratio for fifo_we_0 slave DLL, 1 - use provided in reg_phy_fifo_we_in_delay, data slice 1
                                                     ('reg_phy_fifo_we_slave_ratio',fifo_we_slave_ratio1),  # 0x35 Fraction of the clock cycle (256 = full period) for fifo_we_0 slave DLL, data slice 1. Program manual training ratio
                                                                                     ),force,warn)
# reg  phy_we_cfg0, offs=0x170 dflt:0x40 actual: 0x35
        ddrc_register_set.set_bitfields('phy_we_cfg2',( # PHY FIFO write enable configuration register for data slice 2
                                                     ('reg_phy_fifo_we_in_delay',  0),  # 0 If reg_phy_fifo_we_in_force is 1, use this tap/delay value for fifo_we_0 slave DLL, data slice 2
                                                     ('reg_phy_fifo_we_in_force',  0),  # 0 0 - use reg_phy_fifo_we_slave_ratio for fifo_we_0 slave DLL, 1 - use provided in reg_phy_fifo_we_in_delay, data slice 2
                                                     ('reg_phy_fifo_we_slave_ratio',fifo_we_slave_ratio2),  # 0x35 Fraction of the clock cycle (256 = full period) for fifo_we_0 slave DLL, data slice 2. Program manual training ratio
                                                                                     ),force,warn)
# reg  phy_we_cfg0, offs=0x174 dflt:0x40 actual: 0x35
        ddrc_register_set.set_bitfields('phy_we_cfg3',( # PHY FIFO write enable configuration register for data slice 3
                                                     ('reg_phy_fifo_we_in_delay',  0),  # 0 If reg_phy_fifo_we_in_force is 1, use this tap/delay value for fifo_we_0 slave DLL, data slice 3
                                                     ('reg_phy_fifo_we_in_force',  0),  # 0 0 - use reg_phy_fifo_we_slave_ratio for fifo_we_0 slave DLL, 1 - use provided in reg_phy_fifo_we_in_delay, data slice 3
                                                     ('reg_phy_fifo_we_slave_ratio',fifo_we_slave_ratio3),  # 0x35 Fraction of the clock cycle (256 = full period) for fifo_we_0 slave DLL, data slice 3. Program manual training ratio
                                                                                     ),force,warn)
        wr_data_slave_ratio0=0x40
        wr_data_slave_ratio1=0x40
        wr_data_slave_ratio2=0x40
        wr_data_slave_ratio3=0x40
# reg  wr_data_slv0, offs=0x17c dflt:0x80 actual: 0x40
        ddrc_register_set.set_bitfields('wr_data_slv0',( # PHY write data slave ratio configuration register for data slice 0
                                                     ('reg_phy_wr_data_slave_delay',  0),  # 0 If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write data slave DLL, data slice 0
                                                     ('reg_phy_wr_data_slave_force',  0),  # 0 0 - use reg_phy_wr_dqs_slave_ratio  for the write data slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 0
                                                     ('reg_phy_wr_data_slave_ratio',wr_data_slave_ratio0),  # 0x40 Fraction of the clock cycle (256 = full period) for the write data slave DLL, data slice 0. Program manual training ratio
                                                                                     ),force,warn)
# reg  wr_data_slv1, offs=0x180 dflt:0x80 actual: 0x40
        ddrc_register_set.set_bitfields('wr_data_slv1',( # PHY write data slave ratio configuration register for data slice 1
                                                     ('reg_phy_wr_data_slave_delay',  0),  # 0 If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write data slave DLL, data slice 1
                                                     ('reg_phy_wr_data_slave_force',  0),  # 0 0 - use reg_phy_wr_dqs_slave_ratio  for the write data slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 1
                                                     ('reg_phy_wr_data_slave_ratio',wr_data_slave_ratio1),  # 0x40 Fraction of the clock cycle (256 = full period) for the write data slave DLL, data slice 1. Program manual training ratio
                                                                                     ),force,warn)
# reg  wr_data_slv2, offs=0x184 dflt:0x80 actual: 0x40
        ddrc_register_set.set_bitfields('wr_data_slv2',( # PHY write data slave ratio configuration register for data slice 2
                                                     ('reg_phy_wr_data_slave_delay',  0),  # 0 If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write data slave DLL, data slice 2
                                                     ('reg_phy_wr_data_slave_force',  0),  # 0 0 - use reg_phy_wr_dqs_slave_ratio  for the write data slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 2
                                                     ('reg_phy_wr_data_slave_ratio',wr_data_slave_ratio2),  # 0x40 Fraction of the clock cycle (256 = full period) for the write data slave DLL, data slice 2. Program manual training ratio
                                                                                     ),force,warn)
# reg  wr_data_slv3, offs=0x188 dflt:0x80 actual: 0x40
        ddrc_register_set.set_bitfields('wr_data_slv3',( # PHY write data slave ratio configuration register for data slice 3
                                                     ('reg_phy_wr_data_slave_delay',  0),  # 0 If reg_phy_wr_dqs_slave_force is 1, use this tap/delay value for write data slave DLL, data slice 3
                                                     ('reg_phy_wr_data_slave_force',  0),  # 0 0 - use reg_phy_wr_dqs_slave_ratio  for the write data slave DLL, 1 - use provided in reg_phy_wr_dqs_slave_delay, data slice 3
                                                     ('reg_phy_wr_data_slave_ratio',wr_data_slave_ratio3),  # 0x40 Fraction of the clock cycle (256 = full period) for the write data slave DLL, data slice 3. Program manual training ratio
                                                                                     ),force,warn)
# reg  reg_64, offs=0x190 dflt:0x10020000 actual:0x20000(first time)-0x10020000-0x10020000
        use_rank0_delays = 1 # marked as reserved, but actually is first set to 0 - maybe not needed
        phy_lpddr=       (0,1)[is_LPDDR2]
        ctrl_slave_ratio=0x80 # defualt/actual
        sel_logic       = 0 # Read leveling algorithm select - 0:algorithm 1, 1: algorithm 2 
        ddrc_register_set.set_bitfields('reg_64',( # Training control 2
                                                     ('reg_phy_int_lpbk',          0),  # reserved
                                                     ('reg_phy_cmd_latency',       0),  # 1: Delay command to PHY by a FF
                                                     ('reg_phy_lpddr',     phy_lpddr),  # 0: DDR2/DDR3, 1 - LPDDR2
                                                     ('reg_phy_use_rank0_delays', use_rank0_delays),  # reserved
                                                     ('reg_phy_ctrl_slave_delay',  0),  # when reg_phy_rd_dqs_slave_force==1 this value (combined with bits 18:19 of reg_65) set address/command slave DLL
                                                     ('reg_phy_ctrl_slave_force',  0),  # 0:use reg_phy_ctrl_slave_ratio for addr/cmd slave DLL, 1 - overwrite with reg_phy_ctrl_slave_delay
                                                     ('reg_phy_ctrl_slave_ratio',ctrl_slave_ratio), # address/command delay in clock/256
                                                     ('reg_phy_sel_logic', sel_logic),  # Read leveling algorithm select - 0:algorithm 1, 1: algorithm 2
                                                     ('reg_phy_all_dq_mpr_rd_resp',0),  # reserved
                                                     ('reg_phy_invert_clkout',     0),  # 1 - invert clock polarity to DRAM
                                                     ('reg_phy_bist_mode',         0),  # reserved
                                                     ('reg_phy_bist_force_err',    0),  # reserved
                                                     ('reg_phy_bist_enable',       0),  # reserved
                                                     ('reg_phy_at_spd_atpg',       0),  # reserved
                                                     ('reg_phy_bl2',               0),  # reserved
                                                     ('reg_phy_loopback',          0),  # reserved
                                                                                     ),force,warn)
# reg  reg_65, offs=0x194 dflt:0 actual: 0x3c82
        dll_lock_diff =         0xf #default/actual
        rd_rl_delay   = max(RL-3,1) # 0x4
        wr_rl_delay   = max(WL-4,1) # 0x2
        
# TODO: Maybe more changes are needed to use training, generate ps7* with training enabled and compare results
        ddrc_register_set.set_bitfields('reg_65',( # Training control 3
                                                     ('reg_phy_ctrl_slave_delay',                         0),  # when reg_phy_rd_dqs_slave_force==1 this value (combined with bits 21:27 of reg_64) set address/command slave DLL'},
                                                     ('reg_phy_dis_calib_rst',                            0),  # disable dll_calib from resetting Read Capture FIFO
                                                     ('reg_phy_use_rd_data_eye_level',use_rd_data_eye_level),  # Read Data Eye training control - 0 use fixed register data, 1 use data eye leveling data
                                                     ('reg_phy_use_rd_dqs_gate_level',use_rd_dqs_gate_level),  # Read DQS Gate training control: 0 - used fixed data, 1 - use calculated data
                                                     ('reg_phy_use_wr_level',                  use_wr_level),  # Write leveling control: 0 - used programmed register data, 1 - use calculated data
                                                     ('reg_phy_dll_lock_diff',                dll_lock_diff),  # 0xf Maximal number of DLL taps before DLL deasserts lock
                                                     ('reg_phy_rd_rl_delay',                    rd_rl_delay),  # 0x4
                                                     ('reg_phy_wr_rl_delay',                    wr_rl_delay),  # 0x2
                                                                                     ),force,warn)




# reg  page_mask, offs=0x204 dflt:0 actual: 0
#        page_addr_mask=0 # disable prioritization based on page/bank match 
        ddrc_register_set.set_bitfields('page_mask',( # Arbiter Page Mask
                                                     ('reg_arb_page_addr_mask',page_addr_mask),  # Arbiter page hit/miss: 0 - column address, 1 - row/bank address (applies to 64-bit address, not byte addr)
                                                                                     ),force,warn)

        arb_pri_wr_port0=0x3ff # lowest 
        arb_pri_wr_port1=0x3ff # lowest 
        arb_pri_wr_port2=0x3ff # lowest 
        arb_pri_wr_port3=0x3ff # lowest 
# reg  axi_priority_wr_port0, offs=0x208 dflt:0x803FF actual: 0x803ff
        ddrc_register_set.set_bitfields('axi_priority_wr_port0',( # AXI priority control for write port 0
                                                     ('reserved1',                     0x1),  # 0x1
                                                     ('reg_arb_dis_page_match_wr_portn', 0),  # Disable page match feature
                                                     ('reg_arb_disable_urgent_wr_portn', 0),  # Disable urgent for this Write Port
                                                     ('reg_arb_disable_aging_wr_portn',  0),  # Disable aging for this Write Port
                                                     ('reserved2',                       0),  #
                                                     ('reg_arb_pri_wr_portn',arb_pri_wr_port0),  # 0x3ff Priority for this write port, >=4, lower value - higher priority
                                                                                            ),force,warn)

# reg  axi_priority_wr_port1, offs=0x20c dflt:0x803FF actual: 0x803ff
        ddrc_register_set.set_bitfields('axi_priority_wr_port1',( # AXI priority control for write port 1
                                                     ('reserved1', 0x1),  # 0x1
                                                     ('reserved1',                     0x1),  # 0x1
                                                     ('reg_arb_dis_page_match_wr_portn', 0),  # Disable page match feature
                                                     ('reg_arb_disable_urgent_wr_portn', 0),  # Disable urgent for this Write Port
                                                     ('reg_arb_disable_aging_wr_portn',  0),  # Disable aging for this Write Port
                                                     ('reserved2',                       0),  #
                                                     ('reg_arb_pri_wr_portn',arb_pri_wr_port1),  # 0x3ff Priority for this write port, >=4, lower value - higher priority
                                                                                            ),force,warn)
# reg  axi_priority_wr_port2, offs=0x210 dflt:0x803FF actual: 0x803ff
        ddrc_register_set.set_bitfields('axi_priority_wr_port2',( # AXI priority control for write port 2
                                                     ('reserved1',                     0x1),  # 0x1
                                                     ('reg_arb_dis_page_match_wr_portn', 0),  # Disable page match feature
                                                     ('reg_arb_disable_urgent_wr_portn', 0),  # Disable urgent for this Write Port
                                                     ('reg_arb_disable_aging_wr_portn',  0),  # Disable aging for this Write Port
                                                     ('reserved2',                       0),  #
                                                     ('reg_arb_pri_wr_portn',arb_pri_wr_port2),  # 0x3ff Priority for this write port, >=4, lower value - higher priority
                                                                                            ),force,warn)
# reg  axi_priority_wr_port3, offs=0x214 dflt:0x803FF actual: 0x803ff
        ddrc_register_set.set_bitfields('axi_priority_wr_port3',( # AXI priority control for write port 3
                                                     ('reserved1',                     0x1),  # 0x1
                                                     ('reg_arb_dis_page_match_wr_portn', 0),  # Disable page match feature
                                                     ('reg_arb_disable_urgent_wr_portn', 0),  # Disable urgent for this Write Port
                                                     ('reg_arb_disable_aging_wr_portn',  0),  # Disable aging for this Write Port
                                                     ('reserved2',                       0),  #
                                                     ('reg_arb_pri_wr_portn',arb_pri_wr_port3),  # 0x3ff Priority for this write port, >=4, lower value - higher priority
                                                                                            ),force,warn)
        arb_pri_rd_port0=0x3ff # lowest
        arb_pri_rd_port1=0x3ff # lowest
        arb_pri_rd_port2=0x3ff # lowest
        arb_pri_rd_port3=0x3ff # lowest
# reg  axi_priority_rd_port0, offs=0x218 dflt:0x3ff actual: 0x3ff
        ddrc_register_set.set_bitfields('axi_priority_rd_port0',( # AXI priority control for read port 0
                                                     ('reg_arb_set_hpr_rd_portn',        0),  # Enable reads to be HPR for this port
                                                     ('reg_arb_dis_page_match_rd_portn', 0),  # Disable page match feature
                                                     ('reg_arb_disable_urgent_rd_portn', 0),  # Disable urgent for this Read Port
                                                     ('reg_arb_disable_aging_rd_portn',  0),  # Disable aging for this Read Port
                                                     ('reserved1',                       0),  #
                                                     ('reg_arb_pri_rd_portn',arb_pri_rd_port0),  # 0x3ff Priority for this Read port, lower value - higher priority
                                                                                            ),force,warn)
# reg  axi_priority_rd_port1, offs=0x21c dflt:0x3ff actual: 0x3ff
        ddrc_register_set.set_bitfields('axi_priority_rd_port1',( # AXI priority control for read port 1
                                                     ('reg_arb_set_hpr_rd_portn',        0),  # Enable reads to be HPR for this port
                                                     ('reg_arb_dis_page_match_rd_portn', 0),  # Disable page match feature
                                                     ('reg_arb_disable_urgent_rd_portn', 0),  # Disable urgent for this Read Port
                                                     ('reg_arb_disable_aging_rd_portn',  0),  # Disable aging for this Read Port
                                                     ('reserved1',                       0),  #
                                                     ('reg_arb_pri_rd_portn',arb_pri_rd_port1),  # 0x3ff Priority for this Read port, lower value - higher priority
                                                                                            ),force,warn)
# reg  axi_priority_rd_port2, offs=0x220 dflt:0x3ff actual: 0x3ff
        ddrc_register_set.set_bitfields('axi_priority_rd_port2',( # AXI priority control for read port 2
                                                     ('reg_arb_set_hpr_rd_portn',        0),  # Enable reads to be HPR for this port
                                                     ('reg_arb_dis_page_match_rd_portn', 0),  # Disable page match feature
                                                     ('reg_arb_disable_urgent_rd_portn', 0),  # Disable urgent for this Read Port
                                                     ('reg_arb_disable_aging_rd_portn',  0),  # Disable aging for this Read Port
                                                     ('reserved1',                       0),  #
                                                     ('reg_arb_pri_rd_portn',arb_pri_rd_port2),  # 0x3ff Priority for this Read port, lower value - higher priority
                                                                                            ),force,warn)
# reg  axi_priority_rd_port3, offs=0x224 dflt:0x3ff actual: 0x3ff
        ddrc_register_set.set_bitfields('axi_priority_rd_port3',( # AXI priority control for read port 3
                                                     ('reg_arb_set_hpr_rd_portn',        0),  # Enable reads to be HPR for this port
                                                     ('reg_arb_dis_page_match_rd_portn', 0),  # Disable page match feature
                                                     ('reg_arb_disable_urgent_rd_portn', 0),  # Disable urgent for this Read Port
                                                     ('reg_arb_disable_aging_rd_portn',  0),  # Disable aging for this Read Port
                                                     ('reserved1',                       0),  #
                                                     ('reg_arb_pri_rd_portn',arb_pri_rd_port3),  # 0x3ff Priority for this Read port, lower value - higher priority
                                                                                            ),force,warn)
#Skipping several registers that are either obsolete or reserved 
#     'trusted_mem_cfg':         {'OFFS': 0x290,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Trusted Memory Configuration (obsolete)','FIELDS':{
#     'excl_access_cfg0':        {'OFFS': 0x294,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Exclusive access configuration for port 0','FIELDS':{
#     'excl_access_cfg1':        {'OFFS': 0x298,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Exclusive access configuration for port 1','FIELDS':{
#     'excl_access_cfg2':        {'OFFS': 0x29C,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Exclusive access configuration for port 2','FIELDS':{
#     'excl_access_cfg3':        {'OFFS': 0x2A0,'DFLT':0x00000000,'RW':'RW','COMMENTS':'Exclusive access configuration for port 3','FIELDS':{

#Mobile DRAM settings - probably can be skipped if not is_LPDDR2? ps7* has them still programmed
# reg  lpddr_ctrl0, offs=0x2A8 dflt:0 actual: 0
        lpddr2_derate_enable=0 # This feature may be only enabled after LPDDR2 initialization is completed
        lpddr2=(0,1)[is_LPDDR2]
        ddrc_register_set.set_bitfields('lpddr_ctrl0',( # LPDDR2 control register 0 
                                                     ('reg_ddrc_mr4_margin',    0),  # unused
                                                     ('reserved1',              0),  # reserved
                                                     ('reg_ddrc_derate_enable', lpddr2_derate_enable),  # Timing parameter derating ENABLED using MR4 read data
                                                     ('reserved2',              0),  # reserved
                                                     ('reg_ddrc_lpddr2',   lpddr2),  # 0 - DDR2/DDR3 in use, 1 - LPDDR2 in use
                                                                                     ),force,warn)
# reg  lpddr_ctrl1, offs=0x2AC dflt:0 actual: 0
        ddrc_register_set.set_bitfields('lpddr_ctrl1',( # LPDDR2 control register 1
                                                     ('reg_ddrc_mr4_read_interval', 0),  #
                                                                                     ),force,warn)
# reg  lpddr_ctrl2, offs=0x2B0 dflt:0x3C0015 actual: 0x5125
        t_mrw=                  5
        idle_after_reset_x32=int(math.ceil(self.features.get_par_value('T_INIT4_US')*1000/tCK/32))   # 0x12
        min_stable_clock_x1 =   self.features.get_par_value('INIT2')  #0x5
        ddrc_register_set.set_bitfields('lpddr_ctrl2',( # LPDDR2 control register 2
                                                     ('reg_ddrc_t_mrw',                              t_mrw),  # 0x5  Wait for MR writes, typically required 5???
                                                     ('reg_ddrc_idle_after_reset_x32',idle_after_reset_x32),  # 0x12 Idle time after reset command, tINIT4 (in clockx32)
                                                     ('reg_ddrc_min_stable_clock_x1',  min_stable_clock_x1),  # 0x5  Time to wait after first CKE high, tINIT2 in clock cycles. Typically required 5 (tCK)
                                                                                     ),force,warn)
# reg  lpddr_ctrl3, offs=0x2B4 dflt:0x601 actual: 0x12a8
        #seems there is a BUG in ps7* calculation, the values are 32 times higher (as if max_auto_init_x1024 - is actually max_auto_init_x32)
        #Default value seems closer to result
        lpddr_ctrl3_BUG=1 #32 # change to 1 if confirmed
        dev_zqinit_x32=int(math.ceil(self.features.get_par_value('T_ZQINIT_US')*1000/tCK/32))         # 0x12
        max_auto_init_x1024=int(math.ceil(self.features.get_par_value('T_INIT5_US')*1000/tCK/1024*lpddr_ctrl3_BUG))   #0xa8
        ddrc_register_set.set_bitfields('lpddr_ctrl3',( # LPDDR2 control register 3
                                                     ('reg_ddrc_dev_zqinit_x32',          dev_zqinit_x32), # 0x1200 tZQINIT - ZQ initial calibration (in clockx32). LPDDR2 typically require 1 microsecond
                                                     ('reg_ddrc_max_auto_init_x1024',max_auto_init_x1024), # 0xa8    tINIT5 - maximal duration of autoinitialization (in clockx1024). Typical 10 microseconds
                                                                                     ),force,warn)
##########################################

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
## TODO: find out - what "power down" means - bit 0? or other bits that are already set according to bus width
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
                 
