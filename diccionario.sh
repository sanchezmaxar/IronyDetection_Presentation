#!/bin/bash
elinks -nolist -dump "buscon.rae.es/draeI/SrvltGUIBusUsual?TIPO_HTML=2&LEMA=$1"
| grep -v "Real Academia Española © Todos los derechos reservados"
|grep -v "Emblema de la Real" |grep -v "Vigésima segunda edición"