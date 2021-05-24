# -*- coding: utf-8 -*-
# @Author  : Ming
# @File    : test_backend.py
import requests

from backend.backend import db, TestCase, TestSuite


class TestBackend:
    def test_db_init(self):
        db.create_all()
        # testcase=TestCase.query.first()

    def testcase_demo(self):
        # requests.delete('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})
        # requests.get('http://127.0.0.1:5000/testcase', params={'name': 'testcase2'})
        requests.post('http://127.0.0.1:5000/testcase',
                      params='add',
                      json={
                          'name': 'testcase3',
                          'description': 'des3',
                          'steps': ['a', 'b', 'c']
                      })

    def test_testcase_get(self):
        # 创建测试数据
        requests.post('http://127.0.0.1:5000/testcase',
                      params='add',
                      json={
                          'name': 'testcase1',
                          'description': 'des1',
                          'steps': ['a', 'b', 'c']
                      })
        # 调用读取接口
        r = requests.get('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})
        print(r.json())
        # 数据清洗
        requests.delete('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})



    def test_testcase_add(self):
        # # 清除干扰数据
        requests.delete('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})
        r = requests.get('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})
        size=r.json()['size']
        # 调用新增接口
        r = requests.post('http://127.0.0.1:5000/testcase',
                        params='add',
                        json={
                            'name': 'testcase1',
                            'description': 'des1',
                            'steps': ['a', 'b', 'c']
                        })
        assert r.status_code == 200
        assert r.json()['msg'] == 'add'
        r = requests.get('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})
        size_new = r.json()['size']
        print(r.json())
        assert size_new == size + 1
        # 数据清洗
        requests.delete('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})

    def test_testcase_update(self):
        # 创建测试数据
        requests.post('http://127.0.0.1:5000/testcase',
                      params='add',
                      json={
                          'name': 'testcase1',
                          'description': 'des1',
                          'steps': ['a', 'b', 'c']
                      })
        # 调用更新接口
        json = {
            'name': 'testcase1',
            'description': 'des3',
            'steps': ['a', 'b', 'c']
        }
        r = requests.post('http://127.0.0.1:5000/testcase',
                          params='update',
                          json=json)
        assert r.status_code == 200
        assert r.json()['msg'] == 'updated'
        r=requests.get('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})
        print(r.json())
        assert  r.json()['description'] == 'des3'
        # 数据清洗
        requests.delete('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})

    def test_testcase_delete(self):
        r = requests.get('http://127.0.0.1:5000/testcase',params={'name': 'testcase1'})
        size = len(r.json())
        # 创建测试数据
        requests.post('http://127.0.0.1:5000/testcase',
                          params='add',
                          json={
                              'name': 'testcase1',
                              'description': 'des1',
                              'steps': ['a', 'b', 'c']
                          })
        # 调用删除接口
        r = requests.delete('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})
        assert r.status_code == 200
        assert r.json()['msg'] == 'deleted'
        r = requests.get('http://127.0.0.1:5000/testcase', params={'name': 'testcase1'})
        print(r.json())
        size_new = len(r.json())
        assert size == size_new

    def test_suite(self):
        # testcase=TestCase.query.filter_by(name='testcase1')
        testsuite=TestSuite(name="testsuite1", description='des1', testcase_id=1)
        print(testsuite.name, testsuite.description, testsuite.testcase_id, testsuite.testcases)

    def testsuite_add(self):
        requests.post('http://127.0.0.1:5000/testsuite',
                      params='add',
                      json={
                          'name': 'testsuite1',
                          'description': 'des2',
                          'testcase_id': '1,2,3'
                      })

    def testsuite_get(self):
       r=requests.get('http://127.0.0.1:5000/testsuite', params={'id': '1'})
       print(r.json())

    def testsuite_update(self):
        requests.post('http://127.0.0.1:5000/testsuite',
                      params='update',
                      json={
                          'id': 1,
                          'name': 'testsuite1',
                          'description': 'des2',
                          'testcase_id': '2,3'
                      })

    def testsuite_delete(self):
        r = requests.delete('http://127.0.0.1:5000/testsuite', params={'id': '1'})
        print(r.json())



