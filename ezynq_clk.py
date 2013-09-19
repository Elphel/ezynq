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
CLK_TEMPLATE=[
        {'NAME':'ARM',     'VALUE':'ARM_MHZ',     'SOURCE':'ARM_SRC',     'DIV2':False,'USED':True,                'WEIGHT':1.0},          
        {'NAME':'DDR',     'VALUE':'DDR_MHZ',     'SOURCE':'DDR_SRC',     'DIV2':False,'USED':True,                'WEIGHT':1.0},          
        {'NAME':'DDR2X',   'VALUE':'DDR2X_MHZ',   'SOURCE':'DDR_SRC',     'DIV2':False,'USED':True,                'WEIGHT':1.0},          
        {'NAME':'DDR_DCI', 'VALUE':'DDR_DCI_MHZ', 'SOURCE':'DDR_DCI_SRC', 'DIV2':True, 'USED':True,                'WEIGHT':0.1},          
        {'NAME':'SMC',     'VALUE':'SMC_MHZ',     'SOURCE':'SMC_SRC',     'DIV2':False,'USED':(('NAND',),('NOR',)),'WEIGHT':1.0},          
        {'NAME':'QSPI',    'VALUE':'QSPI_MHZ',    'SOURCE':'QSPI_SRC',    'DIV2':False,'USED':(('QUADSPI',),),     'WEIGHT':1.0},          
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
# Same frequency/derived clocks       
        {'NAME':'CPU_1X',  'VALUE':6,             'SOURCE':'ARM',         'DIV2':False,'USED':True,                'WEIGHT':0.0},          
        {'NAME':'CPU_2X',  'VALUE':3,             'SOURCE':'ARM',         'DIV2':False,'USED':True,                'WEIGHT':0.0},          
        {'NAME':'SDIO0',   'VALUE':1,             'SOURCE':'SDIO',        'DIV2':False,'USED':(('SDIO',0),),       'WEIGHT':0.0},          
        {'NAME':'SDIO1',   'VALUE':1,             'SOURCE':'SDIO',        'DIV2':False,'USED':(('SDIO',1),),       'WEIGHT':0.0},          
        {'NAME':'UART0',   'VALUE':1,             'SOURCE':'UART',        'DIV2':False,'USED':(('UART',0),),       'WEIGHT':0.0},          
        {'NAME':'UART1',   'VALUE':1,             'SOURCE':'UART',        'DIV2':False,'USED':(('UART',1),),       'WEIGHT':0.0},          
        {'NAME':'SPI0',    'VALUE':1,             'SOURCE':'SPI',         'DIV2':False,'USED':(('SPI',0),),        'WEIGHT':0.0},          
        {'NAME':'SPI1',    'VALUE':1,             'SOURCE':'SPI',         'DIV2':False,'USED':(('SPI',1),),        'WEIGHT':0.0},          
        {'NAME':'I2C0',    'VALUE':1,             'SOURCE':'CPU_1X',      'DIV2':False,'USED':(('I2C',0),),        'WEIGHT':0.0},          
        {'NAME':'I2C1',    'VALUE':1,             'SOURCE':'CPU_1X',      'DIV2':False,'USED':(('I2C',1),),        'WEIGHT':0.0},          
        {'NAME':'CAN0',    'VALUE':1,             'SOURCE':'CPU_1X',      'DIV2':False,'USED':(('CAN',0),),        'WEIGHT':0.0},          
        {'NAME':'CAN1',    'VALUE':1,             'SOURCE':'CPU_1X',      'DIV2':False,'USED':(('CAN',1),),        'WEIGHT':0.0},          
    ]


class EzynqClk:
    def __init__(self, verbosity,regs_masked,ddr_type,used_mio_interfaces,permit_undefined_bits=False,force=False,warn=False):
        self.verbosity=verbosity
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
        self.arm_valid_div6=   sorted({x for x in range (1,64) if (x != 1) and (x != 3)})
        self.ddr_3x_valid_div6=sorted({x for x in range (1,64) if (x & 1) == 0})
        self.other_valid_div6= sorted({x for x in range (1,64)})
        self.valid_div6x6=     sorted({x*y for x in range(1,64) for y in range(1,64)})
        self.valid_fdiv={'ARM':self._get_valid_pll_fdiv(), # Now all 3 are the same
                         'DDR':self._get_valid_pll_fdiv(),
                         'IO': self._get_valid_pll_fdiv()}
        self.clk_dict={}
        for c in CLK_TEMPLATE:
            self.clk_dict[c['NAME']]=c
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
    def _get_valid_pll_fdiv(self): # common for all 3
        f_in=self.features.get_par_value_or_default('PS_MHZ')
        pll_min=self.features.get_par_value_or_default('PLL_MIN_MHZ')
        pll_max=self.features.get_par_value_or_default('PLL_MAX_MHZ')
        
        valid_fdiv=set()
        for fdiv in self.pll_pars:
            if (fdiv*f_in>=pll_min) and (fdiv*f_in<=pll_max) :
                valid_fdiv.add(fdiv)
        return valid_fdiv
                    
    def setup_clocks(self):
#        print 'self.verbosity=',self.verbosity
        if self.verbosity>2 :
            for ifc in self.used_mio_interfaces:
                print ifc
        self.get_clk_requirements(self.used_mio_interfaces)    

        

    def div_second_stage(self,d):
        div_sec= [(((n<<1)  | (n >> 5)) & 0x3f) - (n>63) for n in range(1,65) if n != 32]  # [2,4, .. 62,3,5, .. 63,1]
        for d2 in div_sec:
            q,r=divmod(d,d2)
            if (r==0) and (q<=63) and (d2<=q) :
                return (d2,q)
        else:
            raise Exception ('Can not split %i into two 6-bit divisors'%d)    
# temporary, just for reference
# for CAN_ECLK use ['PIN'] to disable from considering (if all used CAN has same channel CAN_ECLK) and set it's clock mux

##'err=%+.3f%%'%-33.33333333

       
    def get_clk_requirements(self,mio):
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
                if fdiv != 'WEIGHT':
                    # verify it is available for all clocks
                    err=0
                    for fdiv_err in fdiv_errors:
                        try:
                            weight=fdiv_err['WEIGHT']
                        except:    
                            weight=1.0
                        if fdiv in fdiv_err:
                            err+=weight*fdiv_err[fdiv][1]
                        else:
                            err=False
                            break
                    if not err is False:
                        combo_err[fdiv]=(fdiv_errors[0][fdiv][0],err)
            return combo_err        
#         valid_div6x6=     sorted({x*y for x in range(1,64) for y in range(1,64)})
        self.f_in=self.features.get_par_value_or_default('PS_MHZ')
        clock_reqs={'ARM':[],'DDR':[],'IO':[]}
        self.iface_divs={} # for each name - PLL, divisor
#        self.secondary_clocks={}
        for template in CLK_TEMPLATE:
            name=   template['NAME']
            div2=   template['DIV2']
            weight= template['WEIGHT']
            value=template['VALUE']
            source=template['SOURCE']
            is_secondary=isinstance(template['VALUE'],int)
            if not is_secondary:
                value=  self.features.get_par_value_or_default(template['VALUE'])
                if value==0:
                    continue
                source= self.features.get_par_value_or_default(source)
            if not template['USED'] is True:
                ifc={i[0]:set() for i in template['USED']}
#                print 'ifc=',ifc
                for i in template['USED']:
#                    print 'i=',i,"template['USED']=",template['USED']
                    if len(i)>1: 
                        ifc[i[0]].add(i[1])
