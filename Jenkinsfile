pipeline {
    agent any

    environment {
        // Update the path to match your actual .env location
        DOTENV_PATH = "E:/gitrepo/invoice_assistant/.env"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Praven4754/invoice_assistant.git'
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
                        "-p 7860:7860 --env-file \"${env.DOTENV_PATH}\""
                    )
                }
            }
        }
    }
}
