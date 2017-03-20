# coding=utf-8
# !/usr/bin/python3

from flask import Flask, jsonify, request

from manage.manageProxy import Proxymanager

app = Flask(__name__)

api_list = {
    'get': u'get an usable proxy',
    'refresh': u'refresh proxy pool',
    'get_all': u'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:8080': u'delete an unable proxy',
}

proxymanager = Proxymanager()


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/get/')
def get():
    proxy = proxymanager.getVerifyProxy()
    return proxy


@app.route('/get_all/')
def getAll():
    proxies = proxymanager.getAllVerifyProxy()
    return jsonify(list(proxies))


@app.route('/refresh/')
def refresh():
    proxymanager.refesh()
    return True


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    proxymanager.delete_proxy(proxy)
    return 'delete success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
