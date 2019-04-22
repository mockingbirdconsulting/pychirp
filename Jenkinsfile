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
                stash includes: "dist/**.whl", name: 'pyloraserver-wheel'
            }
            post {
                always {
                    // Archive unit tests for the future
                    archiveArtifacts (allowEmptyArchive: false,
                                     artifacts: 'dist/*whl',
                                     onlyIfSuccessful: true,
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
                    env.BRANCH_NAME != "master"
                }
            }
            environment {
                PYPI_TEST = credentials('01b30226-ad41-4ba7-ae90-728d683c3318')
            }
            steps {
                unstash 'pyloraserver-wheel'
                sh 'pip3 install -r dev_requirements.txt' 
                sh 'python3 -m twine upload -u ${PYPI_TEST_USR} -p ${PYPI_TEST_PSW} --repository-url https://test.pypi.org/legacy/ **/*.whl'
            }
        }
        stage("Deploy to PyPI Prod Server") {
            agent {
                label "pytest"
                }
            when {
                expression {
                    env.BRANCH_NAME == "master"
                }
            }
            environment {
                PYPI_TEST = credentials('01b30226-ad41-4ba7-ae90-728d683c3318')
            }
            steps {
                unstash 'pyloraserver-wheel'
                sh 'pip3 install -r dev_requirements.txt' 
                sh 'python3 -m twine upload -u ${PYPI_TEST_USR} -p ${PYPI_TEST_PSW} **/*.whl'
            }
        }
    }
}
