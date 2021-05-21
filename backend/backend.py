# -*- coding: utf-8 -*-
# @Author  : Ming
# @File    : backend.py
import json

from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test_back_user:test_back_user@127.0.0.1:3306/backend?charset=utf8'
db = SQLAlchemy(app)


@app.route('/')
def demo():
    return 'Hello World!'


class TestCase(db.Model):
    __tablename__ = 'testcase'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=True)
    steps = db.Column(db.String(1024), unique=False, nullable=True)
    '''
    relationship：是以testcase_id为外键关联一组TestSuite
    backref指定给TestSuite类增加了一个testcase属性，内容是以testcase_id为外键关联的Testcase。
    '''
    testsuite = db.relationship('TestSuite', backref='testcase', lazy=True)

    def __repr__(self):
        return '<name %r>' % self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self._table_.colums}


class TestSuite(db.Model):
    __tablename__ = 'testsuite'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=True)
    testcase_id = db.Column(db.Integer, db.ForeignKey('testcase.id'), unique=True, nullable=True)
    testcases = db.Column(db.String(1024), unique=False, nullable=True)

    def __repr__(self):
        return '<name %r>' % self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self._table_.colums}


class SuiteService(Resource):
    def get(self):
        app.logger.info(request.args)
        testsuite=TestSuite.query.filter_by(name=request.args['name']).first()
        return {
            'name': testsuite.name,
            'description': testsuite.description,
            'testcases': testsuite.testcases
        }

    def post(self):
        app.logger.info(request.args, request.json)
        if 'add' in request.args:
            testsuite = TestSuite(**request.json)
            testcase = TestCase.query.filter_by(id=testsuite.testcase_id).first()
            testsuite.testcases = ';'+testsuite.testcases+f'name:{testcase.name},' \
                                                          f'description:{testcase.description},steps:{testcase.steps}'
            db.session.add(testsuite)
            db.session.commit()
        elif "update" in request.args:
            testsuite = TestSuite.query.filter_by(name=request.json['name']).first()
            testsuite.name = request.json['name']
            testsuite.description = request.json['description']
            testsuite.testcase_id = request.json['testcase_id']
            testcase = TestCase.query.filter_by(id=testsuite.testcase_id).first()
            testsuite.testcases = f'name:{testcase.name},description:{testcase.description},steps:{testcase.steps}'
            db.session.commit()

    def delete(self):
        app.logger.info(request.args)
        testsuite = TestSuite.query.filter_by(name=request.args['name']).first()
        db.session.delete(testsuite)
        db.session.commit()
        return {
            'msg': 'deleted',
            'errcode': '0'
        }

    # class TestCase(dict):
#
#     def __init__(self, name: str, description: str, steps: list[str]):
#         self['name'] = name
#         self['description'] = description
#         self['steps']=


    def __repr__(self):
        return '<name %r>' % self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self._table_.colums}


class TesCaseService(Resource):

    def get(self):
        app.logger.info(request.args, request.json)
        testcase = TestCase.query.filter_by(name=request.args['name']).first()
        if testcase is None:
            return {
                'msg': 'name is None',
                'size': 0
            }
        else:
            return {
                    'name': testcase.name,
                    'description': testcase.description,
                    'steps': testcase.steps,
                    'size': 1
             }

    def post(self):
        app.logger.info(request.args, request.json)
        if 'update' in request.args:
            testcase = TestCase.query.filter_by(name=request.json['name']).first()
            testcase.name = request.json['name']
            testcase.description = request.json['description']
            testcase.steps = str(request.json['steps'])
            db.session.commit()
            # for i in range(len(testcases)):
            #     if testcases[i]['name'] == request.json['name']:
            #         testcases[i] = request.json
            return {
                    'msg': 'updated',
                    'errcode': '0'
                    }
        elif 'add' in request.args:
            testcase = TestCase(**request.json)
            testcase.steps = json.dumps(request.json.get('steps'))
            # testcases.append(testcase)
            db.session.add(testcase)
            db.session.commit()
            return {
                'msg': 'add',
                'errcode': '0'
            }

    def delete(self):
        app.logger.info(request.args)
        # if 'name' in request.args:
        #     for item in testcases:
        #         if item['name'] == request.args['name']:
        #              testcases.remove(item)
        testcase=TestCase.query.filter_by(name=request.args['name']).first()
        if testcase.name == '':
            return {
                'msg': 'name is null'
            }
        db.session.delete(testcase)
        db.session.commit()
        return {
                 'msg': 'deleted',
                 'errcode': '0'
                }

    def put(self):
        pass


api.add_resource(SuiteService, '/testsuite')
api.add_resource(TesCaseService, '/testcase')

if __name__ == '__main__':
    app.run(debug=True)