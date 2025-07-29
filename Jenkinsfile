pipeline {
    agent any

    environment {
        DOTENV_PATH = "/envfile/.env"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('invoice-assistant')
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    docker.image('invoice-assistant').run(
                        "--env-file ${DOTENV_PATH} -p 7860:7860"
                    )
                }
            }
        }
    }
}
