#!/usr/bin/env python
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
import ezynq_ddrc_defs
import ezynq_registers
class EzynqDDR:
    def __init__(self,permit_undefined_bits=False,force=False,warn=False):
        self.DDRC_DEFS=ezynq_ddrc_defs.DDRC_DEFS
        self.register_sets= {'PRE':ezynq_registers.EzynqRegisters(self.DDRC_DEFS,0,permit_undefined_bits),
                            'MAIN':ezynq_registers.EzynqRegisters(self.DDRC_DEFS,0,permit_undefined_bits),
                            'POST':ezynq_registers.EzynqRegisters(self.DDRC_DEFS,0,permit_undefined_bits)}
#        self.set_names=('PRE','MAIN','POST')
        self.set_attribs=(
                          {'NAME':'PRE','POSTFIX':'_PRE','PREFIX':'CONFIG_EZYNQ_DDR_SETREG_','TITLE':"DDR Controller Register Pre-Set"},
                          {'NAME':'MAIN','POSTFIX':'','PREFIX':'CONFIG_EZYNQ_DDR_SETREG_','TITLE':"DDR Controller Register Set"},
                          {'NAME':'POST','POSTFIX':'_POST','PREFIX':'CONFIG_EZYNQ_DDR_SETREG_','TITLE':"DDR Controller Register Post-Set"})
        self.postfixes=[attrib['POSTFIX'] for attrib in self.set_attribs]
    def parse_raw_register_set(self,raw_configs,qualifier_char,force=True,warn=True):
#        for i,attribs in enumerate(self.set_attribs):
        for attribs in self.set_attribs:
            reg_set_name=attribs['NAME']
            reg_set= self.register_sets[reg_set_name]
            prefix= attribs['PREFIX']
            postfix= attribs['POSTFIX']
            reg_set.parse_options_set(raw_configs,prefix,postfix,self.postfixes,qualifier_char,force,warn) #force - readonly/undefined fields, warn: data does not fit in the bit field
    def print_html_registers(self, html_file, show_bit_fields=True, show_comments=True):
        for attribs in self.set_attribs:
            reg_set_name=attribs['NAME']
            reg_set= self.register_sets[reg_set_name]
            if len(reg_set.get_reg_names())>0:
                html_file.write('<h2>'+attribs['TITLE']+'</h2>\n')
                reg_set.print_html_registers(html_file, show_bit_fields, show_comments)
                html_file.write('<br/>\n')
               
#ddr=Ezynq_DDR()
#print ddr.DDRC_DEFS
#    def __init__(self,defines,channel=0,permit_undefined_bits=False):
#    def parse_options_set(self,raw_configs,prefix,postfix,qualifier_char,force=True,warn=True): #force - readonly/undefined fields, warn: data does not fit in the bit field
   