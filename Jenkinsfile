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
        stage('Build package') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh  'python setup.py bdist_wheel  '
            }
            post {
                always {
                    // Archive unit tests for the future
                    archiveArtifacts (allowEmptyArchive: true,
                                     artifacts: 'dist/*whl',
                                     fingerprint: true)
                }
            }
        }
        stage("Deploy to PyPI") {
            steps {
                sh "twine upload dist/*"
            }
        }
    }
}
