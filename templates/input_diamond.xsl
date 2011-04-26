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
			<xsl:value-of select="/experiment/@path" />
			const_parameters.xml
		</xsl:variable>
		<!-- Loop over all elements named "set" from reference xml-file -->
		<xsl:for-each select="/experiment/set">

			<!-- Define path here -->
			<xsl:variable name="path">
				<xsl:value-of select="/experiment/@path" />
				<xsl:value-of select="./@path" />
				/input.xml
			</xsl:variable>

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
						<xsl:attribute name="speciespath"><xsl:value-of
							select="document($constpar)//speciespath/@spa" /></xsl:attribute>
						<xsl:element name="crystal">
							<xsl:attribute name="scale"><xsl:value-of
								select="@scale" /></xsl:attribute>

							<basevect>0.5 0.5 0.0    </basevect>
							<basevect>0.5 0.0 0.5     </basevect>
							<basevect>0.0 0.5 0.5 </basevect>
						</xsl:element>
						<species speciesfile="Al.xml">
							<xsl:attribute name="speciesfile"><xsl:value-of
								select="@species" />.xml</xsl:attribute>
							<atom coord="-0.125 -0.125 -0.125" />
							<atom coord="0.125 0.125 0.125" />
						</species>
					</structure>

					<groundstate vkloff="0.5  0.5  0.5" mixer="msec">
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
				</input>

				<!-- //////////////////////////////////////////////////////////////////////// -->
				<!-- /// The input file ends here /////////////////////////////////////////// -->
				<!-- //////////////////////////////////////////////////////////////////////// -->

			</xsl:document>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
