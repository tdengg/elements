<xsl:stylesheet xmlns:math="http://exslt.org/math" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <head>
            <link type="text/css" href="http://data.exciting-code.org/rest/db/xresult/styles/xres.css"  rel="stylesheet"></link>
        <script src="http://static.exciting-code.org/flot/jquery.js" type="text/javascript" language="javascript"/>
        <script src="http://static.exciting-code.org/flot/jquery.flot.js" type="text/javascript" language="javascript"/>
        <script language="javascript" type="text/javascript" src="http://static.exciting-code.org/flot/jquery.flot.selection.js"/>
        </head>
        <h1> EOS of <xsl:value-of select="//title"/>
        </h1>
        <div>
            <span style="float:left;padding:150px 0cm 0cm 0cm;width=30px; ">
                <span class="ticklabel" style="-webkit-transform: rotate(-90deg);   -moz-transform: rotate(-90deg);display:block;"> E[Ha] </span>
            </span>
            <div id="placeholder" style="width:600px;height:400px;float:left;"/>
            <br class="clearboth"/>
            <div style="width:700px;text-align:center;">
                <span class="ticklabel">Volume Bohr³</span>
            </div>
            <p>
                <div>
                    
                    <table  class="ticklabel" >
                        <tr>
                            <td>
                                Optimal Volume:  
                            </td>
                            <td><xsl:value-of select="//graph/@V"/> Bohr³</td>
                        </tr>
                        <tr>
                            <td>
                                Bulk Modulus:
                            </td>
                            <td><xsl:value-of select="//graph/@B"/> GPa</td>
                        </tr>
                        <tr>
                            <td>
                                Min Energy:
                            </td>
                            <td><xsl:value-of select="//graph/@energy"/> Ha</td>
                        </tr>
                    </table>
                    
                    
                </div>
            </p>
        </div>  
        <script id="source" language="javascript" type="text/javascript"> 

$(function () {
 
                
               
 var d1= [];
           
                 <xsl:for-each select="//point">
   d1.push([<xsl:value-of select="@volume"/>,<xsl:value-of select="@totalEnergy"/>]);                   
             </xsl:for-each>
                 
                 
                
       
 
    var placeholder=$("#placeholder")
    var plot=$.plot(placeholder, [
      
        {  data: d1}
    ], {
        series: {
            lines: { show: false , fill: false},
            points: { show: true }
           
        },
        
         
        grid:{  hoverable: true,
               clickable: true ,
               backgroundColor: { colors: ["#fff", "#eee"] }
        }
    });
    var o;
});


</script>
    </xsl:template>
</xsl:stylesheet>