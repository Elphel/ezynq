#!/usr/bin/env python
# Copyright (C) 2013, Elphel.inc.
# process configuration of features
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
class EzynqFeatures:
    #Modify for this class
    ERRORS={
            'ERR_NOT_A_VARIANT':   'Specified value is not a valid variant',
            'ERR_NOT_AN_INTEGER':  'Value is not an integer',
            'ERR_NOT_A_FLOAT':     'Value is not a float',
            'ERR_NOT_A_BOOLEAN':   'Value is not a boolean'
            }
    BOOLEANS=(('0','FALSE','DISABLE','DISABLED','N','OFF'),
              ('1','TRUE', 'ENABLE','ENABLED','Y','ON'))
#  defines - a list, order determines HTML output order
#  Each element has fields:
#  'NAME' - unique name to access this parameter
#  'CONF_NAME' - how it appears in configuration file, '@' may be replaced by str(channel)
#  'TYPE' - either "I" for integer, F - float, T - text, B- boolean (may be false/true, 0/1 or enable{d}/disable{d} or tuple with valid options for value
#  'MANDATORY' - boolean: this parameter is mandatory (either directly specified or derived from some others)
#  'DERIVED' - TBD later
#  'DEFAULT' - default value (to be suggested on error? Use if not mandatory parameter?
#  'DESCRIPTION' - Parameter description - use in error message?
    def _choice_val(self,t,value):
        if isinstance(t,tuple) :
            for c in t:
                if isinstance(c,int):
                    try:
                        if c==int(value,0):
                            return c
                    except:
                        pass
                elif isinstance(c,float):
                    try:
                        if c==float(value):
                            return c
                    except:
                        pass
                elif isinstance(c, bool):
                    if value in self.BOOLEANS[1]:
                        return True
                    elif value in self.BOOLEANS[0]:
                        return False
                elif isinstance(c, str):
                    try:
                        if c.upper()==value.upper():
                            return c
                    except:
                        pass
#                    return value
            else:
                return None
                         
        
 
    def __init__(self,defines,channel=0):
        self.defs={}
        for i,feature in enumerate(defines):
            self.defs[feature['NAME']]=feature
            self.defs[feature['NAME']]['INDEX']=i
        self.channel=channel
        self.pars={}
        self.target={} # target values (as specified)
        self.config_names={}
        self.defined=set()
        self.calculated=set()
        for name in self.defs:
            cn=self.defs[name];
            self.config_names[cn['CONF_NAME'].replace('@',str(channel))]=name
                            
            
        
    def parse_features(self,raw_configs):
        for line in raw_configs:
            conf_name =  line['KEY']
            value =      line['VALUE']
            value=str(value).upper()
            try:
                name=self.config_names[conf_name]
            except:
                continue
            feature= self.defs[name]
            if (value=='HELP'):
                try:
                    print conf_name+': '+feature['DESCRIPTION']
                except:
                    print conf_name+': description is not available'
                continue
            if isinstance(feature['TYPE'], tuple):
                val=self._choice_val(feature['TYPE'],value)
                if val is None:
                    raise Exception(self.ERRORS['ERR_NOT_A_VARIANT']+': '+line['VALUE'] +' is not a valid variant for parameter '+
                                    conf_name+'. Valid are:'+str(feature['TYPE']))
                else:
                    value=val
            elif (feature['TYPE']=='I') or (feature['TYPE']=='H'):
                try:
                    value= int(value,0)
                except:
                    if value == 'Y':
                        value=1
                    else:    
                        raise Exception(self.ERRORS['ERR_NOT_AN_INTEGER']+': '+line['VALUE'] +' is not a valid INTEGER value for parameter '+ conf_name)
            elif (feature['TYPE']=='F'):
                try:
                    value= float(value)
                except:
                    raise Exception(self.ERRORS['ERR_NOT_A_FLOAT']+': '+line['VALUE'] +' is not a valid FLOAT value for parameter '+ conf_name)
            elif (feature['TYPE']=='B'):
                if value in self.BOOLEANS[1]:
                    value=True
                elif value in self.BOOLEANS[0]:
                    value=False
                else:
