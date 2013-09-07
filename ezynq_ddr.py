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
            _=self._map_ddr_addresses (ca_count,ra_count,ba_count,ba_map,half_width)
            return # all OK already
        except Exception, err:
            print "Specified value for the "+self.features.get_par_confname('BANK_ADDR_MAP')+'='+str(ba_map)+" is not valid:\n"+str(err)
        best_match=None
        for bm in range(3,30):
            if (best_match==None) or (abs(bm-ba_map) < abs(bm-ba_map)):
                try:
                    _=self._map_ddr_addresses (ca_count,ra_count,ba_count,bm,half_width)
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
        return address_mapping
#    def set_max_value(self,name,value):
#    def set_min_value(self,name,value):
            
# CONFIG_EZYNQ_DDR_T_RP = 13.1
# CONFIG_EZYNQ_DDR_T_RCD = 13.1
#CONFIG_EZYNQ_DDR_RRD = 4
#CONFIG_EZYNQ_DDR_T_RRD = 10.0

    
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
#        self.pre_validate() # already done
        
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

#CONFIG_EZYNQ_DDR_CKE =   3
#CONFIG_EZYNQ_DDR_CKSRE =   5
#CONFIG_EZYNQ_DDR_CKSRX =   5

        CKE=  self.features.get_par_value('CKE') # 4
        
        RAS_MIN= int(math.ceil(self.features.get_par_value('T_RAS_MIN')/tCK))
        RAS_MAX=9*tREFI # for Micron
        RAS_MAXx1024=int(RAS_MAX/tCK/1024)
        tFAWx1=int(math.ceil(self.features.get_par_value('T_FAW')/tCK))
        inactiveToPDx32=6 # cycles 'Power down after this many clocks of NOP/DESELECT (if enabled in mcr). Make configurable?
        WR=int(math.ceil(tWR/tCK))
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
# reg DRAM_param_reg3, 0x270872d0 , 0x272872d0, 0x272872d0 (first time reg_ddrc_sdram is not set, the rest is the same)
        enable_pad_powerdown=     True  # ?
        mode_ddr1_ddr2=           1
        en_dfi_dram_clk_disable = 0 # not clear - is it just enable for the action, or actually stopping the clock?
        ddrc_refresh_to_x32=      8 # start refresh after this inactivity (x32 cycles) if it is useful, but not yet required. Dynamic field
        RP=                       self.features.get_par_value('RP')
        refresh_margin=           2 # default, recommended not to be changed
#CONFIG_EZYNQ_DDR_CCD = 4
#CONFIG_EZYNQ_DDR_RRD = 4
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
#        ddrc_register_set.set_word     ('dram_init_param',  0x2007, force)
# CONFIG_EZYNQ_DDR_MRD = 4
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
                raise Exception ("Wrong value for additive latency (CONFIG_EZYNQ_DDR_AL): "+str(AL)+", only 0, CL-1, CL-2 are supported in DDR3 memory. CL is "+str(CL))
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
                raise Exception ("Wrong value for additive latency (CONFIG_EZYNQ_DDR_AL): "+str(AL)+", only 0...6 are supported in DDR2 memory")
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
            wr_options=(16,5,6,7,8,10,12,14)
            try:
                mr_write_recovery=wr_options.index(WR)
            except:
                raise Exception('Wrong value for Write recovery (WR): '+str(WR)+ ' (may be defined by tWR), DDR3 only supports '+str(wr_options))
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
        addr_map =self._map_ddr_addresses (ca_count,ra_count,ba_count,ba_map,half_width)

        
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
#CONFIG_EZYNQ_DDR_ZQCS = 64
#CONFIG_EZYNQ_DDR_ZQCL = 512
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

        
        
#CONFIG_EZYNQ_DDR_BANK_ADDR_COUNT = 3
#CONFIG_EZYNQ_DDR_ROW_ADDR_COUNT = 15
#CONFIG_EZYNQ_DDR_COL_ADDR_COUNT = 10 # not counting A10
#CONFIG_EZYNQ_DDR_BANK_ADDR_MAP  = 10        
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
