pipeline {
    agent { 
        docker { 
            image 'python:3.9'
            args '--user 0:0'
            // args '-v /var/run/docker.sock:/var/run/docker.sock\
            //  -v /usr/bin/docker:/usr/bin/docker\
            //  --privileged\
            //  -u root:root'
        } 
    }

    stages {
        stage('build data pipeline') {
            when {changeset "data_pipeline/**" }

            steps {
                echo 'Building data pipeline..'
                sh 'make build_image'
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
                sh 'make deploy_dags'
            }
        }
    }
}