#                    print line['VALUE'],type(line['VALUE'])
#                    print line['VALUE'] in self.BOOLEANS[1]
                    raise Exception(self.ERRORS['ERR_NOT_A_BOOLEAN']+': '+line['VALUE'] +' is not a valid boolean value for parameter '+ conf_name+
                                    '. Valid for "True" are:'+str(self.BOOLEANS[1])+', for "False" - '+str(self.BOOLEANS[0]))
            elif (feature['TYPE']=='T'):
                pass #keep string value
            self.pars[name]=value
            self.defined.add(name)
            self.target[name]=value
    #check after calculating derivative parameters                    
    def check_missing_features(self):
        all_set=True
        for name in self.defs:
            if (not name in self.pars):
                if self.defs[name]['MANDATORY']:
                    all_set=False
                    print "Configuration file is missing mandatory parameter "+self.defs[name]['CONF_NAME']+': '+self.defs[name]['DESCRIPTION']
                else:
                    if not self.defs[name]['DEFAULT'] is None:
                    # use default parameter
#                    print 'Adding default : ',name,'=', self.defs[name]['DEFAULT']
                        self.pars[name]=self.defs[name]['DEFAULT']
        return all_set
    def get_par_names(self):
#        name_offs=sorted([(name,self.registers[name]['OFFS']) for name in self.registers], key = lambda l: l[1])
#        print '---self.registers=',self.registers 
#        unsorted_name_offs=[(name,self.defs[name]['OFFS']) for name in self.registers]
#        print '---unsorted_name_offs=',unsorted_name_offs 
#        name_offs=sorted(unsorted_name_offs, key = lambda l: l[1]) 
#        print '---name_offs=',name_offs 
#        return [n for n in name_offs]
# sort register names in the order of addresses
#        name_index=sorted([(name,self.defs[name]['INDEX']) for name in self.pars], key = lambda l: l[1])
#        return [n for n in sorted([(name,self.defs[name]['OFFS']) for name in self.registers], key = lambda l: l[1])]
        return [n[0] for n in sorted([(name,self.defs[name]['INDEX']) for name in self.pars], key = lambda l: l[1])]
#TODO: Use SELECT for options?
    def get_par_confname(self,name):
        try:
            return self.defs[name]['CONF_NAME']
        except:
            raise Exception (name+' not found in self.defs') # should not happen with wrong data, program bug
    def get_par_description(self,name):
        try:
            return self.defs[name]['DESCRIPTION']
        except:
            raise Exception (name+' not found in self.defs') # should not happen with wrong data, program bug

    def get_par_value_or_none(self,name):
        try:
            return self.pars[name]
        except:
            try: 
                _=self.defs[name]['CONF_NAME']
            except:    
                raise Exception (name+' not found in self.defs') # should not happen with wrong data, program bug
            return 

    def get_par_value(self,name):
        try:
            return self.pars[name]
        except:
#            print 'name=',name
#            print self.pars
            try: 
                config_name=self.defs[name]['CONF_NAME']
            except:    
                raise Exception (name+' not found in self.defs') # should not happen with wrong data, program bug
            raise Exception (config_name+' is not defined, nor calculated')

    def get_par_value_or_default(self,name):
        try:
            return self.pars[name]
        except:
