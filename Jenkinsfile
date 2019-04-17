pipeline {
    agent none 
    stages {
        stage('Test') { 
            agent {
                label "pytest"
                }
            steps {
                sh 'pip3 install -r dev_requirements.txt' 
                sh 'python3 -m pytest --verbose --junit-xml test-reports/results.xml'
                sh 'python3 -m flake8 --verbose --format=checkstyle > test-reports/pylint.xml'

            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}
