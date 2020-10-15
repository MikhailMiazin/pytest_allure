pipeline {
  agent any
  stages {
    stage('test') {

      steps {
        sh 'pip3 install -r requirements.txt'
        sh 'pytest -n=4 --alluredir=/var/lib/jenkins/workspace/j_pip_main/allure-results tests/'
      }
    }
    stage('reports') {
      
      steps {
        script {
            allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: '/var/lib/jenkins/workspace/j_pip_main/allure-results']]
            ])
        }
      }
    }
  }
}
