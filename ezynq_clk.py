#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Elphel.inc.
# configuration of the SoC clocks
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
import ezynq_slcr_clk_def
import ezynq_registers
import ezynq_clkcfg_defs
import ezynq_feature_config
class EzynqClk:
    def __init__(self,regs_masked,ddr_type,used_mio_interfaces,permit_undefined_bits=False,force=False,warn=False):
        self.SLCR_CLK_DEFS=  ezynq_slcr_clk_def.SLCR_CLK_DEFS
        self.CLK_CFG_DEFS =  ezynq_clkcfg_defs.CLK_CFG_DEFS
        self.features=ezynq_feature_config.EzynqFeatures(self.CLK_CFG_DEFS,0) #CLK_CFG_DEFS
        self.clk_register_set=  ezynq_registers.EzynqRegisters(self.SLCR_CLK_DEFS,0,regs_masked,permit_undefined_bits)
        if not ddr_type:
            ddr_type = 'DDR3' # DDR3, DDR3L, DDR2, LPDDR2
        self.ddr_type=ddr_type
        self.pll_pars={}
        for pll_line in ezynq_slcr_clk_def.PLL_PARS:
            if isinstance(pll_line[0],tuple):
                r=range(pll_line[0][0], pll_line[0][1]+1)
            else:
                r=[pll_line[0]]
            for div in r:
                self.pll_pars[div]={'PLL_CP':pll_line[1],'PLL_RES':pll_line[2],'LOCK_CNT':pll_line[3]}         
#        for f in self.pll_pars: print f,    self.pll_pars[f]
        self.used_mio_interfaces=used_mio_interfaces


    def parse_parameters(self,raw_configs):
        self.features.parse_features(raw_configs)
    def check_missing_features(self):
        self.features.check_missing_features()
    def html_list_features(self,html_file):
        if not html_file:
            return
        html_file.write('<h2>Clock configuration parameters</h2>\n')
        self.features.html_list_features(html_file)
    def calculate_dependent_pars(self):
        speed_grade=self.features.get_par_value_or_default("SPEED_GRADE")
        ddr_type=self.ddr_type
        if not self.features.is_known('PLL_MAX_MHZ'): # ask permission
            self.features.set_calculated_value('PLL_MAX_MHZ',
                 self.features.get_par_value_or_default('DS_PLL_MAX_%i_MHZ'%speed_grade), force=False)
            
        if not self.features.is_known('ARM621_MAX_MHZ'): # ask permission
            self.features.set_calculated_value('ARM621_MAX_MHZ',
                 self.features.get_par_value_or_default('DS_ARM621_MAX_%i_MHZ'%speed_grade), force=False)
            
        if not self.features.is_known('ARM421_MAX_MHZ'): # ask permission
            self.features.set_calculated_value('ARM421_MAX_MHZ',
                 self.features.get_par_value_or_default('DS_ARM421_MAX_%i_MHZ'%speed_grade), force=False)
            
        if not self.features.is_known('DDR_3X_MAX_MHZ'): # ask permission
            if ddr_type=='DDR3':
                self.features.set_calculated_value('DDR_3X_MAX_MHZ',
                    0.5*self.features.get_par_value_or_default('DS_DDR3_MAX_%i_MBPS'%speed_grade), force=False)
            else: # all other DDR types have the same DDR_3x timing for all speed grades
                self.features.set_calculated_value('DDR_3X_MAX_MHZ',
                    0.5*self.features.get_par_value_or_default('DS_DDRX_MAX_X_MBPS'), force=False)

        if not self.features.is_known('DDR_2X_MAX_MHZ'): # ask permission
            self.features.set_calculated_value('DDR_2X_MAX_MHZ',
                 self.features.get_par_value_or_default('DS_DDR_2X_MAX_%i_MHZ'%speed_grade), force=False)
        if not self.features.is_known('DDR2X_MHZ'):
            self.features.set_calculated_value('DDR2X_MHZ', 2.0/3.0*self.features.get_par_value_or_default('DDR_MHZ'))
                                                  
    def check_ds_compliance(self):
        self.is621=(0,1)[self.features.get_par_value_or_default('CPU_MODE')=='6_2_1']
        self.compliance_margin=0.01*self.features.get_par_value_or_default('COMPLIANCE_PERCENT')
        arm_max_mhz=(self.features.get_par_value_or_default('ARM421_MAX_MHZ'),self.features.get_par_value_or_default('ARM621_MAX_MHZ'))[self.is621]
        self.arm6x4x=self.features.get_par_value_or_default('ARM_MHZ')
        if self.arm6x4x > arm_max_mhz*(1+self.compliance_margin):
            max_name=('ARM421_MAX_MHZ','ARM621_MAX_MHZ')[self.is621]
            raise Exception ('Specified frequency for ARM clock (%s = %f) exceeds maximal (%s = %f) by more than %f%%'%(
                   self.features.get_par_confname('ARM_MHZ'),
                   self.features.get_par_value_or_default('ARM_MHZ'),
                   self.features.get_par_confname(max_name),
                   self.features.get_par_value_or_default(max_name),
                   self.features.get_par_value_or_default('COMPLIANCE_PERCENT')))
        self.ddr_3x=self.features.get_par_value_or_default('DDR_MHZ')
        if self.ddr_3x > self.features.get_par_value_or_default('DDR_3X_MAX_MHZ')*(1+self.compliance_margin):
            raise Exception ('Specified frequency for DDR clock (%s = %f) exceeds maximal (%s = %f) by more than %f%%'%(
                   self.features.get_par_confname('DDR_MHZ'),
                   self.features.get_par_value_or_default('DDR_MHZ'),
                   self.features.get_par_confname('DDR_3X_MAX_MHZ'),
                   self.features.get_par_value_or_default('DDR_3X_MAX_MHZ'),
                   self.features.get_par_value_or_default('COMPLIANCE_PERCENT')))
        self.ddr_2x=self.features.get_par_value_or_default('DDR2X_MHZ')
        if self.ddr_2x > self.features.get_par_value_or_default('DDR_2X_MAX_MHZ')*(1+self.compliance_margin):
            raise Exception ('Specified frequency for DDR_2X clock (%s = %f) exceeds maximal (%s = %f) by more than %f%%'%(
                   self.features.get_par_confname('DDR2X_MHZ'),
                   self.features.get_par_value_or_default('DDR2X_MHZ'),
                   self.features.get_par_confname('DDR_2X_MAX_MHZ'),
                   self.features.get_par_value_or_default('DDR_2X_MAX_MHZ'),
                   self.features.get_par_value_or_default('COMPLIANCE_PERCENT')))