##                print name,':',ifc    
                for mio_iface in mio:
                    if (mio_iface['NAME'] in ifc) and ((len(ifc[mio_iface['NAME']])==0) or (mio_iface['CHANNEL'] in ifc[mio_iface['NAME']])):
                        break
                    pass
                else:
                    if source != 'EMIO':
                        continue # no MIO interface uses this clock
                    else:
                        pass #for Ethernet controllers connected to EMIO
                        value=0 # something else?
                        is_secondary=True
            #for trace port that can be EMIO            
            if source == 'EMIO':
                value=0 # something else?
                is_secondary=True
                              
            if is_secondary:
                self.iface_divs[name]={'SOURCE':source,'VALUE':value} #no 'PLL' field   
            elif source in clock_reqs:
                if   name == 'ARM':
                    valid_divs=self.arm_valid_div6
                elif name == 'DDR':    
                    valid_divs=self.ddr_3x_valid_div6
                elif div2:    
                    valid_divs=self.valid_div6x6
                else:    
                    valid_divs=self.other_valid_div6
                clock_reqs[source].append({'NAME':name,'VALUE':value,'DIV':valid_divs,'WEIGHT':weight})
#        print 'clock_reqs=',clock_reqs
#         for pll in clock_reqs:
#             print pll
#             for i,c in enumerate(clock_reqs[pll]):
#                 print i
#                 for n in c: 
#                     print '        ',n,':',c[n]        
        self.pll_fdivs={}
        for pll in clock_reqs: # clocks belonging to the same PLL
            pll_errs=[]
            pll_iface_divs={}
            names=[]
            for clk_req in clock_reqs[pll]: # individual clocks specs for this interface
                iface_pll_errors=pll_errors(self.valid_fdiv[pll],clk_req['DIV'],self.f_in,clk_req['VALUE'])
                iface_pll_errors['WEIGHT']=clk_req['WEIGHT']
                pll_errs.append(iface_pll_errors)
                pll_iface_divs[clk_req['NAME']]=iface_pll_errors
                names.append(clk_req['NAME'])
            if len(pll_errs) == 0:
                continue # nothing for this PLL    
            combo_errors=filter_combine_multiclock(pll_errs)
            if len(combo_errors)==0: #Will never come here
                clk_list=str([self.features.get_par_confname(self.clk_dict[n]['VALUE'])+' = '+self.features.get_par_value(self.clk_dict[n]['VALUE']) for n in names ])                 
                raise Exception('Could not find valid FDIV for %s PLL to satisfy requirements: %s'%(pll,clk_list))
#            print 'combo_errors=',combo_errors
            fdiv=  getBest(combo_errors)
            self.pll_fdivs[pll]=fdiv
            for name in pll_iface_divs:
                div=pll_iface_divs[name][fdiv][0]
                freq=self.f_in*fdiv/div
                self.iface_divs[name]={'PLL':pll,'DIV':div,'FREQ':freq,'TARGET':self.features.get_par_value(self.clk_dict[name]['VALUE'])}
                self.features.set_calculated_value(self.clk_dict[name]['VALUE'],freq,force=True)
#                self.iface_divs[name]={'PLL':pll,'DIV':div,'FREQ':self.f_in*fdiv/div}
                if self.clk_dict[name]['DIV2']:
                    div2,div=self.div_second_stage(div)
                    self.iface_divs[name]['DIV']= div
                    self.iface_divs[name]['DIV2']=div2
        self.iface_divs['CPU_1X']['FREQ']= self.iface_divs['ARM']['FREQ']/(4,6)[self.is621]
        self.iface_divs['CPU_2X']['FREQ']= self.iface_divs['ARM']['FREQ']/(1,3)[self.is621]
        for name in self.iface_divs:
            clk=self.iface_divs[name]
            if (not 'PLL' in clk ) and (not 'FREQ' in clk):
                self.iface_divs[name]['FREQ']=self.iface_divs[self.iface_divs[name]['SOURCE']]['FREQ'] # same frequency - possible to use 'VALUE' as scale   
    def get_plls_used (self):
        return set([pll for pll in self.pll_fdivs])
          
    def html_list_clocks(self,html_file):
        def list_with_children(name):
            result = [name]
            for kid_name in self.iface_divs:
                if  not 'PLL' in self.iface_divs[kid_name]:
                    try:
#                        print name,' ---> ',kid_name,', source=',self.iface_divs[kid_name]['SOURCE']                        
                        if self.iface_divs[kid_name]['SOURCE']==name:
                            result.extend(list_with_children(kid_name))
                    except:
                        pass        
            return result        
            
        html_file.write('<h2>System PLL (input clock - %.3f MHz)</h2>'%self.f_in)
        html_file.write('<table border="1">')
        html_file.write('  <tr><th>PLL name</th><th>Frequency</th><th>FDIV</th></tr>\n')
        for pll_name in ('ARM','DDR','IO'):
            name=pll_name+' PLL'
            if pll_name in self.pll_fdivs:
                freq=self.f_in*self.pll_fdivs[pll_name]
    #            html_file.write('  <tr><th>'+name+'</th><td>'+('%.3f MHz'%freq)+'</td><td>'+str(self.pll_fdivs[pll_name])+'</td></tr>\n')
                html_file.write('  <tr><th>%s</th><td>%.3f MHz</td><td>%s</td></tr>\n'%(name,freq,str(self.pll_fdivs[pll_name])))
            else:
                html_file.write('  <tr><th>%s</th><td colspan="2" align="center">Unused</td></tr>\n'%name)
                    
        html_file.write('</table>')

        html_file.write('<h2>System Clocks</h2>')
        html_file.write('<table border="1">')
        html_file.write('  <tr><th>Name</th><th>Frequency</th><th>Target</th><th>Error</th><th>PLL</th><th>div 1</th><th>div 2</th><th>Config. name</th><th>Comments</th></tr>\n')

#TODO - show secondary clocks together with the main ones (frequency only if different from source. Use rowspan
#   self.iface_divs[name]={'SOURCE':source,'VALUE':value, 'FREQ':frequency} #no 'PLL' field   
#CLK_TEMPLATE
        for line in CLK_TEMPLATE:
            name=line['NAME']
            if (name in self.iface_divs) and ('PLL' in self.iface_divs[name]):
                iface=self.iface_divs[name]
                freq=iface['FREQ']
                target=iface['TARGET']
                rel_err=(freq-target)/target
                pll=iface['PLL']
                div1=iface['DIV']
                conf_name=  self.features.get_par_confname(self.clk_dict[name]['VALUE'])
                description=self.features.get_par_description(self.clk_dict[name]['VALUE'])
                try:
                    div2='%i'%iface['DIV2']
                except:
                    div2='-'
                children=list_with_children(name)
                html_file.write('  <tr><th>%s</th><td>%.3f MHz</td><td>%.3f MHz</td><td>%.2f%%</td><td>%s</td><td>%i</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(
                                          name,        freq,           target,     100*rel_err,    pll,        div1,     div2, conf_name,   description))
                html_file.write('  </tr>')
                for kid_name in children[1:]:
                    kid_freq=self.iface_divs[kid_name]['FREQ']
                    source=self.iface_divs[kid_name]['SOURCE']
                    html_file.write('  <tr><th>%s</th><td>%.3f MHz</td><td colspan="7" align="center">Derived from %s</td></tr>'%(kid_name, kid_freq,source))
