<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl">
 <xd:doc>
  <xd:desc> set2shelcommand.xsl creates shelscript to execute all calculations in experiment setup
  use:
  xsltproc set2shelcommand.xsl experiment.xml
  </xd:desc>
 </xd:doc>
 
 <xsl:output method="text" />
<xsl:template match="/">
 
 
<xsl:variable name="inputfilename"><xsl:text></xsl:text></xsl:variable>
<xsl:variable name="calchome"><xsl:value-of select="/experiment/@path"/></xsl:variable>
<!-- Loop over all elements named "set" from reference xml-file -->
<xsl:for-each select = "/experiment/set">
 
  <!-- Define path here -->
  <xsl:variable name="path">
          <xsl:value-of select="$calchome"/><xsl:value-of select="@path"/>
          <xsl:text></xsl:text>
  </xsl:variable>
 
 <!-- Write document at Path $path -->
<xsl:text>cd </xsl:text> <xsl:value-of select="$path"/>
<xsl:text> 
/fshome/tde/git/exciting/bin/excitingser
cd -
</xsl:text>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>
