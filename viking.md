Viking stuff
=============

Viking custom map source
------------

 - `~/.viking/maps.xml` can contain the local custom tile server; see http://wiki.openstreetmap.org/wiki/Viking#Custom_Map_Tiles_Sources

```
<objects>
   <object class="VikSlippyMapSource">
     <property name="label">Localhost tile server</property>
     <property name="hostname">localhost:8900</property>
     <property name="url">/%d/%d/%d.png</property>
     <property name="id">100</property>
   </object>
 </objects>
```

Other sources ... https://sourceforge.net/p/viking/wikiallura/Maps/

Zooms
----------

It is ok to fix one zoom (Level) and check/download all missing tiles.


- Level   4 - zoom 15 - **YES** streets
- Level   8 - zoom 14 - 
- Level  16 - zoom 13 - 
- Level  32 - zoom 12 - **YES** vilages
- Level  64 - zoom 11
- Level 128 - zoom 10
- Level 256 - zoom 9
- Level 512 - zoom 8 - **YES** but might be some problem with download