#  self.pll_pars[div]={'PLL_CP':pll_line[1],'PLL_RES':pll_line[2],'LOCK_CNT':pll_line[3]}         
    def get_valid_pll_fdiv(self): # common for all 3
        f_in=self.features.get_par_value_or_default('PS_MHZ')
        pll_min=self.features.get_par_value_or_default('PLL_MIN_MHZ')
        pll_max=self.features.get_par_value_or_default('PLL_MAX_MHZ')
        
        valid_fdiv=set()
        for fdiv in self.pll_pars:
            if (fdiv*f_in>=pll_min) and (fdiv*f_in<=pll_max) :
                valid_fdiv.add(fdiv)
        return valid_fdiv
      

            
            
                    
    def setup_clocks(self):
        def pll_errors(valid_fdivs,valid_div6,f_in,f_target):
            result={}
            for fdiv in valid_fdivs:
                freq_ratio=f_in*fdiv/f_target
                best_log_err=None 
                for div6 in valid_div6:
                    log_err=abs(math.log(freq_ratio/div6))
                    if (best_log_err is None) or (log_err < best_log_err):
                        best_div6=div6
                        best_log_err=log_err
                if not (best_log_err is None) :
                    result[fdiv]=(best_div6,best_log_err)
            return result
        def filter_best(fdiv_err):
            best_error=None
            for fdiv in fdiv_err:
                if (best_error is None) or (fdiv_err[fdiv][1]<best_error):
                    best_error=fdiv_err[fdiv][1]
            result = {}
            for fdiv in fdiv_err:
                if (fdiv_err[fdiv][1] == best_error):
                    result[fdiv]= fdiv_err[fdiv]
            return result
        def getBest(fdiv_err):
            filtered=filter_best(fdiv_err)
            lowest=None
            for fdiv in filtered:
                if (lowest is None) or (fdiv < lowest):
                    lowest=fdiv
            return lowest                 
        def filter_combine_multiclock(fdiv_errors):
            combo_err={}
            for fdiv in fdiv_errors[0]:
                # verify it is available for all clocks
                err=0
                for fdiv_err in fdiv_errors:
                    if fdiv in fdiv_err:
                        err+=fdiv_err[fdiv][1]
                    else:
                        err=False
                        break
                    