#                if len(children)>1:
#                    print name, "has children=",children
#            elif name in self.iface_divs:
#                print 'dependent ',name,' -> ',self.iface_divs[name]
                        
        html_file.write('</table>')
    def get_ddr_mhz(self):
        return self.f_in*self.pll_fdivs[self.iface_divs['DDR']['PLL']]/self.iface_divs['DDR']['DIV']

    def get_new_register_sets(self):
        return self.clk_register_set.get_register_sets(True,True)

    def clocks_regs_setup(self,current_reg_sets,unlock_needed=True,force=False,warn=False):
        clk_register_set=self.clk_register_set
        clk_register_set.set_initial_state(current_reg_sets, True)# start from the current registers state
        if unlock_needed:
            self.slcr_unlock()
            _ = clk_register_set.get_register_sets(True,True) # close previous register settings
# Bypass used PLL-s - stage 1 of PLL setup     
        self.clocks_pll_bypass(force=False,warn=False)
        _ = clk_register_set.get_register_sets(True,True) # close previous register settings
# Turn on PLL reset and program feedback -  stage 2 of PLL setup     
        self.clocks_pll_reset_and_fdiv(force=False,warn=False)
        _ = clk_register_set.get_register_sets(True,True) # close previous register settings
# Configure PLL parameters -  stage 3 of PLL setup     
        self.clocks_pll_conf(force=False,warn=False)
        _ = clk_register_set.get_register_sets(True,True) # close previous register settings
# Release reset of the PLLs (let them start) -  stage 4 of PLL setup     
        self.clocks_pll_start(force=False,warn=False)
        _ = clk_register_set.get_register_sets(True,True) # close previous register settings
# stage 5 of clocks setup
        self.clocks_program(force=False,warn=False)
  
# #Trying toggle feature (but actually for now it can be left in reset state - is this on/off/on needed?                
#         _ = ddriob_register_set.get_register_sets(True,True) # close previous register settings
#         ddriob_register_set.set_bitfields('ddriob_dci_ctrl', ('reset',1),force,warn)        
#         _ = ddriob_register_set.get_register_sets(True,True) # close previous register settings
#         ddriob_register_set.set_bitfields('ddriob_dci_ctrl', ('reset',0),force,warn)        
#         _ = ddriob_register_set.get_register_sets(True,True) # close previous register settings
#         ddriob_register_set.set_bitfields('ddriob_dci_ctrl', (('reset', 1),
#                                                               ('enable',1),
#                                                               ('nref_opt1',0),
#                                                               ('nref_opt2',0),
#                                                               ('nref_opt4',1),
#                                                               ('pref_opt2',0),
#                                                               ('update_control',0)),force,warn)        
    
    

#Unlock SLCR (if the code is running after RBL) - stage 0 of PLL setup     
    def slcr_unlock(self):
        clk_register_set=self.clk_register_set
        if self.verbosity>0 :
            print 'Unlocking SLCR'
        clk_register_set.set_word('slcr_unlock',0xdf0d)
  
#Bypass used PLL-s - stage 1 of PLL setup     
    def clocks_pll_bypass(self,force=False,warn=False):
        clk_register_set=self.clk_register_set
        if self.verbosity>0 :
            print 'pll_fdivs=', self.pll_fdivs
        if 'DDR' in self.pll_fdivs:
            clk_register_set.set_bitfields('ddr_pll_ctrl',( # Bypass override control: 1 - bypassed, 0: if pll_bypass_qual==0: enabled, not bypassed else depends on pin strap
                                                     ('pll_bypass_qual',          0), # no more reagard for pin strap
                                                     ('pll_bypass_force',         1)),force,warn)
        if 'IO' in self.pll_fdivs:
            clk_register_set.set_bitfields('io_pll_ctrl', ( # Bypass override control: 1 - bypassed, 0: if pll_bypass_qual==0: enabled, not bypassed else depends on pin strap
                                                     ('pll_bypass_qual',          0), # no more reagard for pin strap
                                                     ('pll_bypass_force',         1)),force,warn)
        if 'ARM' in self.pll_fdivs:
            clk_register_set.set_bitfields('arm_pll_ctrl',( # Bypass override control: 1 - bypassed, 0: if pll_bypass_qual==0: enabled, not bypassed else depends on pin strap
                                                     ('pll_bypass_qual',          0), # no more reagard for pin strap
                                                     ('pll_bypass_force',         1)),force,warn)

# Turn on PLL reset and program feedback -  stage 2 of PLL setup     
    def clocks_pll_reset_and_fdiv(self,force=False,warn=False):
        clk_register_set=self.clk_register_set
        if 'DDR' in self.pll_fdivs:
            clk_register_set.set_bitfields('ddr_pll_ctrl',( # 
                                                     ('pll_fdiv',  self.pll_fdivs['DDR']),
                                                     ('pll_reset',                     1)),force,warn)
        if 'IO' in self.pll_fdivs:
            clk_register_set.set_bitfields('io_pll_ctrl',( # 
                                                     ('pll_fdiv',  self.pll_fdivs['IO']),
                                                     ('pll_reset',                     1)),force,warn)
        if 'ARM' in self.pll_fdivs:
            clk_register_set.set_bitfields('arm_pll_ctrl',( # 
                                                     ('pll_fdiv',  self.pll_fdivs['ARM']),
                                                     ('pll_reset',                     1)),force,warn)
            
# Configure PLL parameters -  stage 3 of PLL setup     
    def clocks_pll_conf(self,force=False,warn=False):
        clk_register_set=self.clk_register_set
        if 'DDR' in self.pll_fdivs:
            ddr_fdiv=self.pll_fdivs['DDR']
            clk_register_set.set_bitfields('ddr_pll_cfg',( # DDR PLL Configuration
                                                      ('lock_cnt',  self.pll_pars[ddr_fdiv]['LOCK_CNT']), # Lock status bit delay (in clock cycles)
                                                      ('pll_cp',    self.pll_pars[ddr_fdiv]['PLL_CP']),   # PLL charge pump control
                                                      ('pll_res',   self.pll_pars[ddr_fdiv]['PLL_RES']),  # PLL loop filter resistor control
                                                                                             ),force,warn)
        if 'IO' in self.pll_fdivs:
            io_fdiv=self.pll_fdivs['IO']
            clk_register_set.set_bitfields('io_pll_cfg',( # IO PLL Configuration
                                                      ('lock_cnt',  self.pll_pars[io_fdiv]['LOCK_CNT']), # Lock status bit delay (in clock cycles)
                                                      ('pll_cp',    self.pll_pars[io_fdiv]['PLL_CP']),   # PLL charge pump control
                                                      ('pll_res',   self.pll_pars[io_fdiv]['PLL_RES']),  # PLL loop filter resistor control
                                                                                             ),force,warn)
        if 'ARM' in self.pll_fdivs:
            arm_fdiv=self.pll_fdivs['ARM']
            clk_register_set.set_bitfields('arm_pll_cfg',( # ARM PLL Configuration
                                                      ('lock_cnt',  self.pll_pars[arm_fdiv]['LOCK_CNT']), # Lock status bit delay (in clock cycles)
                                                      ('pll_cp',    self.pll_pars[arm_fdiv]['PLL_CP']),   # PLL charge pump control
                                                      ('pll_res',   self.pll_pars[arm_fdiv]['PLL_RES']),  # PLL loop filter resistor control
                                                                                             ),force,warn)
# Release reset of the PLLs (let them start) -  stage 4 of PLL setup     
    def clocks_pll_start(self,force=False,warn=False):
        clk_register_set=self.clk_register_set
        if 'DDR' in self.pll_fdivs:
            clk_register_set.set_bitfields('ddr_pll_ctrl',(('pll_reset',   0)),force,warn)
        if 'IO' in self.pll_fdivs:
            clk_register_set.set_bitfields('io_pll_ctrl', (('pll_reset',   0)),force,warn)
        if 'ARM' in self.pll_fdivs:
            clk_register_set.set_bitfields('arm_pll_ctrl',(('pll_reset',   0)),force,warn)

