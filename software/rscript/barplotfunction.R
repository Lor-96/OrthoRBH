barplotnotcommon <- function(mgi_db,odb_db,biomart_db,exanotcom, cdsnotcom) {
  library(forcats)
  library(ggplot2)
  library(dplyr)
  mgi <- read.table(mgi_db,sep='\n',col.names ='MGI' )
  odb <- read.table(odb_db,sep='\n',col.names = 'OrthoDB')
  biomart <- read.table(biomart_db,sep='\n',col.names = 'Biomart')
  exalign_notcommon <- read.table(exanotcom, sep = '\n', col.names = 'Exalign_T')
  cds_notcommon <- read.table(cdsnotcom, sep = '\n', col.names = 'CDS')
  
  barexa <- function(mgi,odb,biomart,exalign_notcommon){
    Exalign=exalign_notcommon$Exalign_T
    Exalign.ODB <- Reduce(intersect, list(Exalign = exalign_notcommon$Exalign_T,odb$OrthoDB))
    Exalign.Biomart <- Reduce(intersect, list(Exalign = exalign_notcommon$Exalign_T,biomart$Biomart))
    Exalign.MGI <- Reduce(intersect, list(Exalign = exalign_notcommon$Exalign_T,mgi$MGI))
    names=c("Exalign", "Exalign-ODB", "Exalign-Biomart", "Exalign-MGI")
    values <- c(length(Exalign),length(Exalign.ODB),length(Exalign.Biomart),length(Exalign.MGI))
    valuesperc <- c((length(Exalign)/length(Exalign))*100,(length(Exalign.ODB)/length(Exalign))*100,(length(Exalign.Biomart)/length(Exalign))*100,(length(Exalign.MGI)/length(Exalign))*100)
    data <- data.frame(name=names, val=values)
    
    tiff("barplot_Exalign.tiff", res=300, width = 1600 , height = 1000)
    print(data %>%
      mutate(name = fct_reorder(name, val)) %>%
      ggplot( aes(x=name, y=val)) +
      geom_bar(stat="identity", fill="#f68060", alpha=.85, width=.95) +
      coord_flip(ylim = c(0,2500) ,expand = TRUE) +
      xlab("") +
      ylab("Exalign-OrthoRBH Orthologs in other databases") +
      theme_bw())
    
    dev.off()
    
    dataperc <- data.frame(name=names, val=valuesperc)
    
    tiff("barplot_Exalign_perc.tiff", res=300, width = 1600 , height = 1000)
    print(dataperc %>%
      mutate(name = fct_reorder(name, val)) %>%
      ggplot( aes(x=name, y=val)) +
      geom_bar(stat="identity", fill="#f68060", alpha=.85, width=.95) +
      coord_flip(ylim = c(0,100) ,expand = TRUE) +
      xlab("") +
      ylab("Percentage") +
      theme_bw())
    
    dev.off()
    
  }
  
  barcds <- function(mgi,odb,biomart,cds_notcommon){
    CDS=cds_notcommon$CDS
    CDS.ODB <- Reduce(intersect, list(CDS = cds_notcommon$CDS,odb$OrthoDB))
    CDS.Biomart <- Reduce(intersect, list(CDS = cds_notcommon$CDS,biomart$Biomart))
    CDS.MGI <- Reduce(intersect, list(CDS = cds_notcommon$CDS,mgi$MGI))
    names=c("CDS", "CDS-ODB", "CDS-Biomart", "CDS-MGI")
    values <- c(length(CDS),length(CDS.ODB),length(CDS.Biomart),length(CDS.MGI))
    valuesperc <- c((length(CDS)/length(CDS))*100,(length(CDS.ODB)/length(CDS))*100,(length(CDS.Biomart)/length(CDS))*100,(length(CDS.MGI)/length(CDS))*100)
    data <- data.frame(name=names, val=values)
    
    tiff("barplot_CDSRBH.tiff", res=300, width = 1600 , height = 1000)
    print(data %>%
      mutate(name = fct_reorder(name, val)) %>%
      ggplot( aes(x=name, y=val)) +
      geom_bar(stat="identity", fill="#f68060", alpha=.85, width=.95) +
      coord_flip(ylim = c(0,2500) ,expand = TRUE) +
      xlab("") +
      ylab("CDS-OrthoRBH Orthologs in other databases") +
      theme_bw())
    
    dev.off()
    
    dataperc <- data.frame(name=names, val=valuesperc)
    
    tiff("barplot_CDSRBH_perc.tiff", res=300, width = 1600 , height = 1000)
    print(dataperc %>%
      mutate(name = fct_reorder(name, val)) %>%
      ggplot( aes(x=name, y=val)) +
      geom_bar(stat="identity", fill="#f68060", alpha=.85, width=.95) +
      coord_flip(ylim = c(0,100) ,expand = TRUE) +
      xlab("") +
      ylab("Percentage") +
      theme_bw())
    
    dev.off()
    
  }
  
  barexa(mgi = mgi,odb = odb,biomart = biomart ,exalign_notcommon = exalign_notcommon)
  
  barcds(mgi = mgi,odb = odb,biomart = biomart , cds_notcommon = cds_notcommon)
  
}
