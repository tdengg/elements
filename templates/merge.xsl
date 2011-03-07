<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:exsl="http://exslt.org/common"
 xmlns:str="http://exslt.org/strings" xmlns:math="http://exslt.org/math">
 <xsl:output method="xml" indent="yes"/>
<xsl:template match="/">

<root>

<xsl:for-each select="//graph" >
<xsl:copy-of select='.'></xsl:copy-of>
</xsl:for-each>
<xsl:for-each select="document('/fshome/tde/elements/convergencetest/eos_data_temp.xml')//graph" > 

<xsl:copy-of select='.'></xsl:copy-of>
</xsl:for-each>

</root>
</xsl:template>
</xsl:stylesheet>
