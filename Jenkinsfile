pipeline {
  agent none
  stages {
    stage('Test') {
      agent {
        docker {
          image 'python:3.8-alpine'
        }

      }
      steps {
        sh 'pip install -r requirements.txt -u 0:0'
        sh 'pytest -n=4 --alluredir=./allure-results tests/'
      }
    }

  }
}