# Release bypass the PLLs (PLLs should be locked already!)     
    def clocks_pll_bypass_off(self,current_reg_sets,force=False,warn=False):
        clk_register_set=self.clk_register_set
        clk_register_set.set_initial_state(current_reg_sets, True)# start from the current registers state

        if 'DDR' in self.pll_fdivs:
            clk_register_set.set_bitfields('ddr_pll_ctrl',(('pll_bypass_force',  0),
                                                           ('pll_bypass_qual',   0)),force,warn)
        if 'IO' in self.pll_fdivs:
            clk_register_set.set_bitfields('io_pll_ctrl', (('pll_bypass_force',  0),
                                                           ('pll_bypass_qual',   0)),force,warn)
        if 'ARM' in self.pll_fdivs:
            clk_register_set.set_bitfields('arm_pll_ctrl',(('pll_bypass_force',  0),
                                                           ('pll_bypass_qual',   0)),force,warn)

#clocks setup 
    def clocks_program(self,force=False,warn=False):
        clk_register_set=self.clk_register_set
# PLLs are now bypassed and reset, now program        
# reg  arm_clk_ctrl, offs=0x120 dflt:0x1f000400 actual: 0x1f000200
        cpu_peri_clkact = 1
        cpu_1x_clkact=    1
        cpu_2x_clkact=    1
        cpu_3x2x_clkact=  1
        cpu_6x4x_clkact=  1
        try:
            cpu_divisor= self.iface_divs['ARM']['DIV'] # Should be set - 0x2
        except:
            raise Exception ('Unknown ARM clock divisor - should be set by now')
        if   self.iface_divs['ARM']['PLL']=='ARM':     
            cpu_srcsel= 0
        elif self.iface_divs['ARM']['PLL']=='DDR':     
            cpu_srcsel= 2
        else: # if self.iface_divs['ARM']['PLL']=='IO':     
            cpu_srcsel= 3
        clk_register_set.set_bitfields('arm_clk_ctrl',( # CPU clock control
#                                                     ('reserved1',                     0),  #
                                                     ('cpu_peri_clkact', cpu_peri_clkact),  # Peripheral clock active (0 - disabled)
                                                     ('cpu_1x_clkact',     cpu_1x_clkact),  # CPU-1x clock active (0 - disabled)
                                                     ('cpu_2x_clkact',     cpu_2x_clkact),  # CPU-2x clock active (0 - disabled)
                                                     ('cpu_3x2x_clkact', cpu_3x2x_clkact),  # CPU-3x2x clock active (0 - disabled)
                                                     ('cpu_6x4x_clkact', cpu_6x4x_clkact),  # CPU-6x4x clock active (0 - disabled)
#                                                     ('reserved2',                     0),  #
                                                     ('divisor',             cpu_divisor),  # Frequency divisor for the CPU clock source. If PLL is NOT bypassed values 1 and 3 are invalid #2
#                                                     ('reserved3',                     0),  #
                                                     ('srcsel',               cpu_srcsel),  # CPU clock source: 0,1 - ARM PLL, 2 - DDR PLL, 3 - IO PLL, This filed is reset by POR only     #0 
#                                                     ('reserved4',                     0),  #
                                                                                            ),force,warn)

# reg  ddr_clk_ctrl, offs=0x124 dflt:0x18400003 actual: 0xc200003
        try:
            ddr_2x_clk_divisor= self.iface_divs['DDR2X']['DIV'] # 0x3
            ddr_2x_clkact = 1
        except:  # not defined
            ddr_2x_clk_divisor= 0
            ddr_2x_clkact = 0
        try:    
            ddr_3x_clk_divisor= self.iface_divs['DDR']['DIV'] # 0x2
            ddr_3x_clkact = 0x1
        except:  # not defined   
            ddr_3x_clk_divisor= 0
            ddr_3x_clkact =     0
        clk_register_set.set_bitfields('ddr_clk_ctrl',( # DDR_3x (including PHY) and DDR_2X clock control
                                                     ('ddr_2x_clk_divisor',  ddr_2x_clk_divisor),  # 0x3  Frequency divisor for ddr_2x clk
                                                     ('ddr_3x_clk_divisor',  ddr_3x_clk_divisor),  # 0x2 Frequency divisor for ddr_3x clk
#                                                     ('reserved1',           0),  # reserved
                                                     ('ddr_2x_clkact',       ddr_2x_clkact),  # 0x1 1 - ddr_2x clk enabled (0 - disabled)
                                                     ('ddr_3x_clkact',       ddr_3x_clkact),  # 0x1 1 - ddr_3x clk enabled (0 - disabled)
                                                                                            ),force,warn)
# reg  dci_clk_ctrl, offs=0x128 dflt:0x18400003 actual: 0x302301
        try:
            dci_divisor1 = self.iface_divs['DDR_DCI']['DIV2'] # 0x3
            dci_divisor0 = self.iface_divs['DDR_DCI']['DIV'] # 0x23
            dci_clkact   = 1 #0x1  
        except: # not defined
            dci_divisor1 = 0
            dci_divisor0 = 0
            dci_clkact   = 0  
        clk_register_set.set_bitfields('dci_clk_ctrl',( # DDR DCI clock control
#                                                     ('reserved1',           0),  #
                                                      ('divisor1', dci_divisor1),  # 0x3 Frequency divisor, second stage
#                                                     ('reserved2',           0),  #
                                                      ('divisor0', dci_divisor0),  # 0x23 Frequency divisor, first stage
#                                                     ('reserved3',           0),  #
                                                      ('clkact',     dci_clkact),  # 0x1 1 - dci clock enabled (0 - disabled)
                                                                                            ),force,warn)

