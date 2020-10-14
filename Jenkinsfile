pipeline {
  agent none
  stages {
    stage('Test') {
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

  }
}