#                 for clock in fdiv_errors:
#                     if fdiv in fdiv_errors[clock]:
#                         err+=fdiv_errors[clock][1]
#                     else:
#                         err=False
#                         break
                if not err is False:
                    combo_err[fdiv]=(fdiv_errors[0][fdiv][0],err)
            return combo_err        
                    
            
        self.f_in=self.features.get_par_value_or_default('PS_MHZ')
        # so far all 2 PLLs have the same
        arm_valid_fdiv=self.get_valid_pll_fdiv() 
        ddr_valid_fdiv=self.get_valid_pll_fdiv()
        io_valid_fdiv=self.get_valid_pll_fdiv()
        # sorted() is not really needed here, maybe will be needed later
        arm_valid_div6=   sorted({x for x in range (1,64) if (x != 1) and (x != 3)})
        ddr_3x_valid_div6=sorted({x for x in range (1,64) if (x & 1) == 0})
        other_valid_div6= sorted({x for x in range (1,64)})
        valid_div6x6=     sorted({x*y for x in range(1,64) for y in range(1,64)})
        
#        print arm_valid_fdiv
        
        # arm_6x4x:
        arm_target=self.features.get_par_value_or_default('ARM_MHZ')
        pll_errs= pll_errors(arm_valid_fdiv,arm_valid_div6,self.f_in,arm_target)
#        print 'pll_errs=',pll_errs
        self.arm_pll_fdiv=  getBest(pll_errs)
        print 'getBest()->',self.arm_pll_fdiv
        arm_pll_errs= filter_best(pll_errs)
        print 'filtered pll_errs=',arm_pll_errs
        self.arm_6x3x_div6=arm_pll_errs[self.arm_pll_fdiv][0]

        
        # ddr
        ddr_3x_target=self.features.get_par_value_or_default('DDR_MHZ')
        ddr_2x_target=self.features.get_par_value_or_default('DDR2X_MHZ')
        pll_errs_ddr_3x= pll_errors(ddr_valid_fdiv,ddr_3x_valid_div6,self.f_in,ddr_3x_target)
        pll_errs_ddr_2x= pll_errors(ddr_valid_fdiv,other_valid_div6, self.f_in,ddr_2x_target)
#        print 'pll_errs_ddr_3x=',pll_errs_ddr_3x
#        print 'pll_errs_ddr_2x=',pll_errs_ddr_2x
        ddr_combo_errors=filter_combine_multiclock((pll_errs_ddr_3x,pll_errs_ddr_2x))
#        print 'ddr_combo_errors=',ddr_combo_errors
        self.ddr_pll_fdiv=  getBest(ddr_combo_errors)
        self.ddr_3x_div6=pll_errs_ddr_3x[self.ddr_pll_fdiv][0]
        self.ddr_2x_div6=pll_errs_ddr_2x[self.ddr_pll_fdiv][0]
        print 'ddr_fdiv=',self.ddr_pll_fdiv,': pll_errs_ddr_3x=',pll_errs_ddr_3x[self.ddr_pll_fdiv],'pll_errs_ddr_2x=',pll_errs_ddr_2x[self.ddr_pll_fdiv]
   
        self.features.set_calculated_value('ARM_MHZ',  self.f_in*self.arm_pll_fdiv/self.arm_6x3x_div6, True)
        self.features.set_calculated_value('DDR_MHZ',  self.f_in*self.ddr_pll_fdiv/self.ddr_3x_div6, True)
        self.features.set_calculated_value('DDR2X_MHZ',self.f_in*self.ddr_pll_fdiv/self.ddr_2x_div6, True)
        
        
        
        for ifc in self.used_mio_interfaces:
            print ifc

        
    def get_ddr_mhz(self):
        return self.f_in*self.ddr_pll_fdiv/self.ddr_3x_div6    
