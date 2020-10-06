pipeline {
  agent none
  stages {
    stage('test') {
      parallel {
        stage('python3') {
          agent {
            dockerfile {
              // Large image with full OpenModelica build dependencies; lacks omc and OMPython
              label 'linux'
              dir '.jenkins/python3'
              additionalBuildArgs '--pull'
            }
          }
          steps {
            sh 'hostname'
            sh 'HOME="$PWD" python3 setup.py install --user'
            sh 'HOME="$PWD" pytest testing'
          }
        }
      }
    }
  }
}
