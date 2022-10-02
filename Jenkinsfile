pipeline {
    agent any
    environment { 
        CC = 'clang'
    }

    stages {
        when {changeset "data_pipeline/*.*" }

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
    
    stages {
        when {changeset "training_pipeline/*.*" }

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