# temporary, just for reference
# for CAN_ECLK use ['PIN'] to disable from considering (if all used CAN has same channel CAN_ECLK) and set it's clock mux
       
    CLK_TEMPLATE=[
        {'NAME':'ARM',     'VALUE':'ARM_MHZ',     'SOURCE':'ARM_SRC',     'DIV2':False,'USED':True,                'WEIGHT':1.0},          
        {'NAME':'DDR',     'VALUE':'DDR_MHZ',     'SOURCE':'DDR_SRC',     'DIV2':False,'USED':True,                'WEIGHT':1.0},          
        {'NAME':'DDR2X',   'VALUE':'DDR2X_MHZ',   'SOURCE':'DDR_SRC',     'DIV2':False,'USED':True,                'WEIGHT':1.0},          
        {'NAME':'DDR_DCI', 'VALUE':'DDR_DCI_MHZ', 'SOURCE':'DDR_DCI_SRC', 'DIV2':False,'USED':True,                'WEIGHT':0.1},          
        {'NAME':'SMC',     'VALUE':'SMC_MHZ',     'SOURCE':'SMC_SRC',     'DIV2':False,'USED':(('NAND',),('NOR',)),'WEIGHT':1.0},          
        {'NAME':'QSPI',    'VALUE':'QSPI_MHZ',    'SOURCE':'QSPI_SRC',    'DIV2':False,'USED':(('QSPI',),),        'WEIGHT':1.0},          
        {'NAME':'GIGE0',   'VALUE':'GIGE0_MHZ',   'SOURCE':'GIGE0_SRC',   'DIV2':True, 'USED':(('ETH',0),),        'WEIGHT':1.0},          
        {'NAME':'GIGE1',   'VALUE':'GIGE1_MHZ',   'SOURCE':'GIGE1_SRC',   'DIV2':True, 'USED':(('ETH',1),),        'WEIGHT':1.0},          
        {'NAME':'SDIO',    'VALUE':'SDIO_MHZ',    'SOURCE':'SDIO_SRC',    'DIV2':False,'USED':(('SDIO',),),        'WEIGHT':1.0},          
        {'NAME':'UART',    'VALUE':'UART_MHZ',    'SOURCE':'UART_SRC',    'DIV2':False,'USED':(('UART',),),        'WEIGHT':1.0},          
        {'NAME':'SPI',     'VALUE':'SPI_MHZ',     'SOURCE':'SPI_SRC',     'DIV2':False,'USED':(('SPI',),),         'WEIGHT':1.0},          
        {'NAME':'CAN',     'VALUE':'CAN_MHZ',     'SOURCE':'CAN_SRC',     'DIV2':True, 'USED':(('CAN',),),         'WEIGHT':1.0},          
        {'NAME':'PCAP',    'VALUE':'PCAP_MHZ',    'SOURCE':'PCAP_SRC',    'DIV2':False,'USED':True,                'WEIGHT':1.0},          
        {'NAME':'TRACE',   'VALUE':'TRACE_MHZ',   'SOURCE':'TRACE_SRC',   'DIV2':False,'USED':True,                'WEIGHT':1.0},          
        {'NAME':'FPGA0',   'VALUE':'FPGA0_MHZ',   'SOURCE':'FPGA0_SRC',   'DIV2':True, 'USED':True,                'WEIGHT':1.0}, # source can be set to None         
        {'NAME':'FPGA1',   'VALUE':'FPGA1_MHZ',   'SOURCE':'FPGA1_SRC',   'DIV2':True, 'USED':True,                'WEIGHT':1.0}, # source can be set to None         
        {'NAME':'FPGA2',   'VALUE':'FPGA2_MHZ',   'SOURCE':'FPGA2_SRC',   'DIV2':True, 'USED':True,                'WEIGHT':1.0}, # source can be set to None         
        {'NAME':'FPGA3',   'VALUE':'FPGA3_MHZ',   'SOURCE':'FPGA3_SRC',   'DIV2':True, 'USED':True,                'WEIGHT':1.0}, # source can be set to None         
                  ]
    def get_clk_requirements(self,mio):
        clock_reqs=[]
        for template in self.CLK_TEMPLATE:
            name=   template['NAME']
            value=  self.features.get_par_value_or_default(template['VALUE'])
            source= self.features.get_par_value_or_default(template['SOURCE'])
############# Main clock settings #############
#CONFIG_EZYNQ_CLK_PS_MHZ =   33.333333 # PS_CLK System clock input frequency (MHz)   
#CONFIG_EZYNQ_CLK_DDR_MHZ = 533.333333 # DDR clock frequency - DDR_3X (MHz)
#CONFIG_EZYNQ_CLK_ARM_MHZ = 667        # ARM CPU clock frequency cpu_6x4x (MHz)
#CONFIG_EZYNQ_CLK_CPU_MODE = 6_2_1     # CPU clocks set 6:2:1 (6:3:2:1) or 4:2:1 (4:2:2:1)