# reg  aper_clk_ctrl, offs=0x12c dflt:0x01ffcccd actual: 0x01ec044d (set after peripherals - does it really need so?
        smc_cpu_1x_clkact     = 'SMC' in self.iface_divs # 0x1
        lqspi_cpu_1x_clkact   = 'QSPI' in self.iface_divs # 0x1
        gpio_cpu_1x_clkact    = 1 # 0x1
        uart1_cpu_1x_clkact   = 'UART1' in self.iface_divs # 0x1
        uart0_cpu_1x_clkact   = 'UART0' in self.iface_divs # 0x1
        i2c1_cpu_1x_clkact    = 'I2C1'  in self.iface_divs # 0x1
        i2c0_cpu_1x_clkact    = 'I2C0'  in self.iface_divs # 0x1
        can1_cpu_1x_clkact    = 'CAN1'  in self.iface_divs # 0x1
        can0_cpu_1x_clkact    = 'CAN0'  in self.iface_divs # 0x1
        spi1_cpu_1x_clkact    = 'SPI1'  in self.iface_divs # 0x1
        spi0_cpu_1x_clkact    = 'SPI0'  in self.iface_divs # 0x1
        sdi1_cpu_1x_clkact    = 'SDI1'  in self.iface_divs # 0x1
        sdi0_cpu_1x_clkact    = 'SDI0'  in self.iface_divs # 0x1
        gem1_cpu_1x_clkact    = 'GIGE1' in self.iface_divs # 0x1
        gem0_cpu_1x_clkact    = 'GIGE0' in self.iface_divs # 0x1
        usb1_cpu_1x_clkact    = 'USB1'  in self.iface_divs # 0x1
        usb0_cpu_1x_clkact    = 'USB1'  in self.iface_divs # 0x1
        dma_cpu_2x_clkact    = 1 # 0x1
        clk_register_set.set_bitfields('aper_clk_ctrl',( # AMBA peripherals clock control
 #                                                    ('reserved1',                       0),  #
                                                     ('smc_cpu_1x_clkact',    smc_cpu_1x_clkact),   # 0x1 SMC AMBA clock control (1- enabled, 0- disabled)
                                                     ('lqspi_cpu_1x_clkact',  lqspi_cpu_1x_clkact), # 0x1 QSPI AMBA clock control (1- enabled, 0- disabled)
                                                     ('gpio_cpu_1x_clkact',   gpio_cpu_1x_clkact),  # 0x1 GPIO AMBA clock control (1- enabled, 0- disabled)
                                                     ('uart1_cpu_1x_clkact',  uart1_cpu_1x_clkact), # 0x1 UART1 AMBA clock control (1- enabled, 0- disabled)
                                                     ('uart0_cpu_1x_clkact',  uart0_cpu_1x_clkact), # 0x1 UART0 AMBA clock control (1- enabled, 0- disabled)
                                                     ('i2c1_cpu_1x_clkact',   i2c1_cpu_1x_clkact),  # 0x1 I2C1 AMBA clock control (1- enabled, 0- disabled)
                                                     ('i2c0_cpu_1x_clkact',   i2c0_cpu_1x_clkact),  # 0x1 I2C0 AMBA clock control (1- enabled, 0- disabled)
                                                     ('can1_cpu_1x_clkact',   can1_cpu_1x_clkact),  # 0x1 CAN1 AMBA clock control (1- enabled, 0- disabled)
                                                     ('can0_cpu_1x_clkact',   can0_cpu_1x_clkact),  # 0x1 CAN0 AMBA clock control (1- enabled, 0- disabled)
                                                     ('spi1_cpu_1x_clkact',   spi1_cpu_1x_clkact),  # 0x1 SPI1 AMBA clock control (1- enabled, 0- disabled)
                                                     ('spi0_cpu_1x_clkact',   spi0_cpu_1x_clkact),  # 0x1 SPI0 AMBA clock control (1- enabled, 0- disabled)
#                                                     ('reserved2',                       0),  #
#                                                     ('reserved3',                       0),  #
                                                     ('sdi1_cpu_1x_clkact',   sdi1_cpu_1x_clkact),  # 0x1 SDI1 AMBA clock control (1- enabled, 0- disabled)
                                                     ('sdi0_cpu_1x_clkact',   sdi0_cpu_1x_clkact),  # 0x1 SDI0 AMBA clock control (1- enabled, 0- disabled)
                                                     ('reserved4',                       0),  #
                                                     ('reserved5',                       0),  #
                                                     ('gem1_cpu_1x_clkact',   gem1_cpu_1x_clkact),  # 0x1 Gigabit Ethernet 1 AMBA clock control (1- enabled, 0- disabled)
                                                     ('gem0_cpu_1x_clkact',   gem0_cpu_1x_clkact),  # 0x1 Gigabit Ethernet 0 AMBA clock control (1- enabled, 0- disabled)
#                                                     ('reserved6',                       0),  #
#                                                     ('reserved7',                       0),  #
                                                     ('usb1_cpu_1x_clkact',   usb1_cpu_1x_clkact),  # 0x1 USB1 AMBA clock control (1- enabled, 0- disabled)
                                                     ('usb0_cpu_1x_clkact',   usb0_cpu_1x_clkact),  # 0x1 USB0 AMBA clock control (1- enabled, 0- disabled)
#                                                     ('reserved2',                       0),  #
                                                     ('dma_cpu_2x_clkact',    dma_cpu_2x_clkact),  # 0x1 DMA controller AMBA clock control (1- enabled, 0- disabled)
                                                                                            ),force,warn)
        
        if 'USB0' in self.iface_divs:                  
# reg  usb0_clk_ctrl, offs=0x130 dflt:0x00101941 actual: never set
            usb0_srcsel= 4 # Only possible
            clk_register_set.set_bitfields('usb0_clk_ctrl',( # USB 0 ULPI clock control
                                                     ('reserved1',                       0),
                                                     ('reserved2',                     0x1),
                                                     ('reserved3',                       0),
                                                     ('reserved4',                    0x19),
                                                     ('reserved5',                       0),
                                                     ('srcsel',                usb0_srcsel),
                                                     ('reserved6',                       0),
                                                     ('reserved7',                       1),
                                                                                            ),force,warn)
        if 'USB1' in self.iface_divs:                  
# reg  usb1_clk_ctrl, offs=0x134 dflt:0x00101941 actual: never set
            usb1_srcsel= 4 # Only possible
            clk_register_set.set_bitfields('usb0_clk_ctrl',( # USB 1 ULPI clock control
#                                                     ('reserved1',                       0),
#                                                     ('reserved2',                     0x1),
#                                                     ('reserved3',                       0),
#                                                     ('reserved4',                    0x19),
#                                                     ('reserved5',                       0),
                                                     ('srcsel',                usb1_srcsel),
#                                                     ('reserved6',                       0),
#                                                     ('reserved7',                       1),
                                                                                            ),force,warn)
# reg  gem0_rclk_ctrl, offs=0x138 dflt:0x1 actual: 0x1
        try:
            gem0_rclk_srcsel=self.iface_divs['GIGE0']['SOURCE']=='EMIO' 
            gem0_rclk_clkact=1
        except:
            gem0_rclk_srcsel=0 
            if 'GIGE0' in self.iface_divs:
                gem0_rclk_clkact=1
            else:    
                gem0_rclk_clkact=0
        clk_register_set.set_bitfields('gem0_rclk_ctrl',( # Gigabit Ethernet 0 RX clock and RX signals select
#                                                     ('reserved1',                       0),  #
                                                     ('srcsel',           gem0_rclk_srcsel),  #
#                                                     ('reserved2',                       0),  #
                                                     ('clkact',           gem0_rclk_clkact),  #
                                                                                            ),force,warn)
# reg  gem1_rclk_ctrl, offs=0x13c dflt:0x1 actual: 0x1
        try:
            gem1_rclk_srcsel=self.iface_divs['GIGE1']['SOURCE']=='EMIO' 
            gem1_rclk_clkact=1
        except:
            gem1_rclk_srcsel=0 
            if 'GIGE1' in self.iface_divs:
                gem1_rclk_clkact=1
            else:    
                gem1_rclk_clkact=0
        clk_register_set.set_bitfields('gem1_rclk_ctrl',( # Gigabit Ethernet 0 RX clock and RX signals select
#                                                     ('reserved1',                       0),  #
                                                     ('srcsel',           gem1_rclk_srcsel),  #
#                                                    ('reserved2',                       0),  #
                                                     ('clkact',           gem1_rclk_clkact),  #
                                                                                            ),force,warn)

