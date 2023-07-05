#!/bin/bash
XML_DIR=xml
# Delete it if it exists
[ -d $XML_DIR ] && rm -r $XML_DIR
mkdir $XML_DIR
cd $XML_DIR

mkdir papersA-B
cd papersA-B
wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.A-B.xml.tar.gz
tar -xf non_comm_use.A-B.xml.tar.gz
rm non_comm_use.A-B.xml.tar.gz
cd ..

mkdir papersC-H
cd papersC-H
wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.C-H.xml.tar.gz
tar -xf non_comm_use.C-H.xml.tar.gz
rm non_comm_use.C-H.xml.tar.gz
cd ..

mkdir papersI-N
cd papersI-N
wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.I-N.xml.tar.gz
tar -xf non_comm_use.I-N.xml.tar.gz
rm non_comm_use.I-N.xml.tar.gz
cd ..

mkdir papersO-Z
cd papersO-Z
wget ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.O-Z.xml.tar.gz
tar -xf non_comm_use.O-Z.xml.tar.gz
rm non_comm_use.O-Z.xml.tar.gz