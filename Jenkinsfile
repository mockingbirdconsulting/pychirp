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
            agent {
                label "pytest"
                }
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh  'python3 setup.py bdist_wheel  '
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
        stage("Deploy to PyPI Test Server") {
            agent {
                label "pytest"
                }
            when {
                expression {
                    currentBuild.branch != "master"
                }
            }
            environment {
                PYPI_TEST = credentials('pypi-test-creds')
            }
            steps {
                sh 'pip3 install -r dev_requirements.txt' 
                sh "echo ${PYPI_TEST}"
                sh "python3 -m twine -u ${PYPI_TEST_USR} -p ${PYPI_TEST_PSW) --repository-url https://test.pypi.org/legacy/ upload dist/*"
            }
        }
    }
}