# reg  gem0_clk_ctrl, offs=0x140 dflt:0x3c01 actual: 0x100801
        # set frequency divisors if specified, otherwise - set them to "1"
        try:
            gem0_divisor=self.iface_divs['GIGE0']['DIV'] 
        except:
            gem0_divisor=1 
        try:
            gem0_divisor1=self.iface_divs['GIGE0']['DIV2'] 
        except:
            gem0_divisor1=1 
        try:
            if self.iface_divs['GIGE0']['SOURCE']=='EMIO': # may cause exception
                gem0_srcsel= 4
                gem0_clkact=1
        except: # GIGE0 or GIGE0 source are not specified
            if 'GIGE0' in self.iface_divs:
                if self.iface_divs['GIGE0']['PLL']=='ARM':     
                    gem0_srcsel= 2
                elif self.iface_divs['GIGE0']['PLL']=='DDR':     
                    gem0_srcsel= 3
                else: # if self.iface_divs['GIGE0']['PLL']=='IO':     
                    gem0_srcsel= 0
                gem0_clkact=1
            else:        
                gem0_srcsel= 0
                gem0_clkact=0
        clk_register_set.set_bitfields('gem0_clk_ctrl',( # Gigabit Ethernet 0 Reference clock control
#                                                     ('reserved1',             0),  #
                                                     ('divisor1',  gem0_divisor1),  # 0x1
#                                                     ('reserved2',             0),  #
                                                     ('divisor',    gem0_divisor),  # 0x8
#                                                     ('reserved3',             0),  #
                                                     ('srcsel',      gem0_srcsel),  # 0x0
#                                                     ('reserved4',             0),  #
                                                     ('clkact',      gem0_clkact),  # 0x1
                                                                                            ),force,warn)
        
# reg  gem1_clk_ctrl, offs=0x144 dflt:0x3c01 actual: never set
        # set frequency divisors if specified, otherwise - set them to "1"
        try:
            gem1_divisor=self.iface_divs['GIGE1']['DIV'] 
        except:
            gem1_divisor=1 
        try:
            gem1_divisor1=self.iface_divs['GIGE1']['DIV2'] 
        except:
            gem1_divisor1=1 
        try:
            if self.iface_divs['GIGE1']['SOURCE']=='EMIO': # may cause exception
                gem1_srcsel= 4
                gem1_clkact=1
        except: # GIGE1 or GIGE1 source are not specified
            if 'GIGE1' in self.iface_divs:
                if self.iface_divs['GIGE1']['PLL']=='ARM':     
                    gem1_srcsel= 2
                elif self.iface_divs['GIGE1']['PLL']=='DDR':     
                    gem1_srcsel= 3
                else: # if self.iface_divs['GIGE1']['PLL']=='IO':     
                    gem1_srcsel= 0
                gem1_clkact=1
            else:        
                gem1_srcsel= 0
                gem1_clkact=0
        clk_register_set.set_bitfields('gem1_clk_ctrl',( # Gigabit Ethernet 1 Reference clock control
#                                                     ('reserved1',             0),  #
                                                     ('divisor1',  gem1_divisor1),  # 0x1
#                                                     ('reserved2',            0),  #
                                                     ('divisor',    gem1_divisor),  # 0x8
#                                                     ('reserved3',             0),  #
                                                     ('srcsel',      gem1_srcsel),  # 0x0
#                                                     ('reserved4',             0),  #
                                                     ('clkact',      gem1_clkact),  # 0x1
                                                                                            ),force,warn)
# Is it OK to modify it now (in RBL) - maybe NAND is being used ?
# reg  smc_clk_ctrl, offs=0x148 dflt:0x3c21 actual: Never modified
        if 'SMC' in self.iface_divs:
            if self.iface_divs['SMC']['PLL']=='ARM':     
                smc_srcsel= 2
            elif self.iface_divs['SMC']['PLL']=='DDR':     
                smc_srcsel= 3
            else: # if self.iface_divs['SMC']['PLL']=='IO':     
                smc_srcsel= 0
            smc_divisor=self.iface_divs['SMC']['DIV']
            smc_clkact=1
                
        else:
            smc_divisor= 1        
            smc_srcsel= 0
            smc_clkact=0
        clk_register_set.set_bitfields('smc_clk_ctrl',( # SMC Reference clock control
                                                     ('reserved1',          0),  #
                                                     ('divisor',  smc_divisor),# Frequency divisor
                                                     ('reserved2',          0),  #
                                                     ('srcsel',    smc_srcsel),  # Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL
                                                     ('reserved3',          0),  #
                                                     ('clkact',    smc_clkact),  # SMC reference clock: 1 -  enabled (0 - disabled)
                                                                                            ),force,warn)

# Is it OK to modify it now (in RBL) - maybe QSPI is being used ?
# reg  lqspi_clk_ctrl, offs=0x14c dflt:0x2821 actual: 0x721
        if 'QSPI' in self.iface_divs:
            if self.iface_divs['QSPI']['PLL']=='ARM':     
                qspi_srcsel= 2
            elif self.iface_divs['QSPI']['PLL']=='DDR':     
                qspi_srcsel= 3
            else: # if self.iface_divs['QSPI']['PLL']=='IO':     
                qspi_srcsel= 0
            qspi_divisor=self.iface_divs['QSPI']['DIV']
            qspi_clkact=1
                
        else:
            qspi_divisor= 1        
            qspi_srcsel= 0
            qspi_clkact=0
        clk_register_set.set_bitfields('lqspi_clk_ctrl',( # Quad SPI Reference clock control
#                                                     ('reserved1',          0),  #
                                                     ('divisor',  qspi_divisor),  # 0x7 Frequency divisor
#                                                     ('reserved2',          0),  #
                                                     ('srcsel',    qspi_srcsel),  # 0x2 Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL
#                                                     ('reserved3',          0),  #
                                                     ('clkact',    qspi_clkact),  # 0x1 Quad SPI reference clock: 1 -  enabled (0 - disabled)
                                                                                            ),force,warn)
# Is it OK to modify it now (in RBL) - if SDIO is being used ?
# reg  sdio_clk_ctrl, offs=0x150 dflt:0x1e03 actual: 0x801
        if 'SDIO' in self.iface_divs:
            if self.iface_divs['SDIO']['PLL']=='ARM':     
                sdio_srcsel= 2
            elif self.iface_divs['SDIO']['PLL']=='DDR':     
                sdio_srcsel= 3
            else: # if self.iface_divs['SDIO']['PLL']=='IO':     
                sdio_srcsel= 0
            sdio_divisor=self.iface_divs['SDIO']['DIV']
            sdio_clkact1='SDIO1' in self.iface_divs
            sdio_clkact0='SDIO0' in self.iface_divs
        else:
            sdio_divisor=  1
            sdio_srcsel =  0
            sdio_clkact1 = 0
            sdio_clkact0 = 0
        clk_register_set.set_bitfields('sdio_clk_ctrl',( # SDIO 0,1 Reference clock control
#                                                     ('reserved1',          0),  #
                                                     ('divisor', sdio_divisor),  # 0x8 Frequency divisor
#                                                     ('reserved2',          0),  #
                                                     ('srcsel',   sdio_srcsel),  # 0x0 Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL
#                                                     ('reserved3',          0),  #
                                                     ('clkact1', sdio_clkact1),  # 0x0 SDIO 1 reference clock: 1 -  enabled (0 - disabled)
                                                     ('clkact0', sdio_clkact0),  # 0x1 SDIO 0 reference clock: 1 -  enabled (0 - disabled)
                                                                                            ),force,warn)

# reg  uart_clk_ctrl, offs=0x154 dflt:0x3f03 actual: 0xa02
        if 'UART' in self.iface_divs:
            if self.iface_divs['UART']['PLL']=='ARM':     
                uart_srcsel= 2
            elif self.iface_divs['UART']['PLL']=='DDR':     
                uart_srcsel= 3
            else: # if self.iface_divs['UART']['PLL']=='IO':     
                uart_srcsel= 0
            uart_divisor=self.iface_divs['UART']['DIV']
            uart_clkact1='UART1' in self.iface_divs
            uart_clkact0='UART0' in self.iface_divs
        else:
            uart_divisor=  1
            uart_srcsel =  0
            uart_clkact1 = 0
            uart_clkact0 = 0

        clk_register_set.set_bitfields('uart_clk_ctrl',( # UART 0,1 Reference clock control
 #                                                    ('reserved1',          0),  #
                                                     ('divisor', uart_divisor),  # 0xa Frequency divisor
 #                                                    ('reserved2',          0),  #
                                                     ('srcsel',   uart_srcsel),  # 0x0 Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL
 #                                                    ('reserved3',          0),  #
                                                     ('clkact1', uart_clkact1),  # 0x1 UART 1 reference clock: 1 -  enabled (0 - disabled)
                                                     ('clkact0', uart_clkact0),  # 0x0 UART 0 reference clock: 1 -  enabled (0 - disabled)
                                                                                            ),force,warn)