#            print 'name=',name
#            print self.pars
            try: 
                config_name=self.defs[name]['CONF_NAME']
            except:    
                raise Exception (name+' not found in self.defs') # should not happen with wrong data, program bug
            try:
                return self.defs[name]['DEFAULT']
            except:
                raise Exception (config_name+' is not defined, nor calculated and no default is provided')
        
    def get_par_target(self,name):
        try:
            return self.target[name]
        except:
            try: 
                config_name=self.defs[name]['CONF_NAME']
            except:    
                raise Exception (name+' not found in self.defs') # should not happen with wrong data, program bug
            raise Exception ('Target value for '+config_name+' is not defined')
    
    def is_known(self,name): # specified or calculated
        return (name in self.defined) or (name in self.calculated)

    def is_mandatory(self,name):
        try:
            return self.defs[name]['MANDATORY']
        except:
            raise Exception (name+' not found in self.defs') # should not happen with wrong data, program bug
    def is_specified(self,name): # directly specified
        return name in self.defined

    def undefine_parameter(self,name):
        if name in self.pars:
            self.pars[name]=None

    
    def set_calculated_value(self,name,value,force=True):
        if (not force) and (name in self.defined):
            config_name=self.defs[name]['CONF_NAME']
            raise Exception (name+' ('+config_name+') is specifically defined in configuration file, value will not change') # should not happen with wrong data, program bug
        else:
            self.pars[name]=value
            self.calculated.add(name)
            if name in self.defined:
                self.defined.remove(name)

    def set_max_value(self,name,value):
#        print 'set_max_value (',name,',',value,')'
        if (not self.is_known(name)) or (value>self.pars[name]):
            self.set_calculated_value(name,value,True)

    def set_min_value(self,name,value):
        if (not self.is_known(name)) or (value<self.pars[name]):
            self.set_calculated_value(name,value,True)
            
                               
    def html_list_features(self,html_file):
        if not html_file:
            return
        html_file.write('<table border="1">\n')
#        html_file.write('<tr><th>Configuration name</th><th>Value<br/>(Target)</th><th>Type/<br/>Choices</th><th>Mandatory</th><th>Origin</th><th>Default</th><th>Description</th></tr>\n')
        html_file.write('<tr><th>Configuration name</th><th>Value (Target)</th><th>Type/<br/>Choices</th><th>Mandatory</th><th>Origin</th><th>Default</th><th>Description</th></tr>\n')
#        print  self.get_par_names()
#        for name in self.pars:
        row_class="even"
        for name in self.get_par_names():
#            name=    self.config_names[conf_name]
            feature= self.defs[name]
            value=   self.get_par_value(name)
            if value is None:
                value='None'
            else:    
                if isinstance(value,int):
                    if (feature['TYPE']=='H'):
                        value=hex(value)
                    else:
                        value=str(value)
            try:
                target_value=self.get_par_target(name)
                if isinstance(target_value,int):
                    if (feature['TYPE']=='H'):
                        target_value=hex(target_value)
                    else:
                        target_value=str(target_value)
                if value != target_value:  # Do not show target_value if it is the same as actual
#                    value+='<br/>('+str(target_value)+')'
                    value='<b>'+str(value)+'</b> ('+str(target_value)+')'
            except: # target_value is not set
                pass
            if name in self.defined:
                origin="Defined"
            elif name in self.calculated:
                origin="Calculated"
            else:    
                origin="Default"
            if isinstance (feature['TYPE'],tuple):
                par_type='<select>\n'
                for t in feature['TYPE']:
                    par_type+='  <option>'+str(t)+'</option>\n'
#                    par_type+=('','<br/>')[i>0]+str(t)
                par_type+='</select>\n'    
            else:        
                par_type={'H':'Integer','I':'Integer','F':'Float','B':'Boolean','T':'Text'}[feature['TYPE']]

#            if name=='BAUD_RATE':
#                print value
            if row_class=="odd": row_class="even" 
            else:                row_class="odd"
            html_file.write('<tr class="'+row_class+'"><td><b>'+feature['CONF_NAME']+'</b></td><td>'+str(value)+'</td><td>'+par_type+
                            '</td><td>'+('-','Y')[feature['MANDATORY']]+'</td><td>'+origin+'</td><td>'+str(feature['DEFAULT'])+'</td><td>'+feature['DESCRIPTION']+'</td></tr>\n')
        html_file.write('</table>\n')

        