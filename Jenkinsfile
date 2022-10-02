pipeline {
    agent any
    environment { 
        CC = 'clang'
    }

    stages {
        stage('build data pipeline') {
            when {changeset "data_pipeline/*.*" }

            steps {
                echo 'Building data pipeline..'
            }
        }

        stage('build training pipeline') {
            when {changeset "training_pipeline/*.*" }

            steps {
                echo 'Building training pipeline..'
            }
        }

        stage('test data pipeline') {
            when {changeset "data_pipeline/*.*" }

            steps {
                echo 'Testing data pipeline..'
            }
        }

        stage('test training pipeline') {
            when {changeset "training_pipeline/*.*" }

            steps {
                echo 'Testing training pipeline..'
            }
        }

        stage('deploy data pipeline') {
            when {changeset "data_pipeline/*.*" }

            steps {
                echo 'Deploying data pipeline..'
            }
        }

        stage('deploy training pipeline') {
            when {changeset "training_pipeline/*.*" }

            steps {
                echo 'Deploying training pipeline..'
            }
        }
    }
}
