pipeline {
    agent any
    
    stages {
	    stage('clone code from git') {
		steps {
		        git 'https://github.com/mteather-usgs/stage-files.git'
		}
	    }
	    
	    stage('create virtual environment'){
		steps {
	        	sh 'python3 -m venv .env'
		}
	    }
	    
	    stage('activate virtual environment & install requirements'){
		steps {
		        sh '. .env/bin/activate & python3 -m pip install -r requirements.txt'
		}
	    }
    
	    stage('activate virtual envirnonment & run script') {
		steps {
		        def url = 'http://simsdev.cr.usgs.gov/SIMSShare/SiteVisitDump/'
		        def temp = '/tmp/'
		        def bucket = 'wma-noms-demo'
		        def files = 'SiteVisitSite.zip,SiteVisitSite.tsv,SiteVisitData.tsv,SiteVisitData.zip'
		        sh ". .env/bin/activate & python3 stage-files.py --baseDownloadUrl ${url} --localTempFolder ${temp} --bucket ${bucket} --fileList ${files}"
		}
	    }    
    }
}
