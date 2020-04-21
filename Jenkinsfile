import groovy.json.JsonSlurper
def json
def response
pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes'
      label 'ci'
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: cd-jenkins
  containers:
  - name: helm
    image: alpine/helm:2.14.3
    command:
    - cat
    tty: true
  - name: gcloud
    image: gcr.io/cloud-builders/gcloud
    command:
    - cat
    tty: true
  - name: curl
    image: gcr.io/cloud-builders/curl
    command:
    - cat
    tty: true
  - name: git
    image: gcr.io/cloud-builders/git
    command:
    - cat
    tty: true
"""
}
  }
   stages {
     stage('Deploy') {
         steps {
        container('helm') {
             script {
               withCredentials([string(credentialsId: 'jenkins_token', variable: 'vault_token')]) {
                 gitorg = input message: 'What is your gitorg', ok: 'Submit', parameters: [choice(choices: ['dev1', 'dev2'], description: 'This is part of the pathing structure for Vault', name: 'input')], submitterParameter: 'merger'
                 dc = input message: 'What is your dc', ok: 'Submit', parameters: [choice(choices: ['dc1', 'dc2'], description: 'This is part of the pathing structure for Vault', name: 'input')], submitterParameter: 'merger'
                 appname = input message: 'What is your appname', ok: 'Submit', parameters: [choice(choices: ['pytestapp', 'javatestapp'], description: 'This is part of the pathing structure for Vault', name: 'input')], submitterParameter: 'merger'
                 role_id_path = ['auth', gitorg, appname, 'role', dc, 'role-id'].join('/')
		 vault_addr = 'http://34.69.161.191'
		 response = httpRequest consoleLogResponseBody: true, customHeaders: [[maskValue: false, name: 'X-Vault-Token', value: 's.PkhyTj8qto5B3G7KASZgzGiT']], httpMode: 'POST', ignoreSslErrors: true, requestBody: '''{
  "metadata": "{ \\"dc\\": \\"dc1\\",  \\"gitorg\\": \\"dev1\\", \\"appname\\": \\"pytestapp\\"}"
}
''', responseHandle: 'NONE', url: 'http://34.69.161.191/v1/auth/dev1/pytestapp/role/dc1/secret-id', wrapAsMultipart: false
		 //echo "${secret_map}"
		 json = new JsonSlurper().parseText(response.content)
                 }
		 echo "msg: ${json.message}"
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'kubeconfig')]) {
                sh("cp \$kubeconfig /kconfig")
                //sh("helm --kubeconfig /kconfig upgrade pytestapp ./helm_chart --install --set gitorg=${gitorg.input} --set appname=${appname.input} --set dc=${dc.input} --set role_id=${json.message.role_id} secret_id=${json.message.secret_id} --wait")
                sh("helm --kubeconfig /kconfig upgrade pytestapp ./helm_chart --install --set gitorg=${gitorg.input} --set appname=${appname.input} --set dc=${dc.input} --wait")
	  }
		}
	}
     }
         }
     }
     }

