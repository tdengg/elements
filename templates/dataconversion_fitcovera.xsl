<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:exsl="http://exslt.org/common"
 xmlns:str="http://exslt.org/strings" xmlns:math="http://exslt.org/math">
 <!-- Usage: xsltproc thistemplate.xsl parsel.xml > yourout.xml -->
 	<xsl:key name="sets" match="set" use="@covera"/>
	<xsl:output method="xml" indent="yes"/>
	
 	<xsl:template name="iter">
 		<xsl:param name="ind" select="1"/>
 		<xsl:param name="max" select="1"/>
 		
 		<xsl:if test="$ind &lt; $max+1">
 		<graph>
		<xsl:for-each select="//set[generate-id() = generate-id(key('sets',@covera)[$ind])]">
			<xsl:variable name="uniquescale"><xsl:value-of select="@covera"/></xsl:variable>
				
						<!-- Define path here -->
						<xsl:variable name="root"><xsl:value-of select="//experiment/@path"/></xsl:variable>
						
						<xsl:variable name="fullpath">
							<xsl:value-of select="$root"/>
							<xsl:value-of select="/rootdir/@path"/>
							<xsl:value-of select="@path"/>
							
						</xsl:variable>
						
						
						<xsl:variable name="infopath">
							<xsl:value-of select="$fullpath"/>
							<xsl:text>info.xml</xsl:text>
						</xsl:variable>
						
						<xsl:variable name="inputpath">
							<xsl:value-of select="$fullpath"/>
							<xsl:text>input.xml</xsl:text>
						</xsl:variable>
						
						<point>
							<xsl:attribute name="volume">
								
								<xsl:value-of select="math:power(document($inputpath)//crystal/@scale,3) *2.0"/>
							</xsl:attribute>
							
							<xsl:attribute name="scale">
								<xsl:value-of select="document($inputpath)//crystal/@scale"/>
							</xsl:attribute>
							<xsl:attribute name="covera">
								<xsl:value-of select="@covera"></xsl:value-of>
							</xsl:attribute>
							
							<xsl:attribute name="path">
								<xsl:value-of select="$fullpath"></xsl:value-of>
							</xsl:attribute>
				
							<xsl:attribute name="totalEnergy">
								<xsl:value-of select="document($infopath)//iter[last()]/energies/@totalEnergy"/>
							</xsl:attribute>
						</point>
				
			</xsl:for-each>
			</graph>
		<xsl:call-template name="iter">
			<xsl:with-param name="ind" select="$ind+1"></xsl:with-param>
			<xsl:with-param name="max" select="$max"></xsl:with-param>
		</xsl:call-template>
		</xsl:if>
	</xsl:template>
 	
 	
 	
	<xsl:template match="/">
		<root>
		<xsl:variable name="initsc" select="/experiment/set[last()]/@covera"></xsl:variable>
		<xsl:variable name="count" select="count(//set[@covera = $initsc])"/>
		<xsl:call-template name="iter">
			<xsl:with-param name="ind" select="1"></xsl:with-param>
			<xsl:with-param name="max" select="$count"></xsl:with-param>
		</xsl:call-template>
		</root>
	</xsl:template>
</xsl:stylesheet>
