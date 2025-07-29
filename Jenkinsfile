pipeline {
    agent any

    environment {
        DOTENV_PATH = "/envfile/.env"  // Path inside Jenkins container
    }

    stages {
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
