pipeline {
    agent { 
        docker { 
            image 'python:3.9'
        } 
    }

    stages {
        stage('build data pipeline') {
            when {changeset "data_pipeline/**" }

            steps {
                echo 'Building data pipeline..'
                sh 'cd data_pipeline/deployment && make build_image'
            }
        }

        stage('test data pipeline') {
            when {changeset "data_pipeline/**" }

            steps {
                echo 'Testing data pipeline..' 
            }
        }

        stage('deploy data pipeline') {
            when {changeset "data_pipeline/**" }

            steps {
                sh 'cd data_pipeline/deployment && make deploy_dags'
            }
        }
    }
}
