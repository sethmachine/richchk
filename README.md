# chkjson
Implement Starcraft's .chk (CHK) format to parse to and from JSON.  

[CHK](http://www.starcraftai.com/wiki/CHK_Format) is a binary format that is unreadable by humans.  Conversion to JSON creates a higher level format that can be more easily read, intepreted, and edited by humans or programming languages like Python, allowing map makers full control over the end to end map making process, and even avoiding any GUI editors except for terrain, pre-placed units, and precise placement of locations.  