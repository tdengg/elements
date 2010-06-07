<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="UTF-8"/>
 
<xsl:template match="/">
<xsl:variable name="layout">tree</xsl:variable>
<!-- Write document to file -->
<xsl:variable name="filename"><xsl:text>lljob_</xsl:text><xsl:value-of select="$layout"/></xsl:variable>
<xsl:document href="{$filename}" method="text">
################################################################################
# This file is generated with XSLTPROC using a template file and a reference file
################################################################################
 
# @ job_type = parallel
# @ job_name  = JOBNAME
# @ class = lesstday
# @ node           = 1
# @ tasks_per_node = 1
# @ arguments= 
# @ executable = /appl/EXCITING/versions/hydrogen/bin/excitingmpi
 
### begin job steps ############################################################
<!--                                                               -->
<!-- set the initial working directory and a string specifier here -->
<!--                                                               -->
<xsl:for-each select = "/experiment/set">
 
  <!-- Define path here -->
  <xsl:variable name="path">
  <!-- Resolve by ID number -->
  <xsl:if test="$layout='id'">
    <xsl:text>./id_</xsl:text>
    <xsl:value-of select="count(.)"/>
  </xsl:if>
  <!-- Resolve as tree in file system -->
  <xsl:if test="$layout='tree'">
    <xsl:text></xsl:text>
    <xsl:for-each select="./@path">
      <xsl:variable name="attr"><xsl:value-of select="@path"/></xsl:variable>
      <xsl:if test="$attr!='id'">

        <xsl:value-of select="."/>
        <xsl:text></xsl:text>
      </xsl:if>
    </xsl:for-each>
  </xsl:if>
  </xsl:variable>
    <!-- Define string here -->
    <xsl:variable name="string">
    <!-- Resolve by ID number -->
    <xsl:if test="$layout='id'">
      <xsl:text>id_</xsl:text>
      <xsl:value-of select="@id"/>
    </xsl:if>
    <!-- Resolve as tree in file system -->
    <xsl:if test="$layout='tree'">
      <xsl:for-each select="./@*">
        <xsl:variable name="attr"><xsl:value-of select="name()"/></xsl:variable>
        <xsl:if test="$attr!='id'">
          <!--<xsl:value-of select="name()"/>--><xsl:text>_</xsl:text>
          <xsl:value-of select="generate-id()"/>
          <xsl:text>1</xsl:text>
        </xsl:if>
      </xsl:for-each>
    </xsl:if>
  </xsl:variable>
<!--                                                              -->
<!-- continue with LoadLeveler statements                         -->
<!--                                                              -->
# @ initialdir = /home/tde/test/calc3/<xsl:value-of select="$path"/>
# @ step_name  = <xsl:value-of select="$string"/>
# @ output = $(job_name).out
# @ error = $(job_name).err
# @ resources = ConsumableCpus(1)
# @ queue
</xsl:for-each>
### end job steps ##############################################################
 
</xsl:document>
</xsl:template>
</xsl:stylesheet>
