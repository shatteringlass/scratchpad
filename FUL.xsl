<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:dd="urn:iso:std:iso:20022:tech:xsd:DRAFT13auth.017.001.01">
    <xsl:output method="text" encoding="UTF-8"/>

    <xsl:strip-space elements="*"/>

    <!-- Set the seperator and terminator to match CSV Styling-->
    <xsl:variable name="separator" select="'&#59;'"/>
    <xsl:variable name="newline" select="'&#xA;'"/>
    <xsl:variable name="quote" select="'&quot;'"/>


    <xsl:template match="/">
        <!-- HEADER ROW -->
        <xsl:value-of select="$quote"/>
        <xsl:text>NSTRMNT_DNTFCTN_CD</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>NSTRMNT_FLL_NM</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>NSTRMNT_CLSSFCTN</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>CMMDTS_R_MSSN_LLWNC_DRVTV_NDCT</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>SSR_R_PRTR_F_TH_TRDNG_VN_DNTFR</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>TRDNG_VN</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>FNNCL_NSTRMNT_SHRT_NM</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>RQST_FR_DMSSN_T_TRDNG_BY_SSR</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>DT_F_RQST_FR_DMSSN_T_TRDNG</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>DT_F_DMSSN_T_TRDNG_R_DT_F_FRST</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>NTNL_CRRNCY_1</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>XPRY_DT</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>PRC_MLTPLR</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>NDRLYNG_NSTRMNT_CD_SN_NSTRMNT</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>NDRLYNG_SSR_L_SSR_CDS_CMPSNG</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>DLVRY_TYP</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>PCMNG_RC</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>TRMNTN_DT</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>SBPRDCT</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>TRNSCTN_TYP</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>PBLCTN_DT</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$separator"/>
        <xsl:value-of select="$quote"/>
        <xsl:text>FNL_PRC_TYP</xsl:text>
        <xsl:value-of select="$quote"/>
        <xsl:value-of select="$newline"/>

        <!-- VALUE FIELDS BELOW -->
        <xsl:for-each select=".//dd:RefData">
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:FinInstrmGnlAttrbts/dd:Id"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:FullNm"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:ClssfctnTp"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:CmmdtyDerivInd"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:Issr"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:TradgVnRltdAttrbts/dd:Id"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:ShrtNm"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:IssrReq"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:ReqForAdmssnDt"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:FrstTradDt"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:NtnlCcy"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:XpryDt"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:PricMltplr"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:for-each select=".//dd:UndrlygInstrm//*[local-name(.) = 'ISIN' or local-name(.) ='LEI']">
                <xsl:value-of select="text()"/>
                <xsl:text>|</xsl:text>
            </xsl:for-each>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:UndrlygInstrm/dd:LEI"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:DlvryTp"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:RlvntCmptntAuthrty"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:TermntnDt"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:SubPdct"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:TxTp"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:PblctnPrd/dd:FrDt"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$separator"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select=".//dd:FnlPricTp"/>
            <xsl:value-of select="$quote"/>
            <xsl:value-of select="$newline"/>

        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>