#CONFIG_EZYNQ_CLK_FPGA0 =        50.0 # FPGA 0 clock frequency (MHz)
#CONFIG_EZYNQ_CLK_FPGA1 =        50.0 # FPGA 1 clock frequency (MHz)
#CONFIG_EZYNQ_CLK_FPGA2 =        50.0 # FPGA 2 clock frequency (MHz)
#CONFIG_EZYNQ_CLK_FPGA3 =        50.0 # FPGA 3 clock frequency (MHz)

#CONFIG_EZYNQ_CLK_FPGA0_SRC =      IO # FPGA 0 clock source
#CONFIG_EZYNQ_CLK_FPGA1_SRC =      IO # FPGA 1 clock source
#CONFIG_EZYNQ_CLK_FPGA2_SRC =      IO # FPGA 2 clock source
#CONFIG_EZYNQ_CLK_FPGA3_SRC =      IO # FPGA 3 clock source

############# Normally do not need to be modified #############
#CONFIG_EZYNQ_CLK_DDR_DCI_MHZ = 10.0   # DDR DCI clock frequency (MHz). Normally 10 Mhz'},
#CONFIG_EZYNQ_CLK_DDR2X_MHZ = 355.556 # DDR2X clock frequency (MHz). Does not need to be exactly 2/3 of DDR3X clock'},
#CONFIG_EZYNQ_CLK_DDR_DCI_MHZ=   10.0 # DDR DCI clock frequency (MHz). Normally 10Mhz
#CONFIG_EZYNQ_CLK_SMC_MHZ =     100.0 # Static memory controller clock frequency (MHz). Normally 100 Mhz
#CONFIG_EZYNQ_CLK_QSPI_MHZ =    200.0 # Quad SPI memory controller clock frequency (MHz). Normally 200 Mhz
#CONFIG_EZYNQ_CLK_GIGE0_MHZ =   125.0 # GigE 0 Ethernet controller reference clock frequency (MHz). Normally 125 Mhz
#CONFIG_EZYNQ_CLK_GIGE1_MHZ =   125.0 # GigE 1 Ethernet controller reference clock frequency (MHz). Normally 125 Mhz
#CONFIG_EZYNQ_CLK_SDIO_MHZ =    100.0 # SDIO controller reference clock frequency (MHz). Normally 100 Mhz
#CONFIG_EZYNQ_CLK_UART_MHZ =     25.0 # UART controller reference clock frequency (MHz). Normally 25 Mhz
#CONFIG_EZYNQ_CLK_SPI_MHZ =     200.0 # SPI controller reference clock frequency (MHz). Normally 200 Mhz
#CONFIG_EZYNQ_CLK_CAN_MHZ =     100.0 # CAN controller reference clock frequency (MHz). Normally 100 Mhz
#CONFIG_EZYNQ_CLK_PCAP_MHZ =    200.0 # PCAP clock frequency (MHz). Normally 200 Mhz
#CONFIG_EZYNQ_CLK_TRACE_MHZ =   100.0 # Trace Port clock frequency (MHz). Normally 100 Mhz
#CONFIG_EZYNQ_CLK_ARM_SRC =       ARM # ARM CPU clock source (normally ARM PLL)
#CONFIG_EZYNQ_CLK_DDR_SRC =       DDR # DDR (DDR2x, DDR3x) clock source (normally DDR PLL)
#CONFIG_EZYNQ_CLK_DCI_SRC =       DDR # DDR DCI clock source (normally DDR PLL)
#CONFIG_EZYNQ_CLK_SMC_SRC =        IO # Static memory controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_QSPI_SRC =       IO # Quad SPI memory controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_GIGE0_SRC =      IO # GigE 0 Ethernet controller clock source (normally IO PLL, can be EMIO)
#CONFIG_EZYNQ_CLK_GIGE1_SRC =      IO # GigE 1 Ethernet controller clock source (normally IO PLL, can be EMIO)
#CONFIG_EZYNQ_CLK_SDIO_SRC =       IO # SDIO controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_UART_SRC =       IO # UART controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_SPI_SRC =        IO # SPI controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_CAN_SRC =        IO # CAN controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_PCAP_SRC =       IO # PCAP controller clock source (normally IO PLL)
#CONFIG_EZYNQ_CLK_TRACE_SRC =      IO # Trace Port clock source (normally IO PLL)
        
        
        
        
                         
        
##### performance data, final values (overwrite calculated) #####              
#CONFIG_EZYNQ_CLK_SPEED_GRADE =        2   # Device speed grade
#CONFIG_EZYNQ_CLK_PLL_MAX_MHZ =     1800.0 # Maximal PLL clock frequency, MHz. Overwrites default for selected speed grade: (Speed grade -1:1600, -2:1800, -3:2000)'},
#CONFIG_EZYNQ_CLK_PLL_MIN_MHZ =      780.0 # Minimal PLL clock frequency, all speed grades (MHz)'},
#CONFIG_EZYNQ_CLK_ARM621_MAX_MHZ =   733.0 # Maximal ARM clk_6x4x in 621 mode, MHz. Overwrites default for selected speed grade: (Speed grade -1:667, -2:733, -3:1000)'},
#CONFIG_EZYNQ_CLK_ARM421_MAX_MHZ = 600.0 # Maximal ARM clk_6x4x in 421 mode, MHz. Overwrites default for selected speed grade: (Speed grade -1:533, -2:600, -3:710)'},
#CONFIG_EZYNQ_CLK_DDR_3X_MAX_MHZ =   533.0 # Maximal DDR clk_3x clock frequency (MHz). Overwrites DDR-type/speed grade specific'},
#CONFIG_EZYNQ_CLK_DDR_2X_MAX_MHZ =   408.0 # Maximal DDR_2X clock frequency (MHz). Overwrites speed grade specific'},

