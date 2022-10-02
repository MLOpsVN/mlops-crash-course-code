pipeline {
    agent any
    environment { 
        CC = 'clang'
    }

    if (changeset "data_pipeline/*.*" ) {
        stages {
            when 
            stage('Build') {
                steps {
                    echo 'Building data pipeline..'
                }
            }
            stage('Test') {
                steps {
                    echo 'Testing data pipeline..'
                }
            }
            stage('Deploy') {
                steps {
                    echo 'Deploying data pipeline..'
                }
            }
        }
    } else if (changeset "training_pipeline/*.*" ) {
        stages {
            stage('Build') {
                steps {
                    echo 'Building training pipeline..'
                }
            }
            stage('Test') {
                steps {
                    echo 'Testing training pipeline..'
                }
            }
            stage('Deploy') {
                steps {
                    echo 'Deploying training pipeline..'
                }
            }
        }
    }
}
