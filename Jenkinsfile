pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'echo "Hello World for b2"'
                sh '''
                    echo "Multiline shell steps works too"
                    ls -lah
                '''
            }
        }
    }
}