# 
#       'spi_clk_ctrl':             {'OFFS': 0x158,'DFLT':0x3f03,'RW':'RW', # Never set
#                                    'COMMENTS':'SPI 0,1 Reference clock control',
#                                    'FIELDS':{
# reg  spi_clk_ctrl, offs=0x158 dflt:0x3f03 actual: Never set
        if 'SPI' in self.iface_divs:
            if self.iface_divs['SPI']['PLL']=='ARM':     
                spi_srcsel= 2
            elif self.iface_divs['SPI']['PLL']=='DDR':     
                spi_srcsel= 3
            else: # if self.iface_divs['SPI']['PLL']=='IO':     
                spi_srcsel= 0
            spi_divisor=self.iface_divs['SPI']['DIV']
            spi_clkact1='SPI1' in self.iface_divs
            spi_clkact0='SPI0' in self.iface_divs
        else:
            spi_divisor=  1
            spi_srcsel =  0
            spi_clkact1 = 0
            spi_clkact0 = 0
        clk_register_set.set_bitfields('spi_clk_ctrl',( # SPI 0,1 Reference clock control
#                                                     ('reserved1',          0),  #
                                                     ('divisor', spi_divisor),  # Frequency divisor
#                                                     ('reserved2',          0),  #
                                                     ('srcsel',   spi_srcsel),  # Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL
#                                                     ('reserved3',          0),  #
                                                     ('clkact1', spi_clkact1),  # SPI 1 reference clock: 1 -  enabled (0 - disabled)
                                                     ('clkact0', spi_clkact0),  # SPI 0 reference clock: 1 -  enabled (0 - disabled)
                                                                                            ),force,warn)

# reg  can_clk_ctrl, offs=0x15c dflt:0x501903 actual: Never set
        if 'CAN' in self.iface_divs:
            if self.iface_divs['CAN']['PLL']=='ARM':     
                can_srcsel= 2
            elif self.iface_divs['CAN']['PLL']=='DDR':     
                can_srcsel= 3
            else: # if self.iface_divs['CAN']['PLL']=='IO':     
                can_srcsel= 0
            can_divisor1=self.iface_divs['CAN']['DIV2']
            can_divisor= self.iface_divs['CAN']['DIV']
            can_clkact1='CAN1' in self.iface_divs
            can_clkact0='CAN0' in self.iface_divs
        else:
            can_divisor1= 1
            can_divisor=  1
            can_srcsel =  0
            can_clkact1 = 0
            can_clkact0 = 0

        clk_register_set.set_bitfields('can_clk_ctrl',( # CAN 0,1 Reference clock control
#                                                     ('reserved1',          0),  #
                                                     ('divisor1',can_divisor1),  # Frequency divisor, second stage
#                                                     ('reserved2',          0),  #
                                                     ('divisor',  can_divisor),  # Frequency divisor
#                                                     ('reserved3',          0),  #
                                                     ('srcsel',    can_srcsel),  # Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL
#                                                     ('reserved4',          0),  #
                                                     ('clkact1',  can_clkact1),  # CAN 1 reference clock: 1 -  enabled (0 - disabled)
                                                     ('clkact0',  can_clkact0),  # can 0 reference clock: 1 -  enabled (0 - disabled)
                                                                                            ),force,warn)

#        print 'self.used_mio_interfaces=',self.used_mio_interfaces
        for mio_iface in self.used_mio_interfaces:
            if (mio_iface['NAME']=='CAN_ECLK') and (mio_iface['CHANNEL']==0):
                can0_mux=  mio_iface['PIN']
                can0_ref_sel=1
                break
        else:
                can0_mux=    0
                can0_ref_sel=0
                
        for mio_iface in self.used_mio_interfaces:
            if (mio_iface['NAME']=='CAN_ECLK') and (mio_iface['CHANNEL']==1):
                can1_mux=  mio_iface['PIN']
                can1_ref_sel=1
                break
        else:
                can1_mux=    0
                can1_ref_sel=0
# reg  can_mioclk_ctrl, offs=0x160 dflt:0x0 actual: Never set
        clk_register_set.set_bitfields('can_mioclk_ctrl',( # CAN MIO clock control
#                                                     ('reserved1',               0),  #
                                                     ('can1_ref_sel', can1_ref_sel),  # CAN1 reference clock selection: 0: from internal PLL, 1 - from MIO based on can1_mux selection
                                                     ('can1_mux',         can1_mux),  # CAN1 MIO pin selection (valid: 0..53)
#                                                     ('reserved2',               0),  #
                                                     ('can0_ref_sel', can0_ref_sel),  # CAN0 reference clock selection: 0: from internal PLL, 1 - from MIO based on can0_mux selection
                                                     ('can0_mux',         can0_mux),  # CAN0 MIO pin selection (valid: 0..53)
                                                                                            ),force,warn)

# reg  dbg_clk_ctrl, offs=0x164 dflt:0xf03 actual: ever set
        if 'TRACE' in self.iface_divs:
            try:
                dbg_divisor=self.iface_divs['TRACE']['DIV'] 
            except:
                dbg_divisor=1 

            try:
                if self.iface_divs['TRACE']['SOURCE']=='EMIO': # may cause exception
                    dbg_srcsel= 4
                    dbg_clkact_trc=1
            except:
                if self.iface_divs['TRACE']['PLL']=='ARM':     
                    dbg_srcsel= 2
                elif self.iface_divs['TRACE']['PLL']=='DDR':     
                    dbg_srcsel= 3
                else: # if self.iface_divs['TRACE']['PLL']=='IO':     
                    dbg_srcsel= 0
                dbg_clkact_trc=1
        else:
            dbg_divisor=0xf # default
            dbg_srcsel= 0   # rurn off
        dbg_cpu_1x_clkact = 1 # always (is it the same as used for otgher peripherals and should be on?)
        clk_register_set.set_bitfields('dbg_clk_ctrl',( # SoC debug clock control
#                                                     ('reserved1',                     0),  #
                                                     ('divisor',             dbg_divisor),  # Frequency divisor
#                                                     ('reserved2',                     0),  #
                                                     ('srcsel',               dbg_srcsel),  # Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL, 4..7 - EMIO trace clock
#                                                     ('reserved3',                     0),  #
                                                     ('cpu_1x_clkact', dbg_cpu_1x_clkact),  # CPU 1x clock: 1 -  enabled (0 - disabled)
                                                     ('clkact_trc',       dbg_clkact_trc),  # Debug trace clock: 1 -  enabled (0 - disabled)
                                                                                            ),force,warn)