##### datasheet data for specific speed grades #####
#CONFIG_EZYNQ_CLK_DS_PLL_MAX_1_MHZ =   1600.0 # Maximal PLL clock frequency for speed grade 1 (MHz)'},
#CONFIG_EZYNQ_CLK_DS_PLL_MAX_2_MHZ =   1800.0 # Maximal PLL clock frequency for speed grade 2 (MHz)'},
#CONFIG_EZYNQ_CLK_DS_PLL_MAX_3_MHZ =   2000.0 # Maximal PLL clock frequency for speed grade 3 (MHz)'},
#CONFIG_EZYNQ_CLK_DS_ARM621_MAX_1_MHZ = 667.0 # Maximal ARM clk_6x4x in 621 mode for speed grade 1, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM621_MAX_2_MHZ = 733.0 #Maximal ARM clk_6x4x in 621 mode for speed grade 2, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM621_MAX_3_MHZ =1000.0 #Maximal ARM clk_6x4x in 621 mode for speed grade 3, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM421_MAX_1_MHZ = 533.0 # Maximal ARM clk_6x4x in 421 mode for speed grade 1, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM421_MAX_2_MHZ = 600.0 # Maximal ARM clk_6x4x in 421 mode for speed grade 2, MHz'},
#CONFIG_EZYNQ_CLK_DS_ARM421_MAX_3_MHZ = 710.0 # Maximal ARM clk_6x4x in 421 mode for speed grade 3, MHz'},

#CONFIG_EZYNQ_CLK_DS_DDR3_MAX_1_MBPS = 1066.0 # Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 1'},
#CONFIG_EZYNQ_CLK_DS_DDR3_MAX_2_MBPS = 1066.0 # Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 2'},
#CONFIG_EZYNQ_CLK_DS_DDR3_MAX_3_MBPS = 1333.0 # Maximal DDR3 performance in Mb/s - twice clock frequency (MHz). Speed grade 3'},
#CONFIG_EZYNQ_CLK_DS_DDRX_MAX_X_MBPS =  800.0 # Maximal DDR3L, DDR2, LPDDR2 performance in Mb/s - twice clock frequency (MHz). All speed grades'},
#CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_1_MHZ = 355.0 # Maximal DDR_2X clock frequency (MHz) for speed grade 1'},
#CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_2_MHZ = 408.0 # Maximal DDR_2X clock frequency (MHz) for speed grade 2'},
#CONFIG_EZYNQ_CLK_DS_DDR_2X_MAX_3_MHZ = 444.0 # Maximal DDR_2X clock frequency (MHz) for speed grade 3'},

