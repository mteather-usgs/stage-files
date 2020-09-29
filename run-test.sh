#!/bin/bash
clear & python stage-files.py \
	--baseDownloadUrl http://simsdev.cr.usgs.gov/SIMSShare/SiteVisitDump/ \
	--localTempFolder /tmp/ \
	--bucket wma-noms-demo \
	--fileList SiteVisitSite.zip,SiteVisitSite.tsv,SiteVisitData.tsv,SiteVisitData.zip
