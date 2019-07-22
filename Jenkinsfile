import groovy.json.JsonSlurperClassic


def curl_failed(String version, String service) {
    def access_token = "https://oapi.dingtalk.com/robot/send?access_token=21c7c8d09f4158467bc6c797d4fc75eb4fdebe89f44ea6eaa8e253f74c6560b0"
    sh("curl " + access_token + " -H 'Content-Type: application/json' -X POST -d '{\"msgtype\": \"text\", \"text\": { \"content\": \"SERVICE: " + service + " \nVERSION: " + version + " \nSTATUS: failed\"}}'")
}


def stop_service_if_running(String name) {
    sh("if docker ps -a|grep -q " + name + "\$; then docker rm -f " + name + ";else echo first start;fi")
}

pipeline {
    environment {
        realPath = sh(script: "pwd| sed 's#/var/jenkins_home#/home/jenkins_hm#g'", returnStdout: true)
    }
    agent any
    parameters {
        //--------------------------------------未迁移服务--------------------------------------
        booleanParam(name: 'buildAll', defaultValue: false, description: '重新构建所有接口')
        booleanParam(name: 'poemService', defaultValue: false, description: '古诗爬虫')

    }
    stages {
        stage('并行启动Docker') {
            parallel {
                stage('Start_Monitoring') {
                    steps {
                        script {
                            if (params.buildAll == true || params.poemService == true) {
                                def name = "poemService"
                                stop_service_if_running(name)
                                def args0 = "--name " + name + " -t --restart=always --network api-net -v ${realPath.trim()}/poem_service:/poem_service -w /poem_service"
                                docker.image('python:3.7').run(args0,
                                        "/bin/bash -c 'pip install -i https://mirrors.aliyun.com/pypi/simple -r requirement.txt && python start_spider.py'")
                            }
                        }
                    }
                }

            }
        }
    }

}
