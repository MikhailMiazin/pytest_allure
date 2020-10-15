pipeline {
  agent none
  stages {
    stage('test') {
      agent {
        docker {
          image 'python:3.8-alpine'
          args '--user 0:0'
        }

      }
      steps {
        sh 'pip install -r requirements.txt'
        sh 'pytest -n=4 --alluredir=./allure-results tests/'
      }
    }
    stage('reports') {
      agent {
        docker {
          image 'frankescobar/allure-docker-service'
          args '--user 0:0'
        }
      }
      steps {
        script {
            allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: './allure-results']]
            ])
        }
      }
    }
  }
}
