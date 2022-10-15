pipeline {
    agent { docker { image 'python:3.9' } }

    stages {
        stage('build model serving') {
            when {changeset "model_deployment/**" }

            steps {
                echo 'Building model serving..'
                sh 'make build_image'
            }
        }

        stage('test model serving') {
            when {changeset "model_deployment/**" }

            steps {
                echo 'Testing model serving..' # (1)
            }
        }

        parallel { # (2)
            stage('deploy serving pipeline') {
                when {changeset "model_deployment/**" }

                steps {
                    sh 'make deploy_dags'
                }
            }

            stage('deploy online serving API') {
                // when {changeset "model_serving/**" }

                steps {
                    sh 'make compose_up'
                }
            }
        }
    }
}