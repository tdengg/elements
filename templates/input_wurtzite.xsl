<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="text" />
	<xsl:template match="/">

		<!-- Authors: chm, jus, sag -->

		<!--///////////////////////////////////////////////////////////////////////// -->
		<!--/// define the name of the input file /////////////////////////////////// -->
		<!--///////////////////////////////////////////////////////////////////////// -->
		<xsl:variable name="inputfilename">
			<xsl:text>input.xml</xsl:text>
		</xsl:variable>
		<xsl:variable name="constpar">
			<xsl:value-of select="/experiment/@path" />const_parameters.xml</xsl:variable>
		<!-- Loop over all elements named "set" from reference xml-file -->
		<xsl:for-each select="/experiment/set">

			<!-- Define path here -->
			<xsl:variable name="path">
				<xsl:value-of select="/experiment/@path" />
				<xsl:value-of select="./@path" />/input.xml</xsl:variable>

			<!-- Write document at Path $path -->
			<xsl:document href="{$path}" method="xml" indent="yes">
				<xsl:comment>
					This file is generated with XSLTPROC using a template file and a
					reference file
					All parameters from the set filled in by XSLTPROC are listed below:
					<!-- list all attributes in input file -->
					<xsl:for-each select="./@*">
						<xsl:text> </xsl:text>
						<xsl:value-of select="name()" />
						<xsl:text> </xsl:text>
						<xsl:value-of select="." />
						<xsl:text>
						>
						</xsl:text>
						<xsl:value-of select="$path" />
					</xsl:for-each>
					<xsl:text></xsl:text>
				</xsl:comment>
				<!-- //////////////////////////////////////////////////////////////////////// -->
				<!-- /// The input file begins here ///////////////////////////////////////// -->
				<!-- //////////////////////////////////////////////////////////////////////// -->

				<input xsi:noNamespaceSchemaLocation="excitinginput.xsd"
					xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsltpath="./"
					scratchpath="/tmp/chm/1">
					<title>
						<xsl:text> </xsl:text>
						<xsl:value-of select="position()" />
					</title>
					<structure>
					<xsl:if test="@autormt"><xsl:attribute name="autormt"><xsl:value-of select="@autormt" /></xsl:attribute></xsl:if>
						<xsl:attribute name="speciespath"><xsl:value-of
							select="document($constpar)//speciespath/@spa" /></xsl:attribute>
						<xsl:element name="crystal">
							<xsl:attribute name="scale"><xsl:value-of
								select="@scale" /></xsl:attribute>

							<basevect>0.5 -0.866025404 0.0    </basevect>
							<basevect>0.5 0.866025404 0.0     </basevect>
							<basevect>0.0 0.0 <xsl:value-of select="@covera"/> </basevect>
						</xsl:element>
						
							<species speciesfile="Zn.xml">
							<xsl:attribute name="speciesfile"><xsl:value-of
								select="@species" />.xml</xsl:attribute>
							<xsl:if test="@rmt"><xsl:attribute name = "rmt"><xsl:value-of select="@rmt"/></xsl:attribute></xsl:if>
								<atom coord="0.33333334 0.66666667 0.0" />
								<atom coord="0.66666667 0.33333334 0.5" />
							</species>
							
							<species speciesfile="S.xml">
							<xsl:attribute name="speciesfile"><xsl:value-of
									select="@species2" />.xml</xsl:attribute>
							<xsl:if test="@rmt"><xsl:attribute name = "rmt"><xsl:value-of select="@rmt"/></xsl:attribute></xsl:if>
								<atom><xsl:attribute name = "coord">0.33333334 0.66666667 0.357</xsl:attribute></atom>
								<atom><xsl:attribute name = "coord">0.66666667 0.33333334 0.857</xsl:attribute></atom>
							</species>
						
					</structure>

					<groundstate vkloff="0.5  0.5  0.5" mixer="msec">
					<xsl:if test="@gmaxvr"><xsl:attribute name="gmaxvr"><xsl:value-of select="@gmaxvr" /></xsl:attribute></xsl:if>
					<xsl:if test="@lmaxvr"><xsl:attribute name="lmaxvr"><xsl:value-of select="@lmaxvr" /></xsl:attribute></xsl:if>
						<xsl:attribute name="swidth"><xsl:value-of
							select="@swidth" /></xsl:attribute>
						<xsl:attribute name="ngridk"><xsl:value-of
							select="@ngridk" /><xsl:text> </xsl:text><xsl:value-of
							select="@ngridk" /><xsl:text> </xsl:text><xsl:value-of
							select="@ngridk" /></xsl:attribute>
						<xsl:attribute name="rgkmax"><xsl:value-of
							select="@rgkmax" /></xsl:attribute>
						<xsl:if test="@xc|@correlation|exchange">
							<libxc>
								<xsl:attribute name="xc"><xsl:value-of
									select="@xc" /></xsl:attribute>
								<xsl:attribute name="correlation"><xsl:value-of
									select="@correlation" /></xsl:attribute>
								<xsl:attribute name="exchange"><xsl:value-of
									select="@exchange" /></xsl:attribute>
							</libxc>
						</xsl:if>
						<xsl:if test="@spin"><spin></spin></xsl:if>
					</groundstate>
					<structureoptimization></structureoptimization>
				</input>

				<!-- //////////////////////////////////////////////////////////////////////// -->
				<!-- /// The input file ends here /////////////////////////////////////////// -->
				<!-- //////////////////////////////////////////////////////////////////////// -->

			</xsl:document>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