# reg  pcap_clk_ctrl, offs=0x168 dflt:0xf01 actual: 0x501
        if 'PCAP' in self.iface_divs:
            try:
                pcap_divisor=self.iface_divs['PCAP']['DIV'] 
            except:
                pcap_divisor=1 
            if self.iface_divs['PCAP']['PLL']=='ARM':     
                pcap_srcsel= 2
            elif self.iface_divs['PCAP']['PLL']=='DDR':     
                pcap_srcsel= 3
            else: # if self.iface_divs['PCAP']['PLL']=='IO':     
                pcap_srcsel= 0
            pcap_clkact=1
        else:
            pcap_srcsel= 0
            pcap_divisor=5 # default 
            pcap_clkact=0    
        clk_register_set.set_bitfields('pcap_clk_ctrl',( # PCAP clock control
#                                                     ('reserved1',           0),  #
                                                     ('divisor',  pcap_divisor),  # 0x5 Frequency divisor
#                                                     ('reserved2',           0),  #
                                                     ('srcsel',    pcap_srcsel),  # Source select: 0,1-IO PLL, 2 - ARM PLL, 3 - DDR PLL
#                                                     ('reserved3',           0),  #
                                                     ('clkact',    pcap_clkact),  # PCAP clock: 1 -  enabled (0 - disabled)
                                                                                ),force,warn)
# reg  topsw_clk_ctrl, offs=0x16c dflt:0 actual: Never set
        clk_dis=  0 # Not disabled (used to put into sleep mode)
        clk_register_set.set_bitfields('topsw_clk_ctrl',( # Central interconnect clock control
#                                                     ('reserved1',     0),  #
                                                     ('clk_dis', clk_dis),  # Central interconnect clock DISABLE: 0 -  enabled (1 - disabled)
                                                                                            ),force,warn)

# reg  fpga0_clk_ctrl, offs=0x170 dflt:0x101800 actual: 0x101400
        if 'FPGA0' in self.iface_divs:
            try:
                fpga0_divisor0=self.iface_divs['FPGA0']['DIV'] 
            except:
                fpga0_divisor0=1
                 
            try:
                fpga0_divisor1=self.iface_divs['FPGA0']['DIV2'] 
            except:
                fpga0_divisor1=1
                 
            if self.iface_divs['FPGA0']['PLL']=='ARM':     
                fpga0_srcsel= 2
            elif self.iface_divs['FPGA0']['PLL']=='DDR':     
                fpga0_srcsel= 3
            else: # if self.iface_divs['FPGA0']['PLL']=='IO':     
                fpga0_srcsel= 0
        else:
            fpga0_srcsel= 0
            fpga0_divisor1=0x1  # default 
            fpga0_divisor0=0x18 # default 

        clk_register_set.set_bitfields('fpga0_clk_ctrl',( # PL clock 0 output control
#                                                     ('reserved1',                0),  #
                                                     ('divisor1',    fpga0_divisor1),  # 0x1
#                                                     ('reserved2',                0),  #
                                                     ('divisor0',    fpga0_divisor0),  # 0x18
#                                                     ('reserved3',                0),  #
                                                     ('srcsel',        fpga0_srcsel),  # 0x0
#                                                     ('reserved4',                0),  #
                                                                                     ),force,warn)


# reg  fpga1_clk_ctrl, offs=0x180 dflt:0x101800 actual: 0x101400
        if 'FPGA1' in self.iface_divs:
            try:
                fpga1_divisor0=self.iface_divs['FPGA1']['DIV'] 
            except:
                fpga1_divisor0=1
                 
            try:
                fpga1_divisor1=self.iface_divs['FPGA1']['DIV2'] 
            except:
                fpga1_divisor1=1
                 
            if self.iface_divs['FPGA1']['PLL']=='ARM':     
                fpga1_srcsel= 2
            elif self.iface_divs['FPGA1']['PLL']=='DDR':     
                fpga1_srcsel= 3
            else: # if self.iface_divs['FPGA1']['PLL']=='IO':     
                fpga1_srcsel= 0
        else:
            fpga1_srcsel= 0
            fpga1_divisor1=0x1  # default 
            fpga1_divisor0=0x18 # default 

        clk_register_set.set_bitfields('fpga1_clk_ctrl',( # PL clock 0 output control
#                                                     ('reserved1',                0),  #
                                                     ('divisor1',    fpga1_divisor1),  # 0x1
#                                                     ('reserved2',                0),  #
                                                     ('divisor0',    fpga1_divisor0),  # 0x18
#                                                     ('reserved3',                0),  #
                                                     ('srcsel',        fpga1_srcsel),  # 0x0
#                                                     ('reserved4',                0),  #
                                                                                     ),force,warn)

# reg  fpga2_clk_ctrl, offs=0x190 dflt:0x101800 actual: 0x101400
        if 'FPGA2' in self.iface_divs:
            try:
                fpga2_divisor0=self.iface_divs['FPGA2']['DIV'] 
            except:
                fpga2_divisor0=1
                 
            try:
                fpga2_divisor1=self.iface_divs['FPGA2']['DIV2'] 
            except:
                fpga2_divisor1=1
                 
            if self.iface_divs['FPGA2']['PLL']=='ARM':     
                fpga2_srcsel= 2
            elif self.iface_divs['FPGA2']['PLL']=='DDR':     
                fpga2_srcsel= 3
            else: # if self.iface_divs['FPGA2']['PLL']=='IO':     
                fpga2_srcsel= 0
        else:
            fpga2_srcsel= 0
            fpga2_divisor1=0x1  # default 
            fpga2_divisor0=0x18 # default 

        clk_register_set.set_bitfields('fpga2_clk_ctrl',( # PL clock 0 output control
#                                                     ('reserved1',                0),  #
                                                     ('divisor1',    fpga2_divisor1),  # 0x1
#                                                     ('reserved2',                0),  #
                                                     ('divisor0',    fpga2_divisor0),  # 0x18
#                                                     ('reserved3',                0),  #
                                                     ('srcsel',        fpga2_srcsel),  # 0x0
#                                                     ('reserved4',                0),  #
                                                                                     ),force,warn)

# reg  fpga3_clk_ctrl, offs=0x1a0 dflt:0x101800 actual: 0x101400
        if 'FPGA3' in self.iface_divs:
            try:
                fpga3_divisor0=self.iface_divs['FPGA3']['DIV'] 
            except:
                fpga3_divisor0=1
                 
            try:
                fpga3_divisor1=self.iface_divs['FPGA3']['DIV2'] 
            except:
                fpga3_divisor1=1
                 
            if self.iface_divs['FPGA3']['PLL']=='ARM':     
                fpga3_srcsel= 2
            elif self.iface_divs['FPGA3']['PLL']=='DDR':     
                fpga3_srcsel= 3
            else: # if self.iface_divs['FPGA3']['PLL']=='IO':     
                fpga3_srcsel= 0
        else:
            fpga3_srcsel= 0
            fpga3_divisor1=0x1  # default 
            fpga3_divisor0=0x18 # default 

        clk_register_set.set_bitfields('fpga3_clk_ctrl',( # PL clock 0 output control
#                                                     ('reserved1',                0),  #
                                                     ('divisor1',    fpga3_divisor1),  # 0x1
#                                                     ('reserved2',                0),  #
                                                     ('divisor0',    fpga3_divisor0),  # 0x18
#                                                     ('reserved3',                0),  #
                                                     ('srcsel',        fpga3_srcsel),  # 0x0
#                                                     ('reserved4',                0),  #
                                                                                     ),force,warn)
# No FPGAx Throttle control here

# reg  clk_621_true, offs=0x1c4 dflt:0x1 actual: 0x1
        clk_register_set.set_bitfields('clk_621_true',( # PU clock ratio mode select
#                                                     ('reserved',              0),  #
                                                     ('clk_621_true', self.is621)),force,warn)  # 0x1 Select the CPU clock ratio: 0- 4:2:1, 1 - 6:2;1. No access to OCM when this value changes

