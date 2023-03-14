upsetplotfunction <- function(mgi_db, odb_db,  biomart_db, orthorbh, exalign, cds, cdsnotcommon ) {
  library(UpSetR)
  mgi <- read.table(mgi_db,sep='\n',col.names ='MGI' )
  odb <- read.table(odb_db,sep='\n',col.names = 'OrthoDB')
  rbh <- read.table(orthorbh,sep='\n',col.names = 'RBH') 
  biomart <- read.table(biomart_db,sep='\n',col.names = 'Biomart')
  exalign_rbh <- read.table(exalign, sep = '\n', col.names = 'Exalign_RBH')
  cds_rbh <-  read.table(cds, sep = '\n', col.names = 'CDS_RBH')
  cdsnotcom <- read.table(cdsnotcommon,sep='\n',col.names ='CDS' )

  upsetdb <- function(mgi, odb, biomart, rbh){
    listInput2 <- list(RBH_Proteins =rbh$RBH , MGI =mgi$MGI , ODB =odb$OrthoDB, Biomart=biomart$Biomart)

    tiff("part1_RBH_MGI_ODB_Biomart_genenames.tiff", res=300, width = 1600 , height = 1500)
    print(upset(fromList(listInput2), nsets = 4, order.by = "freq", number.angles = 30, point.size = 3.5, line.size = 2, 
          mainbar.y.label = "Orthologs Intersections", sets.x.label = "Orthologs Per Database", text.scale = c(1, 1, 1, 1, 1, 0.85)))

    dev.off()
  }

  upsetplotcdsnotcom <- function(mgi_db, odb, rbh, biomart, cdsnotcom){
    listInput1 <- list(CDS =cdsnotcom$CDS , MGI =mgi$MGI , ODB =odb$OrthoDB, RBH_Proteins=rbh$RBH, Biomart=biomart$Biomart)

    tiff("part1_CDSnotcommon_MGI_ODB_RBH_Biomart_genenames.tiff", res=300, width = 1600 , height = 1500)
    print(upset(fromList(listInput1), nsets = 5, order.by = "freq", number.angles = 20, point.size = 3.5, line.size = 2, 
          mainbar.y.label = "Orthologs Intersections", sets.x.label = "Orthologs Per Database", text.scale = c(1, 1, 1, 1, 1, 0.8)))

    dev.off()
  }

  upsetplotall <- function(mgi, odb, rbh, biomart, exalign_rbh, cds_rbh){
    listInput <- list(MGI =mgi$MGI , ODB =odb$OrthoDB, RBH_Proteins= rbh$RBH, Biomart=biomart$Biomart,Exalign_RBH = exalign_rbh$Exalign_RBH, CDS_RBH=cds_rbh$CDS_RBH)

    tiff("part2_MGI_RBH_ODB_Biomart_Exalign_CDS_genenames.tiff", res=350, width = 1800 , height = 1700)
    print(upset(fromList(listInput), nsets = 6, order.by ="freq", nintersects= 25, number.angles = 0, point.size = 2.5, line.size = 1, 
          mainbar.y.label = "Orthologs Intersections", sets.x.label = "Orthologs Per Database", text.scale = c(0.7,0.7, 0.7, 0.7, 0.7, 0.7)))

    dev.off()

  }

  upsetdb(mgi = mgi, odb = odb , biomart = biomart, rbh = rbh)

  upsetplotcdsnotcom(mgi = mgi, odb = odb , biomart = biomart, rbh = rbh, cdsnotcom = cdsnotcom)

  upsetplotall(mgi = mgi, odb = odb , biomart = biomart, rbh = rbh, exalign_rbh = exalign_rbh, cds_rbh= cds_rbh)

}